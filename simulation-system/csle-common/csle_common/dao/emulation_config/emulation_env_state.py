from typing import Union
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.observation.attacker.attacker_observation_state import AttackerObservationState
from csle_common.dao.observation.defender.defender_observation_state import DefenderObservationState
from csle_common.dao.observation.attacker.attacker_machine_observation_state import AttackerMachineObservationState
from csle_common.dao.observation.defender.defender_machine_observation_state import DefenderMachineObservationState
from csle_common.dao.action.attacker.attacker_action_config import AttackerActionConfig
from csle_common.dao.action.defender.defender_action_config import DefenderActionConfig


class EmulationEnvState:
    """
    Represents the combined state of the emulation environment,
    including both the attacker's and the defender's states.
    """

    def __init__(self, emulation_env_config : EmulationEnvConfig, attacker_agent_config: AttackerActionConfig,
                 defender_action_config: DefenderActionConfig,
                 vuln_lookup: dict = None, service_lookup: dict = None, os_lookup: dict = None):
        """
        Initializes the state

        :param emulation_env_config: the environment configuration
        :param vuln_lookup: the vulnerability lookup dict
        :param service_lookup: the service lookup dict
        :param attacker_agent_config: the configuration of the attacker agent
        :param defender_agent_config: the configuration of the defender agent
        :param os_lookup: the operating system lookup dict
        """
        self.attacker_agent_config = attacker_agent_config
        self.defender_agent_config = defender_action_config
        self.emulation_env_config = emulation_env_config
        self.vuln_lookup = vuln_lookup
        self.vuln_lookup_inv = {v: k for k, v in self.vuln_lookup.items()}
        self.service_lookup = service_lookup
        self.service_lookup_inv = {v: k for k, v in self.service_lookup.items()}
        self.os_lookup = os_lookup
        self.os_lookup_inv = {v: k for k, v in self.os_lookup.items()}
        self.attacker_obs_state : Union[AttackerObservationState, None] = None
        self.defender_obs_state : Union[DefenderObservationState, None] = None
        self.attacker_cached_ssh_connections = {}
        self.attacker_cached_telnet_connections = {}
        self.attacker_cached_ftp_connections = {}
        self.attacker_cached_backdoor_credentials = {}
        self.defender_cached_ssh_connections = {}
        self.reset()

    def reset(self) -> None:
        """
        Resets the env state. Caches connections

        :return: None
        """
        agent_reachable = None
        if self.attacker_obs_state is not None:
            agent_reachable = self.attacker_obs_state.agent_reachable
            for m in self.attacker_obs_state.machines:
                for c in m.ssh_connections:
                    self.attacker_cached_ssh_connections[(m.ips, c.username, c.port)] = c
                for c in m.telnet_connections:
                    self.attacker_cached_telnet_connections[(m.ips, c.username, c.port)] = c
                for c in m.ftp_connections:
                    self.attacker_cached_ftp_connections[(m.ips, c.username, c.port)] = c
                for cr in m.backdoor_credentials:
                    self.attacker_cached_backdoor_credentials[(m.ips, cr.username, cr.pw)] = cr
        self.attacker_obs_state = AttackerObservationState(catched_flags=0, agent_reachable=agent_reachable)
        self.attacker_obs_state.last_attacker_action = None
        self.attacker_obs_state.undetected_intrusions_steps = 0
        self.attacker_obs_state.all_flags = False
        self.attacker_obs_state.catched_flags = 0
        self.attacker_obs_state.step = 1

        if self.defender_obs_state is not None:
            for m in self.defender_obs_state.machines:
                if len(m.ssh_connections) > 0:
                    self.defender_cached_ssh_connections[m.ips] = (m.ssh_connections, m.emulation_config)
        else:
            self.defender_obs_state = DefenderObservationState()

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

    def get_attacker_machine(self, ip: str) -> Union[AttackerMachineObservationState, None]:
        """
        Utility function for extracting the attacker machine from the attacker's observation

        :param ip: the ip of the attacker machine
        :return: the machine if is found, otherwise None
        """
        for m in self.attacker_obs_state.machines:
            if m.ips == ip:
                return m
        return None

    def get_defender_machine(self, ip: str) -> Union[DefenderMachineObservationState, None]:
        """
        Utility function for extracting the defender machine from the defender's observation given an IP

        :param ip: the ip of the machine
        :return: the machine if found otherwise None
        """
        for m in self.defender_obs_state.machines:
            if m.ips == ip:
                return m
        return None

    def copy(self) -> "EmulationEnvState":
        """
        :return: a copy of the env state
        """
        copy = EmulationEnvState(emulation_env_config=self.emulation_env_config,
                                 vuln_lookup=self.vuln_lookup,
                                 service_lookup=self.service_lookup, os_lookup=self.os_lookup)
        copy.attacker_obs_state = self.attacker_obs_state.copy()
        copy.defender_obs_state = self.defender_obs_state.copy()
        return copy

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"Attacker observation state: {self.attacker_obs_state}" \
               f"Defender observation state: {self.defender_obs_state}"

