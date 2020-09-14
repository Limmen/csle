import gym
import numpy as np
from gym_pycr_pwcrack.dao.network_config import NetworkConfig

class EnvState:

    def __init__(self, network_config : NetworkConfig):
        self.network_config = network_config
        self.observation_space = gym.spaces.Box(low=0, high=10, dtype=np.int32, shape=(10, 10,))
        self.reward_range = (float(0), float(1))

    def get_observation(self):
        pass

    def reset_state(self):
        pass