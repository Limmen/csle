from typing import Dict, Any


class ClusterNode:
    """
    A DTO Class representing a node in a CSLE cluster
    """

    def __init__(self, ip: str, master: bool):
        """
        Initializes the DTO

        :param ip: the ip of the node
        :param master: boolean indicating whether the node is the master node or not
        """
        self.ip = ip
        self.master = master

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["master"] = self.master
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClusterNode":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = ClusterNode(ip=d["ip"], master=d["master"])
        return dto

    def __str__(self) -> str:
        """
        :return: a string representation of the credential
        """
        return f"ip: {self.ip}, master: {self.master}"

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

    def copy(self) -> "ClusterNode":
        """
        :return: a copy of the DTO
        """
        return ClusterNode.from_dict(self.to_dict())

    @staticmethod
    def schema() -> "ClusterNode":
        """
        :return: get the schema of the DTO
        """
        return ClusterNode(ip="", master=False)
