from Utils.ServiceEnum import ServiceEnum


class Service:
    def __init__(self, NodeFrom, NodeTo, ServiceType):
        self.NodeFrom = NodeFrom
        self.NodeTo = NodeTo
        self.ServiceType = self._serviceTypeToEnum(ServiceType)
        self.MainRoute = []
        self.ProtectionRoute = []

    def _serviceTypeToEnum(self, ServiceType):
        service = ServiceType.rstrip().replace(" ", "")
        if service == "1+0":
            return ServiceEnum.ONLY_ROUTE
        elif service == "1+1":
            return ServiceEnum.MAIN_ROUTE_AND_BACKUP
        elif service == "1+R":
            return ServiceEnum.MAIN_ROUTE_AND_RESTORATION
        elif service == "1+1+R":
            return ServiceEnum.MAIN_ROUTE_AND_BACKUP_AND_RESTORATION
        else:
            return ServiceEnum.NONE
