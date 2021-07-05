"""
This Module should manage the Input/Output files.
All Input data (Network modeling) should be stored in Input folder and
for the output data will be stored at Output folder
"""
from pathlib import Path
import csv
import networkx as nx

from Models.Link import Link
from Models.LinkBundle import LinkBundle
from Models.Service import Service

otnFile = "OTN.csv"
dwdmFile = "DWDM.csv"
servicesFile = "Services.csv"


def importNetworkTopology(folderName):
    dwdmLinks = _readDWDMCSV(folderName)
    otnLinkBundles = _readOTNCSV(folderName)
    Services = _readServiceCSV(folderName)

    return otnLinkBundles, dwdmLinks, Services


def _readDWDMCSV(folderName):
    dwdm = []

    relativePath = "../Input/" + str(folderName) + "/" + dwdmFile
    path = Path(__file__).parent / relativePath

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                dwdm.append(Link(_id=row[0], nodeFrom=row[1], nodeTo=row[2]))
                line_count += 1
    return dwdm


def _readOTNCSV(folderName):
    otn = []

    relativePath = "../Input/" + str(folderName) + "/" + otnFile
    path = Path(__file__).parent / relativePath

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                otn.append(LinkBundle(_id=row[0], nodeFrom=row[1], NodeTo=row[2], dwdmLink=row[3]))
                line_count += 1
    return otn


def _readServiceCSV(folderName):
    Services = []

    relativePath = "../Input/" + str(folderName) + "/" + servicesFile
    path = Path(__file__).parent / relativePath

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                Services.append(Service(NodeTo=row[0], NodeFrom=row[1], ServiceType=str(row[2])))
                line_count += 1
    return Services
