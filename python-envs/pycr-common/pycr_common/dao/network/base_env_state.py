from typing import Tuple
from abc import ABC, abstractmethod
import numpy as np


class BaseEnvState(ABC):

    @abstractmethod
    def get_attacker_observation(self) -> Tuple[np.ndarray, np.ndarray]:
        pass


    @abstractmethod
    def get_defender_observation(self) -> Tuple[np.ndarray, np.ndarray]:
        pass

