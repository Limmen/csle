from typing import Dict, Any
from csle_base.json_serializable import JSONSerializable


class Action(JSONSerializable):
    """
    DTO representing an action in a simulation environment
    """

    def __init__(self, id: int, descr: str):
        """
        Initializes the DTO

        :param id: the id of the action
        :param descr: the description of the action
        """
        self.id = id
        self.descr = descr

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Action":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = Action(
            id=d["id"], descr=d["descr"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["id"] = self.id
        d["descr"] = self.descr
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"id:{self.id}, descr:{self.descr}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "Action":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return Action.from_dict(json.loads(json_str))
