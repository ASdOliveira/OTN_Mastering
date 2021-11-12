import os


def generateGraphs(folder):
    result = {}
    for dirname, _, filenames in os.walk(folder):
        fileContents = []
        for filename in filenames:
            fileContent = readFile(dirname, filename)
            fileContents.append(fileContent)
        if len(fileContents) == 0:
            continue
        verifySizes(fileContents)
        AVGValues = getMeanValues(fileContents)
        algorithmName = dirname.split('\\')[1]
        result[algorithmName] = AVGValues




def readFile(folder, file):
    path = os.path.join(folder, file)
    lineFloat = []
    with open(path, 'r') as fp:
        # read an store all lines into list
        lines = fp.readlines()
        for line in lines:
            lineFloat.append(float(line))

    return lineFloat


def verifySizes(inputList):
    it = iter(inputList)
    the_len = len(next(it))
    if not all(len(l) == the_len for l in it):
        raise ValueError('not all lists have same length!')


def getMeanValues(inputList):
    column_average = [sum(sub_list) / len(sub_list) for sub_list in zip(*inputList)]
    return column_average



generateGraphs('Hist')