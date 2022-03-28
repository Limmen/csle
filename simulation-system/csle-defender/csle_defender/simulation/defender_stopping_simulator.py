import math
from csle_common.dao.network.emulation_env_state import EmulationEnvState
from csle_common.dao.network.emulation_env_agent_config import EmulationEnvAgentConfig
from csle_common.dao.action.defender.defender_action import DefenderAction
from csle_common.dao.action.attacker.attacker_action import AttackerAction


class DefenderStoppingSimulator:
    """
    Class that simulates optimal stopping actions for the defender.
    """

    @staticmethod
    def stop_monitor(s: EmulationEnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                     env_config: EmulationEnvAgentConfig) -> EmulationEnvState:
        """
        Performs a stopping action for the defender (reports an intrusion)

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the attacker's previous action
        :param env_config: the environment configuration
        :return: s_prime
        """
        s_prime = s
        s_prime.defender_obs_state.stops_remaining -= 1
        if (s_prime.defender_obs_state.maximum_number_of_stops - s_prime.defender_obs_state.stops_remaining) == 1:
            s_prime.defender_obs_state.first_stop_step = s_prime.defender_obs_state.step
        elif (s_prime.defender_obs_state.maximum_number_of_stops - s_prime.defender_obs_state.stops_remaining) == 2:
            s_prime.defender_obs_state.second_stop_step = s_prime.defender_obs_state.step
        elif (s_prime.defender_obs_state.maximum_number_of_stops - s_prime.defender_obs_state.stops_remaining) == 3:
            s_prime.defender_obs_state.third_stop_step = s_prime.defender_obs_state.step
        elif (s_prime.defender_obs_state.maximum_number_of_stops - s_prime.defender_obs_state.stops_remaining) == 4:
            s_prime.defender_obs_state.fourth_stop_step = s_prime.defender_obs_state.step
        else:
            raise ValueError("Stopping step not recognized")

        s_prime.defender_obs_state.num_login_attempts_total = 0
        s_prime.defender_obs_state.num_warning_alerts_total = 0
        s_prime.defender_obs_state.num_severe_alerts_total = 0
        s_prime.defender_obs_state.sum_priority_alerts_total = 0
        s_prime.defender_obs_state.num_alerts_total = 0

        return s_prime


    @staticmethod
    def continue_monitor(s: EmulationEnvState, defender_action: DefenderAction, env_config: EmulationEnvAgentConfig,
                         attacker_action: AttackerAction) -> EmulationEnvState:
        """
        Performs a "continue" action for the defender (continues monitoring)

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the attacker's previous action
        :param env_config: the environment configuration
        :return: s_prime
        """
        s_prime = s
        return s_prime

