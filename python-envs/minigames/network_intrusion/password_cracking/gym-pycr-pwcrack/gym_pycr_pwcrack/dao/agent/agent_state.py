import numpy as np
from gym_pycr_pwcrack.dao.agent.agent_log import AgentLog
from gym_pycr_pwcrack.dao.observation.observation_state import ObservationState

class AgentState:

    def __init__(self, obs_state : ObservationState, env_log: AgentLog,
                 episode_reward : int = 0,
                 cumulative_reward : int = 0, time_step : int = 0, num_episodes: int = 0,
                 vuln_lookup : dict = None,
                 service_lookup : dict = None, os_lookup : dict = None,
                 num_detections : int = 0, num_all_flags : int = 0):
        self.obs_state = obs_state
        self.env_log = env_log
        self.episode_reward = episode_reward
        self.cumulative_reward = cumulative_reward
        self.time_step = time_step
        self.num_episodes = num_episodes
        self.num_detections = num_detections
        self.num_all_flags = num_all_flags
        self.vuln_lookup = vuln_lookup
        self.vuln_lookup_inv = {v: k for k, v in self.vuln_lookup.items()}
        self.service_lookup = service_lookup
        self.service_lookup_inv = {v: k for k, v in self.service_lookup.items()}
        self.os_lookup = os_lookup
        self.os_lookup_inv = {v: k for k, v in self.os_lookup.items()}
        self.machines_state = None
        self.ports_state = None
        self.vuln_state = None
        self.os_state = None
        self.flags_state = None
        self.initialize_render_state()


    def initialize_render_state(self) -> np.ndarray:
        self.machines_state = np.zeros((self.obs_state.num_machines, 10 + self.obs_state.num_ports
                                        + self.obs_state.num_vuln + self.obs_state.num_sh))
        self.ports_state = np.zeros((self.obs_state.num_machines * self.obs_state.num_ports, 4))
        self.vuln_state = np.zeros((self.obs_state.num_machines * self.obs_state.num_vuln, 2))
        self.os_state = np.zeros((self.obs_state.num_machines, 1))
        self.flags_state = set()
        vuln_state_idx = 0
        ports_state_idx = 0
        os_state_idx = 0
        self.obs_state.sort_machines()
        for i in range(self.obs_state.num_machines):

            self.machines_state[i][0] = i + 1
            if len(self.obs_state.machines) > i:
                self.obs_state.machines[i].sort_ports()
                self.obs_state.machines[i].sort_vuln(self.vuln_lookup)
                self.obs_state.machines[i].sort_shell_access(self.service_lookup)

                # IP
                host_ip = int(self.obs_state.machines[i].ip.rsplit(".", 1)[-1])
                self.machines_state[i][1] = host_ip

                # OS
                os_id = self.os_lookup[self.obs_state.machines[i].os]
                self.machines_state[i][2] = os_id
                if float(os_id) not in self.os_state[:, 0]:
                    self.os_state[os_state_idx][0] = os_id
                    os_state_idx += 1

                # Ports
                for j, p in enumerate(self.obs_state.machines[i].ports):
                    s_id = self.service_lookup[p.service]
                    if j < self.obs_state.num_ports:
                        self.machines_state[i][j+3] = s_id
                        self.ports_state[ports_state_idx][0] = i
                        self.ports_state[ports_state_idx][1] = p.port
                        self.ports_state[ports_state_idx][2] = s_id
                        self.ports_state[ports_state_idx][3] = p.protocol.value
                        ports_state_idx += 1

                # Vulnerabilities
                for j, sh_c in enumerate(self.obs_state.machines[i].vuln):
                    v_id = self.vuln_lookup[sh_c.name]
                    if j < self.obs_state.num_vuln:
                        self.machines_state[i][j + 3 + self.obs_state.num_ports] = v_id
                        if float(v_id) not in self.vuln_state[:,0]:
                            self.vuln_state[vuln_state_idx][0] = v_id
                            self.vuln_state[vuln_state_idx][1] = sh_c.cvss
                            vuln_state_idx += 1


                # Num Open Ports
                self.machines_state[i][3 + self.obs_state.num_ports + self.obs_state.num_vuln] = len(self.obs_state.machines[i].ports)

                # Num Vulnerabilities
                self.machines_state[i][4 + self.obs_state.num_ports + self.obs_state.num_vuln] = len(self.obs_state.machines[i].vuln)

                # Total CVSS score
                total_cvss = sum(list(map(lambda x: x.cvss, self.obs_state.machines[i].vuln)))
                self.machines_state[i][5 + self.obs_state.num_ports + self.obs_state.num_vuln] = total_cvss

                # Shell Access
                self.machines_state[i][6 + self.obs_state.num_ports + self.obs_state.num_vuln] = int(self.obs_state.machines[i].shell_access)

                # Logged in
                self.machines_state[i][7 + self.obs_state.num_ports + self.obs_state.num_vuln] = int(self.obs_state.machines[i].logged_in)

                # Root Access
                self.machines_state[i][8 + self.obs_state.num_ports + self.obs_state.num_vuln] = int(
                    self.obs_state.machines[i].root)

                # Flag pts
                flag_pts_score = sum([f.score for f in self.obs_state.machines[i].flags_found])
                self.machines_state[i][9 + self.obs_state.num_ports + self.obs_state.num_vuln] = int(flag_pts_score)

                # sh_services
                services = []
                for j, sh_c in enumerate(self.obs_state.machines[i].shell_access_credentials):
                    if sh_c.service is not None:
                        s_id = self.service_lookup[sh_c.service]
                        if j < self.obs_state.num_sh and s_id not in services:
                            services.append(s_id)
                            self.machines_state[i][j + 10 + self.obs_state.num_ports + self.obs_state.num_vuln] = s_id

                # Flags visualize
                self.flags_state = self.flags_state.union(self.obs_state.machines[i].flags_found)




