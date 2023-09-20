from typing import Dict, Any
import numpy as np
import numpy.typing as npt
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
from csle_agents.agents.bayesian_optimization_emukit.bo.gp.gp_config import GPConfig
from csle_agents.agents.bayesian_optimization_emukit.bo.acquisition.acquisition_function_type import \
    AcquisitionFunctionType
from csle_agents.agents.bayesian_optimization_emukit.bo.acquisition.acquisition_optimizer_type import \
    AcquisitionOptimizerType
from csle_agents.common.objective_type import ObjectiveType


class BOConfig:
    """
    DTO representing the configuration of a Bayesian Optimization execution
    """

    def __init__(self, X_init: npt.NDArray[Any],
                 Y_init: npt.NDArray[Any], input_space: ParameterSpace, evaluation_budget: int,
                 gp_config: GPConfig, acquisition_function_type: AcquisitionFunctionType,
                 acquisition_optimizer_type: AcquisitionOptimizerType,
                 objective_type: ObjectiveType, beta: float = 1) -> None:
        """
        Initializes the DTO

        :param X_init: the initial dataset with x-values
        :param Y_init: the initial dataset with y-values
        :param input_space: the input space (i.e. the list of x-variables and their dimensions
        :param evaluation_budget: the evaluation budget (i.e. maximum cost)
        :param gp_config: the configuration of the GP
        :param acquisition_function_type: the acquisition function to use
        :param acquisition_optimizer_type: the type of optimizer for optimizing the acquisition function
        :param objective_type: the objective (min or max)
        :param beta: exploration parameter for GP-UCB
        """
        self.X_init = X_init
        self.Y_init = Y_init
        self.input_space = input_space
        self.evaluation_budget = evaluation_budget
        self.gp_config = gp_config
        self.acquisition_function_type = acquisition_function_type
        self.acquisition_optimizer_type = acquisition_optimizer_type
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
            return NegativeLowerConfidenceBound(surrogate_model, beta=self.beta)
        elif self.acquisition_function_type == AcquisitionFunctionType.PROBABILITY_OF_IMPROVEMENT:
            return ProbabilityOfImprovement(surrogate_model)
        elif self.acquisition_function_type == AcquisitionFunctionType.MAX_VALUE_ENTROPY_SEARCH:
            return MaxValueEntropySearch(surrogate_model, space=self.input_space)
        elif self.acquisition_function_type == AcquisitionFunctionType.MUMBO:
            return MUMBO(surrogate_model, space=self.input_space)
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
        return f"X_init: {self.X_init}, Y_init: {self.Y_init}, input_space: {self.input_space}, " \
               f"evaluation_budget: {self.evaluation_budget}, gp_config: {self.gp_config}," \
               f"acquisition_optimizer_type: {self.acquisition_optimizer_type}, " \
               f"acquisition_function_type: {self.acquisition_function_type}, " \
               f"objective_type: {self.objective_type}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BOConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        dto = BOConfig(
            X_init=np.array(d["X_init"]), Y_init=np.array(d["Y_init"]),
            input_space=ParameterSpace(parameters=[]), evaluation_budget=d["evaluation_budget"],
            gp_config=GPConfig.from_dict(d["gp_config"]), acquisition_function_type=d["acquisition_function_type"],
            acquisition_optimizer_type=d["acquisition_optimizer_type"], objective_type=d["objective_type"],
            beta=d["beta"])
        return dto

    def to_dict(self) -> Dict[str, Any]:
        """
        Gets a dict representation of the object

        :return: A dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["X_init"] = list(self.X_init)
        d["Y_init"] = list(self.Y_init)
        d["evaluation_budget"] = self.evaluation_budget
        d["gp_config"] = self.gp_config.to_dict()
        d["acquisition_function_type"] = self.acquisition_function_type.value
        d["acquisition_optimizer_type"] = self.acquisition_optimizer_type.value
        d["objective_type"] = self.objective_type.value
        d["beta"] = self.beta
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "BOConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return BOConfig.from_dict(json.loads(json_str))
