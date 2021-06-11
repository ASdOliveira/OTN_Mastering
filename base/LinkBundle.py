from base.Enums import LinkBundleType
from base.OpticalLink import OpticalLink
from base.TELink import TELink
from typing import List


class LinkBundle:
    def __init__(self, _OptLink: List[OpticalLink] = None, _TeLink: List[TELink] = None,
                 _RiskGroup: List[str] = None, _admGroup: List[int] = None,
                 _TLinkBundle: LinkBundleType = None):
        self.id = 0
        self.type = _TLinkBundle  # TODO: check type
        self.OtsOrigin = 0
        self.OtsDest = 0
        self.OpticalLinks = _OptLink
        self.TeLinks = _TeLink
        self.SharedGroupRiskList = _RiskGroup
        self.AdministrativeGroup = _admGroup

    def getWeight(self, metrics):
        penalty = 0.0
        ret = 0.0

        if metrics == 0:  # TODO: Check this case
            if self.type == LinkBundleType.Ten:
                ret = 1 + penalty
            else:
                ret = 1

        elif metrics == 1:  # Inverse of availability
            availableQuantity = self.__getAvailableSlots()
            ret = 1 / float(availableQuantity)

        elif metrics == 2:  # Restoration
            ret = self.__getAvailableSlots()

        else:
            pass

        return ret

    def __getAvailableSlots(self):
        availableQuantity = 0
        for TELINK in self.TeLinks:
            for SLOT in TELINK.tributarySlots:
                if not SLOT.IsBusy:
                    availableQuantity += 1
        return availableQuantity

    def HasResource(self, quantity):
        for TELINK in self.TeLinks:
            if TELINK.HasResource(quantity):
                return True
        return False

    def ContainsOpticalLinks(self, Id1, Id2):
        for OptLink in self.OpticalLinks:
            if (OptLink.id == Id1) or (OptLink.id == Id2):
                return True
        return False
