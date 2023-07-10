from typing import List, Dict, Any
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_base.json_serializable import JSONSerializable


class ResourcesConfig(JSONSerializable):
    """
    A DTO representing the resources assigned to the containers in an emulation environment
    """

    def __init__(self, node_resources_configurations: List[NodeResourcesConfig]):
        """
        Initializes the DTO

        :param node_resources_configurations: the list resource configurations for each node
        """
        self.node_resources_configurations = node_resources_configurations

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ResourcesConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ResourcesConfig(
            node_resources_configurations=list(map(lambda x: NodeResourcesConfig.from_dict(x),
                                                   d["node_resources_configurations"]))
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d = {}
        d["node_resources_configurations"] = list(map(lambda x: x.to_dict(), self.node_resources_configurations))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return ",".join(list(map(lambda x: str(x), self.node_resources_configurations)))

    @staticmethod
    def from_json_file(json_file_path: str) -> "ResourcesConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ResourcesConfig.from_dict(json.loads(json_str))

    def copy(self) -> "ResourcesConfig":
        """
        :return: a copy of the DTO
        """
        return ResourcesConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "ResourcesConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.node_resources_configurations = list(map(lambda x: x.create_execution_config(
            ip_first_octet=ip_first_octet), self.node_resources_configurations))
        return config
