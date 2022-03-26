from typing import Tuple
from csle_common.dao.network.env_state import EnvState
from csle_common.dao.network.env_config import CSLEEnvConfig
from csle_common.dao.action.defender.defender_action import DefenderAction


class DefenderStoppingUtil:
    """
    Class that implements functionality for optimal stopping actions for the defender
    """

    @staticmethod
    def stop_monitor(s: EnvState, a: DefenderAction, env_config: CSLEEnvConfig) -> Tuple[EnvState, float, bool]:
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
    def continue_monitor(s: EnvState, a: DefenderAction, env_config: CSLEEnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a "continue" action for the defender (continues monitoring)

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        pass
        # return s_prime, reward, done

