from typing import Tuple
import numpy as np
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_pwcrack.dao.observation.port_observation_state import PortObservationState
from gym_pycr_pwcrack.dao.observation.vulnerability_observation_state import VulnerabilityObservationState
from gym_pycr_pwcrack.dao.action.action_outcome import ActionOutcome
from gym_pycr_pwcrack.envs.logic.common.env_dynamics_util import EnvDynamicsUtil

class SimulatorUtil:
    """
    Class containing utility functions for the simulator
    """

    @staticmethod
    def simulate_port_vuln_scan_helper(s: EnvState, a: Action, env_config: EnvConfig, miss_p: float,
                                       protocol=TransportProtocol.TCP, vuln_scan : bool = False) -> Tuple[EnvState, int]:
        """
        Helper function for simulating port-scan and vuln-scan actions

        :param s: the current environment state
        :param a: the scan action to take
        :param env_config: the current environment configuration
        :param miss_p: the simulated probability that the scan action will not detect a real service or node
        :param protocol: the tranport protocol for the scan
        :param vuln_scan: boolean flag whether the scan is a vulnerability scan or not
        :return: s_prime, reward
        """
        total_new_ports, total_new_os, total_new_vuln, total_new_machines, total_new_shell_access, total_new_root, \
        total_new_flag_pts, total_new_osvb_vuln, total_new_logged_in, total_new_tools_installed, \
        total_new_backdoors_installed = 0,0,0,0,0,0,0,0,0,0,0

        # Scan action on a single host
        if not a.subnet:
            new_m_obs = None
            for node in env_config.network_conf.nodes:
                if node.ip == a.ip:
                    new_m_obs = MachineObservationState(ip=node.ip)
                    for service in node.services:
                        if service.protocol == protocol and \
                                not np.random.rand() < miss_p:
                            port_obs = PortObservationState(port=service.port, open=True, service=service.name,
                                                            protocol=protocol)
                            new_m_obs.ports.append(port_obs)

                    if vuln_scan:
                        for vuln in node.vulnerabilities:
                            if not np.random.rand() < miss_p:
                                vuln_obs = VulnerabilityObservationState(name=vuln.name, port=vuln.port,
                                                                         protocol=vuln.protocol, cvss=vuln.cvss)
                                new_m_obs.cve_vulns.append(vuln_obs)
            new_machines_obs = s.obs_state.machines
            if new_m_obs is not None:
                new_machines_obs = []
                merged = False
                for o_m in s.obs_state.machines:
                    # Machine was already known, merge state
                    if o_m.ip == a.ip:
                        merged_machine_obs, num_new_ports_found, num_new_os_found, num_new_cve_vuln_found, new_shell_access, \
                        new_root, new_flag_pts, num_new_osvdb_vuln_found, num_new_logged_in, num_new_tools_installed, \
                        num_new_backdoors_installed \
                            = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(o_m, new_m_obs)
                        new_machines_obs.append(merged_machine_obs)
                        merged = True
                        total_new_ports += num_new_ports_found
                        total_new_os += num_new_os_found
                        total_new_vuln += num_new_cve_vuln_found
                        total_new_shell_access += new_shell_access
                        total_new_root += new_root
                        total_new_flag_pts += new_flag_pts
                        total_new_osvb_vuln += num_new_osvdb_vuln_found
                        total_new_logged_in += num_new_logged_in
                        total_new_tools_installed += num_new_tools_installed
                        total_new_backdoors_installed += num_new_backdoors_installed
                    else:
                        new_machines_obs.append(o_m)
                # New machine, was not known before
                if not merged:
                    new_machines_obs.append(new_m_obs)
                    total_new_machines +=1
            s_prime = s
            s_prime.obs_state.machines = new_machines_obs
            reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports, num_new_os_found=total_new_os,
                                                   num_new_cve_vuln_found=total_new_vuln,
                                                   num_new_machines=total_new_machines,
                                                   num_new_shell_access=total_new_shell_access,
                                                   num_new_root=total_new_root,
                                                   num_new_flag_pts=total_new_flag_pts,
                                                   num_new_osvdb_vuln_found=total_new_osvb_vuln,
                                                   num_new_logged_in=total_new_logged_in,
                                                   num_new_tools_installed=total_new_tools_installed,
                                                   num_new_backdoors_installed=total_new_backdoors_installed,
                                                   cost=a.cost, env_config=env_config)

        # Scan action on a whole subnet
        else:
            new_m_obs = []
            for node in env_config.network_conf.nodes:
                m_obs = MachineObservationState(ip=node.ip)
                for service in node.services:
                    if service.protocol == protocol and \
                            not np.random.rand() < miss_p:
                        port_obs = PortObservationState(port=service.port, open=True, service=service.name,
                                                        protocol=protocol)
                        m_obs.ports.append(port_obs)

                if vuln_scan:
                    for vuln in node.vulnerabilities:
                        if not np.random.rand() < miss_p:
                            vuln_obs = VulnerabilityObservationState(name=vuln.name, port=vuln.port,
                                                                     protocol=vuln.protocol, cvss=vuln.cvss)
                            m_obs.cve_vulns.append(vuln_obs)

                new_m_obs.append(m_obs)
            new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
            total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
            total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed \
                = EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, new_m_obs, env_config=env_config,
                                                         action=a)
            s_prime = s
            s_prime.obs_state.machines = new_machines_obs
            reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports, num_new_os_found=total_new_os,
                                                   num_new_cve_vuln_found=total_new_vuln,
                                                   num_new_machines = total_new_machines,
                                                   num_new_shell_access=total_new_shell_access,
                                                   num_new_root=total_new_root,
                                                   num_new_flag_pts=total_new_flag_pts,
                                                   num_new_osvdb_vuln_found=total_new_osvdb_vuln_found,
                                                   num_new_logged_in=total_new_logged_in,
                                                   num_new_tools_installed=total_new_tools_installed,
                                                   num_new_backdoors_installed=total_new_backdoors_installed,
                                                   cost=a.cost, env_config=env_config)
        return s_prime, reward

    @staticmethod
    def simulate_host_scan_helper(s: EnvState, a: Action, env_config: EnvConfig, miss_p: float, os=False) -> \
            Tuple[EnvState, int]:
        """
        Helper method for simulating a host-scan (i.e non-port scan) action

        :param s: the current environment state
        :param a: the action to take
        :param env_config: the current environment configuration
        :param miss_p: the simulated probability that the scan action will not detect a real service or node
        :param os: boolean flag whether the host scan should check the operating system too
        :return: s_prime, reward
        """
        total_new_ports, total_new_os, total_new_vuln, total_new_machines, total_new_shell_access, \
        total_new_root, total_new_flag_pts, total_new_osvdb_vuln, total_new_logged_in, \
        total_new_tools_installed, total_new_backdoors_installed = 0,0,0,0,0,0,0,0,0,0,0
        # Scan a a single host
        if not a.subnet:
            new_m_obs = None
            for node in env_config.network_conf.nodes:
                if node.ip == a.ip and not np.random.rand() < miss_p:
                    new_m_obs = MachineObservationState(ip=node.ip)
                    if os:
                        new_m_obs.os = node.os
            new_machines_obs = s.obs_state.machines
            if new_m_obs is not None:
                new_machines_obs = []
                merged = False
                for o_m in s.obs_state.machines:

                    # Existing machine, it was already known
                    if o_m.ip == a.ip:
                        merged_machine_obs, num_new_ports_found, num_new_os_found, num_new_cve_vuln_found, new_shell_access, \
                        new_root, new_flag_pts, num_new_osvdb_vuln, num_new_logged_in, num_new_tools_installed, \
                        num_new_backdoors_installed \
                            = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(o_m, new_m_obs)
                        new_machines_obs.append(merged_machine_obs)
                        merged = True
                        total_new_ports += num_new_ports_found
                        total_new_os += num_new_os_found
                        total_new_vuln += num_new_cve_vuln_found
                        total_new_shell_access += new_shell_access
                        total_new_root += new_root
                        total_new_flag_pts += new_flag_pts
                        total_new_logged_in += num_new_logged_in
                        total_new_osvdb_vuln += num_new_osvdb_vuln
                        total_new_tools_installed += num_new_tools_installed
                        total_new_backdoors_installed += num_new_backdoors_installed
                    else:
                        new_machines_obs.append(o_m)

                # New machine, it was not known before
                if not merged:
                    total_new_machines += 1
                    new_machines_obs.append(new_m_obs)
            s_prime = s
            s_prime.obs_state.machines = new_machines_obs
            reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports, num_new_os_found=total_new_os,
                                                   num_new_cve_vuln_found=total_new_vuln,
                                                   num_new_machines=total_new_machines,
                                                   num_new_shell_access=total_new_shell_access,
                                                   num_new_root=total_new_root,
                                                   num_new_flag_pts=total_new_flag_pts,
                                                   num_new_osvdb_vuln_found=total_new_osvdb_vuln,
                                                   num_new_logged_in=total_new_logged_in,
                                                   num_new_tools_installed=total_new_tools_installed,
                                                   num_new_backdoors_installed=total_new_backdoors_installed,
                                                   cost=a.cost, env_config=env_config)

        # Scan a whole subnetwork
        else:
            new_m_obs = []
            for node in env_config.network_conf.nodes:
                if not np.random.rand() < miss_p:
                    m_obs = MachineObservationState(ip=node.ip)
                    if os:
                        m_obs.os = node.os
                    new_m_obs.append(m_obs)
            new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
            total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
            total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed = \
                EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, new_m_obs, env_config=env_config,
                                                       action=a)
            s_prime = s
            s_prime.obs_state.machines = new_machines_obs

            reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports, num_new_os_found=total_new_os,
                                                   num_new_cve_vuln_found=total_new_vuln,
                                                   num_new_machines=total_new_machines,
                                                   num_new_shell_access=total_new_shell_access,
                                                   num_new_root=total_new_root,
                                                   num_new_flag_pts=total_new_flag_pts,
                                                   num_new_osvdb_vuln_found=total_new_osvdb_vuln_found,
                                                   num_new_logged_in=total_new_logged_in,
                                                   num_new_tools_installed=total_new_tools_installed,
                                                   num_new_backdoors_installed=total_new_backdoors_installed,
                                                   cost=a.cost, env_config=env_config)
        return s_prime, reward

    @staticmethod
    def simulate_dictionary_pw_exploit_same_user(s: EnvState, a: Action, env_config: EnvConfig, miss_p: float,
                                                 vuln_name : str) -> Tuple[EnvState, int]:
        """
        Helper function for simulating dictionary scans against some service and with the constraint that
        only username-password combinations where username==password are tried.

        :param s: the current environment state
        :param a: the scan action to take
        :param env_config: the current environment configuration
        :param miss_p: the simulated probability that the scan action will not detect a real service or node
        :param vuln_name: name of the vulnerability
        :return: s_prime, reward
        """
        total_new_ports, total_new_os, total_new_vuln, total_new_machines, total_new_shell_access, \
        total_new_root, total_new_flag_pts, total_new_osvdb_vuln, total_new_logged_in, \
        total_new_tools_installed, total_new_backdoors_installed = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        # Exploit on a single host
        if not a.subnet:
            new_m_obs = None
            for node in env_config.network_conf.nodes:
                if node.ip == a.ip:
                    new_m_obs = MachineObservationState(ip=node.ip)
                    vuln_match = False
                    vuln_service = None
                    for vuln in node.vulnerabilities:
                        if vuln.name == vuln_name and not np.random.rand() < miss_p:
                            vuln_obs = VulnerabilityObservationState(name=vuln.name, port=vuln.port,
                                                                     protocol=vuln.protocol, cvss=vuln.cvss)
                            new_m_obs.cve_vulns.append(vuln_obs)
                            if a.action_outcome == ActionOutcome.SHELL_ACCESS:
                                new_m_obs.shell_access = True
                                new_m_obs.untried_credentials = True
                                new_m_obs.shell_access_credentials = vuln.credentials
                            vuln_match = True
                            vuln_service = vuln.service

                    if vuln_match:
                        for service in node.services:
                            if service.name == vuln_service:
                                port_obs = PortObservationState(port=service.port, open=True, service=service.name,
                                                                protocol=service.protocol)
                                new_m_obs.ports.append(port_obs)
                    new_m_obs = EnvDynamicsUtil.brute_tried_flags(a=a, m_obs=new_m_obs)
            new_machines_obs = s.obs_state.machines
            if new_m_obs is not None:
                new_machines_obs = []
                merged = False
                for o_m in s.obs_state.machines:
                    # Machine was already known, merge state
                    if o_m.ip == a.ip:
                        merged_machine_obs, num_new_ports_found, num_new_os_found, num_new_cve_vuln_found, new_shell_access, \
                        new_root, new_flag_pts, num_new_osvdb_vuln, num_new_logged_in, num_new_tools_installed, \
                        num_new_backdoors_installed = \
                            EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(o_m, new_m_obs, action=a)
                        new_machines_obs.append(merged_machine_obs)
                        merged = True
                        total_new_vuln += num_new_cve_vuln_found
                        total_new_shell_access += new_shell_access
                        total_new_ports += num_new_ports_found
                        total_new_os += num_new_os_found
                        total_new_root += new_root
                        total_new_flag_pts += new_flag_pts
                        total_new_osvdb_vuln += num_new_osvdb_vuln
                        total_new_logged_in += num_new_logged_in
                        total_new_tools_installed += num_new_tools_installed
                        total_new_backdoors_installed += num_new_backdoors_installed
                    else:
                        new_machines_obs.append(o_m)
                # New machine, was not known before
                if not merged:
                    total_new_machines += 1
                    new_machines_obs.append(new_m_obs)
            s_prime = s
            s_prime.obs_state.machines = new_machines_obs
            reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports,
                                                   num_new_os_found=total_new_os,
                                                   num_new_cve_vuln_found=total_new_vuln,
                                                   num_new_machines=total_new_machines,
                                                   num_new_shell_access=total_new_shell_access,
                                                   num_new_root=total_new_root,
                                                   num_new_flag_pts=total_new_flag_pts,
                                                   num_new_osvdb_vuln_found=total_new_osvdb_vuln,
                                                   num_new_logged_in=total_new_logged_in,
                                                   num_new_tools_installed=total_new_tools_installed,
                                                   num_new_backdoors_installed=total_new_backdoors_installed,
                                                   cost=a.cost, env_config=env_config)

        # Scan action on a whole subnet
        else:
            new_m_obs = []
            for node in env_config.network_conf.nodes:
                m_obs = MachineObservationState(ip=node.ip)
                vulnerable_services = []
                for vuln in node.vulnerabilities:
                    if vuln.name == vuln_name and not np.random.rand() < miss_p:
                        vuln_obs = VulnerabilityObservationState(name=vuln.name, port=vuln.port,
                                                                 protocol=vuln.protocol, cvss=vuln.cvss)
                        if a.action_outcome == ActionOutcome.SHELL_ACCESS:
                            m_obs.shell_access = True
                            m_obs.untried_credentials = True
                            m_obs.shell_access_credentials = vuln.credentials
                        m_obs.cve_vulns.append(vuln_obs)
                        vulnerable_services.append(vuln.name)

                for service in node.services:
                    match = False
                    for vuln_service in vulnerable_services:
                        if service.name == vuln_service:
                            match = True
                    if match:
                        port_obs = PortObservationState(port=service.port, open=True, service=service.name,
                                                        protocol=service.protocol)
                        m_obs.ports.append(port_obs)
                m_obs = EnvDynamicsUtil.brute_tried_flags(a=a, m_obs=m_obs)
                new_m_obs.append(m_obs)

            new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
            total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
            total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed = \
                EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, new_m_obs, env_config=env_config,
                                                       action=a)
            s_prime = s
            s_prime.obs_state.machines = new_machines_obs
            reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports, num_new_os_found=total_new_os,
                                                   num_new_cve_vuln_found=total_new_vuln,
                                                   num_new_machines=total_new_machines,
                                                   num_new_shell_access=total_new_shell_access,
                                                   num_new_root=total_new_root,
                                                   num_new_flag_pts=total_new_flag_pts,
                                                   num_new_osvdb_vuln_found=total_new_osvdb_vuln_found,
                                                   num_new_logged_in=total_new_logged_in,
                                                   num_new_tools_installed=total_new_tools_installed,
                                                   num_new_backdoors_installed=total_new_backdoors_installed,
                                                   cost=a.cost, env_config=env_config)

        return s_prime, reward


    @staticmethod
    def simulate_service_login_helper(s: EnvState, a: Action, env_config: EnvConfig, service_name : str = "ssh") \
            -> Tuple[EnvState, int]:
        """
        Helper function for simulating login to various network services

        :param s: the current state
        :param a: the action to take
        :param env_config: the env config
        :param service_name: the name of the service to login to
        :return: s_prime, reward
        """
        total_new_ports, total_new_os, total_new_vuln, total_new_machines, total_new_shell_access, \
        total_new_root, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, total_new_logged_in, \
        total_new_tools_installed, total_new_backdoors_installed = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        new_obs_machines = []
        for node in env_config.network_conf.nodes:
            new_m_obs = MachineObservationState(ip=node.ip)
            credentials = None
            access = False
            for o_m in s.obs_state.machines:
                if o_m.ip == node.ip:
                    access = o_m.shell_access
                    credentials = o_m.shell_access_credentials
            if access:
                for service in node.services:
                    if service.name == service_name:
                        for cr in service.credentials:
                            for a_cr in credentials:
                                if a_cr.username == cr.username and a_cr.pw == cr.pw:
                                    new_m_obs.logged_in = True

                if new_m_obs.logged_in:
                    for cr in credentials:
                        cr_user = cr.username
                        if cr_user in node.root:
                            new_m_obs.root = True
            new_m_obs.untried_credentials = False
            new_obs_machines.append(new_m_obs)

        new_obs_machines, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
        total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
        total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed = \
            EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, new_obs_machines, env_config=env_config,
                                                   action=a)
        s_prime = s
        s_prime.obs_state.machines = new_obs_machines
        reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports,
                                               num_new_os_found=total_new_os,
                                               num_new_cve_vuln_found=total_new_vuln,
                                               num_new_machines=total_new_machines,
                                               num_new_shell_access=total_new_shell_access,
                                               num_new_root=total_new_root,
                                               num_new_flag_pts=total_new_flag_pts,
                                               num_new_osvdb_vuln_found = total_new_osvdb_vuln_found,
                                               num_new_logged_in=total_new_logged_in,
                                               num_new_tools_installed=total_new_tools_installed,
                                               num_new_backdoors_installed=total_new_backdoors_installed,
                                               cost=a.cost, env_config=env_config)
        return s_prime, reward


    @staticmethod
    def simulate_detection(a: Action, env_config: EnvConfig) -> Tuple[bool, int]:
        """
        Simulates probability that an attack is detected by a defender

        :param a: the action
        :param env_config: the environment config
        :return: boolean, true if detected otherwise false, reward
        """
        if env_config.simulate_detection:
            detected = np.random.rand() < (a.noise + env_config.base_detection_p)
            r = env_config.detection_reward
            if not detected:
                r = 0
            return detected, r
        else:
            return False, 0
