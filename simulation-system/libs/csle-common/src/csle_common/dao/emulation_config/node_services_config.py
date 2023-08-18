from typing import List, Dict, Any
from csle_common.dao.emulation_config.network_service import NetworkService
from csle_common.util.general_util import GeneralUtil
from csle_base.json_serializable import JSONSerializable


class NodeServicesConfig(JSONSerializable):
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
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
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

    @staticmethod
    def from_json_file(json_file_path: str) -> "NodeServicesConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NodeServicesConfig.from_dict(json.loads(json_str))

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
