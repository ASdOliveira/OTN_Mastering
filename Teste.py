from jmetal.algorithm.multiobjective import SMPSO, SPEA2
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.core.quality_indicator import HyperVolume, GenerationalDistance, EpsilonIndicator
from jmetal.operator import SBXCrossover, PolynomialMutation, IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.util.archive import CrowdingDistanceArchive
from jmetal.util.observer import ProgressBarObserver, VisualizerObserver, PrintObjectivesObserver
from jmetal.util.termination_criterion import StoppingByEvaluations, StoppingByQualityIndicator
from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions
from Models.Network import Network
import timeit

from Problem.CustomStopCriterion import StopByHyperVolume, StoppingByEvaluationsCustom
from Problem.ProblemWrapper import OTNProblem
from Utils.Log import Log

from jmetal.lab.experiment import Experiment, Job, generate_summary_from_experiment

startTime = timeit.default_timer()

BestTirf = []
BestInterfaceQuantity = []
solutionsResult = []
frontResult = 0

max_evaluations = 2000
Net = Network(folderName="Topologia1")
problemOTN = OTNProblem(Net, len(Net.LinkBundles))
stopCriterion = StoppingByEvaluationsCustom(max_evaluations, [200, 2.1])  # To topology 1, 200 is enough


def configure_experiment(problems: dict, n_run: int):
    jobs = []

    for run in range(n_run):
        for problem_tag, problem in problems.items():
            jobs.append(
                Job(
                    algorithm=NSGAII(
                        problem=problem,
                        population_size=20,
                        offspring_population_size=20,
                        mutation=IntegerPolynomialMutation(probability=0.05, distribution_index=20),
                        crossover=IntegerSBXCrossover(probability=0.3, distribution_index=20),
                        # termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
                        termination_criterion=stopCriterion
                    ),
                    algorithm_tag='NSGAII',
                    problem_tag=problem_tag,
                    run=run,
                )
            )
            jobs.append(
                Job(
                    algorithm=SPEA2(
                        problem=problem,
                        population_size=20,
                        offspring_population_size=20,
                        mutation=IntegerPolynomialMutation(probability=0.05, distribution_index=20),
                        crossover=IntegerSBXCrossover(probability=0.3, distribution_index=20),
                        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
                    ),
                    algorithm_tag='SPEA2',
                    problem_tag=problem_tag,
                    run=run,
                )
            )
    return jobs

#     progress_bar = ProgressBarObserver(max=max_evaluations)
#     algorithm.observable.register(progress_bar)
#
#     algorithm.run()
#     solutions = algorithm.get_result()
#
#     for solution in solutions:
#         if not solution.objectives[1] >= 1.0:
#             solutionsResult.append(solution)
#
#     if executions == (timesToRun - 1):
#         frontResult = get_non_dominated_solutions(solutionsResult)
#
#
# plot_front = Plot(title='Pareto front approximation', axis_labels=['Interfaces', 'TIRF'])
# plot_front.plot(frontResult, label='NSGAII-OTN')
#
# stopTime = timeit.default_timer()
# print('Execution Time:', stopTime - startTime)


if __name__ == '__main__':
    # Configure the experiments
    jobs = configure_experiment(problems={'OTN': problemOTN}, n_run=30)

    # Run the study
    output_directory = 'data'
    experiment = Experiment(output_dir=output_directory, jobs=jobs)
    experiment.run()

    # Reference fronts is the folder where is the reference to be compared with.
    # generate_summary_from_experiment(
    #     input_dir=output_directory,
    #     reference_fronts='C:\\Users\\aryss\\Documents\\Repositories\\OTN_Mastering\\data\\NSGAII\\OTN',
    #     quality_indicators=[GenerationalDistance(), EpsilonIndicator(), HyperVolume([200, 2.1])]
    # )
