import socket
import paramiko
from confluent_kafka import Producer
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.users_config import UsersConfig
from csle_common.dao.emulation_config.flags_config import FlagsConfig
from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.emulation_config.topology import Topology
from csle_common.dao.emulation_config.traffic_config import TrafficConfig
from csle_common.dao.emulation_config.resources_config import ResourcesConfig
from csle_common.dao.emulation_config.log_sink_config import LogSinkConfig
from csle_common.dao.emulation_config.services_config import ServicesConfig


class EmulationEnvConfig:
    """
    Class representing the configuration of an emulation
    """

    def __init__(self, name: str, containers_config: ContainersConfig, users_config: UsersConfig,
                 flags_config: FlagsConfig,
                 vuln_config: VulnerabilitiesConfig, topology_config: Topology, traffic_config: TrafficConfig,
                 resources_config: ResourcesConfig, log_sink_config: LogSinkConfig, services_config: ServicesConfig):
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
        """
        self.name = name
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

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["name"] = self.name
        d["containers_config"] = self.containers_config.to_dict()
        d["users_config"] = self.users_config.to_dict()
        d["flags_config"] = self.flags_config.to_dict()
        d["vuln_config"] = len(self.vuln_config.to_dict())
        d["topology_config"] = self.topology_config.to_dict()
        d["traffic_config"] = self.traffic_config.to_dict()
        d["resources_config"] = self.resources_config.to_dict()
        d["log_sink_config"] = self.log_sink_config.to_dict()
        d["services_config"] = self.services_config.to_dict()
        d["hostname"] = self.hostname
        return d

    def connect(self, ip: str = "", username: str = "", pw: str = "") -> None:
        """
        Connects to the agent's host with SSH, either directly or through a jumphost

        :param ip: the ip to connect to
        :param username: the username to connect with
        :param pw: the password to connect with

        :return: None
        """
        if ip not in self.connections:
            print(f"Connecting to host: {ip}")
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(ip, username=username, password=pw)
            self.connections[ip] = conn

        print("Connected successfully")

    def create_producer(self) -> None:
        """
        Creates a Kafka producer

        :return: None
        """
        conf = {'bootstrap.servers': f"{self.log_sink_config.container.get_ips()[0]}:{self.log_sink_config.kafka_port}",
                'client.id': self.hostname}
        self.producer = Producer(**conf)


    def close(self) -> None:
        """
        Closes the emulation connection
        :return: None
        """
        for k,v in self.connections.items():
            v.close()
        self.connections = {}

    def __str__(self) -> str:
        """
        :return:  a string representation of the object
        """
        return f"name: {self.name}, containers_config: {self.containers_config}, users_config: {self.users_config}, " \
               f"flags_config: {self.flags_config}, vuln_config: {self.vuln_config}, " \
               f"topology_config: {self.topology_config}, traffic_config: {self.traffic_config}, " \
               f"resources_config: {self.resources_config}, log_sink_config:{self.log_sink_config}, " \
               f"services_config: {self.services_config}, hostname:{self.hostname}"

