from copy import deepcopy
import networkx as nx
from Models.TELink import TELink
from Utils.ServiceEnum import ServiceEnum
from joblib import Parallel, delayed
import multiprocessing


def evaluateNetwork(network, chromosome):
    InterfacesQuantities = _calculateInterfacesQuantity(chromosome)
    TIRF = _calculateTIRF(network, chromosome)

    return [InterfacesQuantities, TIRF]


def _calculateInterfacesQuantity(chromosome):
    """The interface quantity is equal to TeLink x 2,
     because each TeLink is connected to two interface (one per OTS)"""
    InterfacesQuantities = 0
    for gene in chromosome:
        InterfacesQuantities += (round(gene) * 2)
    return InterfacesQuantities


def _calculateTIRF(network, chromosome):
    """TIRF is defined as: IR/TTR. Where, IR = number of failures and
    TTR = Total restore attempts"""
    Network = deepcopy(network)
    NetworkGraph = nx.MultiGraph()
    TELinks = []
    TIRF = 0.0

    # At This point the Network Graph has the Network modeled on TELink rather than Link bundles
    _convertToGraph(chromosome, Network.LinkBundles, NetworkGraph)

    IsAllServicesAllocated = _allocateServicesAndProtection(Network, NetworkGraph)

    if not IsAllServicesAllocated:
        # TODO: Check this penalty
        TIRF = 2.0
        return TIRF

    # At this point the Network is allocated with work and protection routes.
    TIRF = _GetTIRF(Network, NetworkGraph)

    # DEBUG
    # print("NodeFrom", "NodeTo", "MainRoute", "ProtectionRoute", sep=" | ")
    # for services in Network.Services:
    #     print(services.NodeFrom, services.NodeTo, services.MainRoute, services.ProtectionRoute, sep=" | ")
    return TIRF


def _convertToGraph(chromosome, LinkBundles, NetworkGraph):
    count = 0
    TELinks = []
    for linkBundle in LinkBundles:
        TELinks.append(TELink(NodeFrom=linkBundle.NodeFrom,
                              NodeTo=linkBundle.NodeTo,
                              LinkBundleId=linkBundle.id))

    for gene in chromosome:
        TELinkAux = TELinks[count]
        for x in range(round(gene)):
            NetworkGraph.add_edge(TELinkAux.NodeFrom, TELinkAux.NodeTo, key=TELinkAux.LinkBundleId + "_" + str(x))
        count += 1



def _allocateServicesAndProtection(NetworkCopy, NetworkGraph):
    IsServicesAllocated = True

    for service in NetworkCopy.Services:
        edges = _getShortestPathInMultigraph(NetworkGraph, service.NodeFrom, service.NodeTo)

        # allocate service
        if len(edges) == 0:
            IsServicesAllocated = False
            break

        _allocate(edges, NetworkGraph, service.MainRoute)

        # Allocate Protection
        if (service.ServiceType == ServiceEnum.MAIN_ROUTE_AND_BACKUP) or (
                service.ServiceType == ServiceEnum.MAIN_ROUTE_AND_BACKUP_AND_RESTORATION):

            Aux = deepcopy(NetworkGraph)
            edges = _getDisjointPath(Aux, service.NodeFrom, service.NodeTo, service.MainRoute)

            if len(edges) == 0:
                IsServicesAllocated = False
                break

            _allocate(edges, NetworkGraph, service.ProtectionRoute)
    return IsServicesAllocated


def _allocate(edges, NetworkGraphAuxiliary, serviceToAppend):
    for edge in edges:
        serviceToAppend.append(edge[2])
        NetworkGraphAuxiliary.remove_edge(edge[0], edge[1], edge[2])


def _getShortestPathInMultigraph(G, Source, Target):
    edges = []
    if not (G.has_node(Source) and G.has_node(Target)):
        return edges

    try:
        # pathLength = nx.shortest_path_length(G, Source, Target)
        Node_path = nx.shortest_path(G, Source, Target)
        if len(Node_path) == 0:
            return edges
        for index in range(len(Node_path) - 1):
            edge_path = nx.all_simple_edge_paths(G, Node_path[index], Node_path[index + 1], 1)
            edges.append(next(edge_path)[0])

        # all_edge_paths = nx.all_simple_edge_paths(G, Source, Target, pathLength)
        # edges = next(all_edge_paths)

    except:
        edges = []
    return edges


def _getDisjointPath(G, Source, Target, PathToAvoid):
    LinkBundleList = []

    for path in PathToAvoid:
        LinkBundleList.append(path.split("_")[0])  # Given LB1_0, the result will be LB1

    G = _removeEdgesFromLinkBundle(G, LinkBundleList)

    DisjointPath = _getShortestPathInMultigraph(G, Source, Target)
    return DisjointPath


def _CalcTIRF(NetworkCopy, NetworkGraphAuxiliary, failureScenario):
    IR = 0.0
    TTR = 0.0
    NetworkGraphCopy = deepcopy(NetworkGraphAuxiliary)

    NetworkGraphCopy = _removeEdgesFromLinkBundle(NetworkGraphCopy, failureScenario)

    for service in NetworkCopy.Services:
        if (service.ServiceType == ServiceEnum.MAIN_ROUTE_AND_RESTORATION) or (
                service.ServiceType == ServiceEnum.MAIN_ROUTE_AND_BACKUP_AND_RESTORATION):

            IsScenarioFound1 = False
            IsScenarioFound2 = False

            for telink in service.MainRoute:
                if (failureScenario[0] + "_") in telink:
                    IsScenarioFound1 = True
                    break
                if (failureScenario[1] + "_") in telink:
                    IsScenarioFound2 = True
                    break
            needRestoration = IsScenarioFound2 or IsScenarioFound1

            if needRestoration:
                # Let's allocate
                edges = _getShortestPathInMultigraph(NetworkGraphCopy, service.NodeFrom, service.NodeTo)

                TTR += 1.0
                if len(edges) == 0:  # There isn't any route available
                    IR += 1.0
                else:
                    #edgeToBeRemoved = []
                    # for edge in edges:
                    #     edgeToBeRemoved.append((edge[0], edge[1], edge[2]))
                    NetworkGraphCopy.remove_edges_from(edges)

    return [IR, TTR]


def _GetTIRF(NetworkCopy, NetworkGraphAuxiliary):
    IR = 0.0
    TTR = 0.0
    results = []
    # NetworkGraphCopy = deepcopy(NetworkGraphAuxiliary)

    if len(NetworkCopy.LinkBundles) >= 10:
        with Parallel(n_jobs=-1) as parallel:
            results = parallel(
                delayed(_CalcTIRF)(NetworkCopy, NetworkGraphAuxiliary, fs) for fs in NetworkCopy.FailureScenarios)
    else:
        index = 0
        for failureScenarios in NetworkCopy.FailureScenarios:
            results.append(_CalcTIRF(NetworkCopy, NetworkGraphAuxiliary, failureScenarios))
            index += 1

    for result in results:
        IR += result[0]
        TTR += result[1]
    return float(IR / TTR)


def _removeEdgesFromLinkBundle(Graph, LinkBundlesToRemove):
    edgesToBeRemoved = []
    edges = Graph.edges(keys=True)
    for linkBundle in LinkBundlesToRemove:
        for (i, j, k) in edges:
            if (linkBundle + "_") in k:
                edgesToBeRemoved.append((i, j, k))

    Graph.remove_edges_from(edgesToBeRemoved)
    return Graph
