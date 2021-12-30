from abc import ABC, abstractmethod
import gym
from pycr_common.dao.network.base_env_config import BasePyCREnvConfig
from pycr_common.dao.network.base_env_state import BaseEnvState


class BasePyCREnv(gym.Env, ABC):
    """
    Abstract class representing a PyCR Environment
    """

    @staticmethod
    @abstractmethod
    def is_defense_action_legal(defense_action_id: int, env_config: BasePyCREnvConfig, env_state: BaseEnvState) -> bool:
        """
        Checks whether a defender action in the environment is legal or not

        :param defense_action_id: the id of the action
        :param env_config: the environment configuration
        :param env_state: the state of the environment
        :return: True or False
        """
        pass


    @staticmethod
    @abstractmethod
    def is_attack_action_legal(attack_action_id: int, env_config: BasePyCREnvConfig, env_state: BaseEnvState,
                               m_selection: bool = False,
                               m_action: bool = False, m_index: int = None) -> bool:
        """
        Checks whether an attacker action in the environment is legal or not

        :param attack_action_id: the id of the attacker action
        :param env_config: the environment configuration
        :param env_state: the state of the environment
        :param m_selection: the m_selection id in case an auto-regressive policy is used
        :param m_action: the m_action id in case an auto-regressive policy is used
        :param m_index: the m_inded in case an auto-regressive policy is used
        :return: True or False
        """
        pass