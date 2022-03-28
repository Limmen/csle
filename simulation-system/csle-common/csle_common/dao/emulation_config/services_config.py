from typing import List
from csle_common.dao.emulation_config.node_services_config import NodeServicesConfig


class ServicesConfig:
    """
    A DTO object representing the services configuration of an emulation environment
    """

    def __init__(self, services_configs : List[NodeServicesConfig]):
        """
        Initializes the DTO

        :param users: the list of node users configuration
        """
        self.services_configs = services_configs

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["services_configs"] = list(map(lambda x: x.to_dict(), self.services_configs))
        return d

    @staticmethod
    def from_dict(d) -> "ServicesConfig":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = ServicesConfig(services_configs=list(map(lambda x: NodeServicesConfig.from_dict(x),
                                                       d["services_configs"])))
        return dto

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "services_configs:{}".format(",".join(list(map(lambda x: str(x), self.services_configs))))