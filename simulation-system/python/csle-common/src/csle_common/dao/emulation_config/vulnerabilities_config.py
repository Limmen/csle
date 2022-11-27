from typing import List, Dict, Any
from csle_common.dao.emulation_config.node_vulnerability_config import NodeVulnerabilityConfig


class VulnerabilitiesConfig:
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
