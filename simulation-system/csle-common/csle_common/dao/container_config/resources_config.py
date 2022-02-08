from typing import List
from csle_common.dao.container_config.node_resources_config import NodeResourcesConfig


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

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return ",".join(list(map(lambda x: str(x), self.node_resources_configurations)))