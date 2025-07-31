"""
Method 2: Depth-First Search.
"""

import random
import numpy as np
import time as time_measure
from itertools import product
from collections import deque
from fmpy.fmi2 import FMU2Slave
from fmpy import read_model_description, extract

fmu_filename =  'SmallExample.fmu'
possible_combinations = {tuple(combination)
                         for combination in product([True, False], repeat=4)}
len_possible_combinations = len(possible_combinations)
hazard_condition = np.array([300, 150])
step_size = 0.01

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

class Node:
    def __init__(self, obs, action, layer):
        self.obs = obs
        self.action = action
        self.children = []
        self.layer = layer

def iterative_dfs(node):
    stack = [node]
    
    start_time = time_measure.time()
    while stack:
        current_node = stack[-1]
        layer = current_node.layer
        possible_actions = set()
        no_possible_actions = set()

        for child in current_node.children:  # node has children
            no_possible_actions.add(child.action)
        possible_actions = possible_combinations - no_possible_actions
        action = random.choice(list(possible_actions))
        action_buffer.append(action)

        new_obs = simulation(layer)
        elapsed_time = time_measure.time() - start_time
        
        if np.any(new_obs > hazard_condition):
            print("Hazardous state found.")
            return elapsed_time
        
        child_node = Node(new_obs, action, layer+1)
        current_node.children.append(child_node)

        if child_node.layer == max_layer:
            action_buffer.pop()
        else:
            stack.append(child_node)
        
        # Delete children of current node
        if len(current_node.children) == len_possible_combinations:
            current_node.children.clear()
            stack.pop() # delete node from stack
            action_buffer.pop()
        
        if elapsed_time > max_time: # 10 min
            print("Time limit reached. Breaking out of the loop.")
            return elapsed_time


def simulation(layer):
    global old_layer
    global time
    
    if layer > old_layer:  # goes one layer down
        action = action_buffer[-1]
        for j in range(0, int(switch_every_sec/step_size)):
            for i, valve_key in enumerate([valve1_key, valve2_key, valve3_key, valve4_key]):
                valve = action[i]
                fmu.setReal([valve_key], [valve])
            fmu.doStep(currentCommunicationPoint=time,
                       communicationStepSize=step_size)
            time += step_size
    else:  # if we go one layer up, we start new simulation
        time = 0
        fmu.instantiate()
        fmu.setupExperiment(startTime=time)
        fmu.enterInitializationMode()
        fmu.exitInitializationMode()
        for i in range(0, layer + 1):
            action = action_buffer[i]
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
    old_layer = layer
    return new_obs


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
    for j in range(0,10):
        time = 0
        old_layer = -1
        action_buffer = deque()
        
        # Initialize fmu
        fmu.instantiate()
        fmu.setupExperiment(startTime=time)
        fmu.enterInitializationMode()
        fmu.exitInitializationMode()
    
        levelTankA = fmu.getReal([levelTankA_key])[0]/1e5
        levelTankB = fmu.getReal([levelTankB_key])[0]/1e5
    
        obs = np.array([levelTankA, levelTankB])
        root = Node(obs, None, 0)
    
        elapsed_time = iterative_dfs(root)
        elapsed_time_list.append(elapsed_time)
    