"""
This Module should manage the Input/Output files.
All Input data (Network modeling) should be stored in Input folder and
for the output data will be stored at Output folder
"""
from pathlib import Path
import csv
import networkx as nx

from Models.Service import Service


def importNetworkTopology(fileName):
    Graph = nx.MultiGraph()
    Services = []

    relativePath = "../Input/" + str(fileName)
    path = Path(__file__).parent / relativePath

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                Graph.add_edge(row[0], row[1])
                Services.append(Service(row[0], row[1], str(row[2])))
                line_count += 1
    return Graph, Services


