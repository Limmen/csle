from typing import List
from csle_common.dao.emulation_config.node_services_config import NodeServicesConfig
from csle_common.dao.emulation_config.network_service import NetworkService

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

    def get_services_for_ips(self, ips: List[str]) -> List[NetworkService]:
        """
        Gets all services for a list ip addresses

        :param ips: the list of ips
        :return: the list of services
        """
        services = []
        for service_config in self.services_configs:
            if service_config.ip in ips:
                services = services + service_config.services
        return services