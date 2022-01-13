from abc import ABC, abstractmethod


class BaseExperimentResult(ABC):
    """
    Abstract class representing a DTO of the result of an experiment
    """

    @abstractmethod
    def reset(self) -> "BaseExperimentResult":
        """
        Resets the DTO

        :return: the resetted DTO
        """
        pass