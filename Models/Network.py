from Models.LinkBundle import LinkBundle
from Models.OTN import OTN
from Utils.File import importNetworkTopology


class Network:
    def __init__(self, fileName):
        self.fileName = fileName
        self.NodesOTN = []
        self.LinkBundles = []
        self.Services = []
        self.FailureScenarios = []
        self._loadNetwork()

    def _loadNetwork(self):
        Graph, self.Services = importNetworkTopology(self.fileName)

        for node in Graph.nodes:
            self.NodesOTN.append(OTN(node))

        for edge in Graph.edges:
            self.LinkBundles.append(LinkBundle(edge[0], edge[1], edge))
