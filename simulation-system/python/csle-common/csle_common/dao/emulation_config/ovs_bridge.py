from typing import Dict, Any, List
from csle_common.dao.emulation_config.ovs_port import OVSPort


class OVSBridge:
    """
    A DTO representing an OVS bridge
    """

    def __init__(self, level: int, exec_id: int, version: str, bridge_id: int, ports: List[OVSPort]):
        """
        Initializes the bridge

        :param level: the level of the emulation
        :param exec_id: the execution id of the emulation
        :param bridge_id: the id of the bridge
        :param version: the version of the emulation
        :param ports: the OVS ports on the bridge
        """
        self.level = level
        self.ports = ports
        self.bridge_id = bridge_id
        self.exec_id = exec_id
        self.version = version

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"level: {self.level}, ports: {list(map(lambda x: str(x), self.ports))}, bridge_id: {self.level}," \
               f"exec_id: {self.exec_id}, version: {self.version}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OVSBridge":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = OVSBridge(level=d["level"], ports=list(map(lambda x: OVSPort.from_dict(x), d["ports"])),
                        exec_id=d["exec_id"], bridge_id=d["bridge_id"], version=d["version"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["level"] = self.level
        d["exec_id"] = self.exec_id
        d["version"] = self.version
        d["bridge_id"] = self.bridge_id
        d["ports"] = list(map(lambda x: x.to_dict(), self.ports))
        return d

    def get_name(self) -> str:
        """
        :return: the bridge name
        """
        return f"{self.level}-{self.version.replace('.', '')}-{self.bridge_id}-{self.exec_id}"

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
        config.exec_id = ip_first_octet
        return config
