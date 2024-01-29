from typing import List, Any
from abc import ABC, abstractmethod
import gymnasium as gym
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace


class BaseEnv(gym.Env, ABC):  # type: ignore
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

    @abstractmethod
    def set_model(self, model: Any) -> None:
        """
        Sets the model. Useful when using RL frameworks where the stage policy is not easy to extract

        :param model: the model
        :return: None
        """
        pass

    @abstractmethod
    def set_state(self, state: Any) -> None:
        """
        Sets the state. Allows to simulate samples from specific states

        :param state: the state
        :return: None
        """
        pass
