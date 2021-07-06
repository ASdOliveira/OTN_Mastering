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
        print("BKPT")

    def _loadNetwork(self):
        self.LinkBundles, self.LinksDWDM, self.Services = importNetworkTopology(self.folderName)

    def _loadFailureScenarios(self):
        comb = combinations(self.LinksDWDM, 2)
        combinationList = list(comb)
        for COMB in combinationList:
            aux = []
            for LB in self.LinkBundles:
                if (COMB[0].id not in LB.dwdmLink) and (COMB[1].id not in LB.dwdmLink):
                    aux.append(LB)
            self.FailureScenarios.append(copy.deepcopy(aux))

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
