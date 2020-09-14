"""
Abstract TrainAgent
"""
from abc import ABC, abstractmethod
from gym_cgc_bta.dao.experiment_result import ExperimentResult

class TrainAgent(ABC):
    """
    Abstract train agent
    """

    @abstractmethod
    def train(self) -> ExperimentResult:
        pass

    @abstractmethod
    def eval(self) -> ExperimentResult:
        pass

