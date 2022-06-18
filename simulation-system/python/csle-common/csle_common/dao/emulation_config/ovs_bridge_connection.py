from typing import Dict, Any
from csle_common.dao.emulation_config.ovs_bridge import OVSBridge


class OVSBridgeConnection:
    """
    DTO representing a bridge-to-bridge OVS connection
    """

    def __init__(self, bridge_1: OVSBridge, bridge_2: OVSBridge, port_1_name: str, port_2_name: str):
        """
        Initializes the DTO

        :param bridge_1: the first bridge
        :param bridge_2: the second bridge
        :param port_1_name: the name of the port on the first bridge
        :param port_2_name: the name of the port on the second bridge
        """
        self.bridge_1 = bridge_1
        self.bridge_2 = bridge_2
        self.port_1_name = port_1_name
        self.port_2_name = port_2_name

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"bridge_1: {self.bridge_1}, bridge_1: {self.bridge_2}, port_1_name: {self.port_1_name}, " \
               f"port_2_name: {self.port_2_name}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OVSBridgeConnection":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = OVSBridgeConnection(bridge_1=OVSBridge.from_dict(d["bridge_1"]),
                                  bridge_2=OVSBridge.from_dict(d["bridge_2"]), port_1_name=d["port_1_name"],
                                  port_2_name=d["port_2_name"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["bridge_1"] = self.bridge_1.to_dict()
        d["bridge_2"] = self.bridge_2.to_dict()
        d["port_1_name"] = self.port_1_name
        d["port_2_name"] = self.port_2_name
        return d

    def copy(self) -> "OVSBridgeConnection":
        """
        :return: a copy of the DTO
        """
        return OVSBridgeConnection.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "OVSBridgeConnection":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.bridge_1 = config.bridge_1.create_execution_config(ip_first_octet=ip_first_octet)
        config.bridge_2 = config.bridge_1.create_execution_config(ip_first_octet=ip_first_octet)
        return config
