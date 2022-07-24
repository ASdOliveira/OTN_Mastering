# OTN_Mastering

Documentation in construction

## Getting Started
After cloning this repo, it is interesting that you create a virtual environment. The process to create and activate the virtual enviroment can found [HERE](https://realpython.com/python-virtual-environments-a-primer/).


After create and activate the virtual env, you must install all dependencies required, this process can be done by running the following command:

`pip install -r requirements.txt`

## High level explanation

The entry point of this code is at main.py. Which contains a way to test if the core of the planning tools is working as expected.

The files that contains all the data entries should be stored in _Input_ 
_folder_, for example: the files in which have the network topology
and the services demand.

The results (graphs, pareto fronts and others) can be found at 
_Output folder_. The _Data_ folder contains the output from the metaheuristics and _Hist_ contains the hypervolume progress during the code execution.

To run the code for various metaheuristics in the same "block", you should run the "experiments.py" file. After get some results, the "statisticalAnalysis.py" file will generate some boxplots from the data outputs. 