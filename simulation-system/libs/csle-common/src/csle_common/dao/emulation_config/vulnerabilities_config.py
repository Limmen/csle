from typing import List, Dict, Any
from csle_common.dao.emulation_config.node_vulnerability_config import NodeVulnerabilityConfig
from csle_base.json_serializable import JSONSerializable


class VulnerabilitiesConfig(JSONSerializable):
    """
    A DTO class representing the vulnerabilities configuration of an emulation environment
    """

    def __init__(self, node_vulnerability_configs: List[NodeVulnerabilityConfig]):
        """
        Initializes the DTO

        :param node_vulnerability_configs: the list of Node vulnerability configurations
        """
        self.node_vulnerability_configs = node_vulnerability_configs

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d = {}
        d["vulnerabilities"] = list(map(lambda x: x.to_dict(), self.node_vulnerability_configs))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "VulnerabilitiesConfig":
        """
        Converts a dict representation of the object to a DTO representation
        :return: a DTO representation of the object
        """
        vulnerabilities = list(map(lambda x: NodeVulnerabilityConfig.from_dict(x),
                                   d["vulnerabilities"]))
        dto = VulnerabilitiesConfig(node_vulnerability_configs=vulnerabilities)
        return dto

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "vulnerabilities:{}".format(",".join(list(map(lambda x: str(x), self.node_vulnerability_configs))))

    def get_vulnerabilities(self, ips: List[str]) -> List[NodeVulnerabilityConfig]:
        """
        Gets a list of vulnerabilities for a list of ip addresses

        :param ips: the list of ip addresse
        :return: the list of vulnerabilities corresponding to the list of ip addresses
        """
        vulnerabilities = []
        for node_vuln_config in self.node_vulnerability_configs:
            if node_vuln_config.ip in ips:
                vulnerabilities.append(node_vuln_config)
        return vulnerabilities

    @staticmethod
    def from_json_file(json_file_path: str) -> "VulnerabilitiesConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return VulnerabilitiesConfig.from_dict(json.loads(json_str))

    def copy(self) -> "VulnerabilitiesConfig":
        """
        :return: a copy of the DTO
        """
        return VulnerabilitiesConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "VulnerabilitiesConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.node_vulnerability_configs = list(map(lambda x: x.create_execution_config(
            ip_first_octet=ip_first_octet), config.node_vulnerability_configs))
        return config
