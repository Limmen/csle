from typing import List, Dict, Any, Optional, Union
import socket
import paramiko
from confluent_kafka import Producer
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.users_config import UsersConfig
from csle_common.dao.emulation_config.flags_config import FlagsConfig
from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.emulation_config.topology_config import TopologyConfig
from csle_common.dao.emulation_config.traffic_config import TrafficConfig
from csle_common.dao.emulation_config.resources_config import ResourcesConfig
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.services_config import ServicesConfig
from csle_common.dao.emulation_config.ovs_config import OVSConfig
from csle_common.dao.emulation_config.sdn_controller_config import SDNControllerConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_config.host_manager_config import HostManagerConfig
from csle_common.dao.emulation_config.snort_ids_manager_config import SnortIDSManagerConfig
from csle_common.dao.emulation_config.ossec_ids_manager_config import OSSECIDSManagerConfig
from csle_common.dao.emulation_config.docker_stats_manager_config import DockerStatsManagerConfig
from csle_common.dao.emulation_config.beats_config import BeatsConfig
from csle_common.dao.emulation_config.elk_config import ElkConfig
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.util.ssh_util import SSHUtil
from csle_common.logging.log import Logger
import csle_collector.constants.constants as collector_constants
from csle_base.json_serializable import JSONSerializable


class EmulationEnvConfig(JSONSerializable):
    """
    Class representing the configuration of an emulation
    """

    def __init__(self, name: str, containers_config: ContainersConfig, users_config: UsersConfig,
                 flags_config: FlagsConfig,
                 vuln_config: VulnerabilitiesConfig, topology_config: TopologyConfig, traffic_config: TrafficConfig,
                 resources_config: ResourcesConfig, kafka_config: KafkaConfig, services_config: ServicesConfig,
                 descr: str, static_attacker_sequences: Dict[str, List[EmulationAttackerAction]],
                 ovs_config: OVSConfig, sdn_controller_config: Optional[SDNControllerConfig],
                 host_manager_config: HostManagerConfig, snort_ids_manager_config: SnortIDSManagerConfig,
                 ossec_ids_manager_config: OSSECIDSManagerConfig,
                 docker_stats_manager_config: DockerStatsManagerConfig, elk_config: ElkConfig,
                 beats_config: BeatsConfig,
                 level: int, version: str, execution_id: int,
                 csle_collector_version: str = collector_constants.LATEST_VERSION,
                 csle_ryu_version: str = collector_constants.LATEST_VERSION):
        """
        Initializes the object

        :param name: the name of the emulation
        :param containers_config: the containers configuration
        :param users_config: the users configuration
        :param flags_config: the flags configuration
        :param vuln_config: the vulnerabilities configuration
        :param topology_config: the topology configuration
        :param traffic_config: the traffic configuration
        :param resources_config: the resources configuration
        :param services_config: the services configuration
        :param descr: a description of the environment configuration
        :param static_attacker_sequences: dict with static attacker sequences
        :param ovs_config: the OVS config
        :param sdn_controller_config: the SDN controller config
        :param host_manager_config: the host manager config
        :param snort_ids_manager_config: the Snort IDS manager config
        :param ossec_ids_manager_config: the OSSEC IDS manager config
        :param docker_stats_manager_config: the Docker stats manager config
        :param beats_config: the beats config
        :param elk_config: the ELK config
        :param level: the level of the emulation
        :param version: the version of the emulation
        :param execution_id: the execution id of the emulation
        :param csle_collector_version: the version of the CSLE collector library
        :param csle_ryu_version: the version of the CSLE Ryu library
        """
        self.name = name
        self.descr = descr
        self.containers_config = containers_config
        self.users_config = users_config
        self.flags_config = flags_config
        self.vuln_config = vuln_config
        self.topology_config = topology_config
        self.traffic_config = traffic_config
        self.resources_config = resources_config
        self.kafka_config = kafka_config
        self.services_config = services_config
        self.connections: Dict[str, paramiko.SSHClient] = {}
        self.producer: Union[None, Any] = None
        self.hostname = socket.gethostname()
        self.port_forward_port = 1900
        self.running = False
        self.image = None
        self.id = -1
        self.static_attacker_sequences = static_attacker_sequences
        self.ovs_config = ovs_config
        self.sdn_controller_config = sdn_controller_config
        self.level = level
        self.execution_id = execution_id
        self.version = version
        self.host_manager_config = host_manager_config
        self.snort_ids_manager_config = snort_ids_manager_config
        self.ossec_ids_manager_config = ossec_ids_manager_config
        self.docker_stats_manager_config = docker_stats_manager_config
        self.elk_config = elk_config
        self.beats_config = beats_config
        self.csle_collector_version = csle_collector_version
        self.csle_ryu_version = csle_ryu_version

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationEnvConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        static_attacker_sequences = {}
        for k, v in d["static_attacker_sequences"].items():
            static_attacker_sequences[k] = list(map(lambda x: EmulationAttackerAction.from_dict(x), v))
        sdn_controller_config = None
        if d["sdn_controller_config"] is not None:
            sdn_controller_config = SDNControllerConfig.from_dict(d["sdn_controller_config"])
        obj = EmulationEnvConfig(
            name=d["name"], containers_config=ContainersConfig.from_dict(d["containers_config"]),
            users_config=UsersConfig.from_dict(d["users_config"]),
            flags_config=FlagsConfig.from_dict(d["flags_config"]),
            vuln_config=VulnerabilitiesConfig.from_dict(d["vuln_config"]),
            topology_config=TopologyConfig.from_dict(d["topology_config"]),
            traffic_config=TrafficConfig.from_dict(d["traffic_config"]),
            resources_config=ResourcesConfig.from_dict(d["resources_config"]),
            kafka_config=KafkaConfig.from_dict(d["kafka_config"]),
            services_config=ServicesConfig.from_dict(d["services_config"]),
            descr=d["descr"], static_attacker_sequences=static_attacker_sequences,
            ovs_config=OVSConfig.from_dict(d["ovs_config"]),
            sdn_controller_config=sdn_controller_config,
            level=d["level"], execution_id=d["execution_id"], version=d["version"],
            host_manager_config=HostManagerConfig.from_dict(d["host_manager_config"]),
            ossec_ids_manager_config=OSSECIDSManagerConfig.from_dict(d["ossec_ids_manager_config"]),
            snort_ids_manager_config=SnortIDSManagerConfig.from_dict(d["snort_ids_manager_config"]),
            docker_stats_manager_config=DockerStatsManagerConfig.from_dict(d["docker_stats_manager_config"]),
            elk_config=ElkConfig.from_dict(d["elk_config"]), csle_collector_version=d["csle_collector_version"],
            beats_config=BeatsConfig.from_dict(d["beats_config"]), csle_ryu_version=d["csle_ryu_version"]
        )
        obj.running = d["running"]
        obj.image = d["image"]
        obj.id = d["id"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["name"] = self.name
        d["containers_config"] = self.containers_config.to_dict()
        d["users_config"] = self.users_config.to_dict()
        d["flags_config"] = self.flags_config.to_dict()
        d["vuln_config"] = self.vuln_config.to_dict()
        d["topology_config"] = self.topology_config.to_dict()
        d["traffic_config"] = self.traffic_config.to_dict()
        d["resources_config"] = self.resources_config.to_dict()
        d["kafka_config"] = self.kafka_config.to_dict()
        d["services_config"] = self.services_config.to_dict()
        d["hostname"] = self.hostname
        d["running"] = self.running
        d["image"] = self.image
        d["descr"] = self.descr
        d["id"] = self.id
        d["version"] = self.version
        d["level"] = self.level
        d["execution_id"] = self.execution_id
        d["ovs_config"] = self.ovs_config.to_dict()
        if self.sdn_controller_config is not None:
            d["sdn_controller_config"] = self.sdn_controller_config.to_dict()
        else:
            d["sdn_controller_config"] = None
        d2 = {}
        for k, v in self.static_attacker_sequences.items():
            d2[k] = list(map(lambda x: x.to_dict(), v))
        d["static_attacker_sequences"] = d2
        d["host_manager_config"] = self.host_manager_config.to_dict()
        d["snort_ids_manager_config"] = self.snort_ids_manager_config.to_dict()
        d["ossec_ids_manager_config"] = self.ossec_ids_manager_config.to_dict()
        d["docker_stats_manager_config"] = self.docker_stats_manager_config.to_dict()
        d["elk_config"] = self.elk_config.to_dict()
        d["csle_collector_version"] = self.csle_collector_version
        d["beats_config"] = self.beats_config.to_dict()
        d["csle_ryu_version"] = self.csle_ryu_version
        return d

    def connect(self, ip: str = "", username: str = "", pw: str = "",
                create_producer: bool = False) -> paramiko.SSHClient:
        """
        Connects to the agent's host with SSH, either directly or through a jumphost

        :param ip: the ip to connect to
        :param username: the username to connect with
        :param pw: the password to connect with
        :param create_producer: whether the producer should be created if it not already created

        :return: the created conn
        """
        if ip in self.connections:
            old_conn = self.connections[ip]
            old_conn.close()
        if ip in self.connections:
            self.connections.pop(ip)
        Logger.__call__().get_logger().info(f"Connecting to host: {ip}")
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(ip, username=username, password=pw)
        transport = conn.get_transport()
        if transport is not None:
            transport.set_keepalive(5)
        else:
            raise Exception("Connection Failed")
        self.connections[ip] = conn
        if self.producer is None and create_producer:
            self.create_producer()

        Logger.__call__().get_logger().info("Connected successfully")
        return conn

    def get_connection(self, ip: str) -> paramiko.SSHClient:
        """
        Gets a connection to a given IP address

        :param ip: the ip address to get the connection for
        :return: the connection
        """
        if ip in self.connections and EmulationEnvConfig.check_if_ssh_connection_is_alive(self.connections[ip]):
            return self.connections[ip]
        else:
            raise ConnectionError(f"Connection to ip:{ip} is not active")

    def get_hacker_connection(self) -> paramiko.SSHClient:
        """
        Gets an SSH connection to the hacker agent, creates one if it does not exist

        :return: SSH connection to the hacker
        """
        container = self.containers_config.get_agent_container()
        if container is None:
            raise ValueError("No agent_container obtained")
        else:
            hacker_ip = container.docker_gw_bridge_ip
        connected = False
        if hacker_ip in self.connections and self.connections[hacker_ip] is not None:
            transport = self.connections[hacker_ip].get_transport()
            if transport is not None and transport.is_active():
                try:
                    SSHUtil.execute_ssh_cmds(cmds=["ls > /dev/null"], conn=self.connections[hacker_ip])
                    connected = True
                except Exception:
                    pass
        if not connected:
            self.connect(ip=hacker_ip, username=constants.AGENT.USER, pw=constants.AGENT.PW, create_producer=False)
        return self.connections[hacker_ip]

    def cleanup(self) -> None:
        """
        Cleans up old connections

        :return: None
        """
        for ip, conn in self.connections.items():
            conn.close()
        self.connections = {}

    def create_producer(self) -> None:
        """
        Creates a Kafka producer

        :return: None
        """
        conf = {
            collector_constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY:
                f"{self.kafka_config.container.get_ips()[0]}:{self.kafka_config.kafka_port}",
            collector_constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.producer = Producer(**conf)

    def close_all_connections(self) -> None:
        """
        Closes the emulation connection
        :return: None
        """
        for k, v in self.connections.items():
            v.close()
        self.connections = {}

    @staticmethod
    def check_if_ssh_connection_is_alive(conn: paramiko.SSHClient) -> bool:
        """
        Utility function to check whether a SSH connection is alive or not
        :param conn: the connection to check
        :return: true or false
        """
        alive = False
        transport = conn.get_transport()
        if transport is not None:
            alive = transport.is_active()
        else:
            raise ValueError("Could not obtain transport")
        return alive

    def get_port_forward_port(self) -> int:
        """
        :return: the next port to use for forwarding
        """
        self.port_forward_port += 1
        return self.port_forward_port

    def ids(self) -> bool:
        """
        Check if the configuration includes an IDS

        :return: True if it includes an IDS, otherwise False
        """
        for c in self.containers_config.containers:
            if c.name in constants.CONTAINER_IMAGES.SNORT_IDS_IMAGES:
                return True
        return False

    def get_container_from_ip(self, ip: str) -> Union[NodeContainerConfig, None]:
        """
        Utility function for getting a container with a specific IP

        :param ip: the ip of the container
        :return: the container with the given ip or None
        """
        if ip in self.kafka_config.container.get_ips():
            return self.kafka_config.container
        if ip in self.elk_config.container.get_ips():
            return self.elk_config.container
        if self.sdn_controller_config is not None and ip in self.sdn_controller_config.container.get_ips():
            return self.sdn_controller_config.container
        for c in self.containers_config.containers:
            if ip in c.get_ips():
                return c
        return None

    def __str__(self) -> str:
        """
        :return:  a string representation of the object
        """
        return f"name: {self.name}, containers_config: {self.containers_config}, users_config: {self.users_config}, " \
               f"flags_config: {self.flags_config}, vuln_config: {self.vuln_config}, " \
               f"topology_config: {self.topology_config}, traffic_config: {self.traffic_config}, " \
               f"resources_config: {self.resources_config}, kafka_config:{self.kafka_config}, " \
               f"services_config: {self.services_config}, hostname:{self.hostname}, running: {self.running}, " \
               f"descr: {self.descr}, id:{self.id}, static_attacker_sequences: {self.static_attacker_sequences}," \
               f"ovs_config: {self.ovs_config}, sdn_controller_config: {self.sdn_controller_config}," \
               f" host_manager_config: {self.host_manager_config}, " \
               f"snort_ids_manager_config: {self.snort_ids_manager_config}, " \
               f"ossec_ids_manager_config: {self.ossec_ids_manager_config}, " \
               f"docker_stats_manager_config: {self.docker_stats_manager_config}, elk_config: {self.elk_config}," \
               f" csle_collector_version: {self.csle_collector_version}, beats_config: {self.beats_config}," \
               f" csle_ryu_version: {self.csle_ryu_version}"

    def get_all_ips(self) -> List[str]:
        """
        :return: a list of all ip addresses in the emulation
        """
        ips = set()
        for c in self.containers_config.containers:
            for ip_net in c.ips_and_networks:
                ip, _ = ip_net
                ips.add(ip)
        return list(ips)

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationEnvConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationEnvConfig.from_dict(json.loads(json_str))

    def copy(self) -> "EmulationEnvConfig":
        """
        :return: a copy of the DTO
        """
        return EmulationEnvConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int, physical_servers: List[str]) -> "EmulationEnvConfig":
        """
        Creates an execution config from the base config

        :param ip_first_octet:  the id of the execution
        :param physical_servers: the list of physical servers
        :return: the created execution config
        """
        config = self.copy()
        config.execution_id = ip_first_octet
        config.containers_config = config.containers_config.create_execution_config(
            ip_first_octet=ip_first_octet, physical_servers=physical_servers)
        config.users_config = config.users_config.create_execution_config(ip_first_octet=ip_first_octet)
        config.flags_config = config.flags_config.create_execution_config(ip_first_octet=ip_first_octet)
        config.vuln_config = config.vuln_config.create_execution_config(ip_first_octet=ip_first_octet)
        config.topology_config = config.topology_config.create_execution_config(ip_first_octet=ip_first_octet)
        config.traffic_config = config.traffic_config.create_execution_config(ip_first_octet=ip_first_octet)
        config.resources_config = config.resources_config.create_execution_config(ip_first_octet=ip_first_octet)
        config.kafka_config = config.kafka_config.create_execution_config(ip_first_octet=ip_first_octet,
                                                                          physical_servers=physical_servers)
        config.services_config = config.services_config.create_execution_config(ip_first_octet=ip_first_octet)
        config.ovs_config = config.ovs_config.create_execution_config(ip_first_octet=ip_first_octet,
                                                                      physical_servers=physical_servers)
        config.host_manager_config = config.host_manager_config.create_execution_config(ip_first_octet=ip_first_octet)
        config.snort_ids_manager_config = config.snort_ids_manager_config.create_execution_config(
            ip_first_octet=ip_first_octet)
        config.ossec_ids_manager_config = config.ossec_ids_manager_config.create_execution_config(
            ip_first_octet=ip_first_octet)
        config.docker_stats_manager_config = config.docker_stats_manager_config.create_execution_config(
            ip_first_octet=ip_first_octet)
        config.elk_config = config.elk_config.create_execution_config(
            ip_first_octet=ip_first_octet, physical_servers=physical_servers)
        config.beats_config = config.beats_config.create_execution_config(ip_first_octet=ip_first_octet)
        if config.sdn_controller_config is not None:
            config.sdn_controller_config = config.sdn_controller_config.create_execution_config(
                ip_first_octet=ip_first_octet, physical_servers=physical_servers)
        static_attacker_sequences = {}
        for k, v in config.static_attacker_sequences.items():
            static_attacker_sequences[k] = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet),
                                                    config.static_attacker_sequences[k]))
        config.static_attacker_sequences = static_attacker_sequences
        return config

    def get_network_by_name(self, net_name: str) -> Optional[ContainerNetwork]:
        """
        Gets the network by name from the config

        :param net_name: the name of the network
        :return: the network with the given name
        """
        for c in self.containers_config.networks:
            if c.name == net_name:
                return c
            
        return None
