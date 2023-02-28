from typing import Dict, Any


class ClusterNode:
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

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
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
