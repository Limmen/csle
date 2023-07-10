from typing import Dict, Any, List
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_base.json_serializable import JSONSerializable


class ClusterConfig(JSONSerializable):
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
        Converts the object to a dict representation

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

    @staticmethod
    def from_json_file(json_file_path: str) -> "ClusterConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ClusterConfig.from_dict(json.loads(json_str))

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
