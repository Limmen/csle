from typing import List, Dict, Any, Union
from csle_common.dao.docker.docker_container_metadata import DockerContainerMetadata
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_base.json_serializable import JSONSerializable


class DockerEnvMetadata(JSONSerializable):
    """
    DTO Object representing a running environment
    """

    def __init__(self, containers: List[DockerContainerMetadata], name: str, subnet_prefix: str,
                 subnet_mask: str, level: str, config: Union[None, EmulationEnvConfig],
                 kafka_config: Union[None, KafkaConfig]):
        """
        Initializes the DTO

        :param containers: the list of running containers
        :param name: the environment name
        :param subnet_prefix: the subnet prefix
        :param subnet_mask: the subnet mask
        :param level: the level of the environment
        :param config: the configuration of the environment
        :param kafka_config: the kafka configuration
        """
        self.containers = containers
        self.name = name
        self.subnet_prefix = subnet_prefix
        self.subnet_mask = subnet_mask
        self.level = level
        self.config = config
        self.kafka_config = kafka_config

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DockerEnvMetadata":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        config = None
        kafka_config = None
        if d["config"] is not None:
            config = EmulationEnvConfig.from_dict(d["config"])
        if d["kafka_config"] is not None:
            config = KafkaConfig.from_dict(d["kafka_config"])
        obj = DockerEnvMetadata(
            containers=list(map(lambda x: DockerContainerMetadata.from_dict(x), d["containers"])),
            name=d["name"], subnet_prefix=d["subnet_prefix"], subnet_mask=d["subnet_mask"],
            level=d["level"], config=config, kafka_config=kafka_config)
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["containers"] = list(map(lambda x: x.to_dict(), self.containers))
        d["name"] = self.name
        d["subnet_prefix"] = self.subnet_prefix
        d["subnet_mask"] = self.subnet_mask
        d["num_containers"] = len(self.containers)
        d["level"] = self.level
        if self.config is not None:
            d["config"] = self.config.to_dict()
        else:
            d["config"] = None
        if self.kafka_config is not None:
            d["kafka_config"] = self.kafka_config.to_dict()
        else:
            d["kafka_config"] = None
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "DockerEnvMetadata":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return DockerEnvMetadata.from_dict(json.loads(json_str))
