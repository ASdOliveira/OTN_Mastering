from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.core.quality_indicator import HyperVolume
from jmetal.operator import SBXCrossover, PolynomialMutation, IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.util.observer import ProgressBarObserver, VisualizerObserver, PrintObjectivesObserver
from jmetal.util.termination_criterion import StoppingByEvaluations, StoppingByQualityIndicator
from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions
from Models.Network import Network
from Problem import OTNProblem
import timeit

startTime = timeit.default_timer()

BestTirf = []
BestInterfaceQuantity = []

Net = Network(folderName="Topologia1")

for executions in range(30):
    print("Interation number:", executions)

    problem = OTNProblem(Net, len(Net.LinkBundles))

    max_evaluations = 2000

    algorithm = NSGAII(
        problem=problem,
        population_size=20,
        offspring_population_size=20,
        mutation=IntegerPolynomialMutation(probability=0.05, distribution_index=20),
        crossover=IntegerSBXCrossover(probability=0.3, distribution_index=20),
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
    )

    progress_bar = ProgressBarObserver(max=max_evaluations)
    algorithm.observable.register(progress_bar)

    algorithm.run()
    solutions = algorithm.get_result()

    front = get_non_dominated_solutions(solutions)

    InterfaceQuantities = []
    TirfValues = []

    for f in front:
        InterfaceQuantities.append(f.objectives[0])
        TirfValues.append(f.objectives[1])
        # print(f.objectives[0], f.objectives[1])

    TirfValues, InterfaceQuantities = zip(*sorted(zip(TirfValues, InterfaceQuantities)))

    BestTirf.append(TirfValues[0])
    BestInterfaceQuantity.append(InterfaceQuantities[0])
    print(TirfValues[0], InterfaceQuantities[0])

TheBestTirf = sum(BestTirf) / 30.0
TheBestQuantity = sum(BestInterfaceQuantity) / 30
print(TheBestQuantity, TheBestTirf)
#plot_front = Plot(title='Pareto front approximation', axis_labels=['Interfaces', 'TIRF'])
#plot_front.plot(front, label='NSGAII-OTN')
stopTime = timeit.default_timer()
print('Execution Time:', stopTime - startTime)