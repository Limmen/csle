from typing import List, Dict, Any, Union
from csle_common.dao.emulation_config.node_beats_config import NodeBeatsConfig


class BeatsConfig:
    """
    A DTO object representing the beats configuration of an emulation environment
    """

    def __init__(self, node_beats_configs: List[NodeBeatsConfig], num_elastic_shards: int, reload_enabled: bool):
        """
        Initializes the DTO

        :param node_beats_configs: the list of node beats configurations
        :param num_elastic_shards: shards of elasticsearch
        :param reload_enabled: whether reload of beats configurations is enabled
        """
        self.node_beats_configs = node_beats_configs
        self.num_elastic_shards = num_elastic_shards
        self.reload_enabled = reload_enabled

    def get_node_beats_config_by_ips(self, ips: List[str]) -> Union[NodeBeatsConfig, None]:
        """
        Gets a node beats config which matches a list of ips

        :param ips: the ips
        :return: the node beats config or None
        """
        for node_beats_config in self.node_beats_configs:
            if node_beats_config.ip in ips:
                return node_beats_config
        return None

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "BeatsConfig":
        """
        Converts a dict representation of the object into a an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = BeatsConfig(
            node_beats_configs=list(map(lambda x: NodeBeatsConfig.from_dict(x), d["node_beats_configs"])),
            num_elastic_shards=d["num_elastic_shards"], reload_enabled=d["reload_enabled"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["node_beats_configs"] = list(map(lambda x: x.to_dict(), self.node_beats_configs))
        d["num_elastic_shards"] = self.num_elastic_shards
        d["reload_enabled"] = self.reload_enabled
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"node_beats_configs:{','.join(list(map(lambda x: str(x), self.node_beats_configs)))}, " \
               f"num_elastic_shards: {self.num_elastic_shards}, reload_enabled: {self.reload_enabled}"

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

    def copy(self) -> "BeatsConfig":
        """
        :return: a copy of the DTO
        """
        return BeatsConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "BeatsConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.node_beats_configs = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet),
                                             config.node_beats_configs))
        return config
