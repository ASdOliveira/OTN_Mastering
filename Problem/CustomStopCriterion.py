import copy
import os
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


class StoppingByEvaluationsCustom(TerminationCriterion):

    def __init__(self, max_evaluations: int, reference_point: [float] = None, AlgorithmName=''):
        super(StoppingByEvaluationsCustom, self).__init__()
        self.max_evaluations = max_evaluations
        self.evaluations = 0
        self.referencePoint = reference_point
        self.hyperVolumes = []
        self.IGDs = []
        self.AlgorithmName = AlgorithmName
        self._createSubfolder()
        # self.InitialFlag = False

    def update(self, *args, **kwargs):
        self.evaluations = kwargs['EVALUATIONS']
        solutions = kwargs['SOLUTIONS']

        if solutions:
            variables = []
            for s in solutions:
                variables.append(s.objectives)

            hv = HyperVolume(self.referencePoint)
            hv.is_minimization = True
            self.hyperVolumes.append(hv.compute(variables))

            # TODO: Implement to IGD

            if self.evaluations >= self.max_evaluations:
                fileValue = self._getFileValue()
                filename = 'Hist/' + str(self.AlgorithmName) + '/' + 'HV-' + str(fileValue) + '.txt'
                with open(filename, 'w') as f:
                    for hv in self.hyperVolumes:
                        f.write(str(hv))
                        f.write('\n')
    @property
    def is_met(self):
        return self.evaluations >= self.max_evaluations

    def _createSubfolder(self):
        newPath = 'Hist/' + str(self.AlgorithmName)
        if not os.path.isdir(newPath):
            os.makedirs(newPath)

    def _getFileValue(self):
        folderPath = 'Hist/' + str(self.AlgorithmName)
        HVFilesValue = []
        for file in os.listdir(folderPath):
            if 'HV' in file:
                split_first = file.split('-')
                final_split = split_first[1].split('.')
                HVFilesValue.append(int(final_split[0]))  # Given a file "HV-0.txt" the number 0 will be saved.
        if len(HVFilesValue) == 0:
            return 0
        else:
            return max(HVFilesValue) + 1

