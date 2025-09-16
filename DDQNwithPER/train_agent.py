"""
Method 3: DDQN with PER. Start execution here.
"""

from fmpy import read_model_description, dump
from agent import Agent
from environment import Environment

import torch
import random
from random import seed
from numpy import random as rnd
import os
import time as time_measure

# Instantiate environment
parent_dir = os.path.dirname(os.getcwd())
fmu_filename =  'SmallExample.fmu'
file_path = os.path.join(parent_dir, fmu_filename)

model_description = read_model_description(file_path)
dump(file_path)

vrs = {}
for variable in model_description.modelVariables:
    vrs[variable.name] = [variable.valueReference, variable.start]
    
    # get variables
    if variable.name == 'V1_open':
        valve1_key = variable.valueReference
    if variable.name == 'V2_open':
        valve2_key = variable.valueReference
    if variable.name == 'V3_open':
        valve3_key = variable.valueReference
    if variable.name == 'V4_open':
        valve4_key = variable.valueReference
    if variable.name == 'B1.p':
        levelTank1_key = variable.valueReference
    if variable.name == 'B2.p':
        levelTank2_key = variable.valueReference
        
eps_start = 1
eps_end = 0.001
eps_decay = 0.995
elapsed_time_list = []
actions_list = []
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
   
# One seed - one test run.     
for seed in [1]:  # Fibonacci seeds, uses the same weight initialization and the same random operations to obtain comparable results.
    torch.manual_seed(seed)
    random.seed(seed)
    rnd.seed(seed)
    
    start_time = time_measure.time()
    agent = Agent(state_size = 2, action_size = 16, seed = 0, compute_weights = False)
    eps = eps_start
    elapsed_time = 0

    while elapsed_time < max_time:
        env = Environment(file_path, levelTank1_key, levelTank2_key, valve1_key, valve2_key, valve3_key, valve4_key, model_description, switch_every_sec)
        obs = env.initialize()
        done = False
        states = [obs]
        actions = []
        while not done:
            action = agent.act(obs, eps)
            next_obs, reward, terminated_hazard, terminated_time = env.step(action)
            done = terminated_hazard or terminated_time
            agent.step(obs, action, reward, next_obs, terminated_hazard)
            obs = next_obs
            states.append(next_obs)
            actions.append(action)
        eps = max(eps_end, eps_decay*eps) # decrease epsilon
        elapsed_time = time_measure.time() - start_time
        if terminated_hazard:
            break

    elapsed_time = time_measure.time() - start_time
    print("Elapsed time: ", elapsed_time)
    elapsed_time_list.append(elapsed_time)