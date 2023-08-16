from typing import List, Dict, Any
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic
from csle_base.json_serializable import JSONSerializable


class KafkaConfig(JSONSerializable):
    """
    Represents the configuration of the Kafka node in a CSLE emulation
    """

    def __init__(self, container: NodeContainerConfig, resources: NodeResourcesConfig,
                 firewall_config: NodeFirewallConfig,
                 topics: List[KafkaTopic],
                 kafka_manager_log_file: str, kafka_manager_log_dir: str, kafka_manager_max_workers: int,
                 kafka_port: int = 9092, kafka_port_external: int = 9292,
                 time_step_len_seconds: int = 15, kafka_manager_port: int = 50051,
                 version: str = "0.0.1") -> None:
        """
        Initializes the DTO

        :param container: the container for the Kafka server
        :param network: the network
        :param kafka_port: the port that the Kafka server is listening to
        :param kafka_port_external: the external port that the Kafka server is listening to
        :param kafka_manager_port: the default port for gRPC
        :param time_step_len_seconds: the length of a time-step (period for logging)
        :param firewall_config: the firewall configuration
        :param container: the container
        :param topics: list of kafka topics
        :param version: the version
        :param kafka_manager_log_file: log file of the kafka manager
        :param kafka_manager_log_dir: log dir of the kafka manager
        :param kafka_manager_max_workers: maximum number of GRPC workers of the kafka manager
        """
        self.kafka_port = kafka_port
        self.kafka_manager_port = kafka_manager_port
        self.time_step_len_seconds = time_step_len_seconds
        self.version = version
        self.container = container
        self.resources = resources
        self.kafka_port_external = kafka_port_external
        self.topics = topics
        self.firewall_config = firewall_config
        self.kafka_manager_log_file = kafka_manager_log_file
        self.kafka_manager_log_dir = kafka_manager_log_dir
        self.kafka_manager_max_workers = kafka_manager_max_workers

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "KafkaConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = KafkaConfig(
            container=NodeContainerConfig.from_dict(d["container"]),
            resources=NodeResourcesConfig.from_dict(d["resources"]),
            topics=list(map(lambda x: KafkaTopic.from_dict(x), d["topics"])),
            kafka_port=d["kafka_port"], time_step_len_seconds=d["time_step_len_seconds"],
            kafka_manager_port=d["kafka_manager_port"],
            version=d["version"],
            firewall_config=NodeFirewallConfig.from_dict(d["firewall_config"]),
            kafka_manager_log_file=d["kafka_manager_log_file"],
            kafka_manager_log_dir=d["kafka_manager_log_dir"],
            kafka_manager_max_workers=d["kafka_manager_max_workers"],
            kafka_port_external=d["kafka_port_external"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["container"] = self.container.to_dict()
        d["resources"] = self.resources.to_dict()
        d["kafka_port"] = self.kafka_port
        d["kafka_manager_port"] = self.kafka_manager_port
        d["time_step_len_seconds"] = self.time_step_len_seconds
        d["version"] = self.version
        d["topics"] = list(map(lambda x: x.to_dict(), self.topics))
        d["firewall_config"] = self.firewall_config.to_dict()
        d["kafka_manager_max_workers"] = self.kafka_manager_max_workers
        d["kafka_manager_log_dir"] = self.kafka_manager_log_dir
        d["kafka_manager_log_file"] = self.kafka_manager_log_file
        d["kafka_port_external"] = self.kafka_port_external
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"container: {self.container}, " \
               f"kafka server port :{self.kafka_port}, version: {self.version}, resources: {self.resources}, " \
               f"topics: {','.join(list(map(lambda x: str(x), self.topics)))}, " \
               f"kafka_manager_port:{self.kafka_manager_port}, time_step_len_seconds: {self.time_step_len_seconds}, " \
               f"firewall_config: {self.firewall_config}, " \
               f"kafka_manager_log_file: {self.kafka_manager_log_file}, " \
               f"kafka_manager_log_dir: {self.kafka_manager_log_dir}, " \
               f"kafka_manager_max_workers: {self.kafka_manager_max_workers}," \
               f"kafka_port_external: {self.kafka_port_external}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "KafkaConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return KafkaConfig.from_dict(json.loads(json_str))

    def copy(self) -> "KafkaConfig":
        """
        :return: a copy of the DTO
        """
        return KafkaConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int, physical_servers: List[str]) -> "KafkaConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :param physical_servers: the physical servers of the execution
        :return: the new config
        """
        config = self.copy()
        config.container = config.container.create_execution_config(ip_first_octet=ip_first_octet,
                                                                    physical_servers=physical_servers)
        config.resources = config.resources.create_execution_config(ip_first_octet=ip_first_octet)
        config.firewall_config = config.firewall_config.create_execution_config(ip_first_octet=ip_first_octet)
        return config

    @staticmethod
    def schema() -> "KafkaConfig":
        """
        :return: get the schema of the DTO
        """
        return KafkaConfig(container=NodeContainerConfig.schema(), resources=NodeResourcesConfig.schema(),
                           firewall_config=NodeFirewallConfig.schema(), topics=[KafkaTopic.schema()],
                           kafka_manager_max_workers=10, kafka_manager_log_dir="/",
                           kafka_manager_log_file="kafka_manager.log")
