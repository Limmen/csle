from typing import Dict, Any
from csle_common.util.general_util import GeneralUtil


class OVSPort:
    """
    A DTO representing an OVS port
    """

    def __init__(self, port_name: str, container_name: str, ip: str, subnetmask_bits: int,
                 vlan_id: int):
        """
        Initializes the DTO

        :param port_name: the name of the port
        :param container_name: the name of the container to connect with the port
        :param ip: the ipaddress of the container
        :param subnetmask_bits: the number of bits for the subnetmask
        :param vlan_id: the vlan id
        """
        self.port_name = port_name
        self.container_name = container_name
        self.ip = ip
        self.subnetmask_bits = subnetmask_bits
        self.vlan_id = vlan_id

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"port_name: {self.port_name}, " \
               f"container_name: {self.container_name}, " \
               f"ip: {self.ip}, vlan_id: {self.vlan_id}, subnetmask bits: {self.subnetmask_bits}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OVSPort":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = OVSPort(port_name=d["port_name"], container_name=d["container_name"],
                      ip=d["ip"], vlan_id=d["vlan_id"],
                      subnetmask_bits=d["subnetmask_bits"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["port_name"] = self.port_name
        d["container_name"] = self.container_name
        d["ip"] = self.ip
        d["vlan_id"] = self.vlan_id
        d["subnetmask_bits"] = self.subnetmask_bits
        return d

    def copy(self) -> "OVSPort":
        """
        :return: a copy of the DTO
        """
        return OVSPort.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "OVSPort":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.ip = GeneralUtil.replace_first_octet_of_ip(ip=config.ip, ip_first_octet=ip_first_octet)
        config.container_name = config.container_name + f"-{ip_first_octet}"
        return config
