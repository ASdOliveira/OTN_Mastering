from Utils.File import importNetworkTopology

from itertools import combinations
import copy


class Network:
    def __init__(self, folderName):
        self.folderName = folderName

        self.NodesOTN = []
        self.LinkBundles = []
        self.NodesDWDM = []
        self.LinksDWDM = []
        self.Services = []
        self.ConnectionBetweenOTNAndDWDMNodes = {}

        self.FailureScenarios = []

        self._loadNetwork()
        self._loadFailureScenarios()

    def _loadNetwork(self):
        self.LinkBundles, self.LinksDWDM, self.Services = importNetworkTopology(self.folderName)

    def _loadFailureScenarios(self):
        comb = combinations(self.LinksDWDM, 2)
        for COMB in comb:
            aux = []
            for LB in self.LinkBundles:
                if (COMB[0].id in LB.dwdmLink) or (COMB[1].id in LB.dwdmLink):
                    aux.append((LB.NodeFrom, LB.NodeTo, LB.id))
            self.FailureScenarios.append(copy.deepcopy(aux))
