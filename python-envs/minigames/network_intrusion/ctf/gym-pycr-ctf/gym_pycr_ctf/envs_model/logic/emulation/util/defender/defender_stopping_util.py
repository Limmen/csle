from typing import Tuple
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.defender.defender_action import DefenderAction


class DefenderStoppingUtil:
    """
    Class that implements functionality for optimal stopping actions for the defender
    """

    @staticmethod
    def stop_monitor(s: EnvState, a: DefenderAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a stopping action for the defender (reports an intrusion)

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        pass
        #return s_prime, reward, done


    @staticmethod
    def continue_monitor(s: EnvState, a: DefenderAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a "continue" action for the defender (continues monitoring)

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        pass
        # return s_prime, reward, done

