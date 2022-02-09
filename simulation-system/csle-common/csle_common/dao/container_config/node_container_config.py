from typing import List, Tuple
from csle_common.dao.container_config.container_network import ContainerNetwork


class NodeContainerConfig:
    """
    A DTO object representing an individual container in an emulation environment
    """

    def __init__(self, name: str, ips_and_networks: List[Tuple[str, ContainerNetwork]],
                 version: str, level: str, minigame: str, restart_policy: str,
                 suffix: str):
        """
        Intializes the DTO

        :param name: the name of the node container
        :param ips_and_networks: the list of ips and networks that the container is connected to
        :param version: the version of the container
        :param level: the level of the container
        :param minigame: the minigame that it belongs to
        :param restart_policy: the restart policy of the container
        :param suffix: the suffix of the container id
        """
        self.name = name
        self.ips_and_networks = ips_and_networks
        self.version = version
        self.level = level
        self.minigame = minigame
        self.restart_policy = restart_policy
        self.suffix = suffix

    def get_ips(self) -> List[str]:
        """
        :return: a list of ips that this container has
        """
        return list(filter(lambda x: x is not None, map(lambda x: x[0], self.ips_and_networks)))

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["name"] = self.name
        d["ips_and_networks"] = list(map(lambda x: (x[0], x[1].to_dict()), self.ips_and_networks))
        d["version"] = self.version
        d["minigame"] = self.minigame
        d["restart_policy"] = self.restart_policy
        d["suffix"] = self.suffix
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name{self.name}, ips and networks: {self.ips_and_networks}, version: {self.version}, " \
               f"minigame:{self.minigame}, level:{self.level}, restart_policy: {self.restart_policy}, " \
               f"suffix:{self.suffix}"