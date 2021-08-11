from gym_pycr_ctf.dao.network.env_config import EnvConfig

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
        mean_intrusion_time = 1/env_config.attacker_static_opponent.start_p
        reward = env_config.defender_service_reward* (mean_intrusion_time-1)
        reward = reward + env_config.defender_caught_attacker_reward
        return reward

    @staticmethod
    def update_pi_star(env_config: EnvConfig) -> EnvConfig:
        """
        Update information about the attacker's optimal policy

        :param env_config: the environment configuration
        :param env: the environment
        :return: the updated environment configuration
        """
        if env_config.use_upper_bound_pi_star_defender:
            env_config.pi_star_rew_defender = FindPiStarDefender.upper_bound_pi(env_config)
            env_config.pi_star_tau_defender = None
            env_config.pi_star_rew_list_attacker.append(env_config.pi_star_rew_defender)

        return env_config


