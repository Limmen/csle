import paramiko
from _typeshed import Incomplete
from csle_base.json_serializable import JSONSerializable
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction as EmulationAttackerAction
from csle_common.dao.emulation_config.beats_config import BeatsConfig as BeatsConfig
from csle_common.dao.emulation_config.container_network import ContainerNetwork as ContainerNetwork
from csle_common.dao.emulation_config.containers_config import ContainersConfig as ContainersConfig
from csle_common.dao.emulation_config.docker_stats_manager_config import DockerStatsManagerConfig as DockerStatsManagerConfig
from csle_common.dao.emulation_config.elk_config import ElkConfig as ElkConfig
from csle_common.dao.emulation_config.flags_config import FlagsConfig as FlagsConfig
from csle_common.dao.emulation_config.host_manager_config import HostManagerConfig as HostManagerConfig
from csle_common.dao.emulation_config.kafka_config import KafkaConfig as KafkaConfig
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig as NodeContainerConfig
from csle_common.dao.emulation_config.ossec_ids_manager_config import OSSECIDSManagerConfig as OSSECIDSManagerConfig
from csle_common.dao.emulation_config.ovs_config import OVSConfig as OVSConfig
from csle_common.dao.emulation_config.resources_config import ResourcesConfig as ResourcesConfig
from csle_common.dao.emulation_config.sdn_controller_config import SDNControllerConfig as SDNControllerConfig
from csle_common.dao.emulation_config.services_config import ServicesConfig as ServicesConfig
from csle_common.dao.emulation_config.snort_ids_manager_config import SnortIDSManagerConfig as SnortIDSManagerConfig
from csle_common.dao.emulation_config.topology_config import TopologyConfig as TopologyConfig
from csle_common.dao.emulation_config.traffic_config import TrafficConfig as TrafficConfig
from csle_common.dao.emulation_config.users_config import UsersConfig as UsersConfig
from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig as VulnerabilitiesConfig
from csle_common.logging.log import Logger as Logger
from csle_common.util.ssh_util import SSHUtil as SSHUtil
from typing import Any, Dict, List, Optional, Union

class EmulationEnvConfig(JSONSerializable):
    name: Incomplete
    descr: Incomplete
    containers_config: Incomplete
    users_config: Incomplete
    flags_config: Incomplete
    vuln_config: Incomplete
    topology_config: Incomplete
    traffic_config: Incomplete
    resources_config: Incomplete
    kafka_config: Incomplete
    services_config: Incomplete
    connections: Incomplete
    producer: Incomplete
    hostname: Incomplete
    port_forward_port: int
    running: bool
    image: Incomplete
    id: int
    static_attacker_sequences: Incomplete
    ovs_config: Incomplete
    sdn_controller_config: Incomplete
    level: Incomplete
    execution_id: Incomplete
    version: Incomplete
    host_manager_config: Incomplete
    snort_ids_manager_config: Incomplete
    ossec_ids_manager_config: Incomplete
    docker_stats_manager_config: Incomplete
    elk_config: Incomplete
    beats_config: Incomplete
    csle_collector_version: Incomplete
    csle_ryu_version: Incomplete
    def __init__(self, name: str, containers_config: ContainersConfig, users_config: UsersConfig, flags_config: FlagsConfig, vuln_config: VulnerabilitiesConfig, topology_config: TopologyConfig, traffic_config: TrafficConfig, resources_config: ResourcesConfig, kafka_config: KafkaConfig, services_config: ServicesConfig, descr: str, static_attacker_sequences: Dict[str, List[EmulationAttackerAction]], ovs_config: OVSConfig, sdn_controller_config: Optional[SDNControllerConfig], host_manager_config: HostManagerConfig, snort_ids_manager_config: SnortIDSManagerConfig, ossec_ids_manager_config: OSSECIDSManagerConfig, docker_stats_manager_config: DockerStatsManagerConfig, elk_config: ElkConfig, beats_config: BeatsConfig, level: int, version: str, execution_id: int, csle_collector_version: str = ..., csle_ryu_version: str = ...) -> None: ...
    @staticmethod
    def from_dict(d: Dict[str, Any]) -> EmulationEnvConfig: ...
    def to_dict(self) -> Dict[str, Any]: ...
    def connect(self, ip: str = ..., username: str = ..., pw: str = ..., create_producer: bool = ...) -> paramiko.SSHClient: ...
    def get_connection(self, ip: str) -> paramiko.SSHClient: ...
    def get_hacker_connection(self) -> paramiko.SSHClient: ...
    def cleanup(self) -> None: ...
    def create_producer(self) -> None: ...
    def close_all_connections(self) -> None: ...
    @staticmethod
    def check_if_ssh_connection_is_alive(conn: paramiko.SSHClient) -> bool: ...
    def get_port_forward_port(self) -> int: ...
    def ids(self) -> bool: ...
    def get_container_from_ip(self, ip: str) -> Union[NodeContainerConfig, None]: ...
    def get_all_ips(self) -> List[str]: ...
    @staticmethod
    def from_json_file(json_file_path: str) -> EmulationEnvConfig: ...
    def copy(self) -> EmulationEnvConfig: ...
    def create_execution_config(self, ip_first_octet: int, physical_servers: List[str]) -> EmulationEnvConfig: ...
    def get_network_by_name(self, net_name: str) -> ContainerNetwork: ...
