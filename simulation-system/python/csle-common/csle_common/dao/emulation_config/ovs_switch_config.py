from typing import List, Dict, Any
from csle_common.util.general_util import GeneralUtil


class OvsSwitchConfig:
    """
    DTO containing the configuration of an OVS Switch
    """

    def __init__(self, container_name: str, ip: str, openflow_protocols: List[str], controller_ip: str,
                 controller_port: int, controller_transport_protocol: str):
        """
        Initializes the DTO

        :param container_name: the name of the switch container
        :param ip: the ip of the switch container
        :param openflow_protocols: the supported open flow protocols
        :param controller_ip: the ip of the SDN controller
        :param controller_port: the port of the SDN controller
        :param controller_transport_protocol: the transport protocol of the controller
        """
        self.container_name = container_name
        self.ip = ip
        self.openflow_protocols = openflow_protocols
        self.controller_ip = controller_ip
        self.controller_port = controller_port
        self.controller_transport_protocol = controller_transport_protocol

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
                              controller_transport_protocol=d["controller_transport_protocol"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["container_name"] = self.container_name
        d["openflow_protocols"] = self.openflow_protocols
        d["controller_ip"] = self.controller_ip
        d["controller_port"] = self.controller_port
        d["controller_transport_protocol"] = self.controller_transport_protocol
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, container_name: {self.container_name}, openflow_protocols: {self.openflow_protocols}, " \
               f"controller_ip: {self.controller_ip}, controller_port: {self.controller_port}, " \
               f"controller_transport_protocol: {self.controller_transport_protocol}"

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

    def copy(self) -> "OvsSwitchConfig":
        """
        :return: a copy of the DTO
        """
        return OvsSwitchConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "OvsSwitchConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.ip = GeneralUtil.replace_first_octet_of_ip(ip=config.ip, ip_first_octet=ip_first_octet)
        config.controller_ip = GeneralUtil.replace_first_octet_of_ip(ip=config.controller_ip,
                                                                     ip_first_octet=ip_first_octet)
        config.container_name = f"{config.container_name}-{ip_first_octet}"
        return config
