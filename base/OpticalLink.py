class OpticalLink:

    def __init__(self):
        self.id = 0
        # self.fiberType missingType
        self.length = 0.0
        self.attenuationCoefficient = 0.0
        self.pmdCoefficient = 0.0
        self.sharedGroupRisk = ""
        self.regions = []
        # self.mode missingType
        self.zeroDispersionWaveLength = 0.0
        self.sourceSite = 0
        self.destinationSite = 0
        # self.channels missingType
        # self.application missingType
        self.IsOutOfOperation = False
        self.dispersionAt1550Nm = 0.0
