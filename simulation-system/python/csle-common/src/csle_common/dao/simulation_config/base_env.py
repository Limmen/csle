from typing import List
from abc import ABC, abstractmethod
import gym
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace


class BaseEnv(gym.Env, ABC):
    """
    Abstract class representing a csle Environment
    """

    @abstractmethod
    def get_traces(self) -> List[SimulationTrace]:
        """
        :return: the list of simulation traces
        """
        pass

    @abstractmethod
    def reset_traces(self) -> None:
        """
        Resets the list of traces

        :return: None
        """
        pass

    @abstractmethod
    def manual_play(self) -> None:
        """
        An interactive loop for manual play of the environment

        :return: None
        """
        pass
