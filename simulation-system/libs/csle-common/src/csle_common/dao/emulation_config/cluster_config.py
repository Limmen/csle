from typing import Dict, Any, List
from csle_common.dao.emulation_config.cluster_node import ClusterNode


class ClusterConfig:
    """
    A DTO Class representing the config of a CSLE cluster
    """

    def __init__(self, cluster_nodes: List[ClusterNode]):
        """
        Initializes the DTO

        :param cluster_nodes: the list of cluster nodes
        """
        self.cluster_nodes = cluster_nodes

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["cluster_nodes"] = list(map(lambda x: x.to_dict(), self.cluster_nodes))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClusterConfig":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = ClusterConfig(cluster_nodes=list(map(lambda x: ClusterNode.from_dict(x), d["cluster_nodes"])))
        return dto

    def __str__(self) -> str:
        """
        :return: a string representation of the credential
        """
        return f"cluster_nodes: {list(map(lambda x: str(x), self.cluster_nodes))}"

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

    def copy(self) -> "ClusterConfig":
        """
        :return: a copy of the DTO
        """
        return ClusterConfig.from_dict(self.to_dict())

    @staticmethod
    def schema() -> "ClusterConfig":
        """
        :return: get the schema of the DTO
        """
        return ClusterConfig(cluster_nodes=[])
