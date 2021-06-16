"""
This Module should manage the Input/Output files.
All Input data (Network modeling) should be stored in Input folder and
for the output data will be stored at Output folder
"""
from pathlib import Path


def importGraphFromFile(fileName):
    # myPath = os.path.abspath(os.path.dirname(__file__))
    # path = os.path.join(myPath, "..", "Input", str(fileName))
    relativePath = "../Input/" + str(fileName)
    path = Path(__file__).parent / relativePath
    with path.open() as f:
        f = open(path, "r")

