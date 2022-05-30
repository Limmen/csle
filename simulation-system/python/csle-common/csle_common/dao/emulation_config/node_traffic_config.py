from typing import List, Dict, Any


class NodeTrafficConfig:
    """
    A DTO object representing the traffic configuration of an individual container in an emulation
    """

    def __init__(self, ip: str, commands: List[str]):
        """
        Creates a NodeTrafficConfig DTO Object

        :param ip: the ip of the node that generate the traffic
        :param commands: the commands used to generate the traffic
        """
        self.ip = ip
        self.commands = commands


    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeTrafficConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj= NodeTrafficConfig(
            ip=d["ip"], commands=d["commands"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["commands"] = self.commands
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, commands:{}".format(self.ip, self.commands)

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