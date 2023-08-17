from typing import List, Dict, Any
from csle_common.util.general_util import GeneralUtil
from csle_base.json_serializable import JSONSerializable


class OvsSwitchConfig(JSONSerializable):
    """
    DTO containing the configuration of an OVS Switch
    """

    def __init__(self, container_name: str, ip: str, openflow_protocols: List[str], controller_ip: str,
                 controller_port: int, controller_transport_protocol: str, docker_gw_bridge_ip: str = "",
                 physical_host_ip: str = ""):
        """
        Initializes the DTO

        :param container_name: the name of the switch container
        :param ip: the ip of the switch container
        :param openflow_protocols: the supported open flow protocols
        :param controller_ip: the ip of the SDN controller
        :param controller_port: the port of the SDN controller
        :param controller_transport_protocol: the transport protocol of the controller
        :param docker_gw_bridge_ip: IP to reach the container from the host network
        :param physical_host_ip: IP of the physical host where the container is running
        """
        self.container_name = container_name
        self.ip = ip
        self.openflow_protocols = openflow_protocols
        self.controller_ip = controller_ip
        self.controller_port = controller_port
        self.controller_transport_protocol = controller_transport_protocol
        self.docker_gw_bridge_ip = docker_gw_bridge_ip
        self.physical_host_ip = physical_host_ip

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OvsSwitchConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = OvsSwitchConfig(container_name=d["container_name"], ip=d["ip"],
                              openflow_protocols=d["openflow_protocols"], controller_ip=d["controller_ip"],
                              controller_port=d["controller_port"],
                              controller_transport_protocol=d["controller_transport_protocol"],
                              docker_gw_bridge_ip=d["docker_gw_bridge_ip"],
                              physical_host_ip=d["physical_host_ip"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["ip"] = self.ip
        d["container_name"] = self.container_name
        d["openflow_protocols"] = self.openflow_protocols
        d["controller_ip"] = self.controller_ip
        d["controller_port"] = self.controller_port
        d["controller_transport_protocol"] = self.controller_transport_protocol
        d["docker_gw_bridge_ip"] = self.docker_gw_bridge_ip
        d["physical_host_ip"] = self.physical_host_ip
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, container_name: {self.container_name}, openflow_protocols: {self.openflow_protocols}, " \
               f"controller_ip: {self.controller_ip}, controller_port: {self.controller_port}, " \
               f"controller_transport_protocol: {self.controller_transport_protocol}, " \
               f"docker_gw_bridge_ip: {self.docker_gw_bridge_ip}, physical_host_ip: {self.physical_host_ip}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "OvsSwitchConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return OvsSwitchConfig.from_dict(json.loads(json_str))

    def copy(self) -> "OvsSwitchConfig":
        """
        :return: a copy of the DTO
        """
        return OvsSwitchConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int, physical_servers: List[str]) -> "OvsSwitchConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :param physical_servers: the list of physical servers of the execution
        :return: the new config
        """
        config = self.copy()
        config.ip = GeneralUtil.replace_first_octet_of_ip(ip=config.ip, ip_first_octet=ip_first_octet)
        config.controller_ip = GeneralUtil.replace_first_octet_of_ip(ip=config.controller_ip,
                                                                     ip_first_octet=ip_first_octet)
        config.container_name = f"{config.container_name}-{ip_first_octet}"
        config.physical_host_ip = physical_servers[0]  # TODO Update this
        return config
