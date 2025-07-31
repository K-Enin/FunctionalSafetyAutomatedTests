"""
File recreates hazardous scenario in tank 2 as shown in Paper.
"""

import numpy as np
import time as time_measure
from itertools import product
from fmpy.fmi2 import FMU2Slave
from fmpy import read_model_description, extract
import matplotlib.pyplot as plt


fmu_filename =  'SmallExample.fmu'
possible_combinations = list(product([True, False], repeat=4))
hazard_condition = np.array([300, 150])

max_layer = 5
step_size = 0.01
switch_every_sec = 8  # valve is switched every x sec 
time_limit = max_layer * switch_every_sec

possible_combinations = list(product([True, False], repeat=4))
action_list = [possible_combinations[15], possible_combinations[13], possible_combinations[14], possible_combinations[11]] 

levelTankA_list = []
levelTankB_list = []
temp_B1_list = []
temp_B2_list = []

def main(file):
    start_time = time_measure.time()
    elapsed_time = 0
    for j in range(0,1):
        time = 0
        fmu.instantiate()
        fmu.setupExperiment(startTime=time)
        fmu.enterInitializationMode()
        fmu.exitInitializationMode()
        levelTankA = fmu.getReal([levelTankA_key])[0]/1e5
        levelTankB = fmu.getReal([levelTankB_key])[0]/1e5
        levelTankA_list.append(levelTankA)
        levelTankB_list.append(levelTankB)
        
        temp_B1 = fmu.getReal([B1_gas_T_key])[0]
        temp_B2 = fmu.getReal([B2_gas_T_key])[0]
        temp_B1_list.append(temp_B1)
        temp_B2_list.append(temp_B2)
        
        for i in range(0, max_layer): 
            action = action_list[i]
            print(action)
            for j in range(0, int(switch_every_sec/step_size)):
                for i, valve_key in enumerate([valve1_key, valve2_key, valve3_key, valve4_key]):
                    valve = action[i]
                    fmu.setReal([valve_key], [valve])
                fmu.doStep(currentCommunicationPoint=time,
                           communicationStepSize=step_size)
                time += step_size
                levelTankA = fmu.getReal([levelTankA_key])[0]/1e5
                levelTankB = fmu.getReal([levelTankB_key])[0]/1e5
                levelTankA_list.append(levelTankA)
                levelTankB_list.append(levelTankB)
                
                temp_B1 = fmu.getReal([B1_gas_T_key])[0]
                temp_B2 = fmu.getReal([B2_gas_T_key])[0]
                temp_B1_list.append(temp_B1)
                temp_B2_list.append(temp_B2)
                
            new_obs = np.array([levelTankA, levelTankB])
            print(new_obs)
            file.write('Action: ' + str(action) + '\n')
            file.write('Obs: ' + str(new_obs) + '\n')
            
            if np.any(new_obs > hazard_condition):
                print(f"Hazardous state found at {elapsed_time}.")
                return elapsed_time

        file.write('\n''\n')
        
        current_time = time_measure.time()
        elapsed_time = current_time - start_time
        
        if elapsed_time > time_limit:
            print("Time limit reached. Breaking out of the loop.")
            return elapsed_time

if __name__ == '__main__':
    model_description = read_model_description(fmu_filename)
    vrs = {}
    for variable in model_description.modelVariables:
        vrs[variable.name] = [variable.valueReference, variable.start]

        # Extract names
        if variable.name == 'V1_open':
            valve1_key = variable.valueReference
        if variable.name == 'V2_open':
            valve2_key = variable.valueReference
        if variable.name == 'V3_open':
            valve3_key = variable.valueReference
        if variable.name == 'V4_open':
            valve4_key = variable.valueReference
        if variable.name == 'B1.p':
            levelTankA_key = variable.valueReference
        if variable.name == 'B2.p':
            levelTankB_key = variable.valueReference
        if variable.name == "B1.gas.T":
            B1_gas_T_key = variable.valueReference
        if variable.name == "B2.gas.T":
            B2_gas_T_key = variable.valueReference

    unzipdir = extract(fmu_filename)
    fmu = FMU2Slave(guid=model_description.guid,
                    unzipDirectory=unzipdir,
                    modelIdentifier=model_description.modelExchange.modelIdentifier,
                    instanceName='instance1')

    # create file which stores actions and states that lead to hazardous scenario
    with open('measurement_mc.txt', 'w') as file:
        main(file)
    
    # create figure of hazardous scenario
    time_arr = np.linspace(0, time_limit, len(levelTankA_list))
    levelTankA = np.array(levelTankA_list)
    levelTankB = np.array(levelTankB_list)
    temp_B1_list_arr = np.array(temp_B1_list)
    temp_B2_list_arr = np.array(temp_B2_list)
    plt.plot(time_arr, levelTankA, label='tank 1')
    plt.plot(time_arr, levelTankB, label ='tank 2', linestyle="--")
    plt.xlabel('time (sec)')
    plt.ylabel('pressure (bar)')
    
    plt.legend()
    plt.show()