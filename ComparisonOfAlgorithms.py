"""
Storage of runtime values of the three algorithms are shown. 
Values in arrays denote runtime for each test run and were simulated before.
"""

import matplotlib.pyplot as plt
import seaborn as sns

switch = 4
compute_mean = True

if switch == 10: # stopped after 600 sec = 10 minutes
    runtime_random = [48.9, 31.3,24.7,21.6,70.4,11.6,50.1,29.7,87.2,237.4]
    runtime_DFS = [25.1,600.2,600.0,600.1,600.2,600.2,600.0,16.0,600.1,16.8] 
    runtime_RL = [34.4,34.4,34.4,34.3,34.4,44.8,37.1,34.0,34.2,34.2]
    
    if compute_mean:
        mean_value_RL = sum(runtime_RL)/len(runtime_RL)
        mean_random = sum(runtime_random)/len(runtime_random)
        mean_DFS = sum(runtime_DFS)/len(runtime_DFS)
        
        var_RL = sum((x - mean_value_RL)**2 for x in runtime_RL) / (len(runtime_RL)-1)
        var_random = sum((x - mean_random)**2 for x in runtime_random) / (len(runtime_random)-1)
        var_DFS = sum((x - mean_DFS)**2 for x in runtime_DFS) / (len(runtime_DFS)-1)
        
    # create boxplot
    plt.figure(figsize=(6, 6))
    sns.boxplot(data=[runtime_RL, runtime_random, runtime_DFS], palette='muted', showfliers=False)
    sns.stripplot(data=[runtime_RL, runtime_random, runtime_DFS], jitter=True, color='black', size=5)

    plt.xticks([0, 1, 2], ['RL', 'Random', 'DFS'])
    plt.ylabel('runtime (s)')
    plt.grid(visible=True, axis="y")
    plt.show()

if switch == 5: # stopped after 600 sec = 10 minutes
    runtime_random = [217.3,68.4,600,53.6,149.2,321.4,101.2,129,309,252.2]
    runtime_DFS = [600,600,600,600,600,600,600,600,600,600]
    runtime_RL = [39,35.4,31,30,30,31.1,30.9,30.9,30.7,30.67]
    
    if compute_mean:
        mean_value_RL = sum(runtime_RL)/len(runtime_RL)
        mean_random = sum(runtime_random)/len(runtime_random)
        mean_DFS = sum(runtime_DFS)/len(runtime_DFS)
        
        var_RL = sum((x - mean_value_RL)**2 for x in runtime_RL) / (len(runtime_RL)-1)
        var_random = sum((x - mean_random)**2 for x in runtime_random) / (len(runtime_random)-1)
        var_DFS = sum((x - mean_DFS)**2 for x in runtime_DFS) / (len(runtime_DFS)-1)
    
    # create boxplot
    plt.figure(figsize=(6, 6))
    sns.boxplot(data=[runtime_RL, runtime_random, runtime_DFS], palette='muted', showfliers=False)
    sns.stripplot(data=[runtime_RL, runtime_random, runtime_DFS], jitter=True, color='black', size=5)

    plt.xticks([0, 1, 2], ['RL', 'Random', 'DFS'])
    plt.ylabel('runtime (s)')
    plt.grid(visible=True, axis="y")
    plt.show()

if switch == 4: # stopped after 720 sec = 12 minutes
    runtime_RL = [31.2,30.74,24.9,24.8,24.86,24.3,24.3,24.35,24.34,24.35]
    runtime_random = [97,369.3,720.0,720.0,720.0,720.0,269.2,265.7,720.0,56.2] 
    
    if compute_mean:
        mean_value_RL = sum(runtime_RL)/len(runtime_RL)
        mean_random = sum(runtime_random)/len(runtime_random)
        
        var_RL = sum((x - mean_value_RL)**2 for x in runtime_RL) / (len(runtime_RL)-1)
        var_random = sum((x - mean_random)**2 for x in runtime_random) / (len(runtime_random)-1)
    
    # create boxplot
    plt.figure(figsize=(6, 6))
    sns.boxplot(data=[runtime_RL, runtime_random], palette='muted', showfliers=False)
    sns.stripplot(data=[runtime_RL, runtime_random], jitter=True, color='black', size=5)

    plt.xticks([0, 1], ['RL', 'Random'])
    plt.ylabel('runtime (s)')
    plt.grid(visible=True, axis="y")
    plt.show()

