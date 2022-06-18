from typing import Dict, Any, List
from csle_common.dao.emulation_config.ovs_port import OVSPort


class OVSBridge:
    """
    A DTO representing an OVS bridge
    """

    def __init__(self, name: str, ports: List[OVSPort]):
        """
        Initializes the bridge

        :param name: the name of the bridge
        :param ports: the OVS ports on the bridge
        """
        self.name = name
        self.ports = ports

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"name: {self.name}, ports: {list(map(lambda x: str(x), self.ports))}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OVSBridge":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = OVSBridge(name=d["name"], ports=list(map(lambda x: OVSPort.from_dict(x), d["ports"])))
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["name"] = self.name
        d["ports"] = list(map(lambda x: x.to_dict(), self.ports))
        return d

    def copy(self) -> "OVSBridge":
        """
        :return: a copy of the DTO
        """
        return OVSBridge.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "OVSBridge":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.ports = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet), config.ports))
        return config
