from abc import ABC, abstractmethod
import gym
from pycr_common.dao.network.base_env_config import BaseEnvConfig
from pycr_common.dao.network.base_env_state import BaseEnvState


class BasePyCREnv(gym.Env, ABC):

    @staticmethod
    @abstractmethod
    def is_defense_action_legal(defense_action_id: int, env_config: BaseEnvConfig, env_state: BaseEnvState) -> bool:
        pass


    @staticmethod
    @abstractmethod
    def is_attack_action_legal(attack_action_id: int, env_config: BaseEnvConfig, env_state: BaseEnvState,
                               m_selection: bool = False,
                               m_action: bool = False, m_index: int = None) -> bool:
        pass