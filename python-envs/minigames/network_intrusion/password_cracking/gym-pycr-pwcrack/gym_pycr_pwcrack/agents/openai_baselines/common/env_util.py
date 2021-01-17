import os
from typing import Any, Callable, Dict, Optional, Type, Union
import time
import gym

from stable_baselines3.common.atari_wrappers import AtariWrapper
from gym_pycr_pwcrack.agents.openai_baselines.common.monitor import Monitor
from gym_pycr_pwcrack.agents.openai_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv, VecEnv


def unwrap_wrapper(env: gym.Env, wrapper_class: Type[gym.Wrapper]) -> Optional[gym.Wrapper]:
    """
    Retrieve a ``VecEnvWrapper`` object by recursively searching.

    :param env: Environment to unwrap
    :param wrapper_class: Wrapper to look for
    :return: Environment unwrapped till ``wrapper_class`` if it has been wrapped with it
    """
    env_tmp = env
    while isinstance(env_tmp, gym.Wrapper):
        if isinstance(env_tmp, wrapper_class):
            return env_tmp
        env_tmp = env_tmp.env
    return None


def is_wrapped(env: Type[gym.Env], wrapper_class: Type[gym.Wrapper]) -> bool:
    """
    Check if a given environment has been wrapped with a given wrapper.

    :param env: Environment to check
    :param wrapper_class: Wrapper class to look for
    :return: True if environment has been wrapped with ``wrapper_class``.
    """
    return unwrap_wrapper(env, wrapper_class) is not None


def make_vec_env(
    env_id: Union[str, Type[gym.Env]],
    n_envs: int = 1,
    seed: Optional[int] = None,
    start_index: int = 0,
    monitor_dir: Optional[str] = None,
    wrapper_class: Optional[Callable[[gym.Env], gym.Env]] = None,
    env_kwargs: Optional[Dict[str, Any]] = None,
    vec_env_cls: Optional[Type[Union[DummyVecEnv, SubprocVecEnv]]] = None,
    vec_env_kwargs: Optional[Dict[str, Any]] = None,
    monitor_kwargs: Optional[Dict[str, Any]] = None,
    multi_env : bool = False
) -> VecEnv:
    """
    Create a wrapped, monitored ``VecEnv``.
    By default it uses a ``DummyVecEnv`` which is usually faster
    than a ``SubprocVecEnv``.

    :param env_id: the environment ID or the environment class
    :param n_envs: the number of environments you wish to have in parallel
    :param seed: the initial seed for the random number generator
    :param start_index: start rank index
    :param monitor_dir: Path to a folder where the monitor files will be saved.
        If None, no file will be written, however, the env will still be wrapped
        in a Monitor wrapper to provide additional information about training.
    :param wrapper_class: Additional wrapper to use on the environment.
        This can also be a function with single argument that wraps the environment in many things.
    :param env_kwargs: Optional keyword argument to pass to the env constructor
    :param vec_env_cls: A custom ``VecEnv`` class constructor. Default: None.
    :param vec_env_kwargs: Keyword arguments to pass to the ``VecEnv`` class constructor.
    :param monitor_kwargs: Keyword arguments to pass to the ``Monitor`` class constructor.
    :return: The wrapped environment
    """
    if multi_env:
        env_kwargs = [{}] if env_kwargs is None else env_kwargs
    else:
        env_kwargs = {} if env_kwargs is None else env_kwargs
    vec_env_kwargs = {} if vec_env_kwargs is None else vec_env_kwargs
    monitor_kwargs = {} if monitor_kwargs is None else monitor_kwargs

    # No custom VecEnv is passed
    if vec_env_cls is None:
        # Default: use a DummyVecEnv
        vec_env_cls = DummyVecEnv
    
    if multi_env:
        envs_list = []
        for i in range(len(env_kwargs)):
            envs_list = envs_list + [make_env(j + start_index, env_kwargs[i], env_id, seed,
                                               monitor_dir, wrapper_class, monitor_kwargs) for j in range(n_envs)]
    else:
        envs_list = [make_env(i + start_index, env_kwargs, env_id, seed, monitor_dir, wrapper_class, monitor_kwargs)
         for i in range(n_envs)]
    return vec_env_cls(envs_list, **vec_env_kwargs)


def make_env(rank, env_kwargs, env_id, seed, monitor_dir, wrapper_class, monitor_kwargs):
    def _init():
        if "cluster_config" in env_kwargs:
            cluster_config = env_kwargs["cluster_config"]
            if cluster_config is not None:
                cluster_config.port_forward_next_port = cluster_config.port_forward_next_port + 200 * rank
        if "num_nodes" in env_kwargs:
            num_nodes = env_kwargs["num_nodes"]
        else:
            num_nodes = -1
        if isinstance(env_id, str):
            if "containers_config" in env_kwargs and "flags_config" in env_kwargs:
                containers_config = env_kwargs["containers_config"]
                flags_config = env_kwargs["flags_config"]
                if "idx"in env_kwargs:
                    cluster_config.port_forward_next_port = cluster_config.port_forward_next_port + 200 * env_kwargs["idx"]
                    env = gym.make(env_id, env_config=env_kwargs["env_config"], cluster_config=cluster_config,
                                   checkpoint_dir=env_kwargs["checkpoint_dir"], containers_configs=containers_config,
                                   flags_configs=flags_config, idx=env_kwargs["idx"],
                                   num_nodes=num_nodes)
                else:
                    env = gym.make(env_id, env_config=env_kwargs["env_config"], cluster_config=cluster_config,
                                   checkpoint_dir=env_kwargs["checkpoint_dir"], containers_config=containers_config,
                                   flags_config=flags_config, num_nodes=num_nodes)
            elif "dr_max_num_nodes" in env_kwargs:
                dr_max_num_nodes = env_kwargs["dr_max_num_nodes"]
                dr_min_num_nodes = env_kwargs["dr_min_num_nodes"]
                dr_max_num_flags = env_kwargs["dr_max_num_flags"]
                dr_min_num_flags = env_kwargs["dr_min_num_flags"]
                dr_max_num_users = env_kwargs["dr_max_num_users"]
                dr_min_num_users = env_kwargs["dr_min_num_users"]
                idx = env_kwargs["idx"]
                env = gym.make(env_id, env_config=env_kwargs["env_config"],
                               checkpoint_dir=env_kwargs["checkpoint_dir"], dr_max_num_nodes=dr_max_num_nodes,
                               dr_min_num_nodes=dr_min_num_nodes, dr_max_num_flags=dr_max_num_flags,
                               dr_min_num_flags=dr_min_num_flags, dr_max_num_users=dr_max_num_users,
                               dr_min_num_users=dr_min_num_users, idx=idx)
            else:
                env = gym.make(env_id, env_config=env_kwargs["env_config"],
                               cluster_config=cluster_config,
                               checkpoint_dir=env_kwargs["checkpoint_dir"])
        else:
            if "containers_config" in env_kwargs and "flags_config" in env_kwargs:
                containers_config = env_kwargs["containers_config"]
                flags_config = env_kwargs["flags_config"]
                if "idx" in env_kwargs:
                    env = env_id(env_config=env_kwargs["env_config"],
                                 cluster_config=cluster_config,
                                 checkpoint_dir=env_kwargs["checkpoint_dir"], containers_config=containers_config,
                                 flags_config=flags_config, idx=env_kwargs["idx"], num_nodes=num_nodes)
                else:
                    env = env_id(env_config=env_kwargs["env_config"],
                                 cluster_config=cluster_config,
                                 checkpoint_dir=env_kwargs["checkpoint_dir"], containers_config=containers_config,
                                 flags_config=flags_config, num_nodes=num_nodes)
            elif "dr_max_num_nodes" in env_kwargs:
                dr_max_num_nodes = env_kwargs["dr_max_num_nodes"]
                dr_min_num_nodes = env_kwargs["dr_min_num_nodes"]
                dr_max_num_flags = env_kwargs["dr_max_num_flags"]
                dr_min_num_flags = env_kwargs["dr_min_num_flags"]
                dr_max_num_users = env_kwargs["dr_max_num_users"]
                dr_min_num_users = env_kwargs["dr_min_num_users"]
                idx = env_kwargs["idx"]
                env = env_id(env_id, env_config=env_kwargs["env_config"],
                               checkpoint_dir=env_kwargs["checkpoint_dir"], dr_max_num_nodes=dr_max_num_nodes,
                               dr_min_num_nodes=dr_min_num_nodes, dr_max_num_flags=dr_max_num_flags,
                               dr_min_num_flags=dr_min_num_flags, dr_max_num_users=dr_max_num_users,
                               dr_min_num_users=dr_min_num_users, idx=idx)
            else:
                env = env_id(env_config=env_kwargs["env_config"],
                             cluster_config=cluster_config,
                             checkpoint_dir=env_kwargs["checkpoint_dir"])

        if seed is not None:
            env.seed(seed + rank)
            env.action_space.seed(seed + rank)
        # Wrap the env in a Monitor wrapper
        # to have additional training information
        monitor_path = os.path.join(monitor_dir, str(rank)) if monitor_dir is not None else None
        # Create the monitor folder if needed
        if monitor_path is not None:
            os.makedirs(monitor_dir, exist_ok=True)
        env = Monitor(env, filename=monitor_path, **monitor_kwargs)
        # Optionally, wrap the environment with the provided wrapper
        if wrapper_class is not None:
            env = wrapper_class(env)

        return env

    return _init

def make_atari_env(
    env_id: Union[str, Type[gym.Env]],
    n_envs: int = 1,
    seed: Optional[int] = None,
    start_index: int = 0,
    monitor_dir: Optional[str] = None,
    wrapper_kwargs: Optional[Dict[str, Any]] = None,
    env_kwargs: Optional[Dict[str, Any]] = None,
    vec_env_cls: Optional[Union[DummyVecEnv, SubprocVecEnv]] = None,
    vec_env_kwargs: Optional[Dict[str, Any]] = None,
    monitor_kwargs: Optional[Dict[str, Any]] = None,
) -> VecEnv:
    """
    Create a wrapped, monitored VecEnv for Atari.
    It is a wrapper around ``make_vec_env`` that includes common preprocessing for Atari games.

    :param env_id: the environment ID or the environment class
    :param n_envs: the number of environments you wish to have in parallel
    :param seed: the initial seed for the random number generator
    :param start_index: start rank index
    :param monitor_dir: Path to a folder where the monitor files will be saved.
        If None, no file will be written, however, the env will still be wrapped
        in a Monitor wrapper to provide additional information about training.
    :param wrapper_kwargs: Optional keyword argument to pass to the ``AtariWrapper``
    :param env_kwargs: Optional keyword argument to pass to the env constructor
    :param vec_env_cls: A custom ``VecEnv`` class constructor. Default: None.
    :param vec_env_kwargs: Keyword arguments to pass to the ``VecEnv`` class constructor.
    :param monitor_kwargs: Keyword arguments to pass to the ``Monitor`` class constructor.
    :return: The wrapped environment
    """
    if wrapper_kwargs is None:
        wrapper_kwargs = {}

    def atari_wrapper(env: gym.Env) -> gym.Env:
        env = AtariWrapper(env, **wrapper_kwargs)
        return env

    return make_vec_env(
        env_id,
        n_envs=n_envs,
        seed=seed,
        start_index=start_index,
        monitor_dir=monitor_dir,
        wrapper_class=atari_wrapper,
        env_kwargs=env_kwargs,
        vec_env_cls=vec_env_cls,
        vec_env_kwargs=vec_env_kwargs,
        monitor_kwargs=monitor_kwargs,
    )