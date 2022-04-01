from csle_common.dao.emulation_observation.common.emulation_port_observation_state \
    import EmulationPortObservationState
from csle_common.dao.emulation_observation.common.emulation_vulnerability_observation_state \
    import EmulationVulnerabilityObservationState
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_observation.attacker.emulation_attacker_machine_observation_state \
    import EmulationAttackerMachineObservationState
from csle_common.util.env_dynamics_util import EnvDynamicsUtil
from csle_attacker.simulation.util.simulator_util import SimulatorUtil


class ReconSimulatorUtil:
    """
    Class containing utility functions for simulating Recon actions
    """

    @staticmethod
    def simulate_port_vuln_scan_helper(s: EmulationEnvState, a: EmulationAttackerAction,protocol=TransportProtocol.TCP,
                                       vuln_scan : bool = False) -> EmulationEnvState:
        """
        Helper function for simulating port-scan and vuln-scan actions

        :param s: the current environment state
        :param a: the scan action to take
        :param protocol: the tranport protocol for the scan
        :param vuln_scan: boolean flag whether the scan is a vulnerability scan or not
        :return: s_prime
        """
        reachable_nodes = SimulatorUtil.reachable_nodes(state=s)
        attacker_machine_observations= []
        # Scan action on a single host
        if not a.subnet:
            new_m_obs = None
            for c in s.emulation_env_config.containers_config.containers:
                for ip in a.ips:
                    if ip in c.get_ips() and ip in reachable_nodes:
                        new_m_obs = EmulationAttackerMachineObservationState(ips=c.get_ips())
                        new_m_obs.reachable = s.emulation_env_config.containers_config.get_reachable_ips(container=c)
                        for service in s.emulation_env_config.services_config.get_services_for_ips(ips=c.get_ips()):
                            if service.protocol == protocol:
                                port_obs = EmulationPortObservationState(port=service.port, open=True,
                                                                         service=service.name,
                                                                         protocol=protocol)
                                new_m_obs.ports.append(port_obs)

                        if vuln_scan:
                            for vuln in s.emulation_env_config.vuln_config.get_vulnerabilities(ips=c.get_ips()):
                                vuln_obs = EmulationVulnerabilityObservationState(
                                    name=vuln.name, port=vuln.port, protocol=vuln.protocol, cvss=vuln.cvss,
                                    service=vuln.service, credentials=vuln.credentials)
                                new_m_obs.cve_vulns.append(vuln_obs)
                        break
            if new_m_obs is not None:
                merged = False
                for o_m in s.attacker_obs_state.machines:
                    # Machine was already known, merge state
                    if o_m.ips == a.ips:
                        attacker_machine_observation = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(
                            o_m, new_m_obs, action=a)
                        merged_machine_obs = attacker_machine_observation
                        merged = True
                    else:
                        attacker_machine_observations.append(o_m)
                # New machine, was not known before
                if not merged:
                    attacker_machine_observations.append(new_m_obs)
            else:
                attacker_machine_observations = s.attacker_obs_state.machines
            s_prime = s
            s_prime.attacker_obs_state.machines = attacker_machine_observations

        # Scan action on a whole subnet
        else:
            new_m_obs = []
            for c in s.emulation_env_config.containers_config.containers:
                if not c.reachable(reachable_ips=list(reachable_nodes)):
                    continue
                m_obs = EmulationAttackerMachineObservationState(ips=c.get_ips())
                m_obs.reachable = s.emulation_env_config.containers_config.get_reachable_ips(container=c)
                for service in s.emulation_env_config.services_config.get_services_for_ips(ips=c.get_ips()):
                    if service.protocol == protocol:
                        port_obs = EmulationPortObservationState(port=service.port, open=True, service=service.name,
                                                                 protocol=protocol)
                        m_obs.ports.append(port_obs)

                if vuln_scan:
                    for vuln in s.emulation_env_config.vuln_config.get_vulnerabilities(ips=c.get_ips()):
                        vuln_obs = EmulationVulnerabilityObservationState(
                            name=vuln.name, port=vuln.port, protocol=vuln.protocol, cvss=vuln.cvss,
                            service=vuln.service, credentials=vuln.credentials)
                        m_obs.cve_vulns.append(vuln_obs)

                new_m_obs.append(m_obs)
            attacker_machine_observations = EnvDynamicsUtil.merge_new_obs_with_old(
                s.attacker_obs_state.machines, new_m_obs, emulation_env_config=s.emulation_env_config, action=a)
            s_prime = s
            s_prime.attacker_obs_state.machines = attacker_machine_observations

        return s_prime

    @staticmethod
    def simulate_host_scan_helper(s: EmulationEnvState, a: EmulationAttackerAction, os=False) -> EmulationEnvState:
        """
        Helper method for simulating a host-scan (i.e non-port scan) action

        :param s: the current environment state
        :param a: the action to take
        :param os: boolean flag whether the host scan should check the operating system too
        :return: s_prime
        """
        reachable_nodes = SimulatorUtil.reachable_nodes(state=s)
        attacker_machine_observations = []
        # Scan a a single host
        if not a.subnet:
            new_m_obs = None

            for c in s.emulation_env_config.containers_config.containers:
                if c.get_ips() == a.ips and c.get_ips() in reachable_nodes:
                    new_m_obs = EmulationAttackerMachineObservationState(ips=c.get_ips())
                    new_m_obs.reachable = s.emulation_env_config.containers_config.get_reachable_ips(container=c)
                    if os:
                        new_m_obs.os = c.os

            if new_m_obs is not None:
                merged = False
                for o_m in s.attacker_obs_state.machines:
                    # Machine was already known, merge state
                    if o_m.ips == a.ips:
                        attacker_machine_observation = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(
                            o_m, new_m_obs, action=a)
                        merged_machine_obs = attacker_machine_observation
                        merged = True
                    else:
                        attacker_machine_observations.append(o_m)
                # New machine, was not known before
                if not merged:
                    attacker_machine_observations.append(new_m_obs)
            else:
                attacker_machine_observations = s.attacker_obs_state.machines
            s_prime = s
            s_prime.attacker_obs_state.machines = attacker_machine_observations

        # Scan a whole subnetwork
        else:
            new_m_obs = []
            for c in s.emulation_env_config.containers_config.containers:
                for ip in c.get_ips():
                    if ip in reachable_nodes:
                        m_obs = EmulationAttackerMachineObservationState(ips=c.get_ips())
                        m_obs.reachable = s.emulation_env_config.containers_config.get_reachable_ips(container=c)
                        if os:
                            m_obs.os = c.os
                        new_m_obs.append(m_obs)
                        continue
            attacker_machine_observations = EnvDynamicsUtil.merge_new_obs_with_old(
                s.attacker_obs_state.machines, new_m_obs, emulation_env_config=s.emulation_env_config, action=a)
            s_prime = s
            s_prime.attacker_obs_state.machines = attacker_machine_observations

        return s_prime

