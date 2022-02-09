from typing import List
from csle_common.dao.container_config.node_vulnerability_config import NodeVulnerabilityConfig


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

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "vulnerabilities:{}".format(",".join(list(map(lambda x: str(x), self.vulnerabilities))))