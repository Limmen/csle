import math
from gym_pycr_ctf.dao.network.env_config import PyCREnvConfig


class FindPiStarDefender:
    """
    Class with utility methods for finding pi-star for the defender, can be used to
    evaluate learning performance
    """


    @staticmethod
    def upper_bound_pi(env_config) -> float:
        """
        Returns an upper bound reward for an environment

        :param env_config: the environment configuration
        :return: the upper bound reward
        """
        intrusion_len = len(env_config.attacker_static_opponent.strategy)
        mean_intrusion_time = 1 / env_config.attacker_static_opponent.start_p
        if not env_config.multiple_stopping_environment:
            reward = env_config.defender_service_reward* (mean_intrusion_time)
            reward = reward + env_config.defender_caught_attacker_reward
        else:
            average_episode_len = mean_intrusion_time + intrusion_len
            optimal_costs = 0
            for i in range(env_config.maximum_number_of_defender_stop_actions - 1, -1, -1):
                optimal_costs += env_config.multistop_costs[i]
                if i == env_config.attacker_prevented_stops_remaining:
                    break

            optimal_stopping_time = max(mean_intrusion_time + 1,
                                        env_config.maximum_number_of_defender_stop_actions - env_config.attacker_prevented_stops_remaining)
            optimal_service_reward = 0
            optimal_service_reward = optimal_service_reward + env_config.defender_service_reward * \
                                     max(0, (optimal_stopping_time -
                                             (env_config.maximum_number_of_defender_stop_actions -
                                              env_config.attacker_prevented_stops_remaining)))

            for i in range(env_config.maximum_number_of_defender_stop_actions, 0, -1):
                if i < env_config.attacker_prevented_stops_remaining:
                    break
                elif i == env_config.attacker_prevented_stops_remaining:
                    if env_config.attacker_prevented_stops_remaining > 0:
                        optimal_service_reward += (max(0, average_episode_len - optimal_stopping_time + 1)) * \
                                                  env_config.defender_service_reward / (
                                                      math.pow(2,
                                                               env_config.maximum_number_of_defender_stop_actions - i))


            reward = optimal_service_reward + optimal_costs + env_config.defender_caught_attacker_reward

        return reward

    @staticmethod
    def update_pi_star(env_config: PyCREnvConfig) -> PyCREnvConfig:
        """
        Update information about the attacker's optimal policy

        :param env_config: the environment configuration
        :param env: the environment
        :return: the updated environment configuration
        """
        if env_config.use_upper_bound_pi_star_defender and env_config.attacker_static_opponent is not None:
            env_config.pi_star_rew_defender = FindPiStarDefender.upper_bound_pi(env_config)
            env_config.pi_star_tau_defender = None
            env_config.pi_star_rew_list_attacker.append(env_config.pi_star_rew_defender)

        return env_config


