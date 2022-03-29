from typing import List
from csle_common.dao.emulation_config.node_vulnerability_config import NodeVulnerabilityConfig


class VulnerabilitiesConfig:
    """
    A DTO class representing the vulnerabilities configuration of an emulation environment
    """

    def __init__(self, node_vulnerability_configs : List[NodeVulnerabilityConfig]):
        """
        Initializes the DTO

        :param node_vulnerability_configs: the list of Node vulnerability configurations
        """
        self.node_vulnerability_configs = node_vulnerability_configs

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["vulnerabilities"] = list(map(lambda x: x.to_dict(), self.node_vulnerability_configs))
        return d

    @staticmethod
    def from_dict(d) -> "VulnerabilitiesConfig":
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