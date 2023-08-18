from typing import Union, List, Dict, Any
from csle_base.json_serializable import JSONSerializable


class HParam(JSONSerializable):
    """
    DTO class representing a hyperparameter
    """

    def __init__(self, value: Union[int, float, str, List[Any]], name: str, descr: str):
        """
        Initializes the DTO

        :param value: the value of the hyperparameter
        :param name: the name of the hyperparameter
        :param descr: the description of the hyperparameter
        """
        self.value = value
        self.name = name
        self.descr = descr

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d = {}
        d["value"] = self.value
        d["name"] = self.name
        d["descr"] = self.descr
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "HParam":
        """
        Creates an instance from a dict representation

        :param d: the dict reppresentation
        :return: the instance
        """
        obj = HParam(value=d["value"], name=d["name"], descr=d["descr"])
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "HParam":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return HParam.from_dict(json.loads(json_str))
