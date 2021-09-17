from typing import Union
import numpy as np
from pycr_common.dao.agent.agent_log import AgentLog
from pycr_common.dao.network.attacker.base_attacker_agent_state import BaseAttackerAgentState
from gym_pycr_ctf.dao.observation.attacker.attacker_observation_state import AttackerObservationState
from gym_pycr_ctf.dao.observation.attacker.attacker_machine_observation_state import AttackerMachineObservationState


class AttackerAgentState(BaseAttackerAgentState):
    """
    DTO with attacker agent's state information for rendering
    """
    def __init__(self, attacker_obs_state : AttackerObservationState, env_log: AgentLog,
                 episode_reward : int = 0,
                 cumulative_reward : int = 0, time_step : int = 0, num_episodes: int = 0,
                 vuln_lookup : dict = None,
                 service_lookup : dict = None, os_lookup : dict = None,
                 num_detections : int = 0, num_all_flags : int = 0):
        """
        Initializes the attacker agent's state

        :param attacker_obs_state: the attacker's observation state
        :param env_log: the log
        :param episode_reward: the reward
        :param cumulative_reward: the cumulative reward
        :param time_step: the time-step
        :param num_episodes: the number of episodes
        :param vuln_lookup: the vuln lookup table
        :param service_lookup: the service lookup table
        :param os_lookup: the os lookup table
        :param num_detections: the number of detections
        :param num_all_flags: the number of flags
        """
        self.attacker_obs_state = attacker_obs_state
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
        self.manual_action = ""

    def get_machine(self, ip: str) -> Union[AttackerMachineObservationState, None]:
        """
        Gets the machine from the state with a given ip

        :param ip: the ip
        :return: the machine if it exists or otherwise None
        """
        for m in self.attacker_obs_state.machines:
            if m.ip == ip:
                return m
        return None

    def initialize_render_state(self) -> None:
        """
        Initializes the render state

        :return: None
        """
        self.machines_state = np.zeros((self.attacker_obs_state.num_machines, 12 + self.attacker_obs_state.num_ports
                                        + self.attacker_obs_state.num_vuln + self.attacker_obs_state.num_sh))
        self.ports_state = np.zeros((self.attacker_obs_state.num_machines * self.attacker_obs_state.num_ports, 4))
        self.vuln_state = np.zeros((self.attacker_obs_state.num_machines * self.attacker_obs_state.num_vuln, 2))
        self.os_state = np.zeros((self.attacker_obs_state.num_machines, 1))
        self.flags_state = set()
        vuln_state_idx = 0
        ports_state_idx = 0
        os_state_idx = 0
        self.attacker_obs_state.sort_machines()
        for i in range(self.attacker_obs_state.num_machines):

            self.machines_state[i][0] = i + 1
            if len(self.attacker_obs_state.machines) > i:
                self.attacker_obs_state.machines[i].sort_ports()
                self.attacker_obs_state.machines[i].sort_cve_vuln(self.vuln_lookup)
                self.attacker_obs_state.machines[i].sort_shell_access(self.service_lookup)

                # IP
                host_ip = int(self.attacker_obs_state.machines[i].ip.rsplit(".", 1)[-1])
                self.machines_state[i][1] = host_ip

                # OS
                os_id = self.os_lookup[self.attacker_obs_state.machines[i].os]
                self.machines_state[i][2] = os_id
                if float(os_id) not in self.os_state[:, 0]:
                    self.os_state[os_state_idx][0] = os_id
                    os_state_idx += 1

                # Ports
                for j, p in enumerate(self.attacker_obs_state.machines[i].ports):
                    s_id = self.service_lookup[p.service]
                    if j < self.attacker_obs_state.num_ports:
                        self.machines_state[i][j+3] = s_id
                        self.ports_state[ports_state_idx][0] = i
                        self.ports_state[ports_state_idx][1] = p.port
                        self.ports_state[ports_state_idx][2] = s_id
                        self.ports_state[ports_state_idx][3] = p.protocol.value
                        ports_state_idx += 1

                # Vulnerabilities
                for j, sh_c in enumerate(self.attacker_obs_state.machines[i].cve_vulns):
                    v_id = self.attacker_obs_state.machines[i]._vuln_lookup(name=sh_c.name, lookup_table=self.vuln_lookup)
                    if j < self.attacker_obs_state.num_vuln:
                        self.machines_state[i][j + 3 + self.attacker_obs_state.num_ports] = v_id
                        if float(v_id) not in self.vuln_state[:,0]:
                            self.vuln_state[vuln_state_idx][0] = v_id
                            self.vuln_state[vuln_state_idx][1] = sh_c.cvss
                            vuln_state_idx += 1


                # Num Open Ports
                self.machines_state[i][3 + self.attacker_obs_state.num_ports + self.attacker_obs_state.num_vuln] = len(self.attacker_obs_state.machines[i].ports)

                # Num CVE Vulnerabilities
                self.machines_state[i][4 + self.attacker_obs_state.num_ports + self.attacker_obs_state.num_vuln] = len(self.attacker_obs_state.machines[i].cve_vulns)

                # Total CVSS score
                total_cvss = sum(list(map(lambda x: x.cvss, self.attacker_obs_state.machines[i].cve_vulns)))
                self.machines_state[i][5 + self.attacker_obs_state.num_ports + self.attacker_obs_state.num_vuln] = total_cvss

                # Shell Access
                self.machines_state[i][6 + self.attacker_obs_state.num_ports + self.attacker_obs_state.num_vuln] = int(self.attacker_obs_state.machines[i].shell_access)

                # Logged in
                self.machines_state[i][7 + self.attacker_obs_state.num_ports + self.attacker_obs_state.num_vuln] = int(self.attacker_obs_state.machines[i].logged_in)

                # Root Access
                self.machines_state[i][8 + self.attacker_obs_state.num_ports + self.attacker_obs_state.num_vuln] = int(
                    self.attacker_obs_state.machines[i].root)

                # Flag pts
                flag_pts_score = sum([f.score for f in self.attacker_obs_state.machines[i].flags_found])
                self.machines_state[i][9 + self.attacker_obs_state.num_ports + self.attacker_obs_state.num_vuln] = int(flag_pts_score)

                # sh_services
                services = []
                for j, sh_c in enumerate(self.attacker_obs_state.machines[i].shell_access_credentials):
                    if sh_c.service is not None:
                        s_id = self.service_lookup[sh_c.service]
                        if j < self.attacker_obs_state.num_sh and s_id not in services:
                            services.append(s_id)
                            self.machines_state[i][j + 10 + self.attacker_obs_state.num_ports + self.attacker_obs_state.num_vuln] = s_id

                # Flags visualize
                self.flags_state = self.flags_state.union(self.attacker_obs_state.machines[i].flags_found)

                # Tools installed
                self.machines_state[i][10 + self.attacker_obs_state.num_ports + self.attacker_obs_state.num_vuln
                                       + self.attacker_obs_state.num_sh] = int(self.attacker_obs_state.machines[i].tools_installed)

                # Backdoor
                self.machines_state[i][11 + self.attacker_obs_state.num_ports + self.attacker_obs_state.num_vuln
                                       + self.attacker_obs_state.num_sh] = int(self.attacker_obs_state.machines[i].backdoor_installed)




