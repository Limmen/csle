from typing import List
from csle_common.dao.container_config.node_container_config import NodeContainerConfig
from csle_common.dao.container_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.container_config.kafka_topic import KafkaTopic


class LogSinkConfig:
    """
    Represents the configuration of a LogSink in CSLE
    """

    def __init__(self, name: str,
                 container: NodeContainerConfig,
                 resources: NodeResourcesConfig,
                 topics: List[KafkaTopic],
                 kafka_port: int= 9092,
                 kafka_manager_port=50051,
                 version: str = "0.0.1"):
        """
        Initializes the DTO

        :param name: the name of the log sink
        :param container: the container for the Kafka server
        :param network: the network
        :param kafka_port: the port that the Kafka server is listening to
        :param kafka_manager_port: the port that the Kafka manager is listening to
        :param container: the container
        :param topics: list of kafka topics
        :param version: the version
        """
        self.name = name
        self.kafka_port = kafka_port
        self.kafka_manager_port = kafka_manager_port
        self.version = version
        self.container = container
        self.resources = resources
        self.topics = topics

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["name"] = self.name
        d["container"] = self.container.to_dict()
        d["resources"] = self.resources.to_dict()
        d["kafka_port"] = self.kafka_port
        d["kafka_manager_port"] = self.kafka_manager_port
        d["version"] = self.version
        d["topics"] = list(map(lambda x: x.to_dict(), self.topics))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name:{self.name}, container: {self.container}, " \
               f"port:{self.kafka_port}, version: {self.version}, resources: {self.resources}, " \
               f"topics: {','.join(list(map(lambda x: str(x), self.topics)))}, " \
               f"kafka_manager_port:{self.kafka_manager_port}"

