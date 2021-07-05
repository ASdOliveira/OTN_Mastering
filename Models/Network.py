from Models.LinkBundle import LinkBundle
from Models.OTN import OTN
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
        # count = 0

        # for node in OtnGraph.nodes:
        #     self.NodesOTN.append(OTN(node))
        #
        # for edge in OtnGraph.edges:
        #     self.LinkBundles.append(LinkBundle(count, edge[0], edge[1], edge))
        #     count += 1
        #
        # for node in dwdmGraph.nodes:
        #     self.NodesDWDM.append(OTN(node))
        #
        # for edge in dwdmGraph.edges:
        #     self.LinksDWDM.append(LinkBundle(count, edge[0], edge[1], edge))
        #     count += 1

    def _loadFailureScenarios(self):
        comb = combinations(self.LinkBundles, 2)

        for COMB in comb:
            aux = []
            for LB in self.LinkBundles:
                if LB not in COMB:
                    aux.append(LB)
            self.FailureScenarios = copy.deepcopy(aux)

    def evaluateNetwork(self, chromosome):
        """
        Two parameters should be evaluated:
        1: Interface quantity
        2: TIRF = (IR/TTR), where:
        TIRF = Taxa de insucesso de Restauração de falhas
        IR = Quantidade de insucessos
        TTR = Total de tentativas de restauração
        """
        InterfacesQuantities = 0

        for gene in chromosome:
            InterfacesQuantities += (gene * 2)

    def _convertToNetwork(self, chromosome):
        pass



