from typing import Tuple
from gym_csle_ctf.dao.network.env_state import EnvState
from gym_csle_ctf.dao.network.env_config import csleEnvConfig
from gym_csle_ctf.dao.action.defender.defender_action import DefenderAction
from gym_csle_ctf.dao.action.attacker.attacker_action import AttackerAction


class DefenderStoppingMiddleware:
    """
    Class that implements optimal stopping actions for the defender.
    """

    @staticmethod
    def stop_monitor(s: EnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                     env_config: csleEnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a stopping action for the defender (reports an intrusion)

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the previous action of the attacker
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime = s

        if s_prime.attacker_obs_state.ongoing_intrusion():
            s_prime.attacker_obs_state.undetected_intrusions_steps += 1
            s_prime.defender_obs_state.caught_attacker = True
        else:
            s_prime.defender_obs_state.stopped = True
        return s_prime, 0, True


    @staticmethod
    def continue_monitor(s: EnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                         env_config: csleEnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a "continue" action for the defender (continues monitoring)

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the previous action of the attacker
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime = s
        if s_prime.attacker_obs_state.ongoing_intrusion():
            s_prime.attacker_obs_state.undetected_intrusions_steps += 1
        return s_prime, 0, False

