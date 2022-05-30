from typing import List, Dict, Any
from csle_common.dao.docker.docker_container_metadata import DockerContainerMetadata
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.log_sink_config import LogSinkConfig


class DockerEnvMetadata:
    """
    DTO Object representing a running environment
    """

    def __init__(self, containers: List[DockerContainerMetadata], name: str, subnet_prefix: str,
                 subnet_mask : str, level: str, config: EmulationEnvConfig, log_sink_config: LogSinkConfig):
        """
        Initializes the DTO

        :param containers: the list of running containers
        :param name: the environment name
        :param subnet_prefix: the subnet prefix
        :param subnet_mask: the subnet mask
        :param level: the level of the environment
        :param config: the configuration of the environment
        :param logsink_config: the configuration of the log sink
        """
        self.containers = containers
        self.name = name
        self.subnet_prefix=subnet_prefix
        self.subnet_mask = subnet_mask
        self.level = level
        self.config = config
        self.log_sink_config = log_sink_config


    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DockerEnvMetadata":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = DockerEnvMetadata(
            containers=list(map(lambda x: DockerContainerMetadata.from_dict(x), d["containers"])),
            name=d["name"], subnet_prefix=d["subnet_prefix"], subnet_mask=d["subnet_mask"],
            level=d["level"], config=d["config"], log_sink_config=LogSinkConfig.from_dict(d["log_sink_config"])
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["containers"] = list(map(lambda x: x.to_dict(), self.containers))
        d["name"] = self.name
        d["subnet_prefix"] = self.subnet_prefix
        d["subnet_mask"] = self.subnet_mask
        d["num_containers"] = len(self.containers)
        d["level"] = self.level
        if self.config is not None:
            d["config"] = self.config.to_dict()
        else:
            d["config"] = {}
        if self.log_sink_config is not None:
            d["log_sink_config"] = self.log_sink_config.to_dict()
        else:
            d["log_sink_config"] = {}
        return d

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)