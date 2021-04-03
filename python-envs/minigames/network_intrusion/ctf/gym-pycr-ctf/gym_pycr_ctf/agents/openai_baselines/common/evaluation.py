import typing
from typing import Callable, List, Optional, Tuple, Union

import gym
import numpy as np
import time
from gym_pycr_ctf.agents.openai_baselines.common.vec_env import VecEnv
from gym_pycr_ctf.dao.network.env_config import EnvConfig

if typing.TYPE_CHECKING:
    from gym_pycr_ctf.agents.openai_baselines.common.base_class import BaseAlgorithm
from gym_pycr_ctf.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.agents.openai_baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from gym_pycr_ctf.agents.openai_baselines.common.vec_env.subproc_vec_env import SubprocVecEnv

def evaluate_policy(model: "BaseAlgorithm", env: Union[gym.Env, VecEnv], env_2: Union[gym.Env, VecEnv],
                    n_eval_episodes : int=10,
                    deterministic : bool= True,
                    render : bool =False, callback: Optional[Callable] = None,
                    reward_threshold: Optional[float] = None,
                    return_episode_rewards: bool = False, attacker_agent_config : AgentConfig = None,
                    train_episode = 1, env_config = None, env_configs = None):
    """
    Runs policy for ``n_eval_episodes`` episodes and returns average reward.
    This is made to work only with one env.

    :param model: (BaseRLModel) The RL agent you want to evaluate.
    :param env: (gym.Env or VecEnv) The gym environment. In the case of a ``VecEnv``
        this must contain only one environment.
    :param env_2: (gym.Env or VecEnv) The second gym environment. In the case of a ``VecEnv``
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
    eval_mean_reward, eval_std_reward = -1, -1
    train_eval_mean_reward, train_eval_std_reward = _eval_helper(env=env, attacker_agent_config=attacker_agent_config,
                                                                 n_eval_episodes=n_eval_episodes,
                                                                 deterministic=deterministic,
                                                                 callback=callback, train_episode=train_episode,
                                                                 model=model, env_config=env_config,
                                                                 env_configs=env_configs)
    if env_2 is not None:
        eval_mean_reward, eval_std_reward = _eval_helper(
            env=env_2, attacker_agent_config=attacker_agent_config, n_eval_episodes=n_eval_episodes,  deterministic=deterministic,
            callback=callback, train_episode=train_episode, model=model, env_config=env_config,
            env_configs=env_configs)
    return train_eval_mean_reward, train_eval_std_reward, eval_mean_reward, eval_std_reward


def _eval_helper(env, attacker_agent_config: AgentConfig, model, n_eval_episodes, deterministic,
                 callback, train_episode, env_config, env_configs):
    attacker_agent_config.logger.info("Starting Evaluation")

    model.num_eval_episodes = 0
    if attacker_agent_config.eval_episodes < 1:
        return

    done = False
    state = None

    # Tracking metrics
    episode_rewards = []
    episode_steps = []
    episode_flags = []
    episode_flags_percentage = []
    eval_episode_rewards_env_specific = {}
    eval_episode_steps_env_specific = {}
    eval_episode_flags_env_specific = {}
    eval_episode_flags_percentage_env_specific = {}

    if env.num_envs == 1 and not isinstance(env, SubprocVecEnv):
        env.envs[0].enabled = True
        env.envs[0].stats_recorder.closed = False
        env.envs[0].episode_id = 0


    for episode in range(n_eval_episodes):
        infos = np.array([{"non_legal_actions": env.initial_illegal_actions} for i in range(env.num_envs)])

        for i in range(env.num_envs):
            if env_configs is not None:
                if i < len(env_configs):
                    env_conf = env_configs[i]
                else:
                    env_conf = env_configs[0]
            else:
                env_conf = env_config
            if isinstance(env, SubprocVecEnv):
                obs = env.eval_reset(idx=i)
            elif isinstance(env, DummyVecEnv):
                obs = env.envs[i].reset()
            done = False
            state = None
            env_state = None
            episode_reward = 0.0
            episode_length = 0
            time_str = str(time.time())
            while not done:
                if isinstance(env, DummyVecEnv):
                    env_state = env.envs[i].env_state

                if env.num_envs == 1 and not isinstance(env, SubprocVecEnv) and attacker_agent_config.eval_render:
                    time.sleep(1)
                    env.render()

                actions, state = model.predict_attacker(obs, state=state, deterministic=deterministic, infos=infos,
                                                        env_config=env_conf,
                                                        env_configs=env_configs, env=env, env_idx=i,
                                                        env_state=env_state)
                action = actions[0]
                if isinstance(env, SubprocVecEnv):
                    obs, reward, done, _info = env.eval_step(action, idx=i)
                elif isinstance(env, DummyVecEnv):
                    obs, reward, done, _info = env.envs[i].step(action)
                infos = [_info]
                episode_reward += reward
                episode_length += 1

            # Render final frame when game completed
            if env.num_envs == 1 and attacker_agent_config.eval_render:
                env.render()

            # Record episode metrics
            episode_rewards.append(episode_reward)
            episode_steps.append(episode_length)
            episode_flags.append(_info["flags"])
            episode_flags_percentage.append(_info["flags"] / env_conf.num_flags)
            eval_episode_rewards_env_specific, eval_episode_steps_env_specific, \
            eval_episode_flags_env_specific, eval_episode_flags_percentage_env_specific = \
                update_env_specific_metrics(env_conf, eval_episode_rewards_env_specific,
                                            eval_episode_steps_env_specific, eval_episode_flags_env_specific,
                                            eval_episode_flags_percentage_env_specific, episode_reward, episode_length,
                                            _info, i)

            if isinstance(env, SubprocVecEnv):
                obs = env.eval_reset(idx=i)
            elif isinstance(env, DummyVecEnv):
                obs = env.envs[i].reset()
            if env.num_envs == 1:
                env.close()

            # Update eval stats
            model.num_eval_episodes += 1
            model.num_eval_episodes_total += 1


            # Save gifs
            if env.num_envs == 1 and not isinstance(env, SubprocVecEnv) and attacker_agent_config.gifs or attacker_agent_config.video:
                # Add frames to tensorboard
                for idx, frame in enumerate(env.envs[0].episode_frames):
                    model.tensorboard_writer.add_image(str(train_episode) + "_eval_frames/" + str(idx),
                                                       frame, global_step=train_episode,
                                                       dataformats="HWC")

                # Save Gif
                env.envs[0].generate_gif(attacker_agent_config.gif_dir + "episode_" + str(train_episode) + "_"
                                         + time_str + ".gif", attacker_agent_config.video_fps)
        # Log average metrics every <self.config.eval_log_frequency> episodes
        if episode % attacker_agent_config.eval_log_frequency == 0:
            model.log_metrics_attacker(iteration=episode, result=model.eval_result, episode_rewards=episode_rewards,
                                       episode_steps=episode_steps, eval=True, episode_flags=episode_flags,
                                       episode_flags_percentage=episode_flags_percentage)

    # Log average eval statistics
    model.log_metrics_attacker(iteration=train_episode, result=model.eval_result, episode_rewards=episode_rewards,
                               episode_steps=episode_steps, eval=True, episode_flags=episode_flags,
                               episode_flags_percentage=episode_flags_percentage)

    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)

    attacker_agent_config.logger.info("Evaluation Complete")
    print("Evaluation Complete")
    # env.close()
    # env.reset()
    return mean_reward, std_reward


def quick_evaluate_policy(model: "BaseAlgorithm", env: Union[gym.Env, VecEnv], env_2: Union[gym.Env, VecEnv],
                          n_eval_episodes_train : int=10, n_eval_episodes_eval2 : int=10,
                          deterministic : bool= True, attacker_agent_config : AgentConfig = None,
                          env_config: EnvConfig = None, env_configs : List[EnvConfig] = None,
                          eval_env_config: EnvConfig = None, eval_envs_configs: List[EnvConfig] = None):
    """
    Runs policy for ``n_eval_episodes`` episodes and returns average reward.
    This is made to work only with one env.

    :param model: (BaseRLModel) The RL agent you want to evaluate.
    :param env: (gym.Env or VecEnv) The gym environment. In the case of a ``VecEnv``
        this must contain only one environment.
    :param n_eval_episodes_train: (int) Number of episode to evaluate the agent
    :param deterministic: (bool) Whether to use deterministic or stochastic actions
    :param attacker_agent_config: agent config
    :return: episode_rewards, episode_steps, episode_flags_percentage, episode_flags
    """
    eval_episode_rewards, eval_episode_steps, eval_episode_flags_percentage, eval_episode_flags = 0,0,0,0
    eval_episode_rewards_env_specific, eval_episode_steps_env_specific, eval_episode_flags_env_specific, \
    eval_episode_flags_percentage_env_specific, eval_2_episode_rewards_env_specific, \
    eval_2_episode_steps_env_specific, eval_2_episode_flags_env_specific, \
    eval_2_episode_flags_percentage_env_specific = {}, {}, {}, {}, {}, {}, {}, {}

    episode_rewards, episode_steps, episode_flags_percentage, episode_flags, eval_episode_rewards_env_specific, \
    eval_episode_steps_env_specific, eval_episode_flags_env_specific, \
    eval_episode_flags_percentage_env_specific = _quick_eval_helper(
        env=env, model=model, n_eval_episodes=n_eval_episodes_train, deterministic=True, env_config=env_config,
        env_configs =env_configs)

    if env_2 is not None:
        eval_episode_rewards, eval_episode_steps, eval_episode_flags_percentage, eval_episode_flags, \
        eval_2_episode_rewards_env_specific, eval_2_episode_steps_env_specific, eval_2_episode_flags_env_specific, \
        eval_2_episode_flags_percentage_env_specific = _quick_eval_helper(
            env=env_2, model=model, n_eval_episodes=n_eval_episodes_eval2, deterministic=deterministic, env_config=eval_env_config,
            env_configs=eval_envs_configs)
    return episode_rewards, episode_steps, episode_flags_percentage, episode_flags, \
           eval_episode_rewards, eval_episode_steps, eval_episode_flags_percentage, eval_episode_flags, \
           eval_episode_rewards_env_specific, eval_episode_steps_env_specific, eval_episode_flags_env_specific, \
           eval_episode_flags_percentage_env_specific, eval_2_episode_rewards_env_specific, \
           eval_2_episode_steps_env_specific, eval_2_episode_flags_env_specific, \
           eval_2_episode_flags_percentage_env_specific


def _quick_eval_helper(env, model, n_eval_episodes, deterministic, env_config, env_configs = None):
    # Tracking metrics
    episode_rewards = []
    episode_steps = []
    episode_flags = []
    episode_flags_percentage = []
    eval_episode_rewards_env_specific = {}
    eval_episode_steps_env_specific = {}
    eval_episode_flags_env_specific = {}
    eval_episode_flags_percentage_env_specific = {}

    for episode in range(n_eval_episodes):
        if isinstance(env, SubprocVecEnv):
            infos = np.array([{"attacker_non_legal_actions": env.attacker_initial_illegal_actions,
                               "defender_non_legal_actions": env.defender_initial_illegal_actions
                               } for i in range(env.num_envs)])
        elif isinstance(env, DummyVecEnv):
            infos = np.array([{"attacker_non_legal_actions": env.envs[i].attacker_initial_illegal_actions,
                               "defender_non_legal_actions": env.envs[i].defender_initial_illegal_actions
                               } for i in range(env.num_envs)])
        for i in range(env.num_envs):
            if env_configs is not None:
                env_conf = env_configs[i]
            else:
                env_conf = env_config
            if isinstance(env, SubprocVecEnv):
                obs = env.eval_reset(idx=i)
            elif isinstance(env, DummyVecEnv):
                obs = env.envs[i].reset()
                env_conf = env.env_config(i)
                env_configs = env.env_configs()
            done = False
            state = None
            env_state = None
            episode_reward = 0.0
            episode_length = 0
            while not done:
                if isinstance(env, DummyVecEnv):
                    env_state = env.envs[i].env_state
                obs_attacker, obs_defender = obs
                attacker_actions, state = model.predict(np.array([obs_attacker]), state=state,
                                                        deterministic=deterministic,
                                                        infos=infos,
                                                        env_config = env_conf,
                                                        env_configs=env_configs, env=env, env_idx=i,
                                                        env_state=env_state)
                defender_action = None
                attacker_action = attacker_actions[0]
                action = (attacker_action, defender_action)
                if isinstance(env, SubprocVecEnv):
                    obs, reward, done, _info = env.eval_step(action, idx=i)
                elif isinstance(env, DummyVecEnv):
                    obs, reward, done, _info = env.envs[i].step(action)
                attacker_reward, defender_reward = reward
                infos = [_info]
                episode_reward += attacker_reward
                episode_length += 1
            # Record episode metrics
            episode_rewards.append(episode_reward)
            episode_steps.append(episode_length)
            episode_flags.append(_info["flags"])
            episode_flags_percentage.append(_info["flags"] / env_conf.num_flags)
            eval_episode_rewards_env_specific, eval_episode_steps_env_specific, \
            eval_episode_flags_env_specific, eval_episode_flags_percentage_env_specific = \
                update_env_specific_metrics(env_conf, eval_episode_rewards_env_specific,
                                        eval_episode_steps_env_specific, eval_episode_flags_env_specific,
                                        eval_episode_flags_percentage_env_specific, episode_reward,episode_length,
                                        _info, i)
            if isinstance(env, SubprocVecEnv):
                obs = env.eval_reset(idx=i)
            elif isinstance(env, DummyVecEnv):
                obs = env.envs[i].reset()
                env_conf = env.env_config(i)
                env_configs = env.env_configs()
    return episode_rewards, episode_steps, episode_flags_percentage, episode_flags, \
           eval_episode_rewards_env_specific, eval_episode_steps_env_specific, eval_episode_flags_env_specific, \
           eval_episode_flags_percentage_env_specific


def update_env_specific_metrics(env_config, env_specific_rewards, env_specific_steps, env_specific_flags,
                                env_specific_flags_percentage, episode_reward, episode_step, infos, i):
    if env_config.emulation_config is not None:
        agent_ip = env_config.emulation_config.agent_ip
    else:
        agent_ip = env_config.idx
    num_flags = env_config.num_flags

    if agent_ip not in env_specific_rewards:
        env_specific_rewards[agent_ip] = [episode_reward]
    else:
        env_specific_rewards[agent_ip].append(episode_reward)

    if agent_ip not in env_specific_steps:
        env_specific_steps[agent_ip] = [episode_step]
    else:
        env_specific_steps[agent_ip].append(episode_step)

    if agent_ip not in env_specific_flags:
        env_specific_flags[agent_ip] = [infos["flags"]]
    else:
        env_specific_flags[agent_ip].append(infos["flags"])

    if agent_ip not in env_specific_flags_percentage:
        env_specific_flags_percentage[agent_ip] = [infos["flags"] / num_flags]
    else:
        env_specific_flags_percentage[agent_ip].append(infos["flags"] / num_flags)

    return env_specific_rewards, env_specific_steps, env_specific_flags, env_specific_flags_percentage