from typing import List, Dict, Any
from csle_common.dao.emulation_config.ovs_switch_config import OvsSwitchConfig


class OVSConfig:
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
        config.switch_configs = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet),
                                         config.switch_configs))
        return config
