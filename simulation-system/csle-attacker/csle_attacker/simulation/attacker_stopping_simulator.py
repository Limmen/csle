from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction


class AttackerStoppingSimulator:
    """
    Class that simulates implements optimal stopping actions for the attacker
    """

    @staticmethod
    def stop_intrusion(s: EmulationEnvState, a: EmulationAttackerAction, emulation_env_config: EmulationEnvConfig) \
            -> EmulationEnvState:
        """
        Performs a stopping action for the defender (reports an intrusion)

        :param s: the current state
        :param a: the action to take
        :param emulation_env_config: the emulation environment configuration
        :return: s_prime
        """
        raise NotImplemented("Not Implemented yet")


    @staticmethod
    def continue_intrusion(s: EmulationEnvState, a: EmulationAttackerAction, emulation_env_config: EmulationEnvConfig) \
            -> EmulationEnvState:
        """
        Performs a "continue" action for the defender (continues monitoring)

        :param s: the current state
        :param a: the action to take
        :param emulation_env_config: the emulation environment configuration
        :return: s_prime
        """
        return s

