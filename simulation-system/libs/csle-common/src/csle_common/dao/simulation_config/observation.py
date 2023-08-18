from typing import Dict, Any
from csle_base.json_serializable import JSONSerializable


class Observation(JSONSerializable):
    """
    DTO class representing an observation in a simulation
    """

    def __init__(self, id: int, val: int, descr: str):
        """
        Initializes the DTO

        :param id: the id of the observation
        :param val: in case the val and the id are different
        :param descr: a description of the observation
        """
        self.id = id
        self.val = val
        self.descr = descr

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Observation":
        """
        Converts a dict representation to an instance
        :param d: the dict to convert
        :return: the created instance
        """
        obj = Observation(
            id=d["id"], descr=d["descr"], val=d["val"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["id"] = self.id
        d["descr"] = self.descr
        d["val"] = self.val
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"id: {self.id}, descr: {self.descr}, val: {self.val}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "Observation":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return Observation.from_dict(json.loads(json_str))
