# this file should remove the punishment values
import os

from Problem.Config import PENALTY_VALUE


def RemovePenalty(input_dir: str):
    for dirname, _, filenames in os.walk(input_dir):
        for filename in filenames:
            if 'FUN' in filename:
                fullPath = os.path.join(dirname, filename)
                linesToBeFiltered = getSolutionsToBeFiltered(fullPath)
                if len(linesToBeFiltered) > 0:
                    filterSolutions(fullPath, linesToBeFiltered)
                    newFileName = filename.replace('FUN', 'VAR')
                    filterSolutions(os.path.join(dirname, newFileName), linesToBeFiltered)


def filterSolutions(filename: str, lineNumbers):
    with open(filename, 'r') as fp:
        # read an store all lines into list
        lines = fp.readlines()

    # Write file
    with open(filename, 'w') as fp:
        for number, line in enumerate(lines):
            if number not in lineNumbers:
                fp.write(line)


def getSolutionsToBeFiltered(filename):
    linesFound = []
    lineIndex = 0
    with open(filename) as file:
        for line in file:
            vector = [float(x) for x in line.split()]
            if vector[1] == PENALTY_VALUE:
                linesFound.append(lineIndex)
            lineIndex += 1

    return linesFound
