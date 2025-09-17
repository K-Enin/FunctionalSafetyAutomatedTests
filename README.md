# DDQNwithPER

## Digital Twin

## Test method
*HardousCondition.py* replicates the failure to be detected with the test methods, which is the only failure to be found within 40 sec.

In each test file the possibility of choosing the switch rate is given through an if condition. 
In the file *RandomInput.py*, a random choice method is implemented. The values of the valves are chosen uniformally at random at each switch time step.
In the file *DFS.py* a Depth-First Search approach was implemented. 
The last for-loop in these files executes the method 10 times to get an oveview.
The following library versions were used: Python 3.8.20, fmpy 0.3.19, PyTorch 2.3.0
