from Models.Network import Network
from Problem.Evaluation import evaluateNetwork
import timeit

# 1: Load the Network Topology
# 2: Load the service (demand)
# 3: Model the data
# 4: Calculate the fails Scenario

startTime = timeit.default_timer()
# log = Log()
#
# log.log("teste")
# log.save()

Net = Network(folderName="Topologia2")
chromosomeTest = [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
                   50, 50, 50, 50, 50, 50, 50, 50, 50,50, 50, 50, 50, 50, 50, 50, 50] # TODO: sizeof linkBundles!!
#chromosomeTest = [2, 35, 17, 18, 53, 36, 39, 26, 41, 27, 14, 35, 38, 21, 30, 36, 5, 18, 53, 44, 45, 35, 35, 48, 49, 29, 14, 28, 47, 48, 26, 7]
#chromosomeTest = [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
#chromosomeTest = [2, 2, 2, 2, 2, 2, 2]
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
