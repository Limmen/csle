from typing import List, Dict, Any
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig


class ResourcesConfig:
    """
    A DTO representing the resources assigned to the containers in an emulation environment
    """

    def __init__(self, node_resources_configurations : List[NodeResourcesConfig]):
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