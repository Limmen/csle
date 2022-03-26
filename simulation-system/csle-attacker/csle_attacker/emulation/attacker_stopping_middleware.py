from typing import Tuple
import time
from csle_common.dao.network.env_state import EnvState
from csle_common.dao.network.env_config import CSLEEnvConfig
from csle_common.dao.action.attacker.attacker_action import AttackerAction


class AttackerStoppingMiddleware:
    """
    Class that implements optimal stopping actions for the attacker
    """

    @staticmethod
    def stop_intrusion(s: EnvState, a: AttackerAction, env_config: CSLEEnvConfig) \
            -> Tuple[EnvState, float, bool]:
        """
        Performs a stopping action for the attacker

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        raise NotImplemented("Not Implemented yet")


    @staticmethod
    def continue_intrusion(s: EnvState, a: AttackerAction, env_config: CSLEEnvConfig) \
            -> Tuple[EnvState, float, bool]:
        """
        Performs a "continue" action for the attacker (does nothing)

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        if not env_config.use_attacker_action_stats_to_update_defender_state:
            time.sleep(env_config.attacker_continue_action_sleep)
        return s, 0, False

