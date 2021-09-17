from typing import Tuple
from abc import ABC, abstractmethod
import numpy as np


class BaseEnvState(ABC):
    """
    Abstract class representing the state of the environment
    """

    @abstractmethod
    def get_attacker_observation(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        :return: the attacker observation
        """
        pass


    @abstractmethod
    def get_defender_observation(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        :return: The defender observation
        """
        pass

