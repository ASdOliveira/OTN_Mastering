from typing import List


class Interfaces:
    def __init__(self, _Demands: List[int] = None):
        self.id = 0
        # self.rate (TOtnInterfaceRate missing type)
        # self.fecTypeList(FecType missingType)
        self.numPorts = 0
        # self.formFactor (TFormFactor missingType)
        self.portIndex = 0
        # self.supportedProtocolList (protocolType missingType)
        self.demands = _Demands
