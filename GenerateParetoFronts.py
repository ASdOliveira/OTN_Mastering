import os
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file, read_solutions, \
    get_non_dominated_solutions
import matplotlib.pyplot as plt
import itertools
from Problem.Config import PENALTY_VALUE


def generateParetoFront(folder):
    result = {}
    for dirname, _, filenames in os.walk(folder):
        solution_list = []
        algorithm = ""
        for filename in filenames:
            algorithm, problem = dirname.split('\\')[-2:]
            if 'FUN' in filename:
                solutions = read_solutions(os.path.join(dirname, filename))
                solution_list.append(solutions)
        if not algorithm == "":
            SolutionList = mergeSolutions(solution_list)
            paretoFront = get_non_dominated_solutions(SolutionList)
            result[algorithm] = obtainParetoFront(paretoFront)
    #createGraph(result)
    createGraphWithMultipleData(result)


def obtainParetoFront(ParetoFront):
    paretoFrontFiltered = []
    for pareto in ParetoFront:
        paretoFrontFiltered.append([pareto.objectives[1], pareto.objectives[0]])
    return paretoFrontFiltered


def mergeSolutions(SolutionListOfLists):
    mergedSolutionList = list(itertools.chain(*SolutionListOfLists))
    mergedSolutionListFiltered = filterPenalties(mergedSolutionList)
    return mergedSolutionListFiltered


def filterPenalties(SolutionList):
    solutionResult = []
    for solution in SolutionList:
        if not solution.objectives[1] == PENALTY_VALUE:
            solutionResult.append(solution)
    return solutionResult


def createGraph(InputData):
    for key in InputData.keys():
        Yvalues = getAxisValue(InputData[key], 0)
        Xvalues = getAxisValue(InputData[key], 1)

        plt.ylabel('TIRF')
        plt.xlabel('Quantidade de Interfaces')
        plt.title(str(key))
        plt.scatter(Xvalues, Yvalues, s=5)
        plt.show()


def getAxisValue(InputList, position):
    OutputList = []
    for data in InputList:
        OutputList.append(data[position])
    return OutputList


def createGraphWithMultipleData(InputData):
    markers = ["o", "v", "^", "s", "*", "d", "^"]
    markerIndex = 0
    for key in InputData.keys():
        Yvalues = getAxisValue(InputData[key], 0)
        Xvalues = getAxisValue(InputData[key], 1)
        plt.scatter(Xvalues, Yvalues, s=5, label=str(key), marker=markers[markerIndex])
        markerIndex += 1
    plt.ylabel('TIRF')
    plt.xlabel('Quantidade de Interfaces')
    plt.title('Pareto front comparison')
    plt.legend()
    plt.show()


generateParetoFront('data')
