
class Interfaces:
    __id = 0
    # __rate (TOtnInterfaceRate missing type)
    # __fecTypeList (FecType missingType)
    __numPorts = 0
    # __formFactor (TFormFactor missingType)
    __portIndex = 0
    # __supportedProtocolList = 0 (protocolType missingType)
    __demands = []

    def getId(self):
        return self.__id

    def setId(self, newId):
        self.__id = newId

    def getNumPorts(self):
        return self.__numPorts

    def setNumPorts(self, newNumPort):
        self.__numPorts = newNumPort

    def getDemands(self):
        return self.__demands

    def setDemands(self, newDemands):
        self.__demands.append(newDemands)
