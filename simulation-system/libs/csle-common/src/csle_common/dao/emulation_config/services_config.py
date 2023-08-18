from typing import List, Dict, Any
from csle_common.dao.emulation_config.node_services_config import NodeServicesConfig
from csle_common.dao.emulation_config.network_service import NetworkService
from csle_base.json_serializable import JSONSerializable


class ServicesConfig(JSONSerializable):
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
        Converts the object to a dict representation
        
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
        services: List[NetworkService] = []
        for service_config in self.services_configs:
            if service_config.ip in ips:
                services = services + service_config.services
        return services

    @staticmethod
    def from_json_file(json_file_path: str) -> "ServicesConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ServicesConfig.from_dict(json.loads(json_str))

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
