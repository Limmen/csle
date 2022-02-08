from typing import Tuple
from gym_csle_ctf.dao.network.env_state import EnvState
from gym_csle_ctf.dao.network.env_config import csleEnvConfig
from gym_csle_ctf.dao.action.attacker.attacker_action import AttackerAction


class AttackerStoppingSimulator:
    """
    Class that simulates implements optimal stopping actions for the attacker
    """

    @staticmethod
    def stop_intrusion(s: EnvState, a: AttackerAction, env_config: csleEnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a stopping action for the defender (reports an intrusion)

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        raise NotImplemented("Not Implemented yet")


    @staticmethod
    def continue_intrusion(s: EnvState, a: AttackerAction, env_config: csleEnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a "continue" action for the defender (continues monitoring)

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

