import numpy as np
from gym_pycr_pwcrack.dao.agent.agent_log import AgentLog
from gym_pycr_pwcrack.dao.observation.observation_state import ObservationState

class AgentState:

    def __init__(self, obs_state : ObservationState, env_log: AgentLog, episode_reward : int = 0,
                 cumulative_reward : int = 0, time_step : int = 0, num_episodes: int = 0,
                 vuln_lookup : dict = None,
                 service_lookup : dict = None, os_lookup : dict = None):
        self.obs_state = obs_state
        self.env_log = env_log
        self.episode_reward = episode_reward
        self.cumulative_reward = cumulative_reward
        self.time_step = time_step
        self.num_episodes = num_episodes
        self.vuln_lookup = vuln_lookup
        self.vuln_lookup_inv = {v: k for k, v in self.vuln_lookup.items()}
        self.service_lookup = service_lookup
        self.service_lookup_inv = {v: k for k, v in self.service_lookup.items()}
        self.os_lookup = os_lookup
        self.os_lookup_inv = {v: k for k, v in self.os_lookup.items()}
        self.machines_state = None
        self.ports_state = None
        self.initialize_render_state()


    def initialize_render_state(self) -> np.ndarray:
        self.machines_state = np.zeros((self.obs_state.num_machines, 3 + self.obs_state.num_ports + self.obs_state.num_vuln))
        self.ports_state = np.zeros((self.obs_state.num_machines * self.obs_state.num_ports, 4))
        ports_state_idx = 0
        for i in range(self.obs_state.num_machines):
            self.machines_state[i][0] = i + 1
            if len(self.obs_state.machines) > i:
                host_ip = int(self.obs_state.machines[i].ip.rsplit(".", 1)[-1])
                self.machines_state[i][1] = host_ip
                self.machines_state[i][2] = self.os_lookup[self.obs_state.machines[i].os]
                for j, p in enumerate(self.obs_state.machines[i].ports):
                    s_id = self.service_lookup[p.service]
                    self.machines_state[i][j+3] = s_id
                    self.ports_state[ports_state_idx][0] = i
                    self.ports_state[ports_state_idx][1] = p.port
                    self.ports_state[ports_state_idx][2] = s_id
                    self.ports_state[ports_state_idx][3] = p.protocol.value
                    ports_state_idx += 1
