"""Abstract base classes for RL algorithms."""

import io
import pathlib
import time
from abc import ABC, abstractmethod
from collections import deque
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type, Union

import gym
import numpy as np
import torch as th
from torch.utils.tensorboard import SummaryWriter

from stable_baselines3.common import logger, utils
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.noise import ActionNoise
from stable_baselines3.common.preprocessing import is_image_space
from gym_pycr_pwcrack.agents.openai_baselines.common.save_util import load_from_zip_file, recursive_getattr, \
    recursive_setattr, save_to_zip_file

from gym_pycr_pwcrack.agents.openai_baselines.common.utils import (
    check_for_correct_spaces,
    get_device,
    get_schedule_fn,
    set_random_seed,
    update_learning_rate,
)
from gym_pycr_pwcrack.agents.openai_baselines.common.type_aliases import GymEnv, MaybeCallback
from gym_pycr_pwcrack.agents.openai_baselines.common.callbacks import BaseCallback, CallbackList, ConvertCallback, EvalCallback
from gym_pycr_pwcrack.agents.openai_baselines.common.vec_env import DummyVecEnv, VecEnv, VecNormalize, VecTransposeImage, unwrap_vec_normalize, SubprocVecEnv

from gym_pycr_pwcrack.agents.openai_baselines.common.policies import BasePolicy, get_policy_from_name
from gym_pycr_pwcrack.agents.config.agent_config import AgentConfig
from gym_pycr_pwcrack.dao.experiment.experiment_result import ExperimentResult
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.network.env_state import EnvState
import gym_pycr_pwcrack.envs.logic.common.util as pycr_util


def maybe_make_env(env: Union[GymEnv, str, None], monitor_wrapper: bool, verbose: int) -> Optional[GymEnv]:
    """If env is a string, make the environment; otherwise, return env.

    :param env: (Union[GymEnv, str, None]) The environment to learn from.
    :param monitor_wrapper: (bool) Whether to wrap env in a Monitor when creating env.
    :param verbose: (int) logging verbosity
    :return A Gym (vector) environment.
    """
    if isinstance(env, str):
        if verbose >= 1:
            print(f"Creating environment from the given name '{env}'")
        env = gym.make(env)
        if monitor_wrapper:
            env = Monitor(env, filename=None)

    return env


class BaseAlgorithm(ABC):
    """
    The base of RL algorithms

    :param policy: (Type[BasePolicy]) Policy object
    :param env: (Union[GymEnv, str, None]) The environment to learn from
                (if registered in Gym, can be str. Can be None for loading trained models)
    :param policy_base: (Type[BasePolicy]) The base policy used by this method
    :param learning_rate: (float or callable) learning rate for the optimizer,
        it can be a function of the current progress remaining (from 1 to 0)
    :param policy_kwargs: (Dict[str, Any]) Additional arguments to be passed to the policy on creation
    :param verbose: (int) The verbosity level: 0 none, 1 training information, 2 debug
    :param device: (Union[th.device, str]) Device on which the code should run.
        By default, it will try to use a Cuda compatible device and fallback to cpu
        if it is not possible.
    :param support_multi_env: (bool) Whether the algorithm supports training
        with multiple environments (as in A2C)
    :param create_eval_env: (bool) Whether to create a second environment that will be
        used for evaluating the agent periodically. (Only available when passing string for the environment)
    :param monitor_wrapper: (bool) When creating an environment, whether to wrap it
        or not in a Monitor wrapper.
    :param seed: (Optional[int]) Seed for the pseudo random generators
    :param use_sde: (bool) Whether to use generalized State Dependent Exploration (gSDE)
        instead of action noise exploration (default: False)
    :param sde_sample_freq: (int) Sample a new noise matrix every n steps when using gSDE
        Default: -1 (only sample at the beginning of the rollout)
    """

    def __init__(
            self,
            policy: Type[BasePolicy],
            env: Union[GymEnv, str, None],
            policy_base: Type[BasePolicy],
            learning_rate: Union[float, Callable],
            policy_kwargs: Dict[str, Any] = None,
            verbose: int = 0,
            device: Union[th.device, str] = "auto",
            support_multi_env: bool = False,
            create_eval_env: bool = False,
            monitor_wrapper: bool = True,
            seed: Optional[int] = None,
            use_sde: bool = False,
            sde_sample_freq: int = -1,
            agent_config: AgentConfig = None,
            env_2: Union[GymEnv, str, None] = None
    ):
        self.agent_config = agent_config
        self.train_result = ExperimentResult()
        self.eval_result = ExperimentResult()

        try:
            self.tensorboard_writer = SummaryWriter(self.agent_config.tensorboard_dir)
            self.tensorboard_writer.add_hparams(self.agent_config.hparams_dict(), {})
        except:
            print("error creating tensorboard writer")

        if isinstance(policy, str) and policy_base is not None:
            self.policy_class = get_policy_from_name(policy_base, policy)
        else:
            self.policy_class = policy

        self.device = get_device(device, agent_config=self.agent_config)
        if verbose > 0:
            print(f"Using {self.device} device")

        self.env = None  # type: Optional[GymEnv]
        self.env_2 = None  # type: Optional[GymEnv]
        # get VecNormalize object if needed
        self._vec_normalize_env = unwrap_vec_normalize(env)
        self.verbose = verbose
        self.policy_kwargs = {} if policy_kwargs is None else policy_kwargs
        self.observation_space = None  # type: Optional[gym.spaces.Space]
        self.action_space = None  # type: Optional[gym.spaces.Space]
        self.n_envs = None
        self.num_timesteps = 0
        # Used for updating schedules
        self._total_timesteps = 0
        self.eval_env = None
        self.seed = seed
        self.action_noise = None  # type: Optional[ActionNoise]
        self.start_time = None
        self.policy = None
        self.m_selection_policy = None
        self.m_action_policy = None
        self.learning_rate = learning_rate
        self.lr_schedule = None  # type: Optional[Callable]
        self._last_obs = None  # type: Optional[np.ndarray]
        self._last_dones = None  # type: Optional[np.ndarray]
        self._last_infos = None
        # When using VecNormalize:
        self._last_original_obs = None  # type: Optional[np.ndarray]
        self._episode_num = 0
        # Used for gSDE only
        self.use_sde = use_sde
        self.sde_sample_freq = sde_sample_freq
        # Track the training progress remaining (from 1 to 0)
        # this is used to update the learning rate
        self._current_progress_remaining = 1
        # Buffers for logging
        self.ep_info_buffer = None  # type: Optional[deque]
        self.ep_success_buffer = None  # type: Optional[deque]
        # For logging
        self._n_updates = 0  # type: int

        self.num_episodes = 0
        self.num_eval_episodes = 0
        self.num_eval_episodes_total = 0
        self.num_episodes_total = 0
        self.cumulative_reward = 0

        # Create and wrap the env if needed
        if env is not None:
            if isinstance(env, str):
                if create_eval_env:
                    self.eval_env = maybe_make_env(env, monitor_wrapper, self.verbose)

            env = maybe_make_env(env, monitor_wrapper, self.verbose)
            env = self._wrap_env(env)

            self.observation_space = env.observation_space
            self.action_space = env.action_space
            self.n_envs = env.num_envs
            self.env = env

        if env_2 is not None:
            env_2 = maybe_make_env(env_2, monitor_wrapper, self.verbose)
            env_2 = self._wrap_env(env_2)
            # self.observation_space = env_2.observation_space
            # self.action_space = env_2.action_space
            # self.n_envs = env_2.num_envs
            self.env_2 = env_2

            if not support_multi_env and self.n_envs > 1:
                raise ValueError(
                    "Error: the model does not support multiple envs; it requires " "a single vectorized environment."
                )

        if self.use_sde and not isinstance(self.observation_space, gym.spaces.Box):
            raise ValueError("generalized State-Dependent Exploration (gSDE) can only be used with continuous actions.")

    def _wrap_env(self, env: GymEnv) -> VecEnv:
        if not isinstance(env, VecEnv):
            print("Wrapping the env in a DummyVecEnv.")
            env = DummyVecEnv([lambda: env])

        if is_image_space(env.observation_space) and not isinstance(env, VecTransposeImage):
            if self.verbose >= 1:
                print("Wrapping the env in a VecTransposeImage.")
            env = VecTransposeImage(env)
        return env

    def log_metrics(self, iteration: int, result: ExperimentResult, episode_rewards: list,
                    episode_steps: list, episode_avg_loss: list = None,
                    eval: bool = False, lr: float = None, total_num_episodes: int = 0,
                    episode_flags : list = None, episode_flags_percentage: list = None,
                    eps: float = None, progress_left : float = 1.0,
                    n_af: int = 0, n_d : int = 0, eval_episode_rewards: list = None,
                    eval_episode_steps :list = None, eval_episode_flags_percentage :list = None,
                    eval_episode_flags : list = None, eval_2_episode_rewards: list = None,
                    eval_2_episode_steps :list = None, eval_2_episode_flags_percentage :list = None,
                    eval_2_episode_flags : list = None, train_env_specific_rewards : dict = None,
                    train_env_specific_steps: dict = None, train_env_specific_flags : dict = None,
                    train_env_specific_flags_percentage: dict = None,
                    eval_env_specific_rewards: dict = None,
                    eval_env_specific_steps: dict = None, eval_env_specific_flags: dict = None,
                    eval_env_specific_flags_percentage: dict = None,
                    eval_2_env_specific_rewards: dict = None,
                    eval_2_env_specific_steps: dict = None, eval_2_env_specific_flags: dict = None,
                    eval_2_env_specific_flags_percentage: dict = None,
                    rollout_times = None, env_response_times = None, action_pred_times = None,
                    grad_comp_times = None, weight_update_times = None
                    ) -> None:
        """
        Logs average metrics for the last <self.config.log_frequency> episodes

        :param iteration: the training iteration (equivalent to episode if batching is not used)
        :param result: the result object to add the results to
        :param episode_rewards: list of attacker episode rewards for the last <self.config.log_frequency> episodes
        :param episode_steps: list of episode steps for the last <self.config.log_frequency> episodes
        :param episode_avg_loss: list of episode attacker loss for the last <self.config.log_frequency> episodes
        :param eval: boolean flag whether the metrics are logged in an evaluation context.
        :param lr: the learning rate of the attacker
        :param total_num_episodes: number of training episodes
        :param episode_flags: number of flags catched per episode
        :param episode_flags_percentage: percentage of flags catched per episode
        :param eps: epsilon exploration rate
        :param eval_episode_rewards: deterministic policy eval rewards
        :param eval_episode_steps: deterministic policy eval steps
        :param eval_episode_flags: deterministic policy eval flags
        :param eval_episode_flags_percentage: deterministic policy eval flag percentage
        :param eval_2_episode_rewards: deterministic policy eval rewards
        :param eval_2_episode_steps: deterministic policy eval steps
        :param eval_2_episode_flags: deterministic policy eval flags
        :param eval_2_episode_flags_percentage: deterministic policy eval flag percentage
        :param train_env_specific_rewards: episodic rewards per train env
        :param train_env_specific_steps: episodic steps per train env
        :param train_env_specific_flags: episodic flags per train env
        :param train_env_specific_flags_percentage: episodic flags_percentage per train env
        :param eval_env_specific_rewards: episodic rewards per train eval env
        :param eval_env_specific_steps: episodic steps per train eval env
        :param eval_env_specific_flags: episodic flags per train eval env
        :param eval_env_specific_flags_percentage: episodic flags_percentage per train eval env
        :return: None
        """
        if eps is None:
            eps = 0.0
        avg_episode_rewards = np.mean(episode_rewards)
        avg_episode_flags = np.mean(episode_flags)
        avg_episode_flags_percentage = np.mean(episode_flags_percentage)
        avg_episode_steps = np.mean(episode_steps)

        train_env_specific_regret = {}
        eval_env_specific_regret = {}
        eval_2_env_specific_regret = {}
        train_env_specific_opt_frac = {}
        eval_env_specific_opt_frac = {}
        eval_2_env_specific_opt_frac = {}

        if result.avg_episode_rewards is not None:
            rolling_avg_rewards = pycr_util.running_average(result.avg_episode_rewards + [avg_episode_rewards],
                                                            self.agent_config.running_avg)
        else:
            rolling_avg_rewards = 0.0

        if result.avg_episode_steps is not None:
            rolling_avg_steps = pycr_util.running_average(result.avg_episode_steps + [avg_episode_steps],
                                                            self.agent_config.running_avg)
        else:
            rolling_avg_steps = 0.0

        if lr is None:
            lr = 0.0
        if not eval and episode_avg_loss is not None:
            avg_episode_loss = np.mean(episode_avg_loss)
        else:
            avg_episode_loss = 0.0

        if not eval and eval_episode_rewards is not None:
            eval_avg_episode_rewards = np.mean(eval_episode_rewards)
        else:
            eval_avg_episode_rewards = 0.0
        if self.agent_config.log_regret:
            if self.env.env_config is not None:
                pi_star_rews = self.env.envs[0].env_config.pi_star_rew_list[-len(episode_rewards):]
                r = [pi_star_rews[i] - episode_rewards[i] for i in range(len(episode_rewards))]
                avg_regret = np.mean(np.array(r))

                if eval_episode_rewards is not None:
                    pi_star_rews = self.env.envs[0].env_config.pi_star_rew_list[-len(eval_episode_rewards):]
                    r = [pi_star_rews[i] - eval_episode_rewards[i] for i in range(len(eval_episode_rewards))]
                    avg_eval_regret = np.mean(np.array(r))
                else:
                    avg_eval_regret = 0.0

            elif train_env_specific_rewards is None and eval_env_specific_rewards is None:
                env_regret = self.env.get_pi_star_rew()[0]
                ip = env_regret[0]
                pi_star_rews = env_regret[2][-len(episode_rewards):]
                r = [pi_star_rews[i] - episode_rewards[i] for i in range(len(episode_rewards))]
                avg_regret = np.mean(np.array(r))
                if eval_episode_rewards is not None:
                    pi_star_rews = env_regret[2][-len(eval_episode_rewards):]
                    r = [pi_star_rews[i] - eval_episode_rewards[i] for i in range(len(eval_episode_rewards))]
                    avg_eval_regret = np.mean(np.array(r))
                else:
                    avg_eval_regret = 0.0
            else:
                regrets = []
                eval_regrets = []
                pi_star_rew_per_env = self.env.get_pi_star_rew()
                for env_regret in pi_star_rew_per_env:
                    ip = env_regret[0]
                    pi_star_rew = env_regret[1]
                    if train_env_specific_rewards is not None:
                        rewards = train_env_specific_rewards[ip]
                        pi_star_rews = env_regret[2][-len(rewards):]
                        r = [pi_star_rews[i] - rewards[i] for i in range(len(rewards))]
                        #r = list(map(lambda x: pi_star_rew - x, rewards))
                        train_env_specific_regret[ip] = r
                        regrets = regrets + r
                    if eval_env_specific_rewards is not None:
                        rewards = eval_env_specific_rewards[ip]
                        pi_star_rews = env_regret[2][-len(rewards):]
                        r = [pi_star_rews[i] - rewards[i] for i in range(len(rewards))]
                        #r = list(map(lambda x: pi_star_rew - x, rewards))
                        eval_env_specific_regret[ip] = r
                        eval_regrets = eval_regrets + r

                avg_regret = np.mean(np.array(regrets))
                avg_eval_regret = np.mean(eval_regrets)

            if self.env_2 is not None:
                if self.env_2.env_config is not None:
                    pi_star_rews = self.env_2.envs[0].env_config.pi_star_rew_list[-len(eval_2_episode_rewards):]
                    r = [pi_star_rews[i] - eval_2_episode_rewards[i] for i in range(len(eval_2_episode_rewards))]
                    avg_regret_2 = np.mean(np.array(r))

                    of = [eval_2_episode_rewards[i] / pi_star_rews[i] for i in range(len(eval_2_episode_rewards))]
                    avg_opt_frac_2 = np.mean(np.array(of))
                else:
                    regrets_2 = []
                    pi_star_rew_per_env_2 = self.env_2.get_pi_star_rew()
                    for env_regret in pi_star_rew_per_env_2:
                        ip = env_regret[0]
                        pi_star_rew = env_regret[1]
                        if eval_2_env_specific_rewards is not None:
                            rewards = eval_2_env_specific_rewards[ip]
                            pi_star_rews = env_regret[2][-len(rewards):]
                            r = [pi_star_rews[i] - rewards[i] for i in range(len(rewards))]
                            #r = list(map(lambda x: pi_star_rew - x, rewards))
                            eval_2_env_specific_regret[ip] = r
                            regrets_2 = regrets_2 + r
                    avg_regret_2 = np.mean(np.array(regrets_2))

                    opt_fracs = []
                    for env_pi_star in pi_star_rew_per_env_2:
                        ip = env_pi_star[0]
                        pi_star_rew = env_pi_star[1]
                        if eval_2_env_specific_rewards is not None:
                            rewards = eval_2_env_specific_rewards[ip]
                            pi_star_rews = env_regret[2][-len(rewards):]
                            of = [rewards[i]/pi_star_rews[i] for i in range(len(rewards))]
                            #of = list(map(lambda x: x / pi_star_rew, rewards))
                            eval_2_env_specific_opt_frac[ip] = of
                            opt_fracs = opt_fracs + of
                    avg_opt_frac_2 = np.mean(np.array(opt_fracs))
            else:
                avg_regret_2 = 0.0
                avg_opt_frac_2 = 0.0
            if self.env.env_config is not None:
                pi_star_rews = self.env.envs[0].env_config.pi_star_rew_list[-len(episode_rewards):]
                of = [episode_rewards[i]/pi_star_rews[i] for i in range(len(episode_rewards))]
                avg_opt_frac = np.mean(np.array(of))

                if eval_episode_rewards is not None:
                    pi_star_rews = self.env.envs[0].env_config.pi_star_rew_list[-len(eval_episode_rewards):]
                    of = [eval_episode_rewards[i]/pi_star_rews[i] for i in range(len(eval_episode_rewards))]
                    eval_avg_opt_frac = np.mean(np.array(of))
                else:
                    eval_avg_opt_frac = 0.0
            elif train_env_specific_rewards is None and eval_env_specific_rewards is None:
                env_regret = self.env.get_pi_star_rew()[0]
                ip = env_regret[0]

                pi_star_rews = env_regret[2][-len(episode_rewards):]
                of = [episode_rewards[i]/pi_star_rews[i] for i in range(len(episode_rewards))]
                avg_opt_frac = np.mean(np.array(of))
                if eval_episode_rewards is not None:
                    pi_star_rews = env_regret[2][-len(eval_episode_rewards):]
                    of = [episode_rewards[i] / pi_star_rews[i] for i in range(len(eval_episode_rewards))]
                    eval_avg_opt_frac = np.mean(np.array(of))
                else:
                    eval_avg_opt_frac = 0.0
            else:
                opt_fracs = []
                eval_opt_fracs = []
                pi_star_rew_per_env = self.env.get_pi_star_rew()
                for env_pi_star in pi_star_rew_per_env:
                    ip = env_pi_star[0]
                    pi_star_rew = env_pi_star[1]
                    if train_env_specific_rewards is not None:
                        rewards = train_env_specific_rewards[ip]
                        pi_star_rews = env_pi_star[2][-len(rewards):]
                        of = [rewards[i] / pi_star_rews[i] for i in range(len(rewards))]
                        #of = list(map(lambda x: x / pi_star_rew, rewards))
                        train_env_specific_opt_frac[ip] = of
                        opt_fracs = opt_fracs + of
                    elif eval_env_specific_rewards is not None:
                        rewards = eval_env_specific_rewards[ip]
                        pi_star_rews = env_pi_star[2][-len(rewards):]
                        of = [rewards[i] / pi_star_rews[i] for i in range(len(rewards))]
                        #of = list(map(lambda x: x / pi_star_rew, rewards))
                        eval_env_specific_opt_frac[ip] = of
                        eval_opt_fracs = eval_opt_fracs + of
                avg_opt_frac = np.mean(np.array(opt_fracs))
                eval_avg_opt_frac = np.mean(eval_opt_fracs)
        else:
            avg_regret = 0.0
            avg_eval_regret = 0.0
            avg_eval2_regret = 0.0
            avg_opt_frac = 0.0
            eval_avg_opt_frac = 0.0
            avg_opt_frac_2 = 0.0
        if not eval and eval_episode_flags is not None:
            eval_avg_episode_flags = np.mean(eval_episode_flags)
        else:
            eval_avg_episode_flags = 0.0
        if not eval and eval_episode_flags_percentage is not None:
            eval_avg_episode_flags_percentage = np.mean(eval_episode_flags_percentage)
        else:
            eval_avg_episode_flags_percentage = 0.0
        if not eval and eval_episode_steps is not None:
            eval_avg_episode_steps = np.mean(eval_episode_steps)
        else:
            eval_avg_episode_steps = 0.0

        if not eval and eval_2_episode_rewards is not None:
            eval_2_avg_episode_rewards = np.mean(eval_2_episode_rewards)
        else:
            eval_2_avg_episode_rewards = 0.0
        if not eval and eval_2_episode_flags is not None:
            eval_2_avg_episode_flags = np.mean(eval_2_episode_flags)
        else:
            eval_2_avg_episode_flags = 0.0
        if not eval and eval_2_episode_flags_percentage is not None:
            eval_2_avg_episode_flags_percentage = np.mean(eval_2_episode_flags_percentage)
        else:
            eval_2_avg_episode_flags_percentage = 0.0
        if not eval and eval_2_episode_steps is not None:
            eval_2_avg_episode_steps = np.mean(eval_2_episode_steps)
        else:
            eval_2_avg_episode_steps = 0.0
        if rollout_times is not None:
            if len(rollout_times)> 0:
                avg_rollout_times = np.mean(rollout_times)
            else:
                avg_rollout_times = 0.0
        else:
            avg_rollout_times = 0.0
        if env_response_times is not None and len(env_response_times) > 0:
            if len(env_response_times) > 0:
                avg_env_response_times = np.mean(env_response_times)
            else:
                avg_env_response_times = 0.0
        else:
            avg_env_response_times = 0.0
        if action_pred_times is not None and len(action_pred_times) > 0:
            if len(action_pred_times) > 0:
                avg_action_pred_times = np.mean(action_pred_times)
            else:
                avg_action_pred_times = 0.0
        else:
            avg_action_pred_times = 0.0
        if grad_comp_times is not None and len(grad_comp_times) > 0:
            if len(grad_comp_times) > 0:
                avg_grad_comp_times = np.mean(grad_comp_times)
            else:
                avg_grad_comp_times = 0.0
        else:
            avg_grad_comp_times = 0.0
        if weight_update_times is not None and len(weight_update_times) > 0:
            if len(weight_update_times):
                avg_weight_update_times = np.mean(weight_update_times)
            else:
                avg_weight_update_times = 0.0
        else:
            avg_weight_update_times = 0.0

        if eval:
            log_str = "[Eval] iter:{},Avg_Reg:{:.2f},Opt_frac:{:.2f},avg_R:{:.2f},rolling_avg_R:{:.2f}," \
                      "avg_t:{:.2f},rolling_avg_t:{:.2f},lr:{:.2E},avg_F:{:.2f},avg_F%:{:.2f}," \
                      "n_af:{},n_d:{}".format(
                iteration, avg_regret, avg_opt_frac, avg_episode_rewards, rolling_avg_rewards,
                avg_episode_steps, rolling_avg_steps, lr, avg_episode_flags,
                avg_episode_flags_percentage, n_af, n_d)
        else:
            log_str = "[Train] iter:{:.2f},avg_reg_T:{:.2f},opt_frac_T:{:.2f},avg_R_T:{:.2f},rolling_avg_R_T:{:.2f}," \
                      "avg_t_T:{:.2f},rolling_avg_t_T:{:.2f}," \
                      "loss:{:.6f},lr:{:.2E},episode:{},avg_F_T:{:.2f},avg_F_T%:{:.2f},eps:{:.2f}," \
                      "n_af:{},n_d:{},avg_R_E:{:.2f},avg_reg_E:{:.2f},avg_opt_frac_E:{:.2f}," \
                      "avg_t_E:{:.2f},avg_F_E:{:.2f},avg_F_E%:{:.2f}," \
                      "avg_R_E2:{:.2f},Avg_Reg_E2:{:.2f},Opt_frac_E2:{:.2f},avg_t_E2:{:.2f},avg_F_E2:{:.2f}," \
                      "avg_F_E2%:{:.2f},epsilon:{:.2f}".format(
                iteration, avg_regret, avg_opt_frac, avg_episode_rewards, rolling_avg_rewards,
                avg_episode_steps, rolling_avg_steps, avg_episode_loss,
                lr, total_num_episodes, avg_episode_flags, avg_episode_flags_percentage, eps, n_af, n_d,
                eval_avg_episode_rewards, avg_eval_regret, eval_avg_opt_frac, eval_avg_episode_steps,
                eval_avg_episode_flags,
                eval_avg_episode_flags_percentage, eval_2_avg_episode_rewards, avg_regret_2, avg_opt_frac_2,
                eval_2_avg_episode_steps,
                eval_2_avg_episode_flags, eval_2_avg_episode_flags_percentage,self.agent_config.epsilon)
        self.agent_config.logger.info(log_str)
        print(log_str)
        if self.agent_config.tensorboard:
            self.log_tensorboard(iteration, avg_episode_rewards,avg_episode_steps,
                                 avg_episode_loss, eps, lr, eval=eval,
                                 avg_flags_catched=avg_episode_flags,
                                 avg_episode_flags_percentage=avg_episode_flags_percentage,
                                 eval_avg_episode_rewards=eval_avg_episode_rewards,
                                 eval_avg_episode_steps=eval_avg_episode_steps,
                                 eval_avg_episode_flags=eval_avg_episode_flags,
                                 eval_avg_episode_flags_percentage=eval_avg_episode_flags_percentage,
                                 eval_2_avg_episode_rewards=eval_2_avg_episode_rewards,
                                 eval_2_avg_episode_steps=eval_2_avg_episode_steps,
                                 eval_2_avg_episode_flags=eval_2_avg_episode_flags,
                                 eval_2_avg_episode_flags_percentage=eval_2_avg_episode_flags_percentage,
                                 rolling_avg_episode_rewards=rolling_avg_rewards,
                                 rolling_avg_episode_steps=rolling_avg_steps
                                 )

        result.avg_episode_steps.append(avg_episode_steps)
        result.avg_episode_rewards.append(avg_episode_rewards)
        result.epsilon_values.append(self.agent_config.epsilon)
        result.avg_episode_loss.append(avg_episode_loss)
        result.avg_episode_flags.append(avg_episode_flags)
        result.avg_episode_flags_percentage.append(avg_episode_flags_percentage)
        result.eval_avg_episode_rewards.append(eval_avg_episode_rewards)
        result.eval_avg_episode_steps.append(eval_avg_episode_steps)
        result.eval_avg_episode_flags.append(eval_avg_episode_flags)
        result.eval_avg_episode_flags_percentage.append(eval_avg_episode_flags_percentage)
        result.eval_2_avg_episode_rewards.append(eval_2_avg_episode_rewards)
        result.eval_2_avg_episode_steps.append(eval_2_avg_episode_steps)
        result.eval_2_avg_episode_flags.append(eval_2_avg_episode_flags)
        result.eval_2_avg_episode_flags_percentage.append(eval_2_avg_episode_flags_percentage)
        result.lr_list.append(lr)
        result.rollout_times.append(avg_rollout_times)
        result.env_response_times.append(avg_env_response_times)
        result.action_pred_times.append(avg_action_pred_times)
        result.grad_comp_times.append(avg_grad_comp_times)
        result.weight_update_times.append(avg_weight_update_times)
        result.avg_regret.append(avg_regret)
        result.avg_opt_frac.append(avg_opt_frac)
        result.eval_avg_regret.append(avg_eval_regret)
        result.eval_avg_opt_frac.append(eval_avg_opt_frac)
        result.eval_2_avg_regret.append(avg_regret_2)
        result.eval_2_avg_opt_frac.append(avg_opt_frac_2)
        if train_env_specific_rewards is not None:
            for key in train_env_specific_rewards.keys():
                avg = np.mean(train_env_specific_rewards[key])
                if key in result.train_env_specific_rewards:
                    result.train_env_specific_rewards[key].append(avg)
                else:
                    result.train_env_specific_rewards[key] = [avg]
        if train_env_specific_regret is not None:
            for key in train_env_specific_regret.keys():
                avg = np.mean(train_env_specific_regret[key])
                if key in result.train_env_specific_regrets:
                    result.train_env_specific_regrets[key].append(avg)
                else:
                    result.train_env_specific_regrets[key] = [avg]
        if train_env_specific_opt_frac is not None:
            for key in train_env_specific_opt_frac.keys():
                avg = np.mean(train_env_specific_opt_frac[key])
                if key in result.train_env_specific_opt_fracs:
                    result.train_env_specific_opt_fracs[key].append(avg)
                else:
                    result.train_env_specific_opt_fracs[key] = [avg]
        if train_env_specific_steps is not None:
            for key in train_env_specific_steps.keys():
                avg = np.mean(train_env_specific_steps[key])
                if key in result.train_env_specific_steps:
                    result.train_env_specific_steps[key].append(avg)
                else:
                    result.train_env_specific_steps[key] = [avg]
        if train_env_specific_flags is not None:
            for key in train_env_specific_flags.keys():
                avg = np.mean(train_env_specific_flags[key])
                if key in result.train_env_specific_flags:
                    result.train_env_specific_flags[key].append(avg)
                else:
                    result.train_env_specific_flags[key] = [avg]
        if train_env_specific_flags_percentage is not None:
            for key in train_env_specific_flags_percentage.keys():
                avg = np.mean(train_env_specific_flags_percentage[key])
                if key in result.train_env_specific_flags_percentage:
                    result.train_env_specific_flags_percentage[key].append(avg)
                else:
                    result.train_env_specific_flags_percentage[key] = [avg]

        if eval_env_specific_rewards is not None:
            for key in eval_env_specific_rewards.keys():
                avg = np.mean(eval_env_specific_rewards[key])
                if key in result.eval_env_specific_rewards:
                    result.eval_env_specific_rewards[key].append(avg)
                else:
                    result.eval_env_specific_rewards[key] = [avg]
        if eval_env_specific_regret is not None:
            for key in eval_env_specific_regret.keys():
                avg = np.mean(eval_env_specific_regret[key])
                if key in result.eval_env_specific_regrets:
                    result.eval_env_specific_regrets[key].append(avg)
                else:
                    result.eval_env_specific_regrets[key] = [avg]
        if eval_env_specific_opt_frac is not None:
            for key in eval_env_specific_opt_frac.keys():
                avg = np.mean(eval_env_specific_opt_frac[key])
                if key in result.eval_env_specific_opt_fracs:
                    result.eval_env_specific_opt_fracs[key].append(avg)
                else:
                    result.eval_env_specific_opt_fracs[key] = [avg]
        if eval_env_specific_steps is not None:
            for key in eval_env_specific_steps.keys():
                avg = np.mean(eval_env_specific_steps[key])
                if key in result.eval_env_specific_steps:
                    result.eval_env_specific_steps[key].append(avg)
                else:
                    result.eval_env_specific_steps[key] = [avg]
        if eval_env_specific_flags is not None:
            for key in eval_env_specific_flags.keys():
                avg = np.mean(eval_env_specific_flags[key])
                if key in result.eval_env_specific_flags:
                    result.eval_env_specific_flags[key].append(avg)
                else:
                    result.eval_env_specific_flags[key] = [avg]
        if eval_env_specific_flags_percentage is not None:
            for key in eval_env_specific_flags_percentage.keys():
                avg = np.mean(eval_env_specific_flags_percentage[key])
                if key in result.eval_env_specific_flags_percentage:
                    result.eval_env_specific_flags_percentage[key].append(avg)
                else:
                    result.eval_env_specific_flags_percentage[key] = [avg]

        if eval_2_env_specific_rewards is not None:
            for key in eval_2_env_specific_rewards.keys():
                avg = np.mean(eval_2_env_specific_rewards[key])
                if key in result.eval_2_env_specific_rewards:
                    result.eval_2_env_specific_rewards[key].append(avg)
                else:
                    result.eval_2_env_specific_rewards[key] = [avg]
        if eval_2_env_specific_regret is not None:
            for key in eval_2_env_specific_regret.keys():
                avg = np.mean(eval_2_env_specific_regret[key])
                if key in result.eval_2_env_specific_regrets:
                    result.eval_2_env_specific_regrets[key].append(avg)
                else:
                    result.eval_2_env_specific_regrets[key] = [avg]
        if eval_2_env_specific_opt_frac is not None:
            for key in eval_2_env_specific_opt_frac.keys():
                avg = np.mean(eval_2_env_specific_opt_frac[key])
                if key in result.eval_2_env_specific_opt_fracs:
                    result.eval_2_env_specific_opt_fracs[key].append(avg)
                else:
                    result.eval_2_env_specific_opt_fracs[key] = [avg]
        if eval_2_env_specific_steps is not None:
            for key in eval_2_env_specific_steps.keys():
                avg = np.mean(eval_2_env_specific_steps[key])
                if key in result.eval_2_env_specific_steps:
                    result.eval_2_env_specific_steps[key].append(avg)
                else:
                    result.eval_2_env_specific_steps[key] = [avg]
        if eval_2_env_specific_flags is not None:
            for key in eval_2_env_specific_flags.keys():
                avg = np.mean(eval_2_env_specific_flags[key])
                if key in result.eval_2_env_specific_flags:
                    result.eval_2_env_specific_flags[key].append(avg)
                else:
                    result.eval_2_env_specific_flags[key] = [avg]
        if eval_2_env_specific_flags_percentage is not None:
            for key in eval_2_env_specific_flags_percentage.keys():
                avg = np.mean(eval_2_env_specific_flags_percentage[key])
                if key in result.eval_2_env_specific_flags_percentage:
                    result.eval_2_env_specific_flags_percentage[key].append(avg)
                else:
                    result.eval_2_env_specific_flags_percentage[key] = [avg]
        if isinstance(self.env, SubprocVecEnv):
            if not eval:
                self.env.reset_pi_star_rew()
        else:
            if not eval:
                self.env.envs[0].env_config.pi_star_rew_list = [self.env.envs[0].env_config.pi_star_rew]

        if self.env_2 is not None:
            if not eval:
                if isinstance(self.env_2, SubprocVecEnv):
                    self.env_2.reset_pi_star_rew()
                else:
                    self.env_2.envs[0].env_config.pi_star_rew_list = [self.env_2.envs[0].env_config.pi_star_rew]

    def log_tensorboard(self, episode: int, avg_episode_rewards: float,
                        avg_episode_steps: float, episode_avg_loss: float,
                        epsilon: float, lr: float, eval=False, avg_flags_catched : int = 0,
                        avg_episode_flags_percentage : list = None,
                        eval_avg_episode_rewards: float = 0.0,
                        eval_avg_episode_steps: float = 0.0,
                        eval_avg_episode_flags: float = 0.0,
                        eval_avg_episode_flags_percentage: float = 0.0,
                        eval_2_avg_episode_rewards: float = 0.0,
                        eval_2_avg_episode_steps: float = 0.0,
                        eval_2_avg_episode_flags: float = 0.0,
                        eval_2_avg_episode_flags_percentage: float = 0.0,
                        rolling_avg_episode_rewards: float = 0.0,
                        rolling_avg_episode_steps: float = 0.0
                        ) -> None:
        """
        Log metrics to tensorboard

        :param episode: the episode
        :param avg_episode_rewards: the average attacker episode reward
        :param avg_episode_steps: the average number of episode steps
        :param episode_avg_loss: the average episode loss
        :param epsilon: the exploration rate
        :param lr: the learning rate of the attacker
        :param eval: boolean flag whether eval or not
        :param avg_flags_catched: avg number of flags catched per episode
        :param avg_episode_flags_percentage: avg percentage of flags catched per episode
        :param eval_avg_episode_rewards: average reward eval deterministic policy
        :param eval_avg_episode_steps: average steps eval deterministic policy
        :param eval_avg_episode_flags: average flags eval deterministic policy
        :param eval_avg_episode_flags_percentage: average flags_percentage eval deterministic policy
        :param eval_avg_episode_rewards: average reward 2nd eval deterministic policy
        :param eval_avg_episode_steps: average steps 2nd eval deterministic policy
        :param eval_avg_episode_flags: average flags 2nd eval deterministic policy
        :param eval_avg_episode_flags_percentage: average flags_percentage 2nd eval deterministic policy
        :return: None
        """
        train_or_eval = "eval" if eval else "train"
        self.tensorboard_writer.add_scalar('avg_episode_rewards/' + train_or_eval,
                                           avg_episode_rewards, episode)
        self.tensorboard_writer.add_scalar('rolling_avg_episode_rewards/' + train_or_eval,
                                           rolling_avg_episode_rewards, episode)
        self.tensorboard_writer.add_scalar('avg_episode_steps/' + train_or_eval, avg_episode_steps, episode)
        self.tensorboard_writer.add_scalar('rolling_avg_episode_steps/' + train_or_eval, rolling_avg_episode_steps, episode)
        self.tensorboard_writer.add_scalar('episode_avg_loss/' + train_or_eval, episode_avg_loss, episode)
        self.tensorboard_writer.add_scalar('epsilon/' + train_or_eval, epsilon, episode)
        self.tensorboard_writer.add_scalar('avg_episode_flags/' + train_or_eval, avg_flags_catched, episode)
        self.tensorboard_writer.add_scalar('avg_episode_flags_percentage/' + train_or_eval,
                                           avg_episode_flags_percentage, episode)
        self.tensorboard_writer.add_scalar('eval_avg_episode_rewards/' + train_or_eval,
                                           eval_avg_episode_rewards, episode)
        self.tensorboard_writer.add_scalar('eval_avg_episode_steps/' + train_or_eval, eval_avg_episode_steps, episode)
        self.tensorboard_writer.add_scalar('eval_avg_episode_flags/' + train_or_eval, eval_avg_episode_flags, episode)
        self.tensorboard_writer.add_scalar('eval_avg_episode_flags_percentage/' + train_or_eval,
                                           eval_avg_episode_flags_percentage, episode)

        self.tensorboard_writer.add_scalar('eval_2_avg_episode_rewards/' + train_or_eval,
                                           eval_2_avg_episode_rewards, episode)
        self.tensorboard_writer.add_scalar('eval_2_avg_episode_steps/' + train_or_eval, eval_2_avg_episode_steps, episode)
        self.tensorboard_writer.add_scalar('eval_2_avg_episode_flags/' + train_or_eval, eval_2_avg_episode_flags, episode)
        self.tensorboard_writer.add_scalar('eval_2_avg_episode_flags_percentage/' + train_or_eval,
                                           eval_2_avg_episode_flags_percentage, episode)
        if not eval:
            self.tensorboard_writer.add_scalar('lr', lr, episode)

    @abstractmethod
    def _setup_model(self) -> None:
        """Create networks, buffer and optimizers."""

    def _get_eval_env(self, eval_env: Optional[GymEnv]) -> Optional[GymEnv]:
        """
        Return the environment that will be used for evaluation.

        :param eval_env: (Optional[GymEnv]))
        :return: (Optional[GymEnv])
        """
        if eval_env is None:
            eval_env = self.eval_env

        if eval_env is not None:
            eval_env = self._wrap_env(eval_env)
            #assert eval_env.num_envs == 1
        return eval_env

    def _setup_lr_schedule(self) -> None:
        """Transform to callable if needed."""
        self.lr_schedule = get_schedule_fn(self.learning_rate)

    def _update_current_progress_remaining(self, num_timesteps: int, total_timesteps: int) -> None:
        """
        Compute current progress remaining (starts from 1 and ends to 0)

        :param num_timesteps: current number of timesteps
        :param total_timesteps:
        """
        self._current_progress_remaining = 1.0 - float(num_timesteps) / float(total_timesteps)

    def _update_learning_rate(self, optimizers: Union[List[th.optim.Optimizer], th.optim.Optimizer]) -> None:
        """
        Update the optimizers learning rate using the current learning rate schedule
        and the current progress remaining (from 1 to 0).

        :param optimizers: (Union[List[th.optim.Optimizer], th.optim.Optimizer])
            An optimizer or a list of optimizers.
        """
        # Log the current learning rate
        logger.record("train/learning_rate", self.lr_schedule(self._current_progress_remaining))

        if not isinstance(optimizers, list):
            optimizers = [optimizers]
        for optimizer in optimizers:
            update_learning_rate(optimizer, self.lr_schedule(self._current_progress_remaining))

    def get_env(self) -> Optional[VecEnv]:
        """
        Returns the current environment (can be None if not defined).

        :return: (Optional[VecEnv]) The current environment
        """
        return self.env

    def get_vec_normalize_env(self) -> Optional[VecNormalize]:
        """
        Return the ``VecNormalize`` wrapper of the training env
        if it exists.
        :return: Optional[VecNormalize] The ``VecNormalize`` env.
        """
        return self._vec_normalize_env

    def set_env(self, env: GymEnv) -> None:
        """
        Checks the validity of the environment, and if it is coherent, set it as the current environment.
        Furthermore wrap any non vectorized env into a vectorized
        checked parameters:
        - observation_space
        - action_space

        :param env: The environment for learning a policy
        """
        check_for_correct_spaces(env, self.observation_space, self.action_space)
        # it must be coherent now
        # if it is not a VecEnv, make it a VecEnv
        env = self._wrap_env(env)

        self.n_envs = env.num_envs
        self.env = env

    def get_torch_variables(self) -> Tuple[List[str], List[str]]:
        """
        Get the name of the torch variables that will be saved.
        ``th.save`` and ``th.load`` will be used with the right device
        instead of the default pickling strategy.

        :return: (Tuple[List[str], List[str]])
            name of the variables with state dicts to save, name of additional torch tensors,
        """
        state_dicts = ["policy"]

        return state_dicts, []

    @abstractmethod
    def learn(
            self,
            total_timesteps: int,
            callback: MaybeCallback = None,
            log_interval: int = 100,
            tb_log_name: str = "run",
            eval_env: Optional[GymEnv] = None,
            eval_freq: int = -1,
            n_eval_episodes: int = 5,
            eval_log_path: Optional[str] = None,
            reset_num_timesteps: bool = True,
    ) -> "BaseAlgorithm":
        """
        Return a trained model.

        :param total_timesteps: (int) The total number of samples (env steps) to train on
        :param callback: (MaybeCallback) callback(s) called at every step with state of the algorithm.
        :param log_interval: (int) The number of timesteps before logging.
        :param tb_log_name: (str) the name of the run for TensorBoard logging
        :param eval_env: (gym.Env) Environment that will be used to evaluate the agent
        :param eval_freq: (int) Evaluate the agent every ``eval_freq`` timesteps (this may vary a little)
        :param n_eval_episodes: (int) Number of episode to evaluate the agent
        :param eval_log_path: (Optional[str]) Path to a folder where the evaluations will be saved
        :param reset_num_timesteps: (bool) whether or not to reset the current timestep number (used in logging)
        :return: (BaseAlgorithm) the trained model
        """

    def predict(
            self,
            observation: np.ndarray,
            state: Optional[np.ndarray] = None,
            mask: Optional[np.ndarray] = None,
            deterministic: bool = False,
            env_config : EnvConfig = None,
            env_configs: List[EnvConfig] = None,
            env_state : EnvState = None,
            infos = None,
            env_idx: int = None,
            m_index: int = None,
            mask_actions: bool = True,
            env=None
    ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Get the model's action(s) from an observation

        :param observation: (np.ndarray) the input observation
        :param state: (Optional[np.ndarray]) The last states (can be None, used in recurrent policies)
        :param mask: (Optional[np.ndarray]) The last masks (can be None, used in recurrent policies)
        :param deterministic: (bool) Whether or not to return deterministic actions.
        :return: (Tuple[np.ndarray, Optional[np.ndarray]]) the model's action and the next state
            (used in recurrent policies)
        """
        if not self.agent_config.ar_policy:
            return self.policy.predict(observation, state, mask, deterministic,
                                       env_config=env_config,
                                       env_state=env_state, env_configs=env_configs,
                                       env=env, infos=infos, env_idx=env_idx, mask_actions=mask_actions)
        else:
            m_selection_actions, state1 = self.m_selection_policy.predict(observation, state, mask, deterministic,
                                                                          env_config=env_config,
                                                                          env_state=env_state,
                                                                          infos=infos)
            obs_2 = observation.reshape((observation.shape[0],) + self.env.envs[0].network_orig_shape)
            idx = m_selection_actions[0]
            if m_selection_actions[0] > 5:
                idx = 0
            machine_obs = obs_2[:, idx].reshape((observation.shape[0],) + self.env.envs[0].machine_orig_shape)
            machine_obs_tensor = th.as_tensor(machine_obs).to(self.device)
            m_actions, state2 = self.m_action_policy.predict(machine_obs_tensor, state, mask, deterministic,
                                                    env_config=env_config,
                                                    env_state=env_state, infos=infos)
            actions = self.env.envs[0].convert_ar_action(m_selection_actions[0], m_actions[0])
            actions = np.array([actions])
            return actions, state2

    @classmethod
    def load(
            cls, load_path: str, env: Optional[GymEnv] = None, device: Union[th.device, str] = "auto",
            agent_config: AgentConfig = None, **kwargs
    ) -> "BaseAlgorithm":
        """
        Load the model from a zip-file

        :param load_path: the location of the saved data
        :param env: the new environment to run the loaded model on
            (can be None if you only need prediction from a trained model) has priority over any saved environment
        :param device: (Union[th.device, str]) Device on which the code should run.
        :param kwargs: extra arguments to change the model when loading
        """
        data, params, tensors = load_from_zip_file(load_path)

        # if "policy_kwargs" in data:
        #     for arg_to_remove in ["device"]:
        #         if arg_to_remove in data["policy_kwargs"]:
        #             del data["policy_kwargs"][arg_to_remove]

        # if "policy_kwargs" in kwargs and kwargs["policy_kwargs"] != data["policy_kwargs"]:
        #     raise ValueError(
        #         f"The specified policy kwargs do not equal the stored policy kwargs."
        #         f"Stored kwargs: {data['policy_kwargs']}, specified kwargs: {kwargs['policy_kwargs']}"
        #     )

        # # check if observation space and action space are part of the saved parameters
        # if "observation_space" not in data or "action_space" not in data:
        #     raise KeyError("The observation_space and action_space were not given, can't verify new environments")
        # check if given env is valid
        # if env is not None:
        #     check_for_correct_spaces(env, data["observation_space"], data["action_space"])
        # if no new env was given use stored env if possible
        if env is None and "env" in data:
            env = data["env"]

        # noinspection PyArgumentList
        model = cls(
            policy=data["policy_class"],
            env=env,
            device=device,
            _init_setup_model=False,  # pytype: disable=not-instantiable,wrong-keyword-args
        )

        # load parameters
        model.__dict__.update(data)
        model.__dict__.update(kwargs)
        model._setup_model()

        # put state_dicts back in place
        for name in params:
            attr = recursive_getattr(model, name)
            attr.load_state_dict(params[name])

        # put tensors back in place
        if tensors is not None:
            for name in tensors:
                recursive_setattr(model, name, tensors[name])

        # Sample gSDE exploration matrix, so it uses the right device
        # see issue #44
        if model.use_sde:
            model.policy.reset_noise()  # pytype: disable=attribute-error
        return model

    def set_random_seed(self, seed: Optional[int] = None) -> None:
        """
        Set the seed of the pseudo-random generators
        (python, numpy, pytorch, gym, action_space)

        :param seed: (int)
        """
        if seed is None:
            return
        set_random_seed(seed, using_cuda=self.device == th.device("cuda"))
        self.action_space.seed(seed)
        if self.env is not None:
            self.env.seed(seed)
        if self.eval_env is not None:
            self.eval_env.seed(seed)

    def _init_callback(
            self,
            callback: MaybeCallback,
            eval_env: Optional[VecEnv] = None,
            eval_env_2: Optional[VecEnv] = None,
            eval_freq: int = 10000,
            n_eval_episodes: int = 5,
            log_path: Optional[str] = None,
    ) -> BaseCallback:
        """
        :param callback: (MaybeCallback) Callback(s) called at every step with state of the algorithm.
        :param eval_freq: (Optional[int]) How many steps between evaluations; if None, do not evaluate.
        :param n_eval_episodes: (int) How many episodes to play per evaluation
        :param n_eval_episodes: (int) Number of episodes to rollout during evaluation.
        :param log_path: (Optional[str]) Path to a folder where the evaluations will be saved
        :return: (BaseCallback) A hybrid callback calling `callback` and performing evaluation.
        """
        # Convert a list of callbacks into a callback
        if isinstance(callback, list):
            callback = CallbackList(callback)

        # Convert functional callback to object
        if not isinstance(callback, BaseCallback):
            callback = ConvertCallback(callback)

        # Create eval callback in charge of the evaluation
        if eval_env is not None:
            eval_callback = EvalCallback(
                eval_env,
                eval_env_2,
                deterministic=self.agent_config.eval_deterministic,
                best_model_save_path=log_path,
                log_path=log_path,
                eval_freq=eval_freq,
                n_eval_episodes=n_eval_episodes,
                agent_config=self.agent_config
            )
            callback = CallbackList([callback, eval_callback])

        callback.init_callback(self)
        return callback

    def _setup_learn(
            self,
            total_timesteps: int,
            eval_env: Optional[GymEnv],
            eval_env_2: Optional[GymEnv],
            callback: MaybeCallback = None,
            eval_freq: int = 10000,
            n_eval_episodes: int = 5,
            log_path: Optional[str] = None,
            reset_num_timesteps: bool = True,
            tb_log_name: str = "run",
    ) -> Tuple[int, BaseCallback]:
        """
        Initialize different variables needed for training.

        :param total_timesteps: (int) The total number of samples (env steps) to train on
        :param eval_env: (Optional[VecEnv]) Environment to use for evaluation.
        :param eval_env_2: (Optional[VecEnv]) Second Environment to use for evaluation.
        :param callback: (MaybeCallback) Callback(s) called at every step with state of the algorithm.
        :param eval_freq: (int) How many steps between evaluations
        :param n_eval_episodes: (int) How many episodes to play per evaluation
        :param log_path: (Optional[str]) Path to a folder where the evaluations will be saved
        :param reset_num_timesteps: (bool) Whether to reset or not the ``num_timesteps`` attribute
        :param tb_log_name: (str) the name of the run for tensorboard log
        :return: (Tuple[int, BaseCallback])
        """
        self.start_time = time.time()
        if self.ep_info_buffer is None or reset_num_timesteps:
            # Initialize buffers if they don't exist, or reinitialize if resetting counters
            self.ep_info_buffer = deque(maxlen=100)
            self.ep_success_buffer = deque(maxlen=100)

        if self.action_noise is not None:
            self.action_noise.reset()

        if reset_num_timesteps:
            self.num_timesteps = 0
            self._episode_num = 0
        else:
            # Make sure training timesteps are ahead of the internal counter
            total_timesteps += self.num_timesteps
        self._total_timesteps = total_timesteps

        # Avoid resetting the environment when calling ``.learn()`` consecutive times
        if reset_num_timesteps or self._last_obs is None:
            self._last_obs = self.env.reset()
            if len(self._last_obs.shape) == 3:
                self._last_obs = self._last_obs.reshape((self._last_obs.shape[0], self.observation_space.shape[0]))
            self._last_dones = np.zeros((self.env.num_envs,), dtype=np.bool)
            if isinstance(self.env, SubprocVecEnv):
                self._last_infos = np.array([{"non_legal_actions": self.env.initial_illegal_actions} for i in range(self.env.num_envs)])
            else:
                self._last_infos = np.array([{"non_legal_actions": []} for i in range(self.env.num_envs)])

            # Retrieve unnormalized observation for saving into the buffer
            if self._vec_normalize_env is not None:
                self._last_original_obs = self._vec_normalize_env.get_original_obs()

        if eval_env is not None and self.seed is not None:
            eval_env.seed(self.seed)

        if eval_env_2 is not None and self.seed is not None:
            eval_env_2.seed(self.seed)

        eval_env = self._get_eval_env(eval_env)
        eval_env_2 = self._get_eval_env(eval_env_2)

        # Create eval callback if needed
        callback = self._init_callback(callback, eval_env, eval_env_2, eval_freq, n_eval_episodes, log_path)

        return total_timesteps, callback

    def _update_info_buffer(self, infos: List[Dict[str, Any]], dones: Optional[np.ndarray] = None) -> None:
        """
        Retrieve reward and episode length and update the buffer
        if using Monitor wrapper.

        :param infos: ([dict])
        """
        if dones is None:
            dones = np.array([False] * len(infos))
        for idx, info in enumerate(infos):
            maybe_ep_info = info.get("episode")
            maybe_is_success = info.get("is_success")
            if maybe_ep_info is not None:
                self.ep_info_buffer.extend([maybe_ep_info])
            if maybe_is_success is not None and dones[idx]:
                self.ep_success_buffer.append(maybe_is_success)

    def excluded_save_params(self) -> List[str]:
        """
        Returns the names of the parameters that should be excluded by default
        when saving the model.

        :return: ([str]) List of parameters that should be excluded from save
        """
        return ["device", "env", "eval_env", "replay_buffer", "rollout_buffer", "_vec_normalize_env"]

    def save(
            self,
            path: Union[str, pathlib.Path, io.BufferedIOBase],
            exclude: Optional[Iterable[str]] = None,
            include: Optional[Iterable[str]] = None,
    ) -> None:
        """
        Save all the attributes of the object and the model parameters in a zip-file.

        :param (Union[str, pathlib.Path, io.BufferedIOBase]): path to the file where the rl agent should be saved
        :param exclude: name of parameters that should be excluded in addition to the default one
        :param include: name of parameters that might be excluded but should be included anyway
        """
        # copy parameter list so we don't mutate the original dict
        data = self.__dict__.copy()

        # Exclude is union of specified parameters (if any) and standard exclusions
        if exclude is None:
            exclude = []
        exclude = set(exclude).union(self.excluded_save_params())

        # Do not exclude params if they are specifically included
        if include is not None:
            exclude = exclude.difference(include)

        state_dicts_names, tensors_names = self.get_torch_variables()
        # any params that are in the save vars must not be saved by data
        torch_variables = state_dicts_names + tensors_names
        for torch_var in torch_variables:
            # we need to get only the name of the top most module as we'll remove that
            var_name = torch_var.split(".")[0]
            exclude.add(var_name)

        # Remove parameter entries of parameters which are to be excluded
        for param_name in exclude:
            data.pop(param_name, None)

        # Build dict of tensor variables
        tensors = None
        if tensors_names is not None:
            tensors = {}
            for name in tensors_names:
                attr = recursive_getattr(self, name)
                tensors[name] = attr

        # Build dict of state_dicts
        params_to_save = {}
        for name in state_dicts_names:
            attr = recursive_getattr(self, name)
            # Retrieve state dict
            params_to_save[name] = attr.state_dict()

        save_to_zip_file(path, data=data, params=params_to_save, tensors=tensors)

    def save_model(self) -> None:
        """
        Saves the PyTorch Model Weights

        :return: None
        """
        time_str = str(time.time())
        if self.agent_config.save_dir is not None:
            path = self.agent_config.save_dir + "/" + time_str + "_policy_network.zip"
            self.agent_config.logger.info("Saving policy-network to: {}".format(path))
            env_config = self.agent_config.env_config
            env_configs = self.agent_config.env_configs
            eval_env_config = self.agent_config.eval_env_config
            eval_env_configs = self.agent_config.eval_env_configs
            self.agent_config.env_config = None
            self.agent_config.env_configs = None
            self.agent_config.eval_env_config = None
            self.agent_config.eval_env_configs = None
            self.save(path, exclude=["tensorboard_writer", "eval_env", "env_2", "env"])
            self.agent_config.env_config = env_config
            self.agent_config.env_configs = env_configs
            self.agent_config.eval_env_config = eval_env_config
            self.agent_config.eval_env_configs = eval_env_configs
        else:
            self.agent_config.logger.warning("Save path not defined, not saving policy-networks to disk")
            print("Save path not defined, not saving policy-networks to disk")
