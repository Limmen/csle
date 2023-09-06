from typing import Dict, Any
from abc import ABC, abstractmethod
from csle_base.encoding.np_encoder import NpEncoder


class JSONSerializable(ABC):
    """
    Abstract class representing objects that are JSON serializable
    """

    @staticmethod
    @abstractmethod
    def from_dict(d: Dict[str, Any]) -> "JSONSerializable":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        pass

    @staticmethod
    @abstractmethod
    def from_json_file(json_file_path: str) -> "JSONSerializable":
        """
        Reads a json file and converts it to an object

        :param json_file_path: the json file path
        :return: the object
        """
        pass

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the object to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    def __eq__(self, other: object) -> bool:
        """
        Compares equality with another object

        :param other: the object to compare with
        :return: True if equals, False otherwise
        """
        if not isinstance(other, JSONSerializable):
            return False
        else:
            return self.to_dict() == other.to_dict()
