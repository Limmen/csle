from typing import List, Dict, Any
from csle_common.dao.emulation_config.network_service import NetworkService
from csle_common.util.general_util import GeneralUtil


class NodeServicesConfig:
    """
    A DTO object representing the services configuration of a node in an emulation environment
    """

    def __init__(self, ip: str, services: List[NetworkService]):
        """
        Initializes the DTO

        :param users: the list of node users configuration
        """
        self.ip = ip
        self.services = services

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["services"] = list(map(lambda x: x.to_dict(), self.services))
        d["ip"] = self.ip
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeServicesConfig":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = NodeServicesConfig(ip=d["ip"],
                                 services=list(map(lambda x: NetworkService.from_dict(x), d["services"])))
        return dto

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, services:{}".format(self.ip, ",".join(list(map(lambda x: str(x), self.services))))

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

    def copy(self) -> "NodeServicesConfig":
        """
        :return: a copy of the DTO
        """
        return NodeServicesConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "NodeServicesConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.ip = GeneralUtil.replace_first_octet_of_ip(ip=config.ip, ip_first_octet=ip_first_octet)
        return config
