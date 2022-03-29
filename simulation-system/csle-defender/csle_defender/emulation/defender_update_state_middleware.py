from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.action.defender.defender_action import DefenderAction
from csle_common.dao.action.attacker.attacker_action import AttackerAction


class DefenderUpdateStateMiddleware:
    """
    Class that implements update state actions for the defender.
    """

    @staticmethod
    def update_belief_state(s: EmulationEnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                            emulation_env_config: EmulationEnvConfig) -> EmulationEnvState:
        """
        Updates the defender's state by measuring the emulation

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the attacker's previous action
        :param emulation_env_config: the emulation environment configuration
        :return: s_prime
        """
        s_prime = s   # TODO
        return s_prime

    @staticmethod
    def initialize_state(s: EmulationEnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                         emulation_env_config: EmulationEnvConfig) -> EmulationEnvState:
        """
        Initializes the defender's state by measuring the emulation

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the attacker's previous action
        :param emulation_env_config: the emulation environment configuration
        :return: s_prime
        """
        s_prime = s# TODO
        return s_prime

    @staticmethod
    def reset_state(s: EmulationEnvState, defender_action: DefenderAction, emulation_env_config: EmulationEnvConfig,
                    attacker_action: AttackerAction) -> EmulationEnvState:
        """
        Resets the defender's state

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the attacker's previous action
        :param emulation_env_config: the emulation environment configuration
        :return: s_prime
        """
        s_prime = s    #TODO
        return s_prime
