"""
Method 1: Random Input Generation. 
"""

import random
import numpy as np
import time as time_measure
from itertools import product
from fmpy.fmi2 import FMU2Slave
from fmpy import read_model_description, extract

fmu_filename =  'SmallExample.fmu'
possible_combinations = list(product([True, False], repeat=4))
hazard_condition = np.array([300, 150])

switch = 1
if switch == 1:
    max_layer = 4
    switch_every_sec = 10
    max_time = 10*60
if switch == 2:
    max_layer = 8
    switch_every_sec = 5
    max_time = 10*60
if switch == 3:
    max_layer = 10
    switch_every_sec = 4
    max_time = 12*60

step_size = 0.01
action_list = []

def Random():
    start_time = time_measure.time()
    while True:
        time = 0
        fmu.instantiate()
        fmu.setupExperiment(startTime=time)
        fmu.enterInitializationMode()
        fmu.exitInitializationMode()
        global action_list 
        action_list = []
        for i in range(0, max_layer): 
            action = random.choice(possible_combinations)
            action_list.append(action)
            for j in range(0, int(switch_every_sec/step_size)):
                for i, valve_key in enumerate([valve1_key, valve2_key, valve3_key, valve4_key]):
                    valve = action[i]
                    fmu.setReal([valve_key], [valve])
                fmu.doStep(currentCommunicationPoint=time,
                           communicationStepSize=step_size)
                time += step_size
            levelTankA = fmu.getReal([levelTankA_key])[0]/1e5
            levelTankB = fmu.getReal([levelTankB_key])[0]/1e5
            new_obs = np.array([levelTankA, levelTankB])
            elapsed_time = time_measure.time() - start_time
            
            if np.any(new_obs > hazard_condition):
                return elapsed_time, new_obs
            
            if elapsed_time > max_time: 
                print("Time limit reached. Breaking out of the loop.")
                return elapsed_time, new_obs

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

    unzipdir = extract(fmu_filename)
    fmu = FMU2Slave(guid=model_description.guid,
                    unzipDirectory=unzipdir,
                    modelIdentifier=model_description.modelExchange.modelIdentifier,
                    instanceName='instance1')

    elapsed_time_list = []
    haz_state = []
    for j in range(0,10):
        print("New round.")
        elapsed_time, new_obs = Random()
        print(f"Hazardous state found at {elapsed_time}.")
        elapsed_time_list.append(elapsed_time)
        haz_state.append(new_obs)