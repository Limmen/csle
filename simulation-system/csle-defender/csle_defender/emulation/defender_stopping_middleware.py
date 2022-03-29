from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.action.defender.defender_action import DefenderAction
from csle_common.dao.action.attacker.attacker_action import AttackerAction


class DefenderStoppingMiddleware:
    """
    Class that implements optimal stopping actions for the defender.
    """

    @staticmethod
    def stop_monitor(s: EmulationEnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                     emulation_env_config: EmulationEnvConfig) -> EmulationEnvState:
        """
        Performs a stopping action for the defender (reports an intrusion)

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the previous action of the attacker
        :param emulation_env_config: the emulation environment configuration
        :return: s_prime
        """
        s_prime = s
        s_prime.defender_obs_state.stopped = True
        return s_prime


    @staticmethod
    def continue_monitor(s: EmulationEnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                         emulation_env_config: EmulationEnvConfig) -> EmulationEnvState:
        """
        Performs a "continue" action for the defender (continues monitoring)

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the previous action of the attacker
        :param emulation_env_config: the emulation environment configuration
        :return: s_prime, reward, done
        """
        s_prime = s
        return s_prime

