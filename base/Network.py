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
