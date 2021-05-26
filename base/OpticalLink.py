from typing import List

class OpticalLink:

    def __init__(self, _regions: List[str] = None):
        self.id = 0
        # self.fiberType missingType
        self.length = 0.0
        self.attenuationCoefficient = 0.0
        self.pmdCoefficient = 0.0
        self.sharedGroupRisk = str
        self.regions = _regions
        # self.mode missingType
        self.zeroDispersionWaveLength = 0.0
        self.sourceSite = 0
        self.destinationSite = 0
        # self.channels missingType
        # self.application missingType
        self.IsOutOfOperation = False
        self.dispersionAt1550Nm = 0.0
