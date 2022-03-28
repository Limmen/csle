from csle_common.dao.network.emulation_env_state import EmulationEnvState
from csle_common.dao.network.emulation_env_agent_config import EmulationEnvAgentConfig
from csle_common.dao.action.attacker.attacker_action import AttackerAction


class AttackerStoppingSimulator:
    """
    Class that simulates implements optimal stopping actions for the attacker
    """

    @staticmethod
    def stop_intrusion(s: EmulationEnvState, a: AttackerAction, env_config: EmulationEnvAgentConfig) -> EmulationEnvState:
        """
        Performs a stopping action for the defender (reports an intrusion)

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime
        """
        raise NotImplemented("Not Implemented yet")


    @staticmethod
    def continue_intrusion(s: EmulationEnvState, a: AttackerAction, env_config: EmulationEnvAgentConfig) -> EmulationEnvState:
        """
        Performs a "continue" action for the defender (continues monitoring)

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime
        """
        return s

