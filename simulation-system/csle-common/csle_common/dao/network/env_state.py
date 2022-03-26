from typing import List, Tuple
import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.state_representation.state_type import StateType
from csle_common.envs_model.logic.emulation.util.common.docker_stats_thread import DockerStatsThread
from csle_common.dao.render.render_config import RenderConfig
from csle_common.dao.network.env_config import CSLEEnvConfig
from csle_common.dao.container_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.observation.attacker.attacker_observation_state import AttackerObservationState
from csle_common.dao.observation.defender.defender_observation_state import DefenderObservationState
from csle_common.dao.observation.attacker.attacker_machine_observation_state import AttackerMachineObservationState
from csle_common.dao.observation.defender.defender_machine_observation_state import DefenderMachineObservationState
from csle_common.envs_model.state_representation.attacker_state_representation import AttackerStateRepresentation
from csle_common.envs_model.state_representation.defender_state_representation import DefenderStateRepresentation
from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_config import EmulationConfig



class EnvState:
    """
    Represents the combined state of the environment, including both the attacker's and the defender's belief states.
    """

    def __init__(self, env_config : CSLEEnvConfig, num_ports : int, num_vuln : int, num_sh : int,
                 num_flags : int, num_nodes : int,
                 vuln_lookup: dict = None, service_lookup: dict = None, os_lookup: dict = None,
                 state_type: StateType = StateType.BASE, ids : bool = False):
        """
        Initializes the state

        :param env_config: the environment configuration
        :param num_ports: the number of ports
        :param num_vuln: the number of vulnerabilities
        :param num_sh: the number of shell access
        :param num_flags: the number of flags
        :param num_nodes: the number of nodes
        :param vuln_lookup: the vulnerability lookup dict
        :param service_lookup: the service lookup dict
        :param os_lookup: the operating system lookup dict
        :param state_type: the state type
        :param ids: whether there is an IDS in the env
        """
        self.env_config = env_config
        self.state_type = state_type
        self.reward_range = (float(0), float(1))
        self.num_ports = num_ports
        self.num_nodes = num_nodes
        self.num_vuln = num_vuln
        self.num_sh = num_sh
        self.num_flags = num_flags
        self.vuln_lookup = vuln_lookup
        self.vuln_lookup_inv = {v: k for k, v in self.vuln_lookup.items()}
        self.service_lookup = service_lookup
        self.service_lookup_inv = {v: k for k, v in self.service_lookup.items()}
        self.os_lookup = os_lookup
        self.os_lookup_inv = {v: k for k, v in self.os_lookup.items()}
        self.ids = ids
        self.attacker_obs_state : AttackerObservationState = None
        self.defender_obs_state : DefenderObservationState = None

        self.attacker_cached_ssh_connections = {}
        self.attacker_cached_telnet_connections = {}
        self.attacker_cached_ftp_connections = {}
        self.attacker_cached_backdoor_credentials = {}
        self.defender_cached_ssh_connections = {}

        self.reset_state() # Init obs state

        self.attacker_observation_space = None
        self.attacker_m_selection_observation_space = None
        self.attacker_network_orig_shape = None
        self.attacker_machine_orig_shape = None
        self.attacker_m_action_observation_space = None
        self.setup_attacker_spaces()

        self.defender_observation_space = None

        self.setup_defender_spaces()

        jumphost_ip = env_config.emulation_config.server_ip if env_config.emulation_config.server_connection else None
        self.docker_stats_thread = DockerStatsThread(jumphost_ip=jumphost_ip)
        self.docker_stats_thread.start()

    def get_attacker_observation(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Gets a numerical observation of the current attacker's state

        :return: machines_obs, ports_protocols_obs
        """
        if self.state_type == StateType.BASE:
            machines_obs, ports_protocols_obs =  \
                AttackerStateRepresentation.base_representation(
                    num_machines=self.attacker_obs_state.num_machines,
                    num_ports = self.attacker_obs_state.num_ports, obs_state=self.attacker_obs_state,
                    vuln_lookup=self.vuln_lookup, service_lookup=self.service_lookup,
                    os_lookup=self.os_lookup)
        elif self.state_type == StateType.COMPACT:
            machines_obs, ports_protocols_obs = \
                AttackerStateRepresentation.compact_representation(
                    num_machines=self.attacker_obs_state.num_machines,
                    num_ports=self.attacker_obs_state.num_ports, obs_state=self.attacker_obs_state)
        elif self.state_type == StateType.ESSENTIAL:
            machines_obs, ports_protocols_obs = \
                AttackerStateRepresentation.essential_representation(
                    num_machines=self.attacker_obs_state.num_machines,
                    num_ports=self.attacker_obs_state.num_ports, obs_state=self.attacker_obs_state)
        elif self.state_type == StateType.SIMPLE:
            machines_obs, ports_protocols_obs = \
                AttackerStateRepresentation.simple_representation(
                    num_machines=self.attacker_obs_state.num_machines, num_ports=self.attacker_obs_state.num_ports,
                    obs_state=self.attacker_obs_state)
        elif self.state_type == StateType.CORE:
            machines_obs, ports_protocols_obs = \
                AttackerStateRepresentation.simple_representation(
                    num_machines=self.attacker_obs_state.num_machines,
                    num_ports=self.attacker_obs_state.num_ports, obs_state=self.attacker_obs_state)
        elif self.state_type == StateType.TEST:
            machines_obs, ports_protocols_obs = \
                AttackerStateRepresentation.test_representation(
                    num_machines=self.attacker_obs_state.num_machines,
                    num_ports=self.attacker_obs_state.num_ports,
                    obs_state=self.attacker_obs_state)
        elif self.state_type == StateType.BASIC:
            machines_obs, ports_protocols_obs = \
                AttackerStateRepresentation.basic_representation(
                    num_machines=self.attacker_obs_state.num_machines,
                    num_ports=self.attacker_obs_state.num_ports,
                    obs_state=self.attacker_obs_state)
            # raise NotImplementedError("Core state type not implemented for the attacker")
        else:
            raise ValueError("State type:{} not recognized".format(self.state_type))
        return machines_obs, ports_protocols_obs

    def get_defender_observation(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Gets a numerical observation of the current defender's state

        :return: machines_obs, ports_protocols_obs
        """
        if self.state_type == StateType.BASE:
            machines_obs, network_obs =  \
                DefenderStateRepresentation.base_representation(
                    num_machines=self.defender_obs_state.num_machines, obs_state=self.defender_obs_state,
                    os_lookup=self.os_lookup, ids=self.ids,
                    multiple_stopping=self.env_config.multiple_stopping_environment, env_config=self.env_config)
        elif self.state_type == StateType.COMPACT:
            machines_obs, network_obs = \
                DefenderStateRepresentation.compact_representation(
                    num_machines=self.defender_obs_state.num_machines,
                    obs_state=self.defender_obs_state,
                    os_lookup=self.os_lookup, ids=self.ids,
                    multiple_stopping=self.env_config.multiple_stopping_environment, env_config=self.env_config)
        elif self.state_type == StateType.ESSENTIAL:
            machines_obs, network_obs = \
                DefenderStateRepresentation.essential_representation(
                    num_machines=self.defender_obs_state.num_machines,
                    obs_state=self.defender_obs_state, os_lookup=self.os_lookup, ids=self.ids,
                    multiple_stopping=self.env_config.multiple_stopping_environment, env_config=self.env_config)
        elif self.state_type == StateType.SIMPLE:
            machines_obs, network_obs = \
                DefenderStateRepresentation.simple_representation(
                    num_machines=self.defender_obs_state.num_machines, obs_state=self.defender_obs_state,
                    os_lookup=self.os_lookup, ids=self.ids,
                    multiple_stopping=self.env_config.multiple_stopping_environment, env_config=self.env_config)
        elif self.state_type == StateType.CORE:
            machines_obs, network_obs = \
                DefenderStateRepresentation.core_representation(
                    num_machines=self.defender_obs_state.num_machines, obs_state=self.defender_obs_state,
                    os_lookup=self.os_lookup, ids=self.ids,
                    multiple_stopping=self.env_config.multiple_stopping_environment, env_config=self.env_config)
        elif self.state_type == StateType.TEST:
            machines_obs = np.array([])
            network_obs = np.array([int(self.attacker_obs_state.ongoing_intrusion()), self.defender_obs_state.step])

        elif self.state_type == StateType.BASIC:
            machines_obs, network_obs = \
                DefenderStateRepresentation.core_representation(
                    num_machines=self.defender_obs_state.num_machines,
                    obs_state=self.defender_obs_state, os_lookup=self.os_lookup, ids=self.ids,
                    multiple_stopping=self.env_config.multiple_stopping_environment, env_config=self.env_config)
        else:
            raise ValueError("State type:{} not recognized".format(self.state_type))
        return machines_obs, network_obs

    def setup_attacker_spaces(self) -> None:
        """
        Sets up the observation spaces used by RL attacker agents

        :return: None
        """
        if self.state_type == StateType.BASE:
            attacker_observation_space, attacker_m_selection_observation_space, attacker_network_orig_shape, \
            attacker_machine_orig_shape, attacker_m_action_observation_space = \
                AttackerStateRepresentation.base_representation_spaces(obs_state=self.attacker_obs_state)
        elif self.state_type == StateType.COMPACT:
            attacker_observation_space, attacker_m_selection_observation_space, attacker_network_orig_shape, \
            attacker_machine_orig_shape, attacker_m_action_observation_space = \
                AttackerStateRepresentation.compact_representation_spaces(obs_state=self.attacker_obs_state)
        elif self.state_type == StateType.ESSENTIAL:
            attacker_observation_space, attacker_m_selection_observation_space, attacker_network_orig_shape, \
            attacker_machine_orig_shape, attacker_m_action_observation_space = \
                AttackerStateRepresentation.essential_representation_spaces(obs_state=self.attacker_obs_state)
        elif self.state_type == StateType.SIMPLE:
            attacker_observation_space, attacker_m_selection_observation_space, attacker_network_orig_shape, \
            attacker_machine_orig_shape, attacker_m_action_observation_space = \
                AttackerStateRepresentation.simple_representation_spaces(obs_state=self.attacker_obs_state)
        elif self.state_type == StateType.CORE:
            attacker_observation_space, attacker_m_selection_observation_space, attacker_network_orig_shape, \
            attacker_machine_orig_shape, attacker_m_action_observation_space = \
                AttackerStateRepresentation.simple_representation_spaces(obs_state=self.attacker_obs_state)
        elif self.state_type == StateType.TEST:
            attacker_observation_space, attacker_m_selection_observation_space, attacker_network_orig_shape, \
            attacker_machine_orig_shape, attacker_m_action_observation_space = \
                AttackerStateRepresentation.test_representation_spaces(obs_state=self.attacker_obs_state)
        elif self.state_type == StateType.BASIC:
            attacker_observation_space, attacker_m_selection_observation_space, attacker_network_orig_shape, \
            attacker_machine_orig_shape, attacker_m_action_observation_space = \
                AttackerStateRepresentation.basic_representation_spaces(obs_state=self.attacker_obs_state)
                # raise NotImplementedError("Core state type not implemented for the attacker")
        else:
            raise ValueError("State type:{} not recognized".format(self.state_type))
        self.attacker_observation_space = attacker_observation_space
        self.attacker_m_selection_observation_space = attacker_m_selection_observation_space
        self.attacker_network_orig_shape = attacker_network_orig_shape
        self.attacker_machine_orig_shape = attacker_machine_orig_shape
        self.attacker_m_action_observation_space = attacker_m_action_observation_space

    def setup_defender_spaces(self) -> None:
        """
        Sets up the observation spaces used by RL defender agents

        :return: None
        """
        if self.state_type == StateType.BASE:
            defender_observation_space = DefenderStateRepresentation.base_representation_spaces(
                obs_state=self.defender_obs_state, multiple_stopping=self.env_config.multiple_stopping_environment)
        elif self.state_type == StateType.COMPACT:
            defender_observation_space = DefenderStateRepresentation.compact_representation_spaces(
                obs_state=self.defender_obs_state, multiple_stopping=self.env_config.multiple_stopping_environment)
        elif self.state_type == StateType.ESSENTIAL:
            defender_observation_space = DefenderStateRepresentation.essential_representation_spaces(
                obs_state=self.defender_obs_state, multiple_stopping=self.env_config.multiple_stopping_environment)
        elif self.state_type == StateType.SIMPLE:
            defender_observation_space = DefenderStateRepresentation.simple_representation_spaces(
                obs_state=self.defender_obs_state, multiple_stopping=self.env_config.multiple_stopping_environment)
        elif self.state_type == StateType.CORE:
            defender_observation_space = DefenderStateRepresentation.core_representation_spaces(
                obs_state=self.defender_obs_state, multiple_stopping=self.env_config.multiple_stopping_environment)
        elif self.state_type == StateType.TEST:
            defender_observation_space = DefenderStateRepresentation.test_representation_spaces(
                obs_state=self.defender_obs_state, multiple_stopping=self.env_config.multiple_stopping_environment)
        elif self.state_type == StateType.BASIC:
            defender_observation_space = DefenderStateRepresentation.core_representation_spaces(
                obs_state=self.defender_obs_state, multiple_stopping=self.env_config.multiple_stopping_environment)
        else:
            raise ValueError("State type:{} not recognized".format(self.state_type))

        self.defender_observation_space = defender_observation_space

    def reset_state(self) -> None:
        """
        Resets the env state. Caches connections

        :return: None
        """
        agent_reachable = None
        if self.attacker_obs_state is not None:
            agent_reachable = self.attacker_obs_state.agent_reachable
            for m in self.attacker_obs_state.machines:
                for c in m.ssh_connections:
                    self.attacker_cached_ssh_connections[(m.ip, c.username, c.port)] = c
                for c in m.telnet_connections:
                    self.attacker_cached_telnet_connections[(m.ip, c.username, c.port)] = c
                for c in m.ftp_connections:
                    self.attacker_cached_ftp_connections[(m.ip, c.username, c.port)] = c
                for cr in m.backdoor_credentials:
                    self.attacker_cached_backdoor_credentials[(m.ip, cr.username, cr.pw)] = cr
        self.attacker_obs_state = AttackerObservationState(num_machines=self.num_nodes, num_ports=self.num_ports,
                                                           num_vuln=self.num_vuln, num_sh=self.num_sh,
                                                           num_flags=self.num_flags,
                                                           catched_flags=0, agent_reachable=agent_reachable)
        self.attacker_obs_state.last_attacker_action = None
        self.attacker_obs_state.undetected_intrusions_steps = 0
        self.attacker_obs_state.all_flags = False
        self.attacker_obs_state.catched_flags = 0
        self.attacker_obs_state.step = 1
        self.attacker_obs_state.cost = 0
        self.attacker_obs_state.cost_norm = 0
        self.attacker_obs_state.alerts = 0
        self.attacker_obs_state.alerts_norm = 0
        #self.attacker_obs_state.num_sh = 0

        if self.defender_obs_state is not None:
            for m in self.defender_obs_state.machines:
                if len(m.ssh_connections) > 0:
                    self.defender_cached_ssh_connections[m.ip] = (m.ssh_connections, m.emulation_config)
        else:
            self.defender_obs_state = DefenderObservationState(
                num_machines=self.num_nodes, ids=self.ids,
                maximum_number_of_stops=self.env_config.maximum_number_of_defender_stop_actions)

    def merge_services_with_emulation(self, emulation_services : List[str]) -> None:
        """
        Merges pre-defined lookup table of services with services downloaded from the emulation

        :param emulation_services: services downloaded from the emulation
        :return: None
        """
        max_id = max(self.service_lookup.values())
        for service in emulation_services:
            if service not in self.service_lookup:
                max_id += 1
                self.service_lookup[service] = max_id
        self.service_lookup_inv = {v: k for k, v in self.service_lookup.items()}

    def merge_cves_with_emulation(self, emulation_cves : List[str]) -> None:
        """
        Merges pre-defined lookup table of CVEs with CVEs downloaded from the emulation

        :param emulation_cves: list of CVEs downloaded from the emulation
        :return: None
        """
        max_id = max(self.vuln_lookup.values())
        for cve in emulation_cves:
            if cve not in self.vuln_lookup:
                max_id += 1
                self.vuln_lookup[cve] = max_id
        self.vuln_lookup_inv = {v: k for k, v in self.vuln_lookup.items()}

    def cleanup(self) -> None:
        """
        Cleanup

        :return: None
        """
        for _, c in self.attacker_cached_ssh_connections.items():
            c.cleanup()
        for _, c in self.attacker_cached_ftp_connections.items():
            c.cleanup()
        for _, c in self.attacker_cached_telnet_connections.items():
            c.cleanup()

        self.attacker_obs_state.cleanup()

        for _, c in self.defender_cached_ssh_connections.items():
            (ssh_conns, _) = c
            for c2 in ssh_conns:
                c2.cleanup()

        self.defender_obs_state.cleanup()

    def get_attacker_machine(self, ip: str) -> AttackerMachineObservationState:
        """
        Utility function for extracting the attacker machine from the attacker's observation

        :param ip: the ip of the attacker machine
        :return: the machine if is found, otherwise None
        """
        for m in self.attacker_obs_state.machines:
            if m.ip == ip:
                return m
        return None

    def get_defender_machine(self, ip: str) -> DefenderMachineObservationState:
        """
        Utility function for extracting the defender machine from the defender's observation given an IP

        :param ip: the ip of the machine
        :return: the machine if found otherwise None
        """
        for m in self.defender_obs_state.machines:
            if m.ip == ip:
                return m
        return None

    def copy(self) -> "EnvState":
        """
        :return: a copy of the env state
        """
        copy = EnvState(env_config=self.env_config, num_ports=self.num_ports, num_vuln=self.num_vuln,
                        num_sh=self.num_sh, num_flags=self.num_flags, num_nodes=self.num_nodes, vuln_lookup=self.vuln_lookup,
                        service_lookup=self.service_lookup, os_lookup=self.os_lookup, state_type=self.state_type,
                        ids=self.ids)
        copy.attacker_obs_state = self.attacker_obs_state.copy()
        copy.defender_obs_state = self.defender_obs_state.copy()
        return copy

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"Attacker observation state: {self.attacker_obs_state}" \
               f"Defender observation state: {self.defender_obs_state}"


    @staticmethod
    def from_emulation_env_config(emulation_env_config: EmulationEnvConfig, attacker_num_ports_obs=2,
                                  attacker_num_vuln_obs = 2, attacker_num_sh_obs=2,
                                  simulate_detection=False, detection_reward=10, base_detection_p : float = 0.01,
                                  manual_play : bool = False, state_type: StateType = StateType.BASE):
        num_nodes = len(emulation_env_config.containers_config.containers)
        hacker_ip = emulation_env_config.containers_config.agent_ip
        router_ip = emulation_env_config.containers_config.router_ip
        render_config = RenderConfig(num_levels = int(num_nodes/4), num_nodes_per_level = 4)

        emulation_config = EmulationConfig(agent_ip=emulation_env_config.containers_config.agent_ip,
                                           agent_username=constants.CSLE_ADMIN.USER,
                                           agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)

        env_config = CSLEEnvConfig(
            attacker_num_ports_obs=attacker_num_ports_obs,
            attacker_num_vuln_obs=attacker_num_vuln_obs,
            attacker_num_sh_obs=attacker_num_sh_obs,
            num_nodes=num_nodes,
            hacker_ip = hacker_ip,
            router_ip = router_ip, render_config=render_config, env_mode=EnvMode.EMULATION,
            emulation_config=emulation_config, simulate_detection=simulate_detection,
            detection_reward=detection_reward, base_detection_p=base_detection_p, manual_play=manual_play,
            state_type=state_type, emulation_env_config=emulation_env_config
        )