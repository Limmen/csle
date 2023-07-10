from typing import List, Dict, Any
from csle_common.dao.emulation_config.ovs_switch_config import OvsSwitchConfig
from csle_base.json_serializable import JSONSerializable


class OVSConfig(JSONSerializable):
    """
    DTO containing the configuration of OVS in an emulation
    """

    def __init__(self, switch_configs: List[OvsSwitchConfig]):
        """
        Initializes the DTO

        :param switch_configs: list of OVS switch configs
        """
        self.switch_configs = switch_configs

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OVSConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = OVSConfig(switch_configs=list(map(lambda x: OvsSwitchConfig.from_dict(x), d["switch_configs"])))
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d = {}
        d["switch_configs"] = list(map(lambda x: x.to_dict(), self.switch_configs))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"switch_configs:{list(map(lambda x: str(x), self.switch_configs))}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "OVSConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return OVSConfig.from_dict(json.loads(json_str))

    def copy(self) -> "OVSConfig":
        """
        :return: a copy of the DTO
        """
        return OVSConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int, physical_servers: List[str]) -> "OVSConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :param physical_servers: the list of physical servers of the execution
        :return: the new config
        """
        config = self.copy()
        config.switch_configs = list(map(lambda x: x.create_execution_config(
            ip_first_octet=ip_first_octet, physical_servers=physical_servers), config.switch_configs))
        return config
