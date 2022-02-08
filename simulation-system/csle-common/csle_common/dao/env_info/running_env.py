from typing import List
from csle_common.dao.env_info.env_container import EnvContainer
from csle_common.dao.container_config.emulation_env_config import EmulationEnvConfig


class RunningEnv:
    """
    DTO Object representing a running environment
    """

    def __init__(self, containers: List[EnvContainer], name: str, subnet_prefix: str, minigame :str,
                 subnet_mask : str, level: str, config: EmulationEnvConfig):
        """
        Initializes the DTO

        :param containers: the list of running containers
        :param name: the environment name
        :param subnet_prefix: the subnet prefix
        :param minigame: the minigame of the environment
        :param subnet_mask: the subnet mask
        :param level: the level of the environment
        :param config: the configuration of the environment
        """
        self.containers = containers
        self.name = name
        self.subnet_prefix=subnet_prefix
        self.minigame = minigame
        self.subnet_mask = subnet_mask
        self.level = level
        self.config = config

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["containers"] = list(map(lambda x: x.to_dict(), self.containers))
        d["name"] = self.name
        d["subnet_prefix"] = self.subnet_prefix
        d["minigame"] = self.minigame
        d["subnet_mask"] = self.subnet_mask
        d["num_containers"] = len(self.containers)
        d["level"] = self.level
        d["config"] = self.config
        return d