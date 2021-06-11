from typing import List

from base.LinkBundle import LinkBundle
from base.OpticalLink import OpticalLink
from base.Site import Site


class Network:
    def __init__(self, _OpticalLinks: List[OpticalLink] = None, _LinkBundles: List[LinkBundle] = None,
                 _nodes: List[Site] = None, _FailureScenario: List[List[int]] = None):
        # self.Network = opticalnetwork TODO: missingType
        self.OpticalLinks = _OpticalLinks
        self.linkBundle = _LinkBundles
        self.Nodes = _nodes
        self.FailureScenario = _FailureScenario
        self.RestoreTwoRoutes = True  # TODO: What's it?
        self.NextIdInterface = 1  # TODO: Check if is needed
        self.NextIdTELinks = 1
        self.NextIdTributarySlot = 1
        # self.RouteMap =          TODO: Check the type (MAP??)

    def UpdateID(self):
        for NODE in self.Nodes:
            for OTS in NODE.OtsList:
                for EInterface in OTS.interfacesList:
                    if EInterface.id > self.NextIdInterface:
                        self.NextIdInterface = EInterface.id

        self.NextIdInterface += 1

    def GenerateDoubleFaultsOpticalLinks(self):
        OptLinks = self.FilterLinks(self.OpticalLinks)
        for i in range(len(OptLinks)):
            for j in range(i, len(OptLinks)):
                if i != j:
                    scenario = []
                    for LnkBundle in self.linkBundle:
                        if LnkBundle.ContainsOpticalLinks(OptLinks[i].id,OptLinks[j].id):
                            scenario.append(LnkBundle.id)
                    if len(scenario) > 0 and not self.ContainsScenario(self.FailureScenario,scenario):
                        self.FailureScenario.append(scenario)

    def FilterLinks(self, opticalLinks: List[OpticalLink]):
        optLinks: List[OpticalLink] = []
        for OptLk0 in opticalLinks:
            flag = False
            for OptLk1 in optLinks:
                if (OptLk0.destinationSite == OptLk1.sourceSite) \
                        and (OptLk0.sourceSite == OptLk1.destinationSite):
                    flag = True
            if not flag:
                optLinks.append(OptLk0)
        return optLinks

    def ContainsScenario(self, doubleFailureScenario, Scenario):
        for Scenario1 in doubleFailureScenario:
            if len(Scenario1) == len(Scenario):
                cont = 0
                for long0 in Scenario:
                    for long1 in Scenario1:
                        if long0 == long1:
                            cont += 1
                if cont == len(Scenario):
                    return True
        return False
