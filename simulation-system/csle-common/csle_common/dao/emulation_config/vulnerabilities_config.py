from typing import List
from csle_common.dao.emulation_config.node_vulnerability_config import NodeVulnerabilityConfig


class VulnerabilitiesConfig:
    """
    A DTO class representing the vulnerabilities configuration of an emulation environment
    """

    def __init__(self, vulnerabilities : List[NodeVulnerabilityConfig]):
        """
        Initializes the DTO

        :param vulnerabilities: the list of Node vulnerability configurations
        """
        self.vulnerabilities = vulnerabilities

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["vulnerabilities"] = list(map(lambda x: x.to_dict(), self.vulnerabilities))
        return d

    @staticmethod
    def from_dict(d) -> "VulnerabilitiesConfig":
        """
        Converts a dict representation of the object to a DTO representation
        :return: a DTO representation of the object
        """
        vulnerabilities = list(map(lambda x: NodeVulnerabilityConfig.from_dict(x),
                                   d["vulnerabilities"]))
        dto = VulnerabilitiesConfig(vulnerabilities=vulnerabilities)
        return dto

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "vulnerabilities:{}".format(",".join(list(map(lambda x: str(x), self.vulnerabilities))))