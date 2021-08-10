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
        reward = 0
        if s_prime.attacker_obs_state.ongoing_intrusion():
            s_prime.attacker_obs_state.undetected_intrusions_steps += 1
            s_prime.defender_obs_state.caught_attacker = True
            reward = env_config.defender_caught_attacker_reward
        else:
            s_prime.defender_obs_state.stopped = True
            reward = env_config.defender_early_stopping_reward
        return s_prime, reward, True


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
            s_prime.attacker_obs_state.undetected_intrusions_steps += 1
            reward = reward + env_config.defender_intrusion_reward
        return s, reward, False

