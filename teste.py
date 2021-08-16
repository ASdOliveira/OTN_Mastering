from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SBXCrossover, PolynomialMutation, IntegerPolynomialMutation
#from jmetal.problem import ZDT1
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.util.observer import ProgressBarObserver, VisualizerObserver
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions

from Models.Network import Network
from Problem import OTNProblem

Net = Network(folderName="Topologia1")
problem = OTNProblem(Net, len(Net.LinkBundles))

max_evaluations = 200

algorithm = NSGAII(
    problem=problem,
    population_size=40,
    offspring_population_size=40,
    mutation=IntegerPolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=0.20),
    crossover=IntegerSBXCrossover(probability=1.0, distribution_index=20),
    termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
)

progress_bar = ProgressBarObserver(max=max_evaluations)
algorithm.observable.register(progress_bar)

algorithm.run()
solutions = algorithm.get_result()

front = get_non_dominated_solutions(solutions)

for f in front:
    print(f.objectives[1])

plot_front = Plot(title='Pareto front approximation', axis_labels=['Interfaces', 'TIRF'])
plot_front.plot(front, label='NSGAII-OTN')