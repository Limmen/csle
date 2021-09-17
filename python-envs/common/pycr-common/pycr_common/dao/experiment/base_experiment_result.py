from abc import ABC, abstractmethod


class BaseExperimentResult(ABC):

    @abstractmethod
    def reset() -> "BaseExperimentResult":
        pass