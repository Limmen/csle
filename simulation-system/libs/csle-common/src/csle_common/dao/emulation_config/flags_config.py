from typing import List, Dict, Any
from csle_common.dao.emulation_config.node_flags_config import NodeFlagsConfig
from csle_common.dao.emulation_config.flag import Flag
from csle_base.json_serializable import JSONSerializable


class FlagsConfig(JSONSerializable):
    """
    A DTO representing the set of flags in an emulation environment
    """

    def __init__(self, node_flag_configs: List[NodeFlagsConfig]):
        """
        Initializes the DTO

        :param node_flag_configs: the list of flags
        """
        self.node_flag_configs = node_flag_configs

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FlagsConfig":
        """
        Converts a dict representation to a an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FlagsConfig(
            node_flag_configs=list(map(lambda x: NodeFlagsConfig.from_dict(x), d["node_flag_configs"]))
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d = {}
        d["node_flag_configs"] = list(map(lambda x: x.to_dict(), self.node_flag_configs))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return ",".join(list(map(lambda x: str(x), self.node_flag_configs)))

    def get_flags_for_ips(self, ips: List[str]) -> List[Flag]:
        """
        Get all flags for a list of ip addresses

        :param ips: the list of ip addresses to get flags for
        :return: the list of flags
        """
        flags: List[Flag] = []
        for node_flag_config in self.node_flag_configs:
            if node_flag_config.ip in ips:
                flags = flags + node_flag_config.flags
        return flags

    @staticmethod
    def from_json_file(json_file_path: str) -> "FlagsConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FlagsConfig.from_dict(json.loads(json_str))

    def copy(self) -> "FlagsConfig":
        """
        :return: a copy of the DTO
        """
        return FlagsConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "FlagsConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.node_flag_configs = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet),
                                        config.node_flag_configs))
        return config
