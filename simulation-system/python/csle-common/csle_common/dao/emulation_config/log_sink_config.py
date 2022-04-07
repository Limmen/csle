from typing import List, Dict, Any
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic


class LogSinkConfig:
    """
    Represents the configuration of a LogSink in CSLE
    """

    def __init__(self, container: NodeContainerConfig, resources: NodeResourcesConfig, topics: List[KafkaTopic],
                 kafka_port: int= 9092, time_step_len_seconds = 15, default_grpc_port = 50051,
                 secondary_grpc_port = 50049,
                 version: str = "0.0.1") -> None:
        """
        Initializes the DTO

        :param container: the container for the Kafka server
        :param network: the network
        :param kafka_port: the port that the Kafka server is listening to
        :param default_grpc_port: the default port for gRPC
        :param time_step_len_seconds: the length of a time-step (period for logging)
        :param container: the container
        :param topics: list of kafka topics
        :param version: the version
        """
        self.kafka_port = kafka_port
        self.default_grpc_port = default_grpc_port
        self.time_step_len_seconds = time_step_len_seconds
        self.version = version
        self.container = container
        self.resources = resources
        self.topics = topics
        self.secondary_grpc_port = secondary_grpc_port

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LogSinkConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = LogSinkConfig(
            container=NodeContainerConfig.from_dict(d["container"]),
            resources=NodeResourcesConfig.from_dict(d["resources"]),
            topics = list(map(lambda x: KafkaTopic.from_dict(x), d["topics"])),
            kafka_port=d["kafka_port"], time_step_len_seconds=d["time_step_len_seconds"],
            default_grpc_port=d["default_grpc_port"], secondary_grpc_port=d["secondary_grpc_port"],
            version=d["version"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["container"] = self.container.to_dict()
        d["resources"] = self.resources.to_dict()
        d["kafka_port"] = self.kafka_port
        d["default_grpc_port"] = self.default_grpc_port
        d["secondary_grpc_port"] = self.secondary_grpc_port
        d["time_step_len_seconds"] = self.time_step_len_seconds
        d["version"] = self.version
        d["topics"] = list(map(lambda x: x.to_dict(), self.topics))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"container: {self.container}, " \
               f"port:{self.kafka_port}, version: {self.version}, resources: {self.resources}, " \
               f"topics: {','.join(list(map(lambda x: str(x), self.topics)))}, " \
               f"default_grpc_port:{self.default_grpc_port}, time_step_len_seconds: {self.time_step_len_seconds}, " \
               f"secondary_grpc_port:{self.secondary_grpc_port}"

