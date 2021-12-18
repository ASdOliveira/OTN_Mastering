from jmetal.algorithm.multiobjective import SPEA2, HYPE, SMPSO, MOCell, MOEAD, OMOPSO
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.core.quality_indicator import GenerationalDistance, EpsilonIndicator, HyperVolume, \
    InvertedGenerationalDistance
from jmetal.core.solution import IntegerSolution
from jmetal.operator import IntegerPolynomialMutation, PolynomialMutation, UniformMutation
from jmetal.operator.crossover import IntegerSBXCrossover, DifferentialEvolutionCrossover
from jmetal.operator.mutation import NonUniformMutation
from jmetal.util.aggregative_function import Tschebycheff
from jmetal.util.archive import CrowdingDistanceArchive
from jmetal.util.neighborhood import C9
from jmetal.util.termination_criterion import StoppingByEvaluations

import Utils
from Models.Network import Network
import timeit

from Problem.CustomStopCriterion import StoppingByEvaluationsCustom
from Problem.ProblemWrapper import OTNProblem, OTNProblemFloat

from jmetal.lab.experiment import Experiment, Job, generate_summary_from_experiment

from Utils import Filter

startTime = timeit.default_timer()

BestTirf = []
BestInterfaceQuantity = []
solutionsResult = []
frontResult = 0

max_evaluations = 20000
Net = Network(folderName="Topologia1")
# problemOTN = OTNProblem(Net, len(Net.LinkBundles))
problemOTN = OTNProblemFloat(Net, len(Net.LinkBundles))
stopCriterion = StoppingByEvaluationsCustom(max_evaluations, [200, 2.1])  # To topology 1, 200 is enough

reference_point = IntegerSolution([0], [8], problemOTN.number_of_objectives, )
reference_point.objectives = [200, 2.1]  # Mandatory for HYPE
mutation_probability = 0.08
swarm_size = 20


def configure_experiment(problems: dict, n_run: int):
    jobs = []

    for run in range(n_run):
        for problem_tag, problem in problems.items():
            # jobs.append(
            #     Job(
            #         algorithm=NSGAII(
            #             problem=problem,
            #             population_size=20,
            #             offspring_population_size=20,
            #             mutation=IntegerPolynomialMutation(probability=0.05, distribution_index=20),
            #             crossover=IntegerSBXCrossover(probability=0.3, distribution_index=20),
            #             termination_criterion=StoppingByEvaluationsCustom(max_evaluations=max_evaluations, reference_point=[200, 2.1],
            #                                               AlgorithmName='NSGAII')
            #             # termination_criterion=stopCriterion
            #         ),
            #         algorithm_tag='NSGAII',
            #         problem_tag=problem_tag,
            #         run=run,
            #     )
            # )
            # jobs.append(
            #     Job(
            #         algorithm=SPEA2(
            #             problem=problem,
            #             population_size=20,
            #             offspring_population_size=20,
            #             mutation=IntegerPolynomialMutation(probability=0.05, distribution_index=20),
            #             crossover=IntegerSBXCrossover(probability=0.3, distribution_index=20),
            #             termination_criterion=StoppingByEvaluationsCustom(max_evaluations=max_evaluations, reference_point=[200, 2.1],
            #                                               AlgorithmName='SPEA2')
            #         ),
            #         algorithm_tag='SPEA2',
            #         problem_tag=problem_tag,
            #         run=run,
            #     )
            # )
            # jobs.append(
            #     Job(
            #         algorithm=HYPE(
            #             problem=problem,
            #             reference_point=reference_point,
            #             population_size=20,
            #             offspring_population_size=20,
            #             mutation=IntegerPolynomialMutation(probability=0.05, distribution_index=20),
            #             crossover=IntegerSBXCrossover(probability=0.3, distribution_index=20),
            #             termination_criterion=StoppingByEvaluationsCustom(max_evaluations=max_evaluations, reference_point=[200, 2.1],
            #                                               AlgorithmName='HYPE')
            #         ),
            #         algorithm_tag='HYPE',
            #         problem_tag=problem_tag,
            #         run=run,
            #     )
            # )
            # jobs.append(
            #     Job(
            #         algorithm=MOCell(
            #             problem=problem,
            #             population_size=20,
            #             neighborhood=C9(4, 4),
            #             archive=CrowdingDistanceArchive(100),
            #             mutation=IntegerPolynomialMutation(probability=0.05, distribution_index=20),
            #             crossover=IntegerSBXCrossover(probability=0.3, distribution_index=20),
            #             termination_criterion=StoppingByEvaluationsCustom(max_evaluations=max_evaluations, reference_point=[200, 2.1],
            #                                               AlgorithmName='MOCell')
            #         ),
            #         algorithm_tag='MOCELL',
            #         problem_tag=problem_tag,
            #         run=run,
            #     )
            # )
            jobs.append(
                Job(
                    algorithm=OMOPSO(
                        problem=problem,
                        swarm_size=swarm_size,
                        epsilon=0.0075,
                        uniform_mutation=UniformMutation(probability=0.05, perturbation=0.5),
                        non_uniform_mutation=NonUniformMutation(mutation_probability, perturbation=0.5,
                                                                max_iterations=int(max_evaluations / swarm_size)),
                        leaders=CrowdingDistanceArchive(10),
                        termination_criterion=StoppingByEvaluationsCustom(max_evaluations=max_evaluations,
                                                                          reference_point=[200, 2.1],
                                                                          AlgorithmName='OMOPSO')
                    ),
                    algorithm_tag='OMOPSO',
                    problem_tag=problem_tag,
                    run=run,
                )
            )
            jobs.append(
                Job(
                    algorithm=SMPSO(
                        problem=problem,
                        swarm_size=20,
                        mutation=PolynomialMutation(probability=0.05, distribution_index=20),
                        leaders=CrowdingDistanceArchive(20),
                        termination_criterion=StoppingByEvaluationsCustom(max_evaluations=max_evaluations,
                                                                          reference_point=[200, 2.1],
                                                                          AlgorithmName='SMPSO')
                    ),
                    algorithm_tag='SMPSO',
                    problem_tag=problem_tag,
                    run=run,
                )
            )
    return jobs


if __name__ == '__main__':
    # Configure the experiments
    jobs = configure_experiment(problems={'OTN': problemOTN}, n_run=30)

    # Run the study
    output_directory = 'data'
    experiment = Experiment(output_dir=output_directory, jobs=jobs)
    experiment.run()

    Filter.RemovePenalty(output_directory)

    # Reference fronts is the folder where is the reference to be compared with.
    generate_summary_from_experiment(
        input_dir=output_directory,
        reference_fronts='C:\\Users\\aryss\\Documents\\Repositories\\OTN_Mastering\\Output\\CT3\\8 services',
        quality_indicators=[InvertedGenerationalDistance(), EpsilonIndicator(), HyperVolume([200, 2.1])]
    )
