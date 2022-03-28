from abc import ABC, abstractmethod
import gym

from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig


class BaseEnv(gym.Env, ABC):
    """
    Abstract class representing a csle Environment
    """

    @staticmethod
    @abstractmethod
    def is_defense_action_legal(defense_action_id: int, emulation_env_config: EmulationEnvConfig, env_state: EmulationEnvState) -> bool:
        """
        Checks whether a defender action in the environment is legal or not

        :param defense_action_id: the id of the action
        :param emulation_env_agent_config: the environment configuration
        :param env_state: the state of the environment
        :return: True or False
        """
        pass


    @staticmethod
    @abstractmethod
    def is_attack_action_legal(attack_action_id: int, emulation_env_config: EmulationEnvConfig,
                               env_state: EmulationEnvState) -> bool:
        """
        Checks whether an attacker action in the environment is legal or not

        :param attack_action_id: the id of the attacker action
        :param emulation_env_config: the environment configuration
        :param env_state: the state of the environment
        :return: True or False
        """
        pass