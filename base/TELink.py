from base.Enums import InterfaceRate
from base.Interfaces import Interfaces
from base.TributarySlot import Slot
from typing import List


class TELink:
    def __init__(self, _TributarySlots: List[Slot] = None):
        self.id = 0
        self.interfaceOrigin = Interfaces()
        self.interfaceDestination = Interfaces()
        self.tributarySlots = _TributarySlots

    def occupationRatio(self):
        BusyQuantity = 0
        for TR in self.tributarySlots:
            if TR.IsBusy:
                BusyQuantity += 1

        return float(BusyQuantity) / float(len(self.tributarySlots))

    def HasResource(self, quantity):
        aux = 0
        for SLOT in self.tributarySlots:
            if not SLOT.IsBusy:
                aux += 1
        return aux >= quantity

    def isRestoration(self):
        for SLOT in self.tributarySlots:
            if SLOT.demandCode is not None:
                return False
        return True

    def getRate(self):
        if len(self.tributarySlots) == 80:
            return InterfaceRate.Ten
        else:
            return InterfaceRate.Hundred




