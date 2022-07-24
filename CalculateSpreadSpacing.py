import math
import os
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file, read_solutions, \
    get_non_dominated_solutions
import matplotlib.pyplot as plt
import itertools
from Problem.Config import PENALTY_VALUE
from scipy.spatial import distance


def calc(folder):
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
    print('---------------SPACING:--------------------------')
    Spacing(result)

    print('---------------SPREAD:--------------------------')
    Spread(result)

def obtainParetoFront(ParetoFront):
    paretoFrontFiltered = []
    for pareto in ParetoFront:
        paretoFrontFiltered.append([pareto.objectives[1], pareto.objectives[0]])
    return paretoFrontFiltered


def Spread(result):
    SpreadDictResult = {}
    result = normalizeResults(result)
    for algorithm in result.keys():
        values = result[algorithm]
        values = sorted(values)
        MinimumValue = values[0]
        MaximumValue = values[-1]
        SpreadResult = distance.euclidean(MinimumValue, MaximumValue)
        SpreadDictResult[algorithm] = SpreadResult
        print(algorithm + ": " + str(SpreadResult))
    return SpreadDictResult


def Spacing(result):
    SpacingDictResult = {}
    result = normalizeResults(result)
    for algorithm in result.keys():
        values = result[algorithm]
        values = sorted(values)
        mean = calculateAvgDistance(values)
        sum = 0
        for i in range(0, len(values)-1):
            di = distance.euclidean(values[i], values[i+1])
            sum += (mean - di) * (mean - di)
        res = (1.0/(len(values) - 1)) * sum
        res = math.sqrt(res)
        SpacingDictResult[algorithm] = res
        print(algorithm + ": " + str(res))
    return SpacingDictResult


def normalizeResults(DictOfResults):
    resultDict = {}
    #Get the max and min values per coordinate
    listOfallResults = []
    for algorithm in DictOfResults.keys():
        listOfallResults.append(DictOfResults[algorithm])
    allResults = list(itertools.chain(*listOfallResults))
    allResults = sorted(allResults)
    Xlist = [results[0] for results in allResults]
    Ylist = [results[1] for results in allResults]

    MinValueX = min(Xlist)
    MinValueY = min(Ylist)
    MaxvalueX = max(Xlist)
    MaxvalueY = max(Ylist)
    MaxValue = [MaxvalueX, MaxvalueY]
    MinValue = [MinValueX, MinValueY]

    #normalize each coordinate
    for algorithm in DictOfResults.keys():
        normalizedResultList = []
        for result in DictOfResults[algorithm]:
            normalizedResultList.append(normalize(MaxValue, MinValue, result))
        resultDict[algorithm] = normalizedResultList

    return resultDict


def normalize(Max, Min, Value):
    normalizedValue = [None, None]
    normalizedValue[0] = (float(Value[0] - Min[0]) / float(Max[0] - Min[0]))
    normalizedValue[1] = (float(Value[1] - Min[1]) / float(Max[1] - Min[1]))
    return normalizedValue

def calculateAvgDistance(points):
    Sum = 0
    for i in range(0, len(points) - 1):
        Sum += distance.euclidean(points[i], points[i+1])
    Avg = Sum / len(points)
    return Avg


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


calc('data')
