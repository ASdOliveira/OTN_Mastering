from Models.LinkBundle import LinkBundle
from Models.Network import Network
from Utils.File import *
import networkx as nx
import matplotlib.pyplot as plt

# 1: Load the Network Topology
# 2: Load the service (demand)
# 3: Model the data
# 4: Calculate the fails Scenario
Net = Network(fileName="Topologia1.csv")

# G, ser = importNetworkTopology("Topologia1.csv")
# print(G.nodes())
# print(G.edges())
#
# for s in ser:
#     print (s.ServiceType)


# for index, tupla in enumerate(G.edges):
#     print(tupla[0])
# pos = nx.spring_layout(G)
# nx.draw_networkx_nodes(G, pos, node_color = 'r', node_size = 100, alpha = 1)
# ax = plt.gca()
# for e in G.edges:
#     ax.annotate("",
#                 xy=pos[e[0]], xycoords='data',
#                 xytext=pos[e[1]], textcoords='data',
#                 arrowprops=dict(arrowstyle="-", color="0.5",
#                                 shrinkA=5, shrinkB=5,
#                                 patchA=None, patchB=None,
#                                 connectionstyle="arc3,rad=rrr".replace('rrr',str(0.3*e[2])
#                                 ),
#                                 ),
#                 )
# plt.axis('off')
# plt.show()


# 5: Runs the Multi-Objective Algorithm
# 5.1: Evaluate the interfaces Quantity
# 5.2: Evaluate the TIFF
# 6: Get results
