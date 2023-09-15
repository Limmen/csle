from typing import Callable
import numpy as np
from emukit.core import ParameterSpace
from emukit.bayesian_optimization.acquisitions.expected_improvement import ExpectedImprovement
from emukit.bayesian_optimization.acquisitions.negative_lower_confidence_bound import NegativeLowerConfidenceBound
from emukit.bayesian_optimization.acquisitions.probability_of_improvement import ProbabilityOfImprovement
from emukit.bayesian_optimization.acquisitions.max_value_entropy_search import MaxValueEntropySearch
from emukit.bayesian_optimization.acquisitions.max_value_entropy_search import MUMBO
from emukit.bayesian_optimization.acquisitions.entropy_search import EntropySearch
from emukit.core.acquisition.acquisition import Acquisition
from emukit.model_wrappers.gpy_model_wrappers import GPyModelWrapper
from emukit.core.optimization import GradientAcquisitionOptimizer
from emukit.core.optimization import AcquisitionOptimizerBase
from csle_tolerance.dao.bo.gp.gp_config import GPConfig
from csle_tolerance.dao.bo.acquisition.acquisition_function_type import AcquisitionFunctionType
from csle_tolerance.dao.bo.acquisition.acquisition_optimizer_type import AcquisitionOptimizerType
from csle_tolerance.dao.bo.optimization.objective_type import ObjectiveType


class BOConfig:
    """
    DTO representing the configuration of a Bayesian Optimization execution
    """

    def __init__(self, objective_function: Callable, cost_function: Callable, X_init: np.ndarray,
                 Y_init: np.ndarray, input_space: ParameterSpace, evaluation_budget: int,
                 gp_config: GPConfig, acquisition_function_type: AcquisitionFunctionType,
                 acquisition_optimizer_type: AcquisitionOptimizerType, log_file: str, log_level: int,
                 objective_type: ObjectiveType, beta: float = 1) -> None:
        """
        Initializes the DTO

        :param objective_function: the objective function to optimize
        :param cost_function: the cost function to minimize (cost of function evaluations)
        :param X_init: the initial dataset with x-values
        :param Y_init: the initial dataset with y-values
        :param input_space: the input space (i.e. the list of x-variables and their dimensions
        :param evaluation_budget: the evaluation budget (i.e. maximum cost)
        :param gp_config: the configuration of the GP
        :param acquisition_function_type: the acquisition function to use
        :param acquisition_optimizer_type: the type of optimizer for optimizing the acquisition function
        :param log_file: the log file to write log entries to
        :param log_level: the level of logging
        :param objective_type: the objective (min or max)
        :param beta: exploration parameter for GP-UCB
        """
        self.objective_function = objective_function
        self.cost_function = cost_function
        self.X_init = X_init
        self.Y_init = Y_init
        self.input_space = input_space
        self.evaluation_budget = evaluation_budget
        self.gp_config = gp_config
        self.acquisition_function_type = acquisition_function_type
        self.acquisition_optimizer_type = acquisition_optimizer_type
        self.log_file = log_file
        self.log_level = log_level
        self.objective_type = objective_type
        self.beta = beta

    def get_acquisition_function(self, surrogate_model: GPyModelWrapper) -> Acquisition:
        """
        Gets the acquisition function for the configuration

        :param surrogate_model: the surrogate model to use for the acquisition
        :return: the acquisition function (from the emukit library)
        """
        if self.acquisition_function_type == AcquisitionFunctionType.EXPECTED_IMPROVEMENT:
            return ExpectedImprovement(surrogate_model)
        elif self.acquisition_function_type == AcquisitionFunctionType.NEGATIVE_LOWER_CONFIDENCE_BOUND:
            return NegativeLowerConfidenceBound(surrogate_model, beta = self.beta)
        elif self.acquisition_function_type == AcquisitionFunctionType.PROBABILITY_OF_IMPROVEMENT:
            return ProbabilityOfImprovement(surrogate_model)
        elif self.acquisition_function_type == AcquisitionFunctionType.MAX_VALUE_ENTROPY_SEARCH:
            return MaxValueEntropySearch(surrogate_model, space=self.input_space)
        elif self.acquisition_function_type == AcquisitionFunctionType.MUMBO:
            return MUMBO(surrogate_model, space = self.input_space)
        elif self.acquisition_function_type == AcquisitionFunctionType.ENTROPY_SEARCH:
            return EntropySearch(surrogate_model, space=self.input_space)
        else:
            raise ValueError(f"Acquisition function type: {self.acquisition_function_type} is not supported")

    def get_acquisition_optimizer(self) -> AcquisitionOptimizerBase:
        """
        Gets the acquisition function optimizer for the given configuration

        :return: the optimizer (from the emukit library)
        """
        if self.acquisition_optimizer_type == AcquisitionOptimizerType.GRADIENT:
            return GradientAcquisitionOptimizer(self.input_space)
        else:
            raise ValueError(f"The specified acquisition optimizer type: {self.acquisition_optimizer_type} "
                             f"is not supported")

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"objetive_function: {self.objective_function}, cost_function: {self.cost_function}, " \
               f"X_init: {self.X_init}, Y_init: {self.Y_init}, input_space: {self.input_space}, " \
               f"evaluation_budget: {self.evaluation_budget}, gp_config: {self.gp_config}," \
               f"acquisition_optimizer_type: {self.acquisition_optimizer_type}, " \
               f"acquisition_function_type: {self.acquisition_function_type}, " \
               f"log_file: {self.log_file}, log_level: {self.log_level}, objective_type: {self.objective_type}"
