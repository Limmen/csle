from typing import List
from abc import ABC, abstractmethod
from pycr_common.agents.config.agent_config import AgentConfig


class BaseRolloutDataDTO(ABC):


    @abstractmethod
    def copy(self) -> "RolloutDataDTO":
        pass

    @abstractmethod
    def initialize(self) -> None:
        pass

    @staticmethod
    def update(self, attacker_rewards: List[int], defender_rewards: List[int], episode_steps: List[int],
               infos: List[dict], i: int, env_response_time: float, action_pred_time: float,
               attacker_agent_config: AgentConfig) -> None:
        pass


    @staticmethod
    def update_done(self, attacker_reward: List[float], defender_reward: List[float], steps: List[int]):
        pass