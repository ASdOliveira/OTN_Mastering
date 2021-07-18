class TELink:
    def __init__(self, NodeFrom, NodeTo, LinkBundleId):
        self.NodeFrom = NodeFrom
        self.NodeTo = NodeTo
        self.IsBusy = False
        self.ServiceId = None
        self.ServiceType = None
        self.LinkBundleId = LinkBundleId
