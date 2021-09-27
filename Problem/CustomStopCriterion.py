import copy

from jmetal.core.quality_indicator import HyperVolume
from jmetal.util.termination_criterion import TerminationCriterion


class StopByHyperVolume(TerminationCriterion):
    def __init__(self, hyperVolumeStagnationPercentage: float, reference_point: [float] = None):
        super(StopByHyperVolume, self).__init__()
        self.lastHyperVolume = 0.0001
        self.currentHyperVolume = 0.0
        self.HyperVolumeStagnationPercentage = hyperVolumeStagnationPercentage
        self.referencePoint = reference_point
        self.HasReachVariation = False
        self.counter = 0

    def update(self, *args, **kwargs):
        solutions = kwargs['SOLUTIONS']

        if solutions:
            variables = []
            for s in solutions:
                variables.append(s.objectives)

            hv = HyperVolume(self.referencePoint)
            hv.is_minimization = True
            self.currentHyperVolume = hv.compute(variables)

            variation = float(abs(self.lastHyperVolume - self.currentHyperVolume) / self.currentHyperVolume)

            if variation <= self.HyperVolumeStagnationPercentage:
                self.counter += 1
                if self.counter >= 15:
                    self.HasReachVariation = True
                else:
                    self.lastHyperVolume = copy.deepcopy(self.currentHyperVolume)
            else:
                self.lastHyperVolume = copy.deepcopy(self.currentHyperVolume)
                self.counter = 0
                self.HasReachVariation = False

            print(self.counter)

    @property
    def is_met(self):
        return self.HasReachVariation
