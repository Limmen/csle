from typing import Tuple
import numpy as np
import gym
from gym_pycr_pwcrack.dao.observation.observation_state import ObservationState

class StateRepresentation:
    """
    Utility class for configuring state and observation representations for the pycr-pwcrack env
    """

    @staticmethod
    def base_representation_spaces(obs_state: ObservationState)-> Tuple:
        """
        Configures observation spaces for the base representation

        :param obs_state: the observation state
        :return: m_selection_obs_space (for AR), network_orig_shape, machine_orig_shape, m_action_obs_space (for AR)
        """
        num_m_features = 17 + obs_state.num_ports + obs_state.num_vuln + obs_state.num_sh
        observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(
            obs_state.num_machines * num_m_features,))
        m_selection_observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(
            obs_state.num_machines * num_m_features,))
        network_orig_shape = (obs_state.num_machines, num_m_features)
        machine_orig_shape = (num_m_features,)
        m_action_observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(num_m_features,))
        return observation_space, m_selection_observation_space, \
               network_orig_shape, machine_orig_shape, m_action_observation_space

    @staticmethod
    def base_representation(num_machines : int, num_ports : int, obs_state :ObservationState,
                            vuln_lookup: dict, service_lookup: dict, os_lookup: dict) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        Base observation representation, includes all available information. E.g. for each machine: ports, ip, os,
        vulnerabilities, services, cvss, shell, root, flags, etc.

        :param num_machines: max number of machines in the obs
        :param num_ports: num ports
        :param obs_state: current observation state to turn into a numeratical representation
        :param vuln_lookup: lookup dict for converting categorical vuln into numerical
        :param service_lookup: lookup dict for converting categorical service into numerical
        :param os_lookup: lookup dict for converting categorical os into numerical
        :return: Machines obs, ports obs, obs_space, m_selection_obs_space (for AR), network_orig_shape,
                 machine_orig_shape, m_action_obs_space (for AR)
        """
        obs_state.sort_machines()
        num_m_features = 17 + obs_state.num_ports + obs_state.num_vuln + obs_state.num_sh
        machines_obs = np.zeros((num_machines, num_m_features))
        ports_protocols_obs = np.zeros((num_machines, num_ports))
        for i in range(num_machines):

            if len(obs_state.machines) > i:
                machines_obs[i][0] = i + 1
                obs_state.machines[i].sort_ports()
                obs_state.machines[i].sort_cve_vuln(vuln_lookup)
                obs_state.machines[i].sort_shell_access(service_lookup)

                # IP
                host_ip = int(obs_state.machines[i].ip.rsplit(".", 1)[-1])
                machines_obs[i][1] = host_ip

                # OS
                os_id = os_lookup[obs_state.machines[i].os]
                machines_obs[i][2] = os_id

                # Ports
                for j, p in enumerate(obs_state.machines[i].ports):
                    s_id = service_lookup[p.service]
                    if j < obs_state.num_ports:
                        machines_obs[i][j + 3] = s_id
                        ports_protocols_obs[i][j] = p.protocol.value

                # Vulnerabilities
                for j, v in enumerate(obs_state.machines[i].cve_vulns):
                    v_id = vuln_lookup[v.name]
                    if j < obs_state.num_vuln:
                        machines_obs[i][j + 3 + obs_state.num_ports] = v_id

                # Num Open Ports
                machines_obs[i][3 + obs_state.num_ports + obs_state.num_vuln] = len(obs_state.machines[i].ports)

                # Num Vulnerabilities
                machines_obs[i][4 + obs_state.num_ports + obs_state.num_vuln] = len(obs_state.machines[i].cve_vulns)

                # Total CVSS score
                total_cvss = sum(list(map(lambda x: x.cvss, obs_state.machines[i].cve_vulns)))
                machines_obs[i][5 + obs_state.num_ports + obs_state.num_vuln] = total_cvss

                # Shell Access
                machines_obs[i][6 + obs_state.num_ports + obs_state.num_vuln] = int(obs_state.machines[i].shell_access)

                # Logged in
                machines_obs[i][7 + obs_state.num_ports + obs_state.num_vuln] = int(obs_state.machines[i].logged_in)

                # Root access
                machines_obs[i][8 + obs_state.num_ports + obs_state.num_vuln] = int(obs_state.machines[i].root)

                # Flag pts
                flag_pts_score = sum([f.score for f in obs_state.machines[i].flags_found])
                machines_obs[i][9 + obs_state.num_ports + obs_state.num_vuln] = int(flag_pts_score)

                # sh_services
                services = []
                for j, sh_c in enumerate(obs_state.machines[i].shell_access_credentials):
                    if sh_c.service is not None:
                        s_id = service_lookup[sh_c.service]
                        if j < obs_state.num_sh and s_id not in services:
                            services.append(s_id)
                            machines_obs[i][j + 10 + obs_state.num_ports + obs_state.num_vuln] = s_id

                # Filesystem searched
                machines_obs[i][10 + obs_state.num_ports + obs_state.num_vuln + obs_state.num_sh] = int(obs_state.machines[i].filesystem_searched)

                # Untried credentials
                machines_obs[i][11 + obs_state.num_ports + obs_state.num_vuln + obs_state.num_sh] = int(obs_state.machines[i].untried_credentials)

                # SSH brute tried
                machines_obs[i][12 + obs_state.num_ports + obs_state.num_vuln + obs_state.num_sh] = int(obs_state.machines[i].ssh_brute_tried)

                # Telnet brute tried
                machines_obs[i][13 + obs_state.num_ports + obs_state.num_vuln + obs_state.num_sh] = int(obs_state.machines[i].telnet_brute_tried)

                # FTP brute tried
                machines_obs[i][14 + obs_state.num_ports + obs_state.num_vuln + obs_state.num_sh] = int(obs_state.machines[i].ftp_brute_tried)

                # Backdoor installed
                machines_obs[i][15 + obs_state.num_ports + obs_state.num_vuln + obs_state.num_sh] = int(obs_state.machines[i].backdoor_installed)

                # Tools installed
                machines_obs[i][16 + obs_state.num_ports + obs_state.num_vuln + obs_state.num_sh] = int(
                    obs_state.machines[i].tools_installed)

        return machines_obs, ports_protocols_obs

    @staticmethod
    def compact_representation_spaces(obs_state: ObservationState) -> Tuple:
        """
        Configures observation spaces for the compact representation

        :param obs_state: the observation state
        :return: m_selection_obs_space (for AR), network_orig_shape, machine_orig_shape, m_action_obs_space (for AR)
        """
        num_m_features = 3
        observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(
            obs_state.num_machines * num_m_features,))
        m_selection_observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(
            obs_state.num_machines * num_m_features,))
        network_orig_shape = (obs_state.num_machines, num_m_features)
        machine_orig_shape = (num_m_features,)
        m_action_observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(num_m_features,))
        return observation_space, m_selection_observation_space, \
               network_orig_shape, machine_orig_shape, m_action_observation_space

    @staticmethod
    def compact_representation(num_machines: int, num_ports: int, obs_state: ObservationState) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        Compact observation representation, includes only aggregate features, e.g. total num open ports rather than
        a list of all ports

        :param num_machines: max number of machines in the obs
        :param num_ports: num ports
        :param obs_state: current observation state to turn into a numeratical representation
        :return: Machines obs, ports obs, obs_space, m_selection_obs_space (for AR), network_orig_shape,
                 machine_orig_shape, m_action_obs_space (for AR)
        """
        obs_state.sort_machines()
        num_m_features = 3
        machines_obs = np.zeros((num_machines, num_m_features))
        ports_protocols_obs = np.zeros((num_machines, num_ports))
        for i in range(num_machines):
            if len(obs_state.machines) > i:
                machines_obs[i][0] = 1 # machine found

                # Shell Access
                machines_obs[i][1] = int(obs_state.machines[i].shell_access)

                # Logged in
                machines_obs[i][2] = int(obs_state.machines[i].logged_in)

                # # Filesystem searched
                # machines_obs[i][3] = int(obs_state.machines[i].filesystem_searched)
                #
                # # Untried credentials
                # machines_obs[i][4] = int(obs_state.machines[i].untried_credentials)
                #
                # # SSH brute tried
                # machines_obs[i][5] = int(obs_state.machines[i].ssh_brute_tried)
                #
                # # Telnet brute tried
                # machines_obs[i][6] = int(obs_state.machines[i].telnet_brute_tried)
                #
                # # FTP brute tried
                # machines_obs[i][7] = int(obs_state.machines[i].ftp_brute_tried)

        return machines_obs, ports_protocols_obs

    @staticmethod
    def essential_representation_spaces(obs_state: ObservationState) -> Tuple:
        """
        Configures observation spaces for the essential representation

        :param obs_state: the observation state
        :return: m_selection_obs_space (for AR), network_orig_shape, machine_orig_shape, m_action_obs_space (for AR)
        """
        num_m_features = 12
        observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(
            obs_state.num_machines * num_m_features,))
        m_selection_observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(
            obs_state.num_machines * num_m_features,))
        network_orig_shape = (obs_state.num_machines, num_m_features)
        machine_orig_shape = (num_m_features,)
        m_action_observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(num_m_features,))
        return observation_space, m_selection_observation_space, \
               network_orig_shape, machine_orig_shape, m_action_observation_space

    @staticmethod
    def essential_representation(num_machines: int, num_ports: int, obs_state: ObservationState) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        Essential observation representation

        :param num_machines: max number of machines in the obs
        :param num_ports: num ports
        :param obs_state: current observation state to turn into a numeratical representation
        :return: Machines obs, ports obs, obs_space, m_selection_obs_space (for AR), network_orig_shape,
                 machine_orig_shape, m_action_obs_space (for AR)
        """
        obs_state.sort_machines()
        num_m_features = 12
        machines_obs = np.zeros((num_machines, num_m_features))
        ports_protocols_obs = np.zeros((num_machines, num_ports))
        for i in range(num_machines):
            if len(obs_state.machines) > i:
                machines_obs[i][0] = 1  # machine found

                # Shell Access
                machines_obs[i][1] = int(obs_state.machines[i].shell_access)

                # Logged in
                machines_obs[i][2] = int(obs_state.machines[i].logged_in)

                # Num Open Ports
                machines_obs[i][3] = len(obs_state.machines[i].ports)

                # Flag pts
                flag_pts_score = sum([f.score for f in obs_state.machines[i].flags_found])
                machines_obs[i][4] = int(flag_pts_score)

                # Filesystem searched
                machines_obs[i][5] = int(
                    obs_state.machines[i].filesystem_searched)

                # Untried credentials
                machines_obs[i][7] = int(obs_state.machines[i].untried_credentials)

                # SSH brute tried
                machines_obs[i][7] = int(
                    obs_state.machines[i].ssh_brute_tried)

                # Telnet brute tried
                machines_obs[i][8] = int(
                    obs_state.machines[i].telnet_brute_tried)

                # FTP brute tried
                machines_obs[i][9] = int(
                    obs_state.machines[i].ftp_brute_tried)

                # Backdoor installed
                machines_obs[i][10] = int(
                    obs_state.machines[i].backdoor_installed)

                # Tools installed
                machines_obs[i][11] = int(obs_state.machines[i].tools_installed)

        return machines_obs, ports_protocols_obs

    @staticmethod
    def simple_representation_spaces(obs_state: ObservationState) -> Tuple:
        """
        Configures observation spaces for the level_1 representation

        :param obs_state: the observation state
        :return: m_selection_obs_space (for AR), network_orig_shape, machine_orig_shape, m_action_obs_space (for AR)
        """
        total_features = 7
        observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(total_features,))
        m_selection_observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(total_features,))
        network_orig_shape = (total_features)
        machine_orig_shape = (total_features)
        m_action_observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(total_features,))
        return observation_space, m_selection_observation_space, \
               network_orig_shape, machine_orig_shape, m_action_observation_space

    @staticmethod
    def simple_representation(num_machines: int, num_ports: int, obs_state: ObservationState) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        Compact observation representation, includes only aggregate features, e.g. total num open ports rather than
        a list of all ports

        :param num_machines: max number of machines in the obs
        :param num_ports: num ports
        :param obs_state: current observation state to turn into a numeratical representation
        :return: Machines obs, ports obs, obs_space, m_selection_obs_space (for AR), network_orig_shape,
                 machine_orig_shape, m_action_obs_space (for AR)
        """
        obs_state.sort_machines()
        total_features = 7
        machines_obs = np.zeros((total_features,))
        untried_credentials = 0
        untried_tools = 0
        untried_backdoor = 0
        untried_fs = 0
        untried_ssh_brute = 0
        untried_ftp_brute = 0
        untried_telnet_brute = 0
        for i in range(num_machines):
            if len(obs_state.machines) > i:
                if obs_state.machines[i].logged_in:
                    if not int(obs_state.machines[i].filesystem_searched):
                        untried_fs = 1
                    if obs_state.machines[i].root:
                        if not obs_state.machines[i].tools_installed and not obs_state.machines[i].install_tools_tried:
                            untried_tools = 1

                    if obs_state.machines[i].tools_installed and not obs_state.machines[i].backdoor_installed and not obs_state.machines[i].backdoor_tried:
                        untried_backdoor = 1
                if obs_state.machines[i].untried_credentials:
                    untried_credentials = 1

                if not obs_state.machines[i].ssh_brute_tried:
                    untried_ssh_brute = 1
                if not obs_state.machines[i].ftp_brute_tried:
                    untried_ftp_brute = 1
                if not obs_state.machines[i].telnet_brute_tried:
                    untried_telnet_brute = 1
            else:
                untried_ftp_brute = 1
                untried_ssh_brute = 1
                untried_telnet_brute = 1

        machines_obs[0] = untried_credentials
        machines_obs[1] = untried_tools
        machines_obs[2] = untried_backdoor
        machines_obs[3] = untried_fs
        machines_obs[4] = untried_ssh_brute
        machines_obs[5] = untried_telnet_brute
        machines_obs[6] = untried_ftp_brute
        return machines_obs, machines_obs
