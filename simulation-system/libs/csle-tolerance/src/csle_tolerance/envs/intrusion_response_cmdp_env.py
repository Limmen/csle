from typing import Tuple, Any, Dict, Union
import gymnasium as gym
import numpy as np
from csle_tolerance.dao.intrusion_response_cmdp_config import IntrusionResponseCmdpConfig
from csle_tolerance.util.general_util import GeneralUtil


class IntrusionResponseCmdpEnv(gym.Env):
    """
    Gym Environment representing the intrusion response CMDP
    """

    def __init__(self, config: IntrusionResponseCmdpConfig):
        """
        Initializes the environment

        :param config: the environment configuration
        """
        self.config = config
        self.action_space = gym.spaces.Discrete(len(self.config.actions))
        self.observation_space = gym.spaces.Box(low=np.int32(min(self.config.states)),
                                                high=np.int32(max(self.config.states)), dtype=np.int32, shape=(1,))
        self.t = 1
        self.s = self.config.initial_state
        self.reset()
        super().__init__()

    def step(self, a: int) -> Tuple[int, float, bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param a: the action
        :return: (obs, reward, terminated, truncated, info)
        """
        done = False
        c = self.config.cost_tensor[self.s]
        self.s = GeneralUtil.sample_next_state(transition_tensor=self.config.transition_tensor,
                                               s=self.s, a=a, states=self.config.states)
        self.t += 1
        info: Dict[str, Any] = {}
        return self.s, c, done, done, info

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[int, Dict[str, Any]]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :param seed: the random seed
        :param soft: boolean flag indicating whether it is a soft reset or not
        :param options: optional configuration parameters
        :return: initial observation and info
        """
        super().reset(seed=seed)
        self.t = 1
        self.s = self.config.initial_state
        info: Dict[str, Any] = {}
        return self.s, info
