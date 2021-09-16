"""Common aliases for type hints"""

from typing import Any, Callable, Dict, List, NamedTuple, Tuple, Union

import gym
import numpy as np
import torch as th

from pycr_common.agents.openai_baselines.common.callbacks import BaseCallback
from pycr_common.agents.openai_baselines.common.vec_env import VecEnv

GymEnv = Union[gym.Env, VecEnv]
GymObs = Union[Tuple, Dict[str, Any], np.ndarray, int]
GymStepReturn = Tuple[GymObs, float, bool, Dict]
TensorDict = Dict[str, th.Tensor]
OptimizerStateDict = Dict[str, Any]
MaybeCallback = Union[None, Callable, List[BaseCallback], BaseCallback]


class RolloutBufferSamples(NamedTuple):
    observations: th.Tensor
    actions: th.Tensor
    old_values: th.Tensor
    old_log_prob: th.Tensor
    advantages: th.Tensor
    returns: th.Tensor


class ReplayBufferSamples(NamedTuple):
    observations: th.Tensor
    actions: th.Tensor
    next_observations: th.Tensor
    dones: th.Tensor
    rewards: th.Tensor


class RolloutReturn(NamedTuple):
    episode_reward: float
    episode_timesteps: int
    n_episodes: int
    continue_training: bool


class RolloutBufferSamplesAR(NamedTuple):
    network_observations: th.Tensor
    machine_observations: th.Tensor
    m_selection_actions: th.Tensor
    m_actions: th.Tensor
    m_selection_old_values: th.Tensor
    m_action_old_values: th.Tensor
    m_selection_old_log_prob: th.Tensor
    m_action_old_log_prob: th.Tensor
    m_selection_advantages: th.Tensor
    m_action_advantages: th.Tensor
    m_selection_returns: th.Tensor
    m_action_returns: th.Tensor