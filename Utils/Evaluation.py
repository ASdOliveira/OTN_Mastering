from copy import deepcopy
import networkx as nx
from Models.TELink import TELink


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
    TELinks = []

    for linkBundle in NetworkCopy.LinkBundles:
        TELinks.append(TELink(NodeFrom=linkBundle.NodeFrom,
                              NodeTo=linkBundle.NodeTo,
                              LinkBundleId=linkBundle.id))
    count = 0
    for gene in chromosome:
        TELinkAux = TELinks[count]
        for x in range(gene):
            NetworkGraph.add_edge(TELinkAux.NodeFrom, TELinkAux.NodeTo, key=TELinkAux.LinkBundleId + "_" + str(x),
                                  link=TELink(TELinkAux.NodeFrom, TELinkAux.NodeTo, TELinkAux.LinkBundleId))
        count += 1
    # At This point the Network Graph has the Network modeled on TELink rather than Link bundles

    # Allocates the services

    # TODO: o problema aqui eh a rota, precisa encontrar uma rota e alocar o servico nela.
    for service in NetworkCopy.Services:
        # a = nx.shortest_path(NetworkGraph, service.NodeFrom, service.NodeTo)
        b = nx.all_simple_edge_paths(NetworkGraph, service.NodeFrom, service.NodeTo)

        AllocationIsCompleted = False
        TELINKAux = []
        for path in b:
            if AllocationIsCompleted:
                break
            else:
                for edge in path:
                    TELINK = (NetworkGraph.get_edge_data(edge[0], edge[1])[edge[2]]).get("link")
                    if TELINK.IsBusy:
                        AllocationIsCompleted = False
                        TELINKAux = []
                        break
                    else:
                        TELINKAux.append(TELINK)
                        AllocationIsCompleted = True
        for link in TELINKAux:
            link.IsBusy = True
            link.ServiceId = service
            link.ServiceType = "MAIN ROUTE"

    return None
