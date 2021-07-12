from copy import deepcopy
import networkx as nx


def evaluateNetwork(network, chromosome):
    InterfacesQuantities = _calculateInterfacesQuantity(chromosome)
    TIRF = _calculateTIRF(network, chromosome)

    return InterfacesQuantities, TIRF


def _calculateInterfacesQuantity(chromosome):
    """The interface quantity is equal to TeLink x 2,
     because each TeLink is connected to two interface (one per OTS)"""
    InterfacesQuantities = 0
    for gene in chromosome:
        InterfacesQuantities += (gene * 2)
    return InterfacesQuantities


def _calculateTIRF(network, chromosome):
    """TIRF is defined as: IR/TTR. Where, IR = number of failures and
    TTR = Total restore attempts"""
    NetworkCopy = deepcopy(network)
    NetworkGraph = nx.MultiGraph()

    for linkBundle in NetworkCopy.LinkBundles:
        NetworkGraph.add_edge(linkBundle.NodeFrom, linkBundle.NodeTo, key=linkBundle.id)
    return None
