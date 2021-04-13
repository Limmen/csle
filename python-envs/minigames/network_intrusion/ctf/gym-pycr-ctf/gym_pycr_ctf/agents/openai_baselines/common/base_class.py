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

from stable_baselines3.common import logger
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.noise import ActionNoise
from stable_baselines3.common.preprocessing import is_image_space
from gym_pycr_ctf.agents.openai_baselines.common.save_util import load_from_zip_file, recursive_getattr, \
    recursive_setattr, save_to_zip_file
from gym_pycr_ctf.dao.agent.train_mode import TrainMode

from gym_pycr_ctf.agents.openai_baselines.common.utils import (
    check_for_correct_spaces,
    get_device,
    get_schedule_fn,
    set_random_seed,
    update_learning_rate,
)
from gym_pycr_ctf.agents.openai_baselines.common.type_aliases import GymEnv, MaybeCallback
from gym_pycr_ctf.agents.openai_baselines.common.callbacks import BaseCallback, CallbackList, ConvertCallback, EvalCallback
from gym_pycr_ctf.agents.openai_baselines.common.vec_env import DummyVecEnv, VecEnv, VecNormalize, VecTransposeImage, unwrap_vec_normalize, SubprocVecEnv

from gym_pycr_ctf.agents.openai_baselines.common.policies import BasePolicy, get_policy_from_name
from gym_pycr_ctf.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.dao.experiment.experiment_result import ExperimentResult
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.env_state import EnvState
import gym_pycr_ctf.envs_model.logic.common.util as pycr_util
from gym_pycr_ctf.dao.agent.train_agent_log_dto import TrainAgentLogDTO
from gym_pycr_ctf.agents.util.log_util import LogUtil


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

    :param attacker_policy: (Type[BasePolicy]) Policy object
    :param env: (Union[GymEnv, str, None]) The environment to learn from
                (if registered in Gym, can be str. Can be None for loading trained models)
    :param attacker_policy_base: (Type[BasePolicy]) The base policy used by this method
    :param attacker_learning_rate: (float or callable) learning rate for the optimizer,
        it can be a function of the current progress remaining (from 1 to 0)
    :param attacker_policy_kwargs: (Dict[str, Any]) Additional arguments to be passed to the policy on creation
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
            attacker_policy: Type[BasePolicy],
            defender_policy: Type[BasePolicy],
            env: Union[GymEnv, str, None],
            attacker_policy_base: Type[BasePolicy],
            defender_policy_base: Type[BasePolicy],
            attacker_learning_rate: Union[float, Callable],
            defender_learning_rate: Union[float, Callable],
            attacker_policy_kwargs: Dict[str, Any] = None,
            defender_policy_kwargs: Dict[str, Any] = None,
            verbose: int = 0,
            device: Union[th.device, str] = "auto",
            support_multi_env: bool = False,
            create_eval_env: bool = False,
            monitor_wrapper: bool = True,
            seed: Optional[int] = None,
            use_sde: bool = False,
            sde_sample_freq: int = -1,
            attacker_agent_config: AgentConfig = None,
            defender_agent_config: AgentConfig = None,
            env_2: Union[GymEnv, str, None] = None,
            train_mode : TrainMode = TrainMode.TRAIN_ATTACKER,
            attacker_opponent=None,
            defender_opponent=None
    ):
        self.attacker_agent_config = attacker_agent_config
        self.defender_agent_config = defender_agent_config
        self.train_result = ExperimentResult()
        self.eval_result = ExperimentResult()
        self.attacker_opponent = attacker_opponent
        self.defender_opponent = defender_opponent
        self.training_start = time.time()

        try:
            self.tensorboard_writer = SummaryWriter(self.attacker_agent_config.tensorboard_dir)
            self.tensorboard_writer.add_hparams(self.attacker_agent_config.hparams_dict(), {})
        except:
            print("error creating tensorboard writer")

        if isinstance(attacker_policy, str) and attacker_policy_base is not None:
            self.attacker_policy_class = get_policy_from_name(attacker_policy_base, attacker_policy)
        else:
            self.attacker_policy_class = attacker_policy

        if isinstance(defender_policy, str) and defender_policy_base is not None:
            self.defender_policy_class = get_policy_from_name(defender_policy_base, defender_policy)
        else:
            self.defender_policy_class = defender_policy

        self.device = get_device(device, agent_config=self.attacker_agent_config)
        if verbose > 0:
            print(f"Using {self.device} device")
        self.train_mode = train_mode
        self.env = None  # type: Optional[GymEnv]
        self.env_2 = None  # type: Optional[GymEnv]
        # get VecNormalize object if needed
        self._vec_normalize_env = unwrap_vec_normalize(env)
        self.verbose = verbose
        self.attacker_policy_kwargs = {} if attacker_policy_kwargs is None else attacker_policy_kwargs
        self.defender_policy_kwargs = {} if defender_policy_kwargs is None else defender_policy_kwargs
        self.attacker_observation_space = None  # type: Optional[gym.spaces.Space]
        self.defender_observation_space = None  # type: Optional[gym.spaces.Space]
        self.attacker_action_space = None  # type: Optional[gym.spaces.Space]
        self.defender_action_space = None  # type: Optional[gym.spaces.Space]
        self.n_envs = None
        self.num_timesteps = 0
        # Used for updating schedules
        self._total_timesteps = 0
        self.eval_env = None
        self.seed = seed
        self.action_noise = None  # type: Optional[ActionNoise]
        self.start_time = None
        self.attacker_policy = None
        self.defender_policy = None
        self.attacker_m_selection_policy = None
        self.attacker_m_action_policy = None
        self.attacker_learning_rate = attacker_learning_rate
        self.defender_learning_rate = defender_learning_rate
        self.attacker_lr_schedule = None  # type: Optional[Callable]
        self.defender_lr_schedule = None  # type: Optional[Callable]
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

            self.attacker_observation_space = env.attacker_observation_space
            self.attacker_action_space = env.attacker_action_space

            self.defender_observation_space = env.defender_observation_space
            self.defender_action_space = env.defender_action_space

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

        if self.use_sde and not isinstance(self.attacker_observation_space, gym.spaces.Box):
            raise ValueError("generalized State-Dependent Exploration (gSDE) can only be used with continuous actions.")

        if self.use_sde and not isinstance(self.defender_observation_space, gym.spaces.Box):
            raise ValueError("generalized State-Dependent Exploration (gSDE) can only be used with continuous actions.")

    def _wrap_env(self, env: GymEnv) -> VecEnv:
        if not isinstance(env, VecEnv):
            print("Wrapping the env in a DummyVecEnv.")
            env = DummyVecEnv([lambda: env])

        if is_image_space(env.attacker_observation_space) and not isinstance(env, VecTransposeImage):
            if self.verbose >= 1:
                print("Wrapping the env in a VecTransposeImage.")
            env = VecTransposeImage(env)
        return env

    def log_metrics_attacker(self, train_log_dto: TrainAgentLogDTO, eps: float = None, eval: bool = False) \
            -> TrainAgentLogDTO:
        """
        Logs average metrics for the last <self.config.log_frequency> episodes

        :param train_log_dto: DTO with the information to log
        :param eps: machine eps
        :param eval: flag whether it is evaluation or not
        :return: the updated train agent log dto
        """
        return LogUtil.log_metrics_attacker(train_log_dto=train_log_dto, eps=eps, eval=eval,
                                     attacker_agent_config=self.attacker_agent_config, env=self.env,
                                     env_2=self.env_2, tensorboard_writer=self.tensorboard_writer)

    def log_metrics_defender(self, train_log_dto: TrainAgentLogDTO, eps: float = None, eval: bool = False) \
            -> TrainAgentLogDTO:
        """
        Logs average metrics for the last <self.config.log_frequency> episodes

        :param train_log_dto: DTO with the information to log
        :param eps: machine eps
        :param eval: flag whether it is evaluation or not
        :return: the updated train agent log dto
        """
        return LogUtil.log_metrics_defender(train_log_dto=train_log_dto, eps=eps, eval=eval, env=self.env,
                                     env_2=self.env_2, defender_agent_config=self.defender_agent_config,
                                     tensorboard_writer=self.tensorboard_writer)

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
        self.attacker_lr_schedule = get_schedule_fn(self.attacker_learning_rate)
        self.defender_lr_schedule = get_schedule_fn(self.defender_learning_rate)

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
        logger.record("train/learning_rate", self.attacker_lr_schedule(self._current_progress_remaining))

        if not isinstance(optimizers, list):
            optimizers = [optimizers]
        for optimizer in optimizers:
            update_learning_rate(optimizer, self.attacker_lr_schedule(self._current_progress_remaining))

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
        check_for_correct_spaces(env, self.attacker_observation_space, self.attacker_action_space)
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
            env=None,
            attacker : bool = False
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
        if attacker:
            if not self.attacker_agent_config.ar_policy:
                return self.attacker_policy.predict(observation, state, mask, deterministic,
                                                    env_config=env_config,
                                                    env_state=env_state, env_configs=env_configs,
                                                    env=env, infos=infos, env_idx=env_idx, mask_actions=mask_actions,
                                                    attacker=attacker)
            else:
                m_selection_actions, state1 = self.attacker_m_selection_policy.predict(observation, state, mask, deterministic,
                                                                                       env_config=env_config,
                                                                                       env_state=env_state,
                                                                                       infos=infos,
                                                                                       attacker=attacker)
                obs_2 = observation.reshape((observation.shape[0],) + self.env.envs[0].network_orig_shape)
                idx = m_selection_actions[0]
                if m_selection_actions[0] > 5:
                    idx = 0
                machine_obs = obs_2[:, idx].reshape((observation.shape[0],) + self.env.envs[0].machine_orig_shape)
                machine_obs_tensor = th.as_tensor(machine_obs).to(self.device)
                m_actions, state2 = self.attacker_m_action_policy.predict(machine_obs_tensor, state, mask, deterministic,
                                                                          env_config=env_config,
                                                                          env_state=env_state, infos=infos,
                                                                          attacker=attacker)
                actions = self.env.envs[0].attacker_convert_ar_action(m_selection_actions[0], m_actions[0])
                actions = np.array([actions])
                return actions, state2
        else:
            return self.defender_policy.predict(observation, state, mask, deterministic,
                                                env_config=env_config,
                                                env_state=env_state, env_configs=env_configs,
                                                env=env, infos=infos, env_idx=env_idx, mask_actions=mask_actions,
                                                attacker=attacker)

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

        if env is None and "env" in data:
            env = data["env"]

        # noinspection PyArgumentList
        model = cls(
            attacker_policy=data["attacker_policy_class"],
            defender_policy=data["defender_policy_class"],
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
            model.attacker_policy.reset_noise()  # pytype: disable=attribute-error
            model.defender_policy.reset_noise()  # pytype: disable=attribute-error
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
        self.attacker_action_space.seed(seed)
        self.defender_action_space.seed(seed)
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
                deterministic=self.attacker_agent_config.eval_deterministic,
                best_model_save_path=log_path,
                log_path=log_path,
                eval_freq=eval_freq,
                n_eval_episodes=n_eval_episodes,
                attacker_agent_config=self.attacker_agent_config,
                defender_agent_config=self.defender_agent_config
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
            if len(self._last_obs[0].shape) == 3:
                self._last_obs = (self._last_obs[0].reshape((self._last_obs[0].shape[0], self.attacker_observation_space.shape[0])),
                                  self._last_obs[1].reshape((self._last_obs[1].shape[0], self.defender_observation_space.shape[0])))
            self._last_dones = np.zeros((self.env.num_envs,), dtype=np.bool)
            if isinstance(self.env, SubprocVecEnv):
                self._last_infos = np.array([{"attacker_non_legal_actions": self.env.attacker_initial_illegal_actions} for i in range(self.env.num_envs)])
                self._last_infos = np.array(
                    [{"defender_non_legal_actions": self.env.defender_initial_illegal_actions} for i in range(self.env.num_envs)])
            else:
                self._last_infos = np.array([{"attacker_non_legal_actions": []} for i in range(self.env.num_envs)])
                self._last_infos = np.array([{"defender_non_legal_actions": []} for i in range(self.env.num_envs)])

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
        return ["device", "env", "eval_env", "replay_buffer", "attacker_rollout_buffer", "defender_rollout_buffer",
                "_vec_normalize_env", "tensoboard_writer"]

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

    def save_model(self, iteration : int = 1) -> None:
        """
        Saves the PyTorch Model Weights

        :return: None
        """
        time_str = str(time.time())
        if self.train_mode == TrainMode.TRAIN_ATTACKER or self.train_mode == TrainMode.SELF_PLAY:
            save_dir = self.attacker_agent_config.save_dir
            seed = self.attacker_agent_config.random_seed
        else:
            save_dir = self.defender_agent_config.save_dir
            seed = self.defender_agent_config.random_seed

        if save_dir is not None:
            path = save_dir + "/" + time_str + "_" + str(seed)  + "_" + str(iteration) + "_policy_network.zip"
            env_config = None
            env_configs = None
            eval_env_config = None
            eval_env_configs = None
            if self.attacker_agent_config is not None:
                self.attacker_agent_config.logger.info("Saving policy-network to: {}".format(path))
                env_config = self.attacker_agent_config.env_config
                env_configs = self.attacker_agent_config.env_configs
                eval_env_config = self.attacker_agent_config.eval_env_config
                eval_env_configs = self.attacker_agent_config.eval_env_configs
                self.attacker_agent_config.env_config = None
                self.attacker_agent_config.env_configs = None
                self.attacker_agent_config.eval_env_config = None
                self.attacker_agent_config.eval_env_configs = None
            if self.defender_agent_config is not None:
                self.defender_agent_config.logger.info("Saving policy-network to: {}".format(path))
                if self.defender_agent_config.env_config is not None:
                    env_config = self.defender_agent_config.env_config
                    env_configs = self.defender_agent_config.env_configs
                    eval_env_config = self.defender_agent_config.eval_env_config
                    eval_env_configs = self.defender_agent_config.eval_env_configs
                    self.defender_agent_config.env_config = None
                    self.defender_agent_config.env_configs = None
                    self.defender_agent_config.eval_env_config = None
                    self.defender_agent_config.eval_env_configs = None
            self.save(path, exclude=["tensorboard_writer", "eval_env", "env_2", "env", "attacker_opponent",
                                     "defender_opponent"])
            if self.attacker_agent_config is not None:
                self.attacker_agent_config.env_config = env_config
                self.attacker_agent_config.env_configs = env_configs
                self.attacker_agent_config.eval_env_config = eval_env_config
                self.attacker_agent_config.eval_env_configs = eval_env_configs
            if self.defender_agent_config is not None:
                self.defender_agent_config.env_config = env_config
                self.defender_agent_config.env_configs = env_configs
                self.defender_agent_config.eval_env_config = eval_env_config
                self.defender_agent_config.eval_env_configs = eval_env_configs
        else:
            if self.attacker_agent_config is not None:
                self.attacker_agent_config.logger.warning("Save path not defined, not saving policy-networks to disk")
                print("Save path not defined, not saving policy-networks to disk")
            if self.defender_agent_config is not None:
                self.defender_agent_config.logger.warning("Save path not defined, not saving policy-networks to disk")
                print("Save path not defined, not saving policy-networks to disk")
