from typing import List
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

    def to_dict(self) -> dict:
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