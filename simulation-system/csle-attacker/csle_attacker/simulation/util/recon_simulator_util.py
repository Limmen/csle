import numpy as np
from csle_common.dao.observation.common.port_observation_state import PortObservationState
from csle_common.dao.observation.common.vulnerability_observation_state import VulnerabilityObservationState
from csle_common.dao.network.transport_protocol import TransportProtocol
from csle_common.dao.network.emulation_env_state import EmulationEnvState
from csle_common.dao.network.emulation_env_agent_config import EmulationEnvAgentConfig
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.observation.attacker.attacker_machine_observation_state import AttackerMachineObservationState
from csle_common.envs_model.util.env_dynamics_util import EnvDynamicsUtil
from csle_common.dao.network.network_outcome import NetworkOutcome
from csle_attacker.simulation.util.simulator_util import SimulatorUtil


class ReconSimulatorUtil:
    """
    Class containing utility functions for simulating Recon actions
    """

    @staticmethod
    def simulate_port_vuln_scan_helper(s: EmulationEnvState, a: AttackerAction,
                                       env_config: EmulationEnvAgentConfig,
                                       protocol=TransportProtocol.TCP, vuln_scan : bool = False) -> EmulationEnvState:
        """
        Helper function for simulating port-scan and vuln-scan actions

        :param s: the current environment state
        :param a: the scan action to take
        :param env_config: the current environment configuration
        :param protocol: the tranport protocol for the scan
        :param vuln_scan: boolean flag whether the scan is a vulnerability scan or not
        :return: s_prime
        """
        net_outcome = NetworkOutcome()
        reachable_nodes = SimulatorUtil.reachable_nodes(state=s, env_config=env_config)
        # Scan action on a single host
        if not a.subnet:
            new_m_obs = None
            for node in env_config.network_conf.nodes:
                if node.ips == a.ips and node.ips in reachable_nodes:
                    new_m_obs = AttackerMachineObservationState(ips=node.ips)
                    new_m_obs.reachable = node.reachable_nodes
                    for service in node.services:
                        if service.protocol == protocol:
                            port_obs = PortObservationState(port=service.port, open=True, service=service.name,
                                                            protocol=protocol)
                            new_m_obs.ports.append(port_obs)

                    if vuln_scan:
                        for vuln in node.vulnerabilities:
                            vuln_obs = VulnerabilityObservationState(
                                name=vuln.name, port=vuln.port, protocol=vuln.protocol, cvss=vuln.cvss,
                                service=vuln.service, credentials=vuln.credentials)
                            new_m_obs.cve_vulns.append(vuln_obs)
            if new_m_obs is not None:
                merged = False
                for o_m in s.attacker_obs_state.machines:
                    # Machine was already known, merge state
                    if o_m.ips == a.ips:
                        new_net_outcome = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(
                            o_m, new_m_obs, action=a)
                        merged_machine_obs = new_net_outcome.attacker_machine_observation
                        net_outcome.update_counts(new_net_outcome)
                        net_outcome.attacker_machine_observations.append(merged_machine_obs)
                        merged = True
                    else:
                        net_outcome.attacker_machine_observations.append(o_m)
                # New machine, was not known before
                if not merged:
                    net_outcome.attacker_machine_observations.append(new_m_obs)
                    net_outcome.total_new_machines_found +=1
            else:
                net_outcome.attacker_machine_observations = s.attacker_obs_state.machines
            s_prime = s
            s_prime.attacker_obs_state.machines = net_outcome.attacker_machine_observations

        # Scan action on a whole subnet
        else:
            new_m_obs = []
            for node in env_config.network_conf.nodes:
                if not node.ips in reachable_nodes:
                    continue
                m_obs = AttackerMachineObservationState(ips=node.ips)
                m_obs.reachable = node.reachable_nodes
                for service in node.services:
                    if service.protocol == protocol:
                        port_obs = PortObservationState(port=service.port, open=True, service=service.name,
                                                        protocol=protocol)
                        m_obs.ports.append(port_obs)

                if vuln_scan:
                    for vuln in node.vulnerabilities:
                        vuln_obs = VulnerabilityObservationState(
                            name=vuln.name, port=vuln.port, protocol=vuln.protocol, cvss=vuln.cvss,
                            service=vuln.service, credentials=vuln.credentials)
                        m_obs.cve_vulns.append(vuln_obs)

                new_m_obs.append(m_obs)
            net_outcome = EnvDynamicsUtil.merge_new_obs_with_old(s.attacker_obs_state.machines, new_m_obs,
                                                                 emulation_env_agent_config=env_config, action=a)
            s_prime = s
            s_prime.attacker_obs_state.machines = net_outcome.attacker_machine_observations

        return s_prime

    @staticmethod
    def simulate_host_scan_helper(s: EmulationEnvState, a: AttackerAction,
                                  env_config: EmulationEnvAgentConfig, os=False) -> EmulationEnvState:
        """
        Helper method for simulating a host-scan (i.e non-port scan) action

        :param s: the current environment state
        :param a: the action to take
        :param env_config: the current environment configuration
        :param os: boolean flag whether the host scan should check the operating system too
        :return: s_prime
        """
        net_outcome = NetworkOutcome()
        reachable_nodes = SimulatorUtil.reachable_nodes(state=s, env_config=env_config)
        # Scan a a single host
        if not a.subnet:
            new_m_obs = None

            for node in env_config.network_conf.nodes:
                if node.ips == a.ips and node.ips in reachable_nodes:
                    new_m_obs = AttackerMachineObservationState(ips=node.ips)
                    new_m_obs.reachable = node.reachable_nodes
                    if os:
                        new_m_obs.os = node.os

            if new_m_obs is not None:
                merged = False
                for o_m in s.attacker_obs_state.machines:
                    # Machine was already known, merge state
                    if o_m.ips == a.ips:
                        new_net_outcome = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(
                            o_m, new_m_obs, action=a)
                        merged_machine_obs = new_net_outcome.attacker_machine_observation
                        net_outcome.update_counts(new_net_outcome)
                        net_outcome.attacker_machine_observations.append(merged_machine_obs)
                        merged = True
                    else:
                        net_outcome.attacker_machine_observations.append(o_m)
                # New machine, was not known before
                if not merged:
                    net_outcome.attacker_machine_observations.append(new_m_obs)
                    net_outcome.total_new_machines_found +=1
            else:
                net_outcome.attacker_machine_observations = s.attacker_obs_state.machines
            s_prime = s
            s_prime.attacker_obs_state.machines = net_outcome.attacker_machine_observations

        # Scan a whole subnetwork
        else:
            new_m_obs = []
            for node in env_config.network_conf.nodes:
                if node.ips in reachable_nodes:
                    m_obs = AttackerMachineObservationState(ips=node.ips)
                    m_obs.reachable = node.reachable_nodes
                    if os:
                        m_obs.os = node.os
                    new_m_obs.append(m_obs)
            net_outcome = EnvDynamicsUtil.merge_new_obs_with_old(s.attacker_obs_state.machines,
                                                                 new_m_obs, emulation_env_agent_config=env_config, action=a)
            s_prime = s
            s_prime.attacker_obs_state.machines = net_outcome.attacker_machine_observations


        return s_prime

