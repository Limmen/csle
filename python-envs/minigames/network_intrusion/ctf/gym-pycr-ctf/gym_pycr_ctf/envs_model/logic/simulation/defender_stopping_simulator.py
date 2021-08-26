from typing import Tuple
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.defender.defender_action import DefenderAction
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction


class DefenderStoppingSimulator:
    """
    Class that simulates optimal stopping actions for the defender.
    """


    @staticmethod
    def stop_monitor(s: EnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                     env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a stopping action for the defender (reports an intrusion)

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the attacker's previous action
        :param env_config: the environment configuration
        :return: s_prime, reward, done
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

        reward = 0
        done = False
        if s_prime.attacker_obs_state.ongoing_intrusion():
            s_prime.attacker_obs_state.undetected_intrusions_steps += 1
            if env_config.attacker_prevented_stops_remaining >= s_prime.defender_obs_state.stops_remaining:
                if not s_prime.defender_obs_state.caught_attacker:
                    s_prime.defender_obs_state.caught_attacker = True
            if s_prime.defender_obs_state.stops_remaining == 0:
                done = True
            else:
                if not s.defender_obs_state.caught_attacker:
                    reward = reward + env_config.defender_intrusion_reward
                    s_prime.attacker_obs_state.undetected_intrusions_steps += 1
        else:
            if s_prime.defender_obs_state.stops_remaining == 0:
                s_prime.defender_obs_state.stopped = True
                done = True

        #costs = 0
        idx = env_config.maximum_number_of_defender_stop_actions - s_prime.defender_obs_state.stops_remaining
        costs = env_config.multistop_costs[idx]
        reward = reward + costs
        if not done:
            reward = reward + env_config.defender_service_reward

        return s_prime, reward, done


    @staticmethod
    def continue_monitor(s: EnvState, defender_action: DefenderAction, env_config: EnvConfig,
                         attacker_action: AttackerAction) -> Tuple[EnvState, float, bool]:
        """
        Performs a "continue" action for the defender (continues monitoring)

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the attacker's previous action
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime = s
        reward = env_config.defender_service_reward
        if s_prime.attacker_obs_state.ongoing_intrusion():
            if not s.defender_obs_state.caught_attacker:
                reward = reward + env_config.defender_intrusion_reward
                s_prime.attacker_obs_state.undetected_intrusions_steps += 1
        return s_prime, reward, False

