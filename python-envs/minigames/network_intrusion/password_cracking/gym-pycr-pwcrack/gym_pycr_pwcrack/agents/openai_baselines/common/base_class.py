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
from stable_baselines3.common.save_util import load_from_zip_file, recursive_getattr, recursive_setattr, \
    save_to_zip_file

from gym_pycr_pwcrack.agents.openai_baselines.common.utils import (
    check_for_correct_spaces,
    get_device,
    get_schedule_fn,
    set_random_seed,
    update_learning_rate,
)
from gym_pycr_pwcrack.agents.openai_baselines.common.type_aliases import GymEnv, MaybeCallback
from gym_pycr_pwcrack.agents.openai_baselines.common.callbacks import BaseCallback, CallbackList, ConvertCallback, EvalCallback
from gym_pycr_pwcrack.agents.openai_baselines.common.vec_env import DummyVecEnv, VecEnv, VecNormalize, VecTransposeImage, unwrap_vec_normalize

from gym_pycr_pwcrack.agents.openai_baselines.common.policies import BasePolicy, get_policy_from_name
from gym_pycr_pwcrack.agents.config.agent_config import AgentConfig
from gym_pycr_pwcrack.dao.experiment.experiment_result import ExperimentResult


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
    :param tensorboard_log: (str) the log location for tensorboard (if None, no logging)
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
            agent_config: AgentConfig = None
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
        self.learning_rate = learning_rate
        self.lr_schedule = None  # type: Optional[Callable]
        self._last_obs = None  # type: Optional[np.ndarray]
        self._last_dones = None  # type: Optional[np.ndarray]
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

            if not support_multi_env and self.n_envs > 1:
                raise ValueError(
                    "Error: the model does not support multiple envs; it requires " "a single vectorized environment."
                )

        if self.use_sde and not isinstance(self.observation_space, gym.spaces.Box):
            raise ValueError("generalized State-Dependent Exploration (gSDE) can only be used with continuous actions.")

    def _wrap_env(self, env: GymEnv) -> VecEnv:
        if not isinstance(env, VecEnv):
            if self.verbose >= 1:
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
                    episode_flags : list = None, episode_flags_percentage: list = None) -> None:
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
        :return: None
        """
        avg_episode_rewards = np.mean(episode_rewards)
        avg_episode_flags = np.mean(episode_flags)
        avg_episode_flags_percentage = np.mean(episode_flags_percentage)
        if lr is None:
            lr = 0.0
        if not eval and episode_avg_loss is not None:
            avg_episode_loss = np.mean(episode_avg_loss)
        else:
            avg_episode_loss = 0.0

        avg_episode_steps = np.mean(episode_steps)
        if eval:
            log_str = "[Eval] iter:{},avg_R:{:.2f},avg_t:{:.2f},lr:{:.2E},avg_F:{:.2f},avg_F%:{:.2f}".format(
                iteration, avg_episode_rewards, avg_episode_steps, lr, avg_episode_flags,
                avg_episode_flags_percentage)
        else:
            log_str = "[Train] iter: {:.2f} epsilon:{:.2f},avg_R:{:.2f},avg_t:{:.2f}," \
                      "loss:{:.6f},lr:{:.2E},episode:{},avg_F:{:.2f},avg_F%:{:.2f}".format(
                iteration, self.agent_config.epsilon, avg_episode_rewards, avg_episode_steps, avg_episode_loss,
                lr, total_num_episodes, avg_episode_flags, avg_episode_flags_percentage)
        self.agent_config.logger.info(log_str)
        print(log_str)
        if self.agent_config.tensorboard:
            self.log_tensorboard(iteration, avg_episode_rewards,avg_episode_steps,
                                 avg_episode_loss, self.agent_config.epsilon, lr, eval=eval,
                                 avg_flags_catched=avg_episode_flags,
                                 avg_episode_flags_percentage=avg_episode_flags_percentage)

        result.avg_episode_steps.append(avg_episode_steps)
        result.avg_episode_rewards.append(avg_episode_rewards)
        result.epsilon_values.append(self.agent_config.epsilon)
        result.avg_episode_loss.append(avg_episode_loss)
        result.avg_episode_flags.append(avg_episode_flags)
        result.avg_episode_flags_percentage.append(avg_episode_flags_percentage)
        result.lr_list.append(lr)

    def log_tensorboard(self, episode: int, avg_episode_rewards: float,
                        avg_episode_steps: float, episode_avg_loss: float,
                        epsilon: float, lr: float, eval=False, avg_flags_catched : int = 0,
                        avg_episode_flags_percentage : list = None) -> None:
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
        :return: None
        """
        train_or_eval = "eval" if eval else "train"
        self.tensorboard_writer.add_scalar('avg_episode_rewards/' + train_or_eval,
                                           avg_episode_rewards, episode)
        self.tensorboard_writer.add_scalar('episode_steps/' + train_or_eval, avg_episode_steps, episode)
        self.tensorboard_writer.add_scalar('episode_avg_loss/' + train_or_eval, episode_avg_loss, episode)
        self.tensorboard_writer.add_scalar('epsilon/' + train_or_eval, epsilon, episode)
        self.tensorboard_writer.add_scalar('avg_episode_flags/' + train_or_eval, avg_flags_catched, episode)
        self.tensorboard_writer.add_scalar('avg_episode_flags_percentage/' + train_or_eval,
                                           avg_episode_flags_percentage, episode)
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
            assert eval_env.num_envs == 1
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
        return self.policy.predict(observation, state, mask, deterministic, env_config=self.env.envs[0].env_config,
                                   env_state=self.env.envs[0].env_state)

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
            self._last_dones = np.zeros((self.env.num_envs,), dtype=np.bool)
            # Retrieve unnormalized observation for saving into the buffer
            if self._vec_normalize_env is not None:
                self._last_original_obs = self._vec_normalize_env.get_original_obs()

        if eval_env is not None and self.seed is not None:
            eval_env.seed(self.seed)

        eval_env = self._get_eval_env(eval_env)

        # Configure logger's outputs
        #utils.configure_logger(self.verbose, self.tensorboard_log, tb_log_name, reset_num_timesteps)

        # Create eval callback if needed
        callback = self._init_callback(callback, eval_env, eval_freq, n_eval_episodes, log_path)

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
        return ["policy", "device", "env", "eval_env", "replay_buffer", "rollout_buffer", "_vec_normalize_env"]

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
