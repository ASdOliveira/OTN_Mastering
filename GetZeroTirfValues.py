import os
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file, read_solutions, \
    get_non_dominated_solutions
import matplotlib.pyplot as plt
import itertools
from Problem.Config import PENALTY_VALUE
import numpy as np


def GetZeroTirfValues(folder):
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
            # paretoFront = get_non_dominated_solutions(SolutionList)
            result[algorithm] = obtainZeroTirfSolutions(SolutionList)
    # createGraph(result)
    createGraphWithMultipleData(result)


def obtainZeroTirfSolutions(Solutions):
    InterfaceAmountWithZeroTirf = []
    for pareto in Solutions:
        if pareto.objectives[1] == 0:
            InterfaceAmountWithZeroTirf.append(([pareto.objectives[0]]))
    return InterfaceAmountWithZeroTirf


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
        values = np.array(InputData[key])
        #plt.ylabel('TIRF')
        #plt.xlabel('Interfaces')
        plt.title(str(key))
        plt.boxplot(values)
        plt.show()


def createGraphWithMultipleData(InputData):
    dataToPlot = []
    labelsToPlot = []
    for key in InputData.keys():
        dataToPlot.append(np.array((InputData[key])))
        labelsToPlot.append(key)
    labelsToPlot = np.array(labelsToPlot)
    dataToPlot = np.array(dataToPlot)
    plt.boxplot(dataToPlot, patch_artist=False, labels=labelsToPlot)
    plt.show()


GetZeroTirfValues("data")