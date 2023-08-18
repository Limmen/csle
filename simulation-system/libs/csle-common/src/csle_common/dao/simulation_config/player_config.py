from typing import Dict, Any
from csle_base.json_serializable import JSONSerializable


class PlayerConfig(JSONSerializable):
    """
    DTO representing the configuration of a player in a simulation environment in CSLE
    """

    def __init__(self, name: str, id: int, descr: str = ""):
        """
        Initializes the DTO

        :param name: the name of the player
        :param id: the id of the player
        :param descr: the description of the player
        """
        self.name = name
        self.id = id
        self.descr = descr

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PlayerConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = PlayerConfig(name=d["name"], id=int(d["id"]), descr=d["descr"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["name"] = self.name
        d["id"] = self.id
        d["descr"] = self.descr
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name: {self.name}, id: {self.id}, descr: {self.descr}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "PlayerConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return PlayerConfig.from_dict(json.loads(json_str))
