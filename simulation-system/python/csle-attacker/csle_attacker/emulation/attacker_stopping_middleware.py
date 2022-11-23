from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction


class AttackerStoppingMiddleware:
    """
    Class that implements optimal stopping actions for the attacker
    """

    @staticmethod
    def stop_intrusion(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a stopping action for the attacker

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        raise NotImplementedError("Not Implemented yet")

    @staticmethod
    def continue_intrusion(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a "continue" action for the attacker (does nothing)

        :param s: the current state
        :param a: the action to take
        :return: s_prime, reward, done
        """
        return s
