from typing import Tuple, Any, Dict, List, Union
import gymnasium as gym
import numpy as np
from csle_tolerance.dao.intrusion_recovery_pomdp_config import IntrusionRecoveryPomdpConfig
from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil
from csle_tolerance.util.general_util import GeneralUtil


class IntrusionRecoveryPomdpEnv(gym.Env):
    """
    Gym Environment representing the Intrusion recovery POMDP
    """

    def __init__(self, config: IntrusionRecoveryPomdpConfig):
        """
        Initializes the environment

        :param config: the environment configuration
        """
        self.config = config
        self.action_space = gym.spaces.Discrete(len(self.config.actions))
        self.observation_space = gym.spaces.Box(
            low=np.array([np.float64(1), np.float64(min(config.observations)), np.float64(0)]),
            high=np.array([np.float64(config.BTR), np.float64(max(config.observations)), np.float64(1)]),
            dtype=np.float64, shape=(3,))
        self.viewer = None
        self.metadata = {'render.modes': ['human', 'rgb_array'], 'video.frames_per_second': 50}
        self.b = self.config.b1.copy()
        self.t = 1
        self.s = IntrusionRecoveryPomdpUtil.sample_initial_state(b1=self.b)
        self.o = 0
        self.reset()
        super().__init__()

    def step(self, a: int) -> Tuple[List[Union[int, int, float]], float, bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param a: the action
        :return: (obs, reward, terminated, truncated, info)
        """
        done = False
        c = self.config.cost_tensor[a][self.s]
        self.s = GeneralUtil.sample_next_state(transition_tensor=self.config.transition_tensor,
                                               s=self.s, a=a, states=self.config.states)
        self.o = IntrusionRecoveryPomdpUtil.sample_next_observation(observation_tensor=self.config.observation_tensor,
                                                                    s_prime=self.s,
                                                                    observations=self.config.observations)
        self.b = IntrusionRecoveryPomdpUtil.next_belief(o=self.o, a=a, b=self.b, states=self.config.states,
                                                        observations=self.config.observations,
                                                        observation_tensor=self.config.observation_tensor,
                                                        transition_tensor=self.config.transition_tensor)
        self.t += 1
        info: Dict[str, Any] = {}
        if self.t >= self.config.BTR or self.s == 2:
            done = True
        return [self.t, self.o, self.b[1]], c, done, done, info

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[List[Union[int, int, float]], Dict[str, Any]]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :param seed: the random seed
        :param soft: boolean flag indicating whether it is a soft reset or not
        :param options: optional configuration parameters
        :return: initial observation and info
        """
        super().reset(seed=seed)
        self.b = self.config.b1.copy()
        self.t = 1
        self.s = IntrusionRecoveryPomdpUtil.sample_initial_state(b1=self.b)
        self.o = 0
        info: Dict[str, Any] = {}
        return [self.t, self.o, self.b[1]], info
