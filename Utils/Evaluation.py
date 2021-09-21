from copy import deepcopy
import networkx as nx
from Models.TELink import TELink
from Utils.ServiceEnum import ServiceEnum
import math

totalLinkBundleDict = {}


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

    IsAllServicesAllocated = _allocateServicesAndProtection(Network, NetworkGraph, NetworkGraphAuxiliary)

    if not IsAllServicesAllocated:
        # TODO: Check this penalty
        TIRF = 1.0
        return TIRF

    # At this point the Network is allocated with work and protection routes.
    TIRF = _GetTIRF(Network, NetworkGraphAuxiliary)

    # DEBUG
    # print("NodeFrom", "NodeTo", "MainRoute", "ProtectionRoute", sep=" | ")
    # for services in Network.Services:
    #     print(services.NodeFrom, services.NodeTo, services.MainRoute, services.ProtectionRoute, sep=" | ")
    return TIRF


def _convertToGraph(chromosome, TELinks, NetworkGraph):
    count = 0
    totalLinkBundleDict.clear()

    for gene in chromosome:
        TELinkAux = TELinks[count]
        if gene == 0:
            amount = math.inf
        else:
            amount = (float)(1.0 / gene)
        totalLinkBundleDict[TELinkAux.LinkBundleId] = amount
        for x in range(gene):
            NetworkGraph.add_edge(TELinkAux.NodeFrom, TELinkAux.NodeTo, key=TELinkAux.LinkBundleId + "_" + str(x),
                                  link=TELink(TELinkAux.NodeFrom, TELinkAux.NodeTo, TELinkAux.LinkBundleId),
                                  weight=amount)
        count += 1


def _allocateServicesAndProtection(NetworkCopy, NetworkGraph, NetworkGraphAuxiliary):
    IsServicesAllocated = True

    for service in NetworkCopy.Services:
        edges = _getShortestPathMultiedgeByWeight(NetworkGraphAuxiliary, service.NodeFrom, service.NodeTo)

        # allocate service
        if len(edges) == 0:
            IsServicesAllocated = False
            break

        _allocate(edges, NetworkGraph, NetworkGraphAuxiliary, service.MainRoute)

        # Allocate Protection
        if (service.ServiceType == ServiceEnum.MAIN_ROUTE_AND_BACKUP) or (
                service.ServiceType == ServiceEnum.MAIN_ROUTE_AND_BACKUP_AND_RESTORATION):

            Aux = deepcopy(NetworkGraphAuxiliary)
            edges = _getDisjointPath(Aux, service.NodeFrom, service.NodeTo, service.MainRoute)

            if len(edges) == 0:
                IsServicesAllocated = False
                break

            _allocate(edges, NetworkGraph, NetworkGraphAuxiliary, service.ProtectionRoute)

    return IsServicesAllocated


def _allocate(edges, NetworkGraph, NetworkGraphAuxiliary, serviceToAppend):
    for edge in edges:
        _updateWeight(NetworkGraph, edge)
        TELINK = (NetworkGraph.get_edge_data(edge[0], edge[1])[edge[2]]).get("link")
        TELINK.IsBusy = True
        serviceToAppend.append(edge[2])
        NetworkGraphAuxiliary.remove_edge(edge[0], edge[1], edge[2])

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

    G = _removeEdgesFromLinkBundle(G, LinkBundleList) #TODO: ESSE G PODE CAUSAR ERRO!!!! ANALISAR ISSO!!!!!

    DisjointPath = _getShortestPathInMultigraph(G, Source, Target)
    return DisjointPath


def _GetTIRF(NetworkCopy, NetworkGraphAuxiliary):
    IR = 0.0
    TTR = 0.0

    for failureScenario in NetworkCopy.FailureScenarios:
        NetworkGraphCopy = deepcopy(NetworkGraphAuxiliary)

        NetworkGraphCopy = _removeEdgesFromLinkBundle(NetworkGraphCopy, failureScenario)

        for service in NetworkCopy.Services:
            if (service.ServiceType == ServiceEnum.MAIN_ROUTE_AND_RESTORATION) or (
                    service.ServiceType == ServiceEnum.MAIN_ROUTE_AND_BACKUP_AND_RESTORATION):

                IsScenarioFound1 = False
                IsScenarioFound2 = False

                for telink in service.MainRoute:
                    if failureScenario[0] in telink:
                        IsScenarioFound1 = True
                    if failureScenario[1] in telink:
                        IsScenarioFound2 = True
                needRestoration = IsScenarioFound2 or IsScenarioFound1

                if needRestoration:
                    # Let's allocate
                    edges = _getShortestPathInMultigraph(NetworkGraphCopy, service.NodeFrom, service.NodeTo)

                    TTR += 1.0
                    if len(edges) == 0:  # There isn't any route available
                        IR += 1.0

                    for edge in edges:
                        NetworkGraphCopy.remove_edge(edge[0], edge[1], edge[2])

    return float(IR / TTR)


def _removeEdgesFromLinkBundle(Graph, LinkBundlesToRemove):
    edgesToBeRemoved = []
    edges = Graph.edges(keys=True)
    for linkBundle in LinkBundlesToRemove:
        for (i, j, k) in edges:
            if linkBundle in k:
                edgesToBeRemoved.append((i, j, k))

    Graph.remove_edges_from(edgesToBeRemoved)
    return Graph


def _getShortestPathMultiedgeByWeight(G, Source, Target):
    edges = []
    id = 0
    weightDict = {}
    if not (G.has_node(Source) and G.has_node(Target)):
        return edges
    all_edge_paths = nx.all_simple_edge_paths(G, Source, Target)

    sorted_all_edge_paths = sorted(list(all_edge_paths), key=lambda a: len(a))
    for single_path in sorted_all_edge_paths:
        weight = 0
        for edge in single_path:
            weight += (G.get_edge_data(edge[0], edge[1])[edge[2]]).get("weight")
        weightDict[id] = weight
        id += 1

    if len(sorted_all_edge_paths) > 0:
        best_key = min(weightDict, key=weightDict.get)
        edges = sorted_all_edge_paths[best_key]
    return edges


def _updateWeight(NetworkGraph, edge):
    linkbundle = edge[2].split("_")[0]
    amount = totalLinkBundleDict[linkbundle]
    amount = float(1.0 / amount)
    newAmount = float(1.0 / (amount - 1))
    totalLinkBundleDict[linkbundle] = newAmount
    edgesToFilter = NetworkGraph.get_edge_data(edge[0], edge[1])
    for edges in edgesToFilter:
        if linkbundle in edges:
            NetworkGraph[edge[0]][edge[1]][edges]["weight"] = newAmount
