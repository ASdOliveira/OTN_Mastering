from jmetal.core.solution import Solution
from jmetal.lab.visualization import Plot
from jmetal.util.solution import get_non_dominated_solutions

from Models.Network import Network
from Problem.Evaluation import evaluateNetwork
import timeit
from itertools import product

from Utils.Log import Log

startTime = timeit.default_timer()

ResultLog = Log("AllResults")
# pfLog = Log("ParetoFront")

minimumValue = 0
maximumValue = 8
sizeOfLinkBundles = 7

solutions = []
iterationNumber = 0

print("Starting...")

# SOLUTION = Solution(number_of_variables=7, number_of_objectives=2)

Net = Network(folderName="Topologia1")
allPossibilities = list(map(list, product(range(minimumValue, maximumValue + 1), repeat=sizeOfLinkBundles)))

for individual in allPossibilities:
    print("Iteration Number: " + str(iterationNumber) + "\tpercentage: " + str(round(float(iterationNumber/len(allPossibilities) * 100), 2)))

    result = evaluateNetwork(Net, individual)
    if not result[1] >= 1.1:
        # SOLUTION = Solution(number_of_variables=7, number_of_objectives=2)
        # SOLUTION.objectives.append(result)
        # SOLUTION.variables.append(individual)
        # solutions.append(SOLUTION)

        ResultLog.log(result)
    iterationNumber += 1

ResultLog.save()

# SOL = get_non_dominated_solutions(solutions)
# pfLog.log(SOL)
# pfLog.save()

# plot_front = Plot(title='Pareto front approximation', axis_labels=['Interfaces', 'TIRF'])
# plot_front.plot(SOL, label='BruteForce - OTN')

stopTime = timeit.default_timer()

print('Execution Time:', stopTime - startTime)
