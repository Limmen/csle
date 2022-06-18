from typing import Dict, Any, List, Union
from csle_common.dao.emulation_config.ovs_bridge import OVSBridge
from csle_common.dao.emulation_config.ovs_bridge_connection import OVSBridgeConnection


class OVSConfig:
    """
    DTO representing an OVS config
    """

    def __init__(self, bridges: List[OVSBridge], bridge_connections: List[OVSBridgeConnection]):
        """
        Initializes the DTO

        :param bridges: the bridge configurations
        :param bridge_connections: the bridge connections
        """
        self.bridges = bridges
        self.bridge_connections = bridge_connections


    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"bridges: {list(map(lambda x: str(x), self.bridges))}, " \
               f"bridge_connections: {list(map(lambda x: str(x), self.bridge_connections))}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Union["OVSConfig", None]:
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        if d is None:
            return None
        obj = OVSConfig(bridges = list(map(lambda x: OVSBridge.from_dict(x), d["bridges"])),
                        bridge_connections=list(map(lambda x: OVSBridgeConnection.from_dict(x),
                                                    d["bridge_connections"])))
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["bridges"] = list(map(lambda x: x.to_dict(), self.bridges))
        d["bridge_connections"] = list(map(lambda x: x.to_dict(), self.bridge_connections))
        return d

    def copy(self) -> "OVSConfig":
        """
        :return: a copy of the DTO
        """
        return OVSConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "OVSConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.bridges = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet), config.bridges))
        config.bridge_connections = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet),
                                             config.bridge_connections))
        return config



