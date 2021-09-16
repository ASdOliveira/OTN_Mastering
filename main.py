from Models.Network import Network
from Utils.Evaluation import evaluateNetwork
from Utils.Log import Log
import timeit

# 1: Load the Network Topology
# 2: Load the service (demand)
# 3: Model the data
# 4: Calculate the fails Scenario

startTime = timeit.default_timer()
log = Log()

log.log("teste")
log.save()

Net = Network(folderName="Topologia1")
#chromosomeTest = [5,  5,5, 5, 5, 5, 5] # TODO: sizeof linkBundles!!
#chromosomeTest = [4, 4, 4, 4, 4, 4, 4] # TODO: sizeof linkBundles!!
#chromosomeTest = [3, 3, 3, 3, 3, 3, 3] # TODO: sizeof linkBundles!!

chromosomeTest = [2, 2, 3, 3, 2, 2, 2] # TODO: sizeof linkBundles!!
#chromosomeTest = [2, 2, 3, 2, 2, 2, 2] # TODO: sizeof linkBundles!!
#chromosomeTest = [2, 2, 2, 2, 2, 2, 2] # TODO: sizeof linkBundles!!
Fitness = evaluateNetwork(Net, chromosomeTest)

stopTime = timeit.default_timer()
print('Fitness Value:', Fitness)
print('Execution Time:', stopTime - startTime)

# 5: Runs the Multi-Objective Algorithm
# 5.1: Evaluate the interfaces Quantity
# 5.2: Evaluate the TIFF
# 5.2.1: Transform the chromosome into a network
# 5.2.2: Allocate the resources into the network
# 5.2.3: Do the protection if necessary
# 5.2.4: Try to get restoration routes
# 6: Get results
