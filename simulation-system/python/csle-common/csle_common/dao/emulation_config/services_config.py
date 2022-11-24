from typing import List, Dict, Any
from csle_common.dao.emulation_config.node_services_config import NodeServicesConfig
from csle_common.dao.emulation_config.network_service import NetworkService


class ServicesConfig:
    """
    A DTO object representing the services configuration of an emulation environment
    """

    def __init__(self, services_configs: List[NodeServicesConfig]):
        """
        Initializes the DTO

        :param users: the list of node users configuration
        """
        self.services_configs = services_configs

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["services_configs"] = list(map(lambda x: x.to_dict(), self.services_configs))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ServicesConfig":
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

    def copy(self) -> "ServicesConfig":
        """
        :return: a copy of the DTO
        """
        return ServicesConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "ServicesConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.services_configs = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet),
                                           self.services_configs))
        return config
