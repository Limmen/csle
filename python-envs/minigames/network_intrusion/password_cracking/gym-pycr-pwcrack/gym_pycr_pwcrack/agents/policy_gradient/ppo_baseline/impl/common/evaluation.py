import typing
from typing import Callable, List, Optional, Tuple, Union

import gym
import numpy as np
import time
from gym_pycr_pwcrack.agents.policy_gradient.ppo_baseline.impl.common.vec_env import VecEnv

if typing.TYPE_CHECKING:
    from gym_pycr_pwcrack.agents.policy_gradient.ppo_baseline.impl.common.base_class import BaseAlgorithm
from gym_pycr_pwcrack.agents.config.pg_agent_config import PolicyGradientAgentConfig

def evaluate_policy(model: "BaseAlgorithm", env: Union[gym.Env, VecEnv], n_eval_episodes : int=10,
                    deterministic : bool= True,
                    render : bool =False, callback: Optional[Callable] = None,
                    reward_threshold: Optional[float] = None,
                    return_episode_rewards: bool = False, pg_agent_config : PolicyGradientAgentConfig = None,
                    train_episode = 1):
    """
    Runs policy for ``n_eval_episodes`` episodes and returns average reward.
    This is made to work only with one env.

    :param model: (BaseRLModel) The RL agent you want to evaluate.
    :param env: (gym.Env or VecEnv) The gym environment. In the case of a ``VecEnv``
        this must contain only one environment.
    :param n_eval_episodes: (int) Number of episode to evaluate the agent
    :param deterministic: (bool) Whether to use deterministic or stochastic actions
    :param render: (bool) Whether to render the environment or not
    :param callback: (callable) callback function to do additional checks,
        called after each step.
    :param reward_threshold: (float) Minimum expected reward per episode,
        this will raise an error if the performance is not met
    :param return_episode_rewards: (bool) If True, a list of reward per episode
        will be returned instead of the mean.
    :return: (float, float) Mean reward per episode, std of reward per episode
        returns ([float], [int]) when ``return_episode_rewards`` is True
    """
    if isinstance(env, VecEnv):
        assert env.num_envs == 1, "You must pass only one environment when using this function"

    pg_agent_config.logger.info("Starting Evaluation")

    model.num_eval_episodes = 0

    if pg_agent_config.eval_episodes < 1:
        return
    done = False
    state = None

    # Tracking metrics
    episode_rewards = []
    episode_steps = []

    env.envs[0].enabled = True
    env.envs[0].stats_recorder.closed = False
    env.envs[0].episode_id = 0

    for episode in range(n_eval_episodes):
        time_str = str(time.time())
        obs = env.reset()
        done = False
        episode_reward = 0.0
        episode_length = 0
        for i in range(pg_agent_config.render_steps):
            if pg_agent_config.eval_render:
                env.render()
                #time.sleep(pg_agent_config.eval_sleep)

            action, state = model.predict(obs, state=state, deterministic=deterministic)
            obs, reward, done, _info = env.step(action)
            episode_reward += reward

            if callback is not None:
                callback(locals(), globals())

            episode_length += 1

            # if render:
            #     env.render()

        # Render final frame when game completed
        if pg_agent_config.eval_render:
            env.render()
            #time.sleep(pg_agent_config.eval_sleep)
        pg_agent_config.logger.info("Eval episode: {}, Episode ended after {} steps".format(episode, episode_length))

        # Record episode metrics
        episode_rewards.append(episode_reward)
        episode_steps.append(episode_length)

        # Update eval stats
        model.num_eval_episodes += 1
        model.num_eval_episodes_total += 1

        # Log average metrics every <self.config.eval_log_frequency> episodes
        if episode % pg_agent_config.eval_log_frequency == 0:
            model.log_metrics(iteration=train_episode, result=model.eval_result, episode_rewards=episode_rewards,
                              episode_steps=episode_steps, eval=True)

        # Save gifs
        if pg_agent_config.gifs or pg_agent_config.video:
            # Add frames to tensorboard
            for idx, frame in enumerate(env.envs[0].episode_frames):
                model.tensorboard_writer.add_image(str(train_episode) + "_eval_frames/" + str(idx),
                                                   frame, global_step=train_episode,
                                                   dataformats="HWC")

            # Save Gif
            env.envs[0].generate_gif(pg_agent_config.gif_dir + "episode_" + str(train_episode) + "_"
                                     + time_str + ".gif", pg_agent_config.video_fps)

    # Log average eval statistics
    model.log_metrics(iteration=train_episode, result=model.eval_result, episode_rewards=episode_rewards,
                      episode_steps=episode_steps, eval=True)

    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)

    pg_agent_config.logger.info("Evaluation Complete")
    print("Evaluation Complete")
    env.close()
    env.reset()
    return mean_reward, std_reward
