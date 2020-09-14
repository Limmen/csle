import numpy as np
from gym_pycr_pwcrack.dao.agent_log import AgentLog

class AgentState:

    def __init__(self, num_servers :int, num_ports:int, num_vuln:int, env_log: AgentLog, episode_reward : int = 0,
                 cumulative_reward : int = 0, time_step : int = 0, num_episodes: int = 0, vuln_lookup : dict = None,
                 service_lookup : dict = None, os_lookup : dict = None):
        self.env_log = env_log
        self.num_servers = num_servers
        self.num_ports = num_ports
        self.num_vuln = num_vuln
        self.episode_reward = episode_reward
        self.cumulative_reward = cumulative_reward
        self.time_step = time_step
        self.num_episodes = num_episodes
        self.vuln_lookup = vuln_lookup
        self.service_lookup = service_lookup
        self.os_lookup = os_lookup
        self.machines_state = None
        self.ports_state = None
        self.initialize_render_state()


    def initialize_render_state(self) -> np.ndarray:
        self.machines_state = np.zeros((self.num_servers, 3 + self.num_ports + self.num_vuln))
        self.ports_state = np.zeros((self.num_servers * self.num_ports, 3))
        for i in range(self.machines_state.shape[0]):
            self.machines_state[i][0] = i + 1
