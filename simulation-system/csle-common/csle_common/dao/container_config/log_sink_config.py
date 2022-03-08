from csle_common.dao.container_config.node_container_config import NodeContainerConfig


class LogSinkConfig:
    """
    Represents the configuration of a LogSink in CSLE
    """

    def __init__(self, name: str,
                 container: NodeContainerConfig,
                 port: int= 9092,
                 version: str = "0.0.1"):
        """
        Initializes the DTO

        :param name: the name of the log sink
        :param container: the container for the Kafka server
        :param network: the network
        :param port: the port that the Kafka server is listening to
        :param container: the container
        :param version: the version
        """
        self.name = name
        self.port = port
        self.version = version
        self.container = container

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["name"] = self.name
        d["container"] = self.container.to_dict()
        d["port"] = self.port
        d["version"] = self.version
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name:{self.name}, container: {self.container}, " \
               f"port:{self.port}, version: {self.version}"

