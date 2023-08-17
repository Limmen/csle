from typing import Dict, Any, Union
from csle_base.json_serializable import JSONSerializable


class ClusterNode(JSONSerializable):
    """
    A DTO Class representing a node in a CSLE cluster
    """

    def __init__(self, ip: str, leader: bool, cpus: int, gpus: int, RAM: int):
        """
        Initializes the DTO

        :param ip: the ip of the node
        :param leader: boolean indicating whether the node is the leader node or not
        :param cpus: the number of CPU cores of the node
        :param gpus: the number of GPUs of the node
        :param RAM: the amount of RAM of the node (GB)
        """
        self.ip = ip
        self.leader = leader
        self.cpus = cpus
        self.gpus = gpus
        self.RAM = RAM

    def to_dict(self) -> Dict[str, Union[str, bool, int]]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, bool, int]] = {}
        d["ip"] = self.ip
        d["leader"] = self.leader
        d["cpus"] = self.cpus
        d["gpus"] = self.gpus
        d["RAM"] = self.RAM
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClusterNode":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = ClusterNode(ip=d["ip"], leader=d["leader"], cpus=d["cpus"], gpus=d["gpus"], RAM=d["RAM"])
        return dto

    def __str__(self) -> str:
        """
        :return: a string representation of the credential
        """
        return f"ip: {self.ip}, leader: {self.leader}, cpus: {self.cpus}, gpus: {self.gpus}, RAM: {self.RAM}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "ClusterNode":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ClusterNode.from_dict(json.loads(json_str))

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
        return ClusterNode(ip="", leader=False, cpus=0, gpus=0, RAM=0)
