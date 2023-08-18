from typing import Union, Dict, Any
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_observation.attacker.emulation_attacker_observation_state \
    import EmulationAttackerObservationState
from csle_common.dao.emulation_observation.defender.emulation_defender_observation_state \
    import EmulationDefenderObservationState
from csle_common.dao.emulation_observation.attacker.emulation_attacker_machine_observation_state \
    import EmulationAttackerMachineObservationState
from csle_common.dao.emulation_observation.defender.emulation_defender_machine_observation_state \
    import EmulationDefenderMachineObservationState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_config import EmulationAttackerActionConfig
from csle_common.dao.emulation_action.defender.emulation_defender_action_config import EmulationDefenderActionConfig
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state import \
    EmulationConnectionObservationState
from csle_common.dao.emulation_config.credential import Credential
from csle_base.json_serializable import JSONSerializable
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.host_manager.dao.host_metrics import HostMetrics


class EmulationEnvState(JSONSerializable):
    """
    Represents the combined state of the emulation environment,
    including both the attacker's and the defender's states.
    """

    def __init__(self, emulation_env_config: EmulationEnvConfig):
        """
        Initializes the state

        :param emulation_env_config: the environment configuration
        :param attacker_action_config: the configuration of the attacker agent
        :param defender_agent_config: the configuration of the defender agent
        """
        self.emulation_env_config = emulation_env_config
        self.attacker_action_config = EmulationAttackerActionConfig.all_actions_config(
            num_nodes=len(self.emulation_env_config.containers_config.containers),
            subnet_masks=self.emulation_env_config.topology_config.subnetwork_masks,
            hacker_ip=self.emulation_env_config.containers_config.agent_ip)
        self.defender_action_config = EmulationDefenderActionConfig.all_actions_config(
            num_nodes=len(self.emulation_env_config.containers_config.containers),
            subnet_masks=self.emulation_env_config.topology_config.subnetwork_masks)
        self.vuln_lookup = constants.VULNERABILITIES.vuln_lookup
        self.vuln_lookup_inv = {v: k for k, v in self.vuln_lookup.items()}
        self.service_lookup = constants.SERVICES.service_lookup
        self.service_lookup_inv = {v: k for k, v in self.service_lookup.items()}
        self.os_lookup = constants.OS.os_lookup
        self.os_lookup_inv = {v: k for k, v in self.os_lookup.items()}
        self.attacker_obs_state: Union[EmulationAttackerObservationState, None] = None
        self.defender_obs_state: Union[EmulationDefenderObservationState, None] = None
        self.attacker_cached_ssh_connections: Dict[Any, Any] = {}
        self.attacker_cached_telnet_connections: Dict[Any, EmulationConnectionObservationState] = {}
        self.attacker_cached_ftp_connections: Dict[Any, EmulationConnectionObservationState] = {}
        self.defender_cached_ssh_connections: Dict[Any, EmulationConnectionObservationState] = {}
        self.attacker_cached_backdoor_credentials: Dict[Any, Credential] = {}
        self.reset()

    def initialize_defender_machines(self) -> None:
        """
        Initializes the defender observation state based on the emulation configuration

        :return: None
        """
        defender_machines = []
        for c in self.emulation_env_config.containers_config.containers:
            defender_machines.append(EmulationDefenderMachineObservationState.from_container(
                c, kafka_config=self.emulation_env_config.kafka_config))
        if self.defender_obs_state is None:
            raise ValueError("EmulationDefenderObservationState is None")
        self.defender_obs_state.machines = defender_machines
        self.defender_obs_state.start_monitoring_threads()

    def reset(self) -> None:
        """
        Resets the env state. Caches connections

        :return: None
        """
        agent_reachable = set()
        if self.attacker_obs_state is not None:
            agent_reachable = self.attacker_obs_state.agent_reachable
            for m in self.attacker_obs_state.machines:
                for c in m.ssh_connections:
                    self.attacker_cached_ssh_connections[(c.ip, c.credential.username, c.port)] = c
                for c in m.telnet_connections:
                    self.attacker_cached_telnet_connections[(c.ip, c.credential.username, c.port)] = c
                for c in m.ftp_connections:
                    self.attacker_cached_ftp_connections[(c.ip, c.credential.username, c.port)] = c
                for cr in m.backdoor_credentials:
                    for ip in m.ips:
                        self.attacker_cached_backdoor_credentials[(ip, cr.username, cr.pw)] = cr
        self.attacker_obs_state = EmulationAttackerObservationState(catched_flags=0, agent_reachable=agent_reachable)
        self.attacker_obs_state.last_attacker_action = None
        self.attacker_obs_state.undetected_intrusions_steps = 0
        self.attacker_obs_state.all_flags = False
        self.attacker_obs_state.catched_flags = 0
        self.attacker_obs_state.step = 1

        if self.defender_obs_state is not None:
            for m in self.defender_obs_state.machines:
                for c in m.ssh_connections:
                    self.defender_cached_ssh_connections[(c.ip, c.credential.username, c.port)] = c
        else:
            self.defender_obs_state = EmulationDefenderObservationState(
                kafka_config=self.emulation_env_config.kafka_config,
                client_population_metrics=ClientPopulationMetrics(),
                docker_stats=DockerStats(), snort_ids_alert_counters=SnortIdsAlertCounters(),
                snort_ids_rule_counters=SnortIdsRuleCounters(), ossec_ids_alert_counters=OSSECIdsAlertCounters(),
                aggregated_host_metrics=HostMetrics(), defender_actions=[], attacker_actions=[])

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

        if self.attacker_obs_state is None:
            raise ValueError("EmualtionAttackerObservationState is None")
        self.attacker_obs_state.cleanup()

        for _, c in self.defender_cached_ssh_connections.items():
            (ssh_conns, _) = c
            for c2 in ssh_conns:
                c2.cleanup()
        if self.defender_obs_state is None:
            raise ValueError("EmulationDefenderObservationState is None")
        self.defender_obs_state.cleanup()

    def get_attacker_machine(self, ip: str) -> Union[EmulationAttackerMachineObservationState, None]:
        """
        Utility function for extracting the attacker machine from the attacker's observation

        :param ip: the ip of the attacker machine
        :return: the machine if is found, otherwise None
        """
        if self.attacker_obs_state is None:
            raise ValueError("EmulationAttackerObservationState is None")
        for m in self.attacker_obs_state.machines:
            for m_ip in m.ips:
                if m_ip == ip:
                    return m
        return None

    def get_defender_machine(self, ip: str) -> Union[EmulationDefenderMachineObservationState, None]:
        """
        Utility function for extracting the defender machine from the defender's observation given an IP

        :param ip: the ip of the machine
        :return: the machine if found otherwise None
        """
        if self.defender_obs_state is None:
            raise ValueError("EmulationDefenderObservationState is None")
        for m in self.defender_obs_state.machines:
            for m_ip in m.ips:
                if m_ip == ip:
                    return m
        return None

    def copy(self) -> "EmulationEnvState":
        """
        :return: a copy of the env state
        """
        copy = EmulationEnvState(emulation_env_config=self.emulation_env_config)
        if self.attacker_obs_state is None:
            raise ValueError("EmulationAttackerObservationState is None")
        if self.defender_obs_state is None:
            raise ValueError("EmulationDefenderObservationState is None")
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
    def from_dict(d: Dict[str, Any]) -> "EmulationEnvState":
        """
        Converts a dict representation of the object into a an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationEnvState(emulation_env_config=EmulationEnvConfig.from_dict(d["emulation_env_config"]))
        obj.attacker_action_config = EmulationAttackerActionConfig.from_dict(d["attacker_action_config"])
        obj.defender_action_config = EmulationDefenderActionConfig.from_dict(d["defender_action_config"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        
        :return: a dict representation of the object
        """
        d = {}
        d["emulation_env_config"] = self.emulation_env_config.to_dict()
        d["attacker_action_config"] = self.attacker_action_config.to_dict()
        d["defender_action_config"] = self.defender_action_config.to_dict()
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationEnvState":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationEnvState.from_dict(json.loads(json_str))
