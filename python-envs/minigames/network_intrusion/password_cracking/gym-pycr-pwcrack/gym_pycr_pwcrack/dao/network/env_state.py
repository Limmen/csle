import gym
import numpy as np
from gym_pycr_pwcrack.dao.network.network_config import NetworkConfig
from gym_pycr_pwcrack.dao.observation.observation_state import ObservationState

class EnvState:

    def __init__(self, network_config : NetworkConfig, num_ports : int, num_vuln : int):
        self.network_config = network_config
        self.observation_space = gym.spaces.Box(low=0, high=10, dtype=np.int32, shape=(10, 10,))
        self.reward_range = (float(0), float(1))
        self.num_ports = num_ports
        self.num_vuln = num_vuln
        self.reset_state()

    def get_observation(self):
        pass

    def reset_state(self):
        self.obs_state = ObservationState(num_machines=len(self.network_config.nodes), num_ports=self.num_ports,
                                          num_vuln=self.num_vuln)