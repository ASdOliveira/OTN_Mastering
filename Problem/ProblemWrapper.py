from jmetal.core.problem import IntegerProblem, FloatProblem
from jmetal.core.solution import IntegerSolution, FloatSolution
from Problem import Evaluation
from Problem.Config import *

class OTNProblem(IntegerProblem):
    def __init__(self, network, number_of_variables):
        super(OTNProblem, self).__init__()
        self.number_of_objectives = 3
        self.number_of_constraints = 0
        self.number_of_variables = number_of_variables

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE, self.MAXIMIZE]
        self.obj_labels = ['InterfacesQuantities', 'TIRF', 'efficiency']

        self.lower_bound = number_of_variables * [LOWER_BOUND]
        self.upper_bound = number_of_variables * [UPPER_BOUND]

        self.network = network

    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        EvaluationResult = Evaluation.evaluateNetwork(self.network, solution.variables)
        solution.objectives[0] = EvaluationResult[0]
        solution.objectives[1] = EvaluationResult[1]
        solution.objectives[2] = EvaluationResult[2]
        # solution.objectives[0] = solution.variables[0]
        # solution.objectives[1] = h * g

        return solution

    def get_name(self):
        return 'OTNProblem'


class OTNProblemFloat(FloatProblem):
    def __init__(self, network, number_of_variables):
        super(OTNProblemFloat, self).__init__()
        self.number_of_objectives = 3
        self.number_of_constraints = 0
        self.number_of_variables = number_of_variables

        self.obj_directions = [self.MINIMIZE, self.MINIMIZE, self.MAXIMIZE]
        self.obj_labels = ['InterfacesQuantities', 'TIRF', 'efficiency']

        self.lower_bound = number_of_variables * [LOWER_BOUND]
        self.upper_bound = number_of_variables * [UPPER_BOUND]

        self.network = network

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        EvaluationResult = Evaluation.evaluateNetwork(self.network, solution.variables)
        solution.objectives[0] = EvaluationResult[0]
        solution.objectives[1] = EvaluationResult[1]
        solution.objectives[2] = EvaluationResult[2]
        # solution.objectives[0] = solution.variables[0]
        # solution.objectives[1] = h * g

        return solution

    def get_name(self):
        return 'OTNProblem'
