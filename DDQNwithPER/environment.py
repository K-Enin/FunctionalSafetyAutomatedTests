"""
Definition of Environment.
"""
from fmpy.fmi2 import FMU2Slave
from fmpy import extract
from itertools import product
import numpy as np


class Environment:
    def __init__(self, fmu_filename, levelTankA_key, levelTankB_key, valve1_key, valve2_key, valve3_key, valve4_key, model_description, switch_every_sec, step_size = 0.01):
        unzipdir = extract(fmu_filename)
        self.fmu = FMU2Slave(guid=model_description.guid,
                        unzipDirectory=unzipdir,
                        modelIdentifier=model_description.modelExchange.modelIdentifier,
                        instanceName='instance1')
        # monitored parameters
        self.levelTankA_key = levelTankA_key
        self.levelTankB_key = levelTankB_key
        # manipulated parameters
        self.valve1_key = valve1_key
        self.valve2_key = valve2_key
        self.valve3_key = valve3_key
        self.valve4_key = valve4_key

        self.possible_combinations = list(product([True, False], repeat=4))
        self.levelTankA = 0
        self.levelTankB = 0
        self.levelTankA_2 = 0
        self.levelTankB_2 = 0
        self.time = 0
        self.step_size = step_size
        self.stop_time = 40
        
        self.terminated_time = False
        self.terminated_hazard = False
        self.switch_rate = switch_every_sec
        
        self.beta = 0 # 0 if intrinsic reward should not be regarded
        
    def initialize(self):
        self.fmu.instantiate()
        self.fmu.setupExperiment(startTime=0)
        self.fmu.enterInitializationMode()
        self.fmu.exitInitializationMode()

        self.levelTankA = self.fmu.getReal([self.levelTankA_key])[0]/1e5
        self.levelTankB = self.fmu.getReal([self.levelTankB_key])[0]/1e5
        obs = np.array([self.levelTankA, self.levelTankB])
        return obs

    def reward_both_tanks(self):
        if self.levelTankA_2 - self.levelTankA > 1e-5 or self.levelTankB_2 - self.levelTankB > 1e-5: # machine accuracy
            reward = 1
        elif self.terminated_hazard: # sparse feedback signal, finding actual goal -> can be omitted
            reward = 100
        else: # tank pressure is decreasing or staying the same
            reward = 0
        return reward
    
    def reward_sparse(self):
        if self.terminated_hazard: 
            reward = 100
        else:
            reward = 0
        return reward
    
    def update_levels(self, levelTankA_2, levelTankB_2):
        self.levelTankA = levelTankA_2
        self.levelTankB = levelTankB_2
        self.levelTankA_2 = 0
        self.levelTankB_2 = 0

    def step(self, action):
        valves = self.possible_combinations[action]
        for i, valve_key in enumerate([self.valve1_key, self.valve2_key, self.valve3_key, self.valve4_key]):
            valve = valves[i]
            self.fmu.setReal([valve_key], [valve])

        for j in range(0, int(self.switch_rate/self.step_size)):
            self.fmu.doStep(currentCommunicationPoint=self.time, communicationStepSize=self.step_size)
            self.time += self.step_size
            self.levelTankA_2 = self.fmu.getReal([self.levelTankA_key])[0]/1e5 # pascal to bar
            self.levelTankB_2 = self.fmu.getReal([self.levelTankB_key])[0]/1e5
        obs = np.array([self.levelTankA_2, self.levelTankB_2])

        # if state is terminated
        if self.levelTankA_2 > 300 or self.levelTankB_2 > 150:
            print("Dangerous state reached at time t: ",  self.time)
            self.terminated_hazard = True

        if self.time > self.stop_time:
            self.terminated_time = True
        
        reward = self.reward_both_tanks()
        self.update_levels(self.levelTankA_2, self.levelTankB_2)
        return obs, reward, self.terminated_hazard, self.terminated_time