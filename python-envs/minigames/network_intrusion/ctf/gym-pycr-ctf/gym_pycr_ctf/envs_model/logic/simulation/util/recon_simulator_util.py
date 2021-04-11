from typing import Tuple
import numpy as np
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.dao.network.transport_protocol import TransportProtocol
from gym_pycr_ctf.dao.observation.attacker.attacker_machine_observation_state import AttackerMachineObservationState
from gym_pycr_ctf.dao.observation.common.port_observation_state import PortObservationState
from gym_pycr_ctf.dao.observation.common.vulnerability_observation_state import VulnerabilityObservationState
from gym_pycr_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
from gym_pycr_ctf.envs_model.logic.simulation.util.simulator_util import SimulatorUtil

class ReconSimulatorUtil:
    """
    Class containing utility functions for simulating Recon actions
    """

    @staticmethod
    def simulate_port_vuln_scan_helper(s: EnvState, a: AttackerAction, env_config: EnvConfig, miss_p: float,
                                       protocol=TransportProtocol.TCP, vuln_scan : bool = False) \
            -> Tuple[EnvState, int]:
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
        reachable_nodes = SimulatorUtil.reachable_nodes(state=s, env_config=env_config)

        # Scan action on a single host
        if not a.subnet:
            new_m_obs = None
            for node in env_config.network_conf.nodes:
                if node.ip == a.ip and node.ip in reachable_nodes:
                    new_m_obs = AttackerMachineObservationState(ip=node.ip)
                    new_m_obs.reachable = node.reachable_nodes
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
            new_machines_obs = s.attacker_obs_state.machines
            if new_m_obs is not None:
                new_machines_obs = []
                merged = False
                for o_m in s.attacker_obs_state.machines:
                    # Machine was already known, merge state
                    if o_m.ip == a.ip:
                        merged_machine_obs, num_new_ports_found, num_new_os_found, num_new_cve_vuln_found, new_shell_access, \
                        new_root, new_flag_pts, num_new_osvdb_vuln_found, num_new_logged_in, num_new_tools_installed, \
                        num_new_backdoors_installed \
                            = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(o_m, new_m_obs, action=a)
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
            s_prime.attacker_obs_state.machines = new_machines_obs
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
                                                   cost=a.cost, env_config=env_config,
                                                   alerts=a.alerts, action=a)

        # Scan action on a whole subnet
        else:
            new_m_obs = []
            for node in env_config.network_conf.nodes:
                if not node.ip in reachable_nodes:
                    continue
                m_obs = AttackerMachineObservationState(ip=node.ip)
                m_obs.reachable = node.reachable_nodes
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
                = EnvDynamicsUtil.merge_new_obs_with_old(s.attacker_obs_state.machines, new_m_obs, env_config=env_config,
                                                         action=a)
            s_prime = s
            s_prime.attacker_obs_state.machines = new_machines_obs
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
                                                   cost=a.cost, env_config=env_config, alerts=a.alerts,
                                                   action=a)
        return s_prime, reward

    @staticmethod
    def simulate_host_scan_helper(s: EnvState, a: AttackerAction, env_config: EnvConfig, miss_p: float, os=False) -> \
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
        reachable_nodes = SimulatorUtil.reachable_nodes(state=s, env_config=env_config)
        # Scan a a single host
        if not a.subnet:
            new_m_obs = None

            for node in env_config.network_conf.nodes:
                if node.ip == a.ip and node.ip in reachable_nodes and not np.random.rand() < miss_p:
                    new_m_obs = AttackerMachineObservationState(ip=node.ip)
                    new_m_obs.reachable = node.reachable_nodes
                    if os:
                        new_m_obs.os = node.os

            new_machines_obs = s.attacker_obs_state.machines
            if new_m_obs is not None:
                new_machines_obs = []
                merged = False
                for o_m in s.attacker_obs_state.machines:

                    # Existing machine, it was already known
                    if o_m.ip == a.ip:
                        merged_machine_obs, num_new_ports_found, num_new_os_found, num_new_cve_vuln_found, new_shell_access, \
                        new_root, new_flag_pts, num_new_osvdb_vuln, num_new_logged_in, num_new_tools_installed, \
                        num_new_backdoors_installed \
                            = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(o_m, new_m_obs, action=a)
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
            s_prime.attacker_obs_state.machines = new_machines_obs
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
                                                   cost=a.cost, env_config=env_config, alerts=a.alerts,
                                                   action=a)

        # Scan a whole subnetwork
        else:
            new_m_obs = []
            for node in env_config.network_conf.nodes:
                if node.ip in reachable_nodes and not np.random.rand() < miss_p:
                    m_obs = AttackerMachineObservationState(ip=node.ip)
                    m_obs.reachable = node.reachable_nodes
                    if os:
                        m_obs.os = node.os
                    new_m_obs.append(m_obs)
            new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
            total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
            total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed = \
                EnvDynamicsUtil.merge_new_obs_with_old(s.attacker_obs_state.machines, new_m_obs, env_config=env_config,
                                                       action=a)
            s_prime = s
            s_prime.attacker_obs_state.machines = new_machines_obs

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
                                                   cost=a.cost, env_config=env_config, alerts=a.alerts,
                                                   action=a)
        return s_prime, reward

