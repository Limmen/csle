from typing import List, Dict, Any
import socket
import paramiko
from confluent_kafka import Producer
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.users_config import UsersConfig
from csle_common.dao.emulation_config.flags_config import FlagsConfig
from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.emulation_config.topology_config import TopologyConfig
from csle_common.dao.emulation_config.traffic_config import TrafficConfig
from csle_common.dao.emulation_config.resources_config import ResourcesConfig
from csle_common.dao.emulation_config.log_sink_config import LogSinkConfig
from csle_common.dao.emulation_config.services_config import ServicesConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.util.ssh_util import SSHUtil
from csle_common.logging.log import Logger


class EmulationEnvConfig:
    """
    Class representing the configuration of an emulation
    """

    def __init__(self, name: str, containers_config: ContainersConfig, users_config: UsersConfig,
                 flags_config: FlagsConfig,
                 vuln_config: VulnerabilitiesConfig, topology_config: TopologyConfig, traffic_config: TrafficConfig,
                 resources_config: ResourcesConfig, log_sink_config: LogSinkConfig, services_config: ServicesConfig,
                 descr: str, static_attacker_sequences: Dict[str, List[EmulationAttackerAction]]):
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
        self.log_sink_config = log_sink_config
        self.services_config = services_config
        self.connections = {}
        self.producer = None
        self.hostname = socket.gethostname()
        self.port_forward_port = 1900
        self.running = False
        self.image = None
        self.id = -1
        self.static_attacker_sequences = static_attacker_sequences

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationEnvConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        static_attacker_sequences = {}
        for k,v in d["static_attacker_sequences"].items():
            static_attacker_sequences[k] = list(map(lambda x: EmulationAttackerAction.from_dict(x), v))
        obj = EmulationEnvConfig(
            name = d["name"], containers_config=ContainersConfig.from_dict(d["containers_config"]),
            users_config=UsersConfig.from_dict(d["users_config"]),
            flags_config = FlagsConfig.from_dict(d["flags_config"]),
            vuln_config=VulnerabilitiesConfig.from_dict(d["vuln_config"]),
            topology_config=TopologyConfig.from_dict(d["topology_config"]),
            traffic_config=TrafficConfig.from_dict(d["traffic_config"]),
            resources_config=ResourcesConfig.from_dict(d["resources_config"]),
            log_sink_config=LogSinkConfig.from_dict(d["log_sink_config"]),
            services_config=ServicesConfig.from_dict(d["services_config"]),
            descr=d["descr"], static_attacker_sequences=static_attacker_sequences
        )
        obj.running = d["running"]
        obj.image = d["image"]
        obj.id = d["id"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["name"] = self.name
        d["containers_config"] = self.containers_config.to_dict()
        d["users_config"] = self.users_config.to_dict()
        d["flags_config"] = self.flags_config.to_dict()
        d["vuln_config"] = self.vuln_config.to_dict()
        d["topology_config"] = self.topology_config.to_dict()
        d["traffic_config"] = self.traffic_config.to_dict()
        d["resources_config"] = self.resources_config.to_dict()
        d["log_sink_config"] = self.log_sink_config.to_dict()
        d["services_config"] = self.services_config.to_dict()
        d["hostname"] = self.hostname
        d["running"] = self.running
        d["image"] = self.image
        d["descr"] = self.descr
        d["id"] = self.id
        d2 = {}
        for k,v in self.static_attacker_sequences.items():
            d2[k] = list(map(lambda x: x.to_dict(), v))
        d["static_attacker_sequences"] = d2
        return d

    def connect(self, ip: str = "", username: str = "", pw: str = "", create_producer: bool = False) -> None:
        """
        Connects to the agent's host with SSH, either directly or through a jumphost

        :param ip: the ip to connect to
        :param username: the username to connect with
        :param pw: the password to connect with
        :param create_producer: whether the producer should be created if it not already created

        :return: None
        """
        if ip not in self.connections or (ip in self.connections
                and not EmulationEnvConfig.check_if_ssh_connection_is_alive(self.connections[ip])):
            if ip in self.connections:
                self.connections.pop(ip)
            Logger.__call__().get_logger().info(f"Connecting to host: {ip}")
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(ip, username=username, password=pw)
            conn.get_transport().set_keepalive(5)
            self.connections[ip] = conn
            if self.producer is None and create_producer:
                self.create_producer()

        Logger.__call__().get_logger().info("Connected successfully")

    def get_connection(self, ip: str) -> paramiko.SSHClient:
        """
        Gets a connection to a given IP address

        :param ip: the ip address to get the connection for
        :return: the connection
        """
        if ip in self.connections and EmulationEnvConfig.check_if_ssh_connection_is_alive(self.connections[ip]):
            return self.connections[ip]
        else:
            raise ConnectionError(f"Connection to ip:{ip} is not activep")

    def get_hacker_connection(self) -> paramiko.SSHClient:
        """
        Gets an SSH connection to the hacker agent, creates one if it does not exist

        :return: SSH connection to the hacker
        """
        hacker_ip = self.containers_config.agent_ip
        if hacker_ip in self.connections and self.connections[hacker_ip] is not None \
                and self.connections[hacker_ip].get_transport() is not None \
                and self.connections[hacker_ip].get_transport().is_active():
            try:
                SSHUtil.execute_ssh_cmds(cmds = ["ls"], conn=self.connections[hacker_ip])
            except Exception as e:
                print("reconnecting attacker")
                self.connect(ip=hacker_ip, username=constants.AGENT.USER, pw=constants.AGENT.PW, create_producer=True)
        else:
            self.connect(ip=hacker_ip, username=constants.AGENT.USER, pw=constants.AGENT.PW, create_producer=True)
        return self.connections[hacker_ip]

    def cleanup(self):
        for ip, conn in self.connections.items():
            conn.close()
        self.connections = {}

    def create_producer(self) -> None:
        """
        Creates a Kafka producer

        :return: None
        """
        conf = {'bootstrap.servers': f"{self.log_sink_config.container.get_ips()[0]}:{self.log_sink_config.kafka_port}",
                'client.id': self.hostname}
        self.producer = Producer(**conf)

    def close_all_connections(self) -> None:
        """
        Closes the emulation connection
        :return: None
        """
        for k,v in self.connections.items():
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
        if conn.get_transport() is not None:
            alive = conn.get_transport().is_active()
        return alive

    def get_port_forward_port(self) -> int:
        """
        :return: the next port to use for forwarding
        """
        self.port_forward_port+=1
        return self.port_forward_port

    def ids(self) -> bool:
        """
        Check if the configuration includes an IDS

        :return: True if it includes an IDS, otherwise False
        """
        for c in self.containers_config.containers:
            if c.name in constants.CONTAINER_IMAGES.IDS_IMAGES:
                return True
        return False

    def __str__(self) -> str:
        """
        :return:  a string representation of the object
        """
        return f"name: {self.name}, containers_config: {self.containers_config}, users_config: {self.users_config}, " \
               f"flags_config: {self.flags_config}, vuln_config: {self.vuln_config}, " \
               f"topology_config: {self.topology_config}, traffic_config: {self.traffic_config}, " \
               f"resources_config: {self.resources_config}, log_sink_config:{self.log_sink_config}, " \
               f"services_config: {self.services_config}, hostname:{self.hostname}, running: {self.running}, " \
               f"descr: {self.descr}, id:{self.id}, static_attacker_sequences: {self.static_attacker_sequences}"

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

