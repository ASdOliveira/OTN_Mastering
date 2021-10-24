from jmetal.core.solution import Solution
from jmetal.lab.visualization import Plot
from jmetal.util.solution import get_non_dominated_solutions

from Models.Network import Network
from Problem.Evaluation import evaluateNetwork
import timeit
from itertools import product

from Utils.Log import Log

fileName = 'AllResults'
startTime = timeit.default_timer()

ResultLog = Log(fileName)

minimumValue = 0
maximumValue = 8
sizeOfLinkBundles = 7

solutions = []
iterationNumber = 0

print("Starting...")

Net = Network(folderName="Topologia1")
allPossibilities = list(map(list, product(range(minimumValue, maximumValue + 1), repeat=sizeOfLinkBundles)))

for individual in allPossibilities:
    print("Iteration Number: " + str(iterationNumber) + "\tpercentage: " + str(round(float(iterationNumber/len(allPossibilities) * 100), 2)))

    result = evaluateNetwork(Net, individual)
    if not result[1] >= 1.1:

        ResultLog.log(result)
    iterationNumber += 1

ResultLog.save()

stopTime = timeit.default_timer()

print('Execution Time:', stopTime - startTime)

with open(fileName + '.txt') as f:
    lines = f.readlines()

solution_list = []
count = 0
for line in lines:
    print('loading file, percentage: \t' + str(round(float(count/len(lines) * 100), 2)))
    solution = Solution(number_of_variables=7, number_of_objectives=2)
    result = eval(line)
    solution.objectives[0] = result[0]
    solution.objectives[1] = result[1]
    solution_list.append(solution)
    count += 1

print('Obtaining the pareto front')
pareto_front = get_non_dominated_solutions(solution_list)

with open('Paretofront.pf', 'w') as f:
    for pareto in pareto_front:
        f.write(str(pareto.objectives))
        f.write('\n')

plot_front = Plot(title='Pareto front approximation', axis_labels=['Interfaces', 'TIRF'])
plot_front.plot(pareto_front, label='NSGAII-OTN')

# ------------------------Saving multithread implementation ----------------
# from jmetal.core.solution import Solution
# from jmetal.lab.visualization import Plot
# from jmetal.util.solution import get_non_dominated_solutions
#
# from Models.Network import Network
# from Problem.Evaluation import evaluateNetwork
# import timeit
# from itertools import product
#
# from Utils.Log import Log
# import multiprocessing as mp
#
# startTime = timeit.default_timer()
#
# ResultLog = Log("AllResults")
# # pfLog = Log("ParetoFront")
#
# minimumValue = 0
# maximumValue = 8
# sizeOfLinkBundles = 7
#
# solutions = []
# iterationNumber = 0
# allPossibilities = list(map(list, product(range(minimumValue, maximumValue + 1), repeat=sizeOfLinkBundles)))
#
#
# def evaluate(Net, chromossome):
#     global iterationNumber
#     result = evaluateNetwork(Net, chromossome)
#     if not result[1] >= 1.1:
#         ResultLog.log(result)
#
#     iterationNumber += 1
#
#     print("Iteration Number: " + str(iterationNumber) + "\tpercentage: " + str(
#         round(float(iterationNumber / len(allPossibilities) * 100), 2)))
#
#     return result
#
# print("Starting...")
# pool = mp.Pool(mp.cpu_count())
# print(mp.cpu_count())
#
# Net = Network(folderName="Topologia1")
#
# results = [pool.apply(evaluate, args=(Net, onePossibility)) for onePossibility in allPossibilities]
#
# pool.close()
# ResultLog.save()
#
# stopTime = timeit.default_timer()
#
# print('Execution Time:', stopTime - startTime)
