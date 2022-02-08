from typing import Tuple
import math
from gym_csle_ctf.dao.network.env_state import EnvState
from gym_csle_ctf.dao.network.env_config import csleEnvConfig
from gym_csle_ctf.dao.action.defender.defender_action import DefenderAction
from gym_csle_ctf.dao.action.attacker.attacker_action import AttackerAction


class DefenderStoppingSimulator:
    """
    Class that simulates optimal stopping actions for the defender.
    """


    @staticmethod
    def stop_monitor(s: EnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                     env_config: csleEnvConfig) -> Tuple[EnvState, float, bool]:
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
        else:
            raise ValueError("Stopping step not recognized")

        s_prime.defender_obs_state.num_login_attempts_total = 0
        s_prime.defender_obs_state.num_warning_alerts_total = 0
        s_prime.defender_obs_state.num_severe_alerts_total = 0
        s_prime.defender_obs_state.sum_priority_alerts_total = 0
        s_prime.defender_obs_state.num_alerts_total = 0

        reward = 0
        done = False
        if s_prime.attacker_obs_state.ongoing_intrusion():
            s_prime.attacker_obs_state.undetected_intrusions_steps += 1
            if env_config.attacker_prevented_stops_remaining == s_prime.defender_obs_state.stops_remaining:
                if not s_prime.defender_obs_state.caught_attacker:
                    s_prime.defender_obs_state.caught_attacker = True
                    reward = reward + env_config.defender_caught_attacker_reward
            if s_prime.defender_obs_state.stops_remaining == 0:
                done = True
        else:
            if s_prime.defender_obs_state.stops_remaining <= env_config.attacker_prevented_stops_remaining:
                s_prime.defender_obs_state.stopped = True

            if s_prime.defender_obs_state.stops_remaining == 0:
                done = True

        # if env_config.attacker_prevented_stops_remaining > s_prime.defender_obs_state.stops_remaining:
        #     reward = reward + env_config.defender_early_stopping_reward

        idx = env_config.maximum_number_of_defender_stop_actions - (env_config.maximum_number_of_defender_stop_actions -
                                                                    s_prime.defender_obs_state.stops_remaining)
        costs = env_config.multistop_costs[idx]
        reward = reward + costs
        # if not done:
        # reward = reward + env_config.defender_service_reward / math.pow(2, (env_config.maximum_number_of_defender_stop_actions -
        #                                                            s_prime.defender_obs_state.stops_remaining))

        return s_prime, reward, done


    @staticmethod
    def continue_monitor(s: EnvState, defender_action: DefenderAction, env_config: csleEnvConfig,
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
        reward = env_config.defender_service_reward/math.pow(2, (env_config.maximum_number_of_defender_stop_actions-
                                                     s_prime.defender_obs_state.stops_remaining))
        if s_prime.attacker_obs_state.ongoing_intrusion():
            if not s.defender_obs_state.caught_attacker \
                    and not env_config.attacker_prevented_stops_remaining >= s_prime.defender_obs_state.stops_remaining:
                reward = reward + env_config.defender_intrusion_reward
                s_prime.attacker_obs_state.undetected_intrusions_steps += 1
        # idx = env_config.maximum_number_of_defender_stop_actions - (env_config.maximum_number_of_defender_stop_actions -
        #                                                             s_prime.defender_obs_state.stops_remaining)
        #costs = env_config.multistop_costs[idx]
        # reward = reward + costs
        return s_prime, reward, False

