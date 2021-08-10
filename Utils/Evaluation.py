from copy import deepcopy
import networkx as nx
from Models.TELink import TELink
from Utils.ServiceEnum import ServiceEnum


def evaluateNetwork(network, chromosome):
    InterfacesQuantities = _calculateInterfacesQuantity(chromosome)
    TIRF = _calculateTIRF(network, chromosome)

    return [InterfacesQuantities, TIRF]


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
    Network = deepcopy(network)
    NetworkGraph = nx.MultiGraph()
    TELinks = []
    TIRF = 0.0

    for linkBundle in Network.LinkBundles:
        TELinks.append(TELink(NodeFrom=linkBundle.NodeFrom,
                              NodeTo=linkBundle.NodeTo,
                              LinkBundleId=linkBundle.id))

    # At This point the Network Graph has the Network modeled on TELink rather than Link bundles
    _convertToGraph(chromosome, TELinks, NetworkGraph)

    NetworkGraphAuxiliary = deepcopy(NetworkGraph)

    IsAllServicesAllocated = _allocateServices(Network, NetworkGraph, NetworkGraphAuxiliary)

    if not IsAllServicesAllocated:
        # TODO: Check this penalty
        TIRF = 1.0
        return TIRF

    IsProtectionRoutesAllocated = _allocateProtection(Network, NetworkGraph, NetworkGraphAuxiliary)

    if not IsProtectionRoutesAllocated:
        # TODO: Check this penalty
        TIRF = 1.0
        return TIRF

    # At this point the Network is allocated with work and protection routes.
    TIRF = _GetTIRF(Network, NetworkGraphAuxiliary)

    # DEBUG
    # print("NodeFrom", "NodeTo", "MainRoute", "ProtectionRoute", sep= " | ")
    # for services in Network.Services:
    #     print(services.NodeFrom, services.NodeTo, services.MainRoute, services.ProtectionRoute, sep=" | ")
    return TIRF


def _convertToGraph(chromosome, TELinks, NetworkGraph):
    count = 0
    for gene in chromosome:
        TELinkAux = TELinks[count]
        for x in range(gene):
            NetworkGraph.add_edge(TELinkAux.NodeFrom, TELinkAux.NodeTo, key=TELinkAux.LinkBundleId + "_" + str(x),
                                  link=TELink(TELinkAux.NodeFrom, TELinkAux.NodeTo, TELinkAux.LinkBundleId))
        count += 1


def _allocateServices(NetworkCopy, NetworkGraph, NetworkGraphAuxiliary):
    NonAllocatedServices = []
    IsServicesAllocated = True

    for service in NetworkCopy.Services:
        edges = _getShortestPathInMultigraph(NetworkGraphAuxiliary, service.NodeFrom, service.NodeTo)

        AllocationIsCompleted = False

        for edge in edges:
            TELINK = (NetworkGraph.get_edge_data(edge[0], edge[1])[edge[2]]).get("link")
            TELINK.IsBusy = True
            service.MainRoute.append(edge[2])
            AllocationIsCompleted = True
            NetworkGraphAuxiliary.remove_edge(edge[0], edge[1], edge[2])

        if not AllocationIsCompleted:
            NonAllocatedServices.append(service)

    if len(NonAllocatedServices) > 0:
        IsServicesAllocated = False

    return IsServicesAllocated


def _allocateProtection(NetworkCopy, NetworkGraph, NetworkGraphAuxiliary):
    NonAllocatedProtection = []
    IsProtectionAllocated = True

    for service in NetworkCopy.Services:
        if service.ServiceType == ServiceEnum.MAIN_ROUTE_AND_BACKUP or ServiceEnum.MAIN_ROUTE_AND_BACKUP_AND_RESTORATION:
            Aux = deepcopy(NetworkGraphAuxiliary)
            edges = _getDisjointPath(Aux, service.NodeFrom, service.NodeTo, service.MainRoute)

            AllocationIsCompleted = False

            for edge in edges:
                TELINK = (NetworkGraph.get_edge_data(edge[0], edge[1])[edge[2]]).get("link")
                TELINK.IsBusy = True
                service.ProtectionRoute.append(edge[2])
                AllocationIsCompleted = True
                NetworkGraphAuxiliary.remove_edge(edge[0], edge[1], edge[2])

            if not AllocationIsCompleted:
                NonAllocatedProtection.append(service)

    if len(NonAllocatedProtection) > 0:
        IsProtectionAllocated = False

    return IsProtectionAllocated


def _getShortestPathInMultigraph(G, Source, Target):
    edges = []
    if not (G.has_node(Source) and G.has_node(Target)):
        return edges
    all_edge_paths = nx.all_simple_edge_paths(G, Source, Target)
    sorted_all_edge_paths = sorted(list(all_edge_paths), key=lambda a: len(a))
    if len(sorted_all_edge_paths) > 0:
        edges = sorted_all_edge_paths[0]
    return edges


def _getDisjointPath(G, Source, Target, PathToAvoid):
    LinkBundleList = []

    for path in PathToAvoid:
        LinkBundleList.append(path.split("_")[0])  # Given LB1_0, the result will be LB1

    G = _removeEdgesFromLinkBundle(G, LinkBundleList)

    DisjointPath = _getShortestPathInMultigraph(G, Source, Target)
    return DisjointPath


def _GetTIRF(NetworkCopy, NetworkGraphAuxiliary):
    IR = 0.0
    TTR = 0.0

    for failureScenario in NetworkCopy.FailureScenarios:
        NetworkGraphCopy = deepcopy(NetworkGraphAuxiliary)

        NetworkGraphCopy = _removeEdgesFromLinkBundle(NetworkGraphCopy, failureScenario)

        for service in NetworkCopy.Services:
            if service.ServiceType == ServiceEnum.MAIN_ROUTE_AND_RESTORATION or ServiceEnum.MAIN_ROUTE_AND_BACKUP_AND_RESTORATION:
                # Let's allocate
                # edges = _getDisjointPath(NetworkGraphCopy, service.NodeFrom, service.NodeTo, service.MainRoute)
                edges = _getShortestPathInMultigraph(NetworkGraphCopy, service.NodeFrom, service.NodeTo)

                TTR += 1.0
                if len(edges) == 0:   # There isn't any route available
                    IR += 1.0

                for edge in edges:
                    NetworkGraphCopy.remove_edge(edge[0], edge[1], edge[2])

    return float(IR/TTR)


def _removeEdgesFromLinkBundle(Graph, LinkBundlesToRemove):
    edgesToBeRemoved = []
    edges = Graph.edges(keys=True)
    for linkBundle in LinkBundlesToRemove:
        for (i, j, k) in edges:
            if linkBundle in k:
                edgesToBeRemoved.append((i, j, k))

    Graph.remove_edges_from(edgesToBeRemoved)
    return Graph
