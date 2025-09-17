# DDQNwithPER
This repository contains the implementation of the methods presented in the paper "A comparative analysis of automated methods for testing the sufficiency of safety functions in process plants".
## Digital Twin
A small fictitious process plant is modelled in Dymola and exported as a FMU. Thsi process plant is equipped with an unsufficient set of safety functions. 
The aim of the presented test algorithms is find this safety failure through these three different test methods: *Random Input.py*, *DFS.py* and *DDQNwithPER* folder.
## Test methods
*HazardousCondition.py* replicates the failure to be detected with the test methods, which is the only failure to be found within 40 sec.

In each test file the possibility of choosing the switch rate is given through an if condition. 
In the file *RandomInput.py*, a random choice method is implemented. The values of the valves are chosen uniformally at random at each switch time step.
In the file *DFS.py* a Depth-First Search approach was implemented. The last for-loop in these files two executes the method 10 times, as due to the random character different runs lead to different time results.  
The folder DDQNwithPER contains the code used for Double-Deep Q-Network (DDQN) with Prioritized Experience Replay (PER). The file to be executed inside the folder is train_agent.py. The number of seeds in this file defines the number of test runs.

The file *ComparisonOfAlgorithms.py* plots the previously obtained runtimes in a boxplot, as depicted in the paper. 
The following library versions were used: Python 3.8.20, fmpy 0.3.19 and PyTorch 2.3.0.

The user is refered to the paper for more details.
