from typing import List
from abc import ABC, abstractmethod
from pycr_common.agents.config.agent_config import AgentConfig


class BaseRolloutDataDTO(ABC):
    """
    Abstract base class for DTOs with rollout data
    """

    @abstractmethod
    def copy(self) -> "RolloutDataDTO":
        """
        :return: a copy of the DTO
        """
        pass

    @abstractmethod
    def initialize(self) -> None:
        """
        Initializes the DTO

        :return: none
        """
        pass

    def update(self, attacker_rewards: List[int], defender_rewards: List[int], episode_steps: List[int],
               infos: List[dict], i: int, env_response_time: float, action_pred_time: float,
               attacker_agent_config: AgentConfig) -> None:
        """
        Updates the DTO with new information

        :param attacker_rewards: list of  attacker rewards
        :param defender_rewards: list of defender rewards
        :param episode_steps: list of episode steps
        :param infos: list of dict infos
        :param i: index
        :param env_response_time: response time from the env for profiling
        :param action_pred_time: action prediction time for profiling
        :param attacker_agent_config: the training configuration
        :return: None
        """
        pass

    def update_done(self, attacker_reward: List[float], defender_reward: List[float], steps: List[int]):
        """
        Performs a final update to the rollout DTO when the episode has ended

        :param self:
        :param attacker_reward:
        :param defender_reward:
        :param steps:
        :return:
        """
        pass