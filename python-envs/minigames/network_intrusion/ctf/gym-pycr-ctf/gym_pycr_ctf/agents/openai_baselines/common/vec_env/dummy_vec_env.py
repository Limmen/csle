from collections import OrderedDict
from copy import deepcopy
from typing import Callable, List, Optional, Sequence
import time
import gym
import numpy as np
from gym_pycr_ctf.agents.openai_baselines.common.vec_env.base_vec_env import VecEnv
from gym_pycr_ctf.agents.openai_baselines.common.vec_env.util import copy_obs_dict, dict_to_obs, obs_space_info
import gym_pycr_ctf.constants.constants as constants

class DummyVecEnv(VecEnv):
    """
    Creates a level_1 vectorized wrapper for multiple environments, calling each environment in sequence on the current
    Python process. This is useful for computationally level_1 environment such as ``cartpole-v1``,
    as the overhead of multiprocess or multithread outweighs the environment computation time.
    This can also be used for RL methods that
    require a vectorized environment, but that you want a single environments to train with.

    :param env_fns: (List[Callable[[], gym.Env]]) a list of functions
        that return environments to vectorize
    """

    def __init__(self, env_fns: List[Callable[[], gym.Env]], env_config = None):
        self.envs = []
        for fn in env_fns:
            print("sleeping")
            time.sleep(constants.SUB_PROC_ENV.SLEEP_TIME_STARTUP)
            print("sleep finished")
            self.envs.append(fn())
        self.envs = [fn() for fn in env_fns]
        env = self.envs[0]
        VecEnv.__init__(self, len(env_fns), env.attacker_observation_space, env.attacker_action_space,
                        env.defender_observation_space, env.defender_action_space)
        attacker_obs_space = env.attacker_observation_space
        self.attacker_keys, attacker_shapes, attacker_dtypes = obs_space_info(attacker_obs_space)
        defender_obs_space = env.defender_observation_space
        self.defender_keys, defender_shapes, defender_dtypes = obs_space_info(defender_obs_space)

        self.buf_obs_attacker = OrderedDict([(k, np.zeros((self.num_envs,) + tuple(attacker_shapes[k]),
                                                          dtype=attacker_dtypes[k])) for k in self.attacker_keys])
        self.buf_obs_defender = OrderedDict([(k, np.zeros((self.num_envs,) + tuple(defender_shapes[k]),
                                                          dtype=defender_dtypes[k])) for k in self.defender_keys])
        self.buf_dones = np.zeros((self.num_envs,), dtype=np.bool)
        self.buf_rews_attacker = np.zeros((self.num_envs,), dtype=np.float32)
        self.buf_rews_defender = np.zeros((self.num_envs,), dtype=np.float32)
        self.buf_infos = [{"idx": self.envs[i].idx} for i in range(self.num_envs)]
        self.actions = None
        self.metadata = env.metadata
        #self.initial_illegal_actions = self.envs[0].initial_illegal_actions
        #self.env_config = self.envs[0].env_config

    def step_async(self, actions: np.ndarray):
        self.actions = actions

    def env_configs(self):
        return [self.envs[i].env_config for i in range(len(self.envs))]

    def env_config(self, idx: int):
        return self.envs[idx].env_config

    def step_wait(self):
        for env_idx in range(self.num_envs):
            obs, rew, done, info = self.envs[env_idx].step(self.actions[env_idx])
            attacker_rew, defender_rew = rew
            self.buf_rews_attacker[env_idx] = attacker_rew
            self.buf_rews_defender[env_idx] = defender_rew
            self.buf_dones[env_idx] = done
            self.buf_infos[env_idx] = info
            self.buf_infos[env_idx]["idx"] = self.envs[env_idx].idx


            if self.buf_dones[env_idx]:
                # save final observation where user can get it, then reset
                self.buf_infos[env_idx]["terminal_observation"] = obs
                obs = self.envs[env_idx].reset()
            self._save_obs(env_idx, obs)
        return (self._obs_from_buf(), (np.copy(self.buf_rews_attacker), np.copy(self.buf_rews_defender)), np.copy(self.buf_dones), deepcopy(self.buf_infos))

    def seed(self, seed: Optional[int] = None) -> List[int]:
        seeds = list()
        for idx, env in enumerate(self.envs):
            seeds.append(env.seed(seed + idx))
        return seeds

    def reset(self):
        for env_idx in range(self.num_envs):
            obs = self.envs[env_idx].reset()
            self._save_obs(env_idx, obs)
        o = self._obs_from_buf()
        return o

    def close(self):
        for env in self.envs:
            env.close()

    def cleanup(self):
        for env in self.envs:
            env.cleanup()

    def get_images(self) -> Sequence[np.ndarray]:
        return [env.render(mode="rgb_array") for env in self.envs]

    def render(self, mode: str = "human"):
        """
        Gym environment rendering. If there are multiple environments then
        they are tiled together in one image via ``BaseVecEnv.render()``.
        Otherwise (if ``self.num_envs == 1``), we pass the render call directly to the
        underlying environment.

        Therefore, some arguments such as ``mode`` will have values that are valid
        only when ``num_envs == 1``.

        :param mode: The rendering type.
        """
        if self.num_envs == 1:
            return self.envs[0].render(mode=mode)
        else:
            return super().render(mode=mode)

    def _save_obs(self, env_idx, obs):
        obs_attacker, obs_defender = obs
        for key in self.attacker_keys:
            if key is None:
                pass
                #self.buf_obs[key][env_idx] = obs
            else:
                self.buf_obs_attacker[key][env_idx] = obs_attacker[key]

        for key in self.defender_keys:
            if key is None:
                pass
                # self.buf_obs[key][env_idx] = obs
            else:
                self.buf_obs_defender[key][env_idx] = obs_defender[key]


    def _obs_from_buf(self):
        attacker_obs = dict_to_obs(self.attacker_observation_space, copy_obs_dict(self.buf_obs_attacker))
        defender_obs = dict_to_obs(self.defender_observation_space, copy_obs_dict(self.buf_obs_defender))
        return (attacker_obs, defender_obs)

    def get_attr(self, attr_name, indices=None):
        """Return attribute from vectorized environment (see base class)."""
        target_envs = self._get_target_envs(indices)
        return [getattr(env_i, attr_name) for env_i in target_envs]

    def set_attr(self, attr_name, value, indices=None):
        """Set attribute inside vectorized environments (see base class)."""
        target_envs = self._get_target_envs(indices)
        for env_i in target_envs:
            setattr(env_i, attr_name, value)

    def env_method(self, method_name, *method_args, indices=None, **method_kwargs):
        """Call instance methods of vectorized environments."""
        target_envs = self._get_target_envs(indices)
        return [getattr(env_i, method_name)(*method_args, **method_kwargs) for env_i in target_envs]

    def _get_target_envs(self, indices):
        indices = self._get_indices(indices)
        return [self.envs[i] for i in indices]