from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.core.quality_indicator import HyperVolume
from jmetal.operator import SBXCrossover, PolynomialMutation, IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.util.observer import ProgressBarObserver, VisualizerObserver, PrintObjectivesObserver
from jmetal.util.termination_criterion import StoppingByEvaluations, StoppingByQualityIndicator
from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions
from Models.Network import Network
import timeit

from Problem.CustomStopCriterion import StopByHyperVolume, StoppingByEvaluationsCustom
from Problem.ProblemWrapper import OTNProblem
from Utils.Log import Log

startTime = timeit.default_timer()

BestTirf = []
BestInterfaceQuantity = []
solutionsResult = []
frontResult = 0
timesToRun = 1

log_front = Log("front_140_Services")

Net = Network(folderName="Topologia2")

for executions in range(timesToRun):
    print("Interation number:", executions)

    problem = OTNProblem(Net, len(Net.LinkBundles))
    max_evaluations = 1000
    # stopCriterion = StoppingByEvaluationsCustom(max_evaluations, [200, 2.1])  # To topology 1, 200 is enough

    algorithm = NSGAII(
        problem=problem,
        population_size=20,
        offspring_population_size=20,
        mutation=IntegerPolynomialMutation(probability=0.05, distribution_index=20),
        crossover=IntegerSBXCrossover(probability=0.3, distribution_index=20),
        termination_criterion=StoppingByEvaluationsCustom(max_evaluations=max_evaluations,
                                                                          reference_point=[5000, 2.1],
                                                                          AlgorithmName='Reference')
        # termination_criterion=stopCriterion
    )

    progress_bar = ProgressBarObserver(max=max_evaluations)
    algorithm.observable.register(progress_bar)

    algorithm.run()
    solutions = algorithm.get_result()

    for solution in solutions:
        if not solution.objectives[1] >= 1.3:
            solutionsResult.append(solution)

    if executions == (timesToRun - 1):
        frontResult = get_non_dominated_solutions(solutionsResult)
        for sol in frontResult:
            log_front.log(str(sol.objectives[0]) + " " + str(sol.objectives[1]))
log_front.save()
plot_front = Plot(title='Pareto front approximation', axis_labels=['Interfaces', 'TIRF'])
plot_front.plot(frontResult, label='NSGAII-OTN')

stopTime = timeit.default_timer()
print('Execution Time:', stopTime - startTime)