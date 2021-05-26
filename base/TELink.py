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
        for i in range(len(self.tributarySlots)):
            if self.tributarySlots[i].IsBusy:
                BusyQuantity += 1

        return float(BusyQuantity) / float(len(self.tributarySlots))

    def HasResource(self, quantity):
        aux = 0
        for SLOT in self.tributarySlots:
            if not SLOT.IsBusy:
                aux += 1
        return aux >= quantity

    def isRestoration(self):
        for i in range(len(self.tributarySlots)):
            if self.tributarySlots[i].demandCode is None:  # TODO: Check This None!!
                return False
        return True

    def getRate(self):
        pass
        """  if len(self.tributarySlots) == 80:
            #What does this TOtnInterfaceRate???
        return(getTributarySlots().size() == 80)?TOtnInterfaceRate._100: TOtnInterfaceRate._10;"""



