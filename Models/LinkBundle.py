class LinkBundle:
    def __init__(self, _id, nodeFrom, NodeTo, dwdmLink):
        self.id = _id
        self.NodeFrom = nodeFrom
        self.NodeTo = NodeTo
        # self.edge = edge
        self.dwdmLink = dwdmLink
        self.TELinks = []
