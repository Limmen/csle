import numpy as np
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.envs_model.logic.exploration.exploration_policy import ExplorationPolicy


class InitialStateRandomizer:
    """
    Class for with functions for randomizing the initial state of the environment
    """

    @staticmethod
    def explore(attacker_exp_policy: ExplorationPolicy, env_config: EnvConfig, env, max_steps : int) -> bool:
        """
        Explores the environment to generate trajectories that can be used to learn a dynamics model

        :param attacker_exp_policy: the exploration policy to use
        :param env_config: the env config
        :param env: the env to explore
        :param max_steps: number of steps to take to find the starting state
        :return: The final observation
        """
        done = False
        step = 0
        defender_action = None
        while not done and step < max_steps:

            # Sample action
            attacker_action = attacker_exp_policy.action(
                env=env, filter_illegal=env_config.attacker_exploration_filter_illegal)

            # Step in the environment
            action = (attacker_action, defender_action)
            obs, reward, done, info = env.step(action)

            step +=1

        #print("returning:{}, steps:{}, detected:{}, flags:{}, ts:{}".format(done, step, env.env_state.attacker_obs_state.detected, env.env_state.attacker_obs_state.all_flags, env.attacker_agent_state.time_step))
        return done

    @staticmethod
    def randomize_starting_state(exp_policy: ExplorationPolicy, env_config: EnvConfig, env, max_steps : int) -> bool:

        # Initialize model
        return InitialStateRandomizer.explore(attacker_exp_policy=exp_policy, env_config=env_config, env=env,
                                       max_steps=max_steps)
