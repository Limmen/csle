from typing import Dict, Any, Union
from csle_base.json_serializable import JSONSerializable


class Flag(JSONSerializable):
    """
    Class that represents a flag in the environment
    """

    def __init__(self, name: str, dir: str, id: int, path: str, requires_root: bool = False, score: int = 1):
        """
        Initializes the DTO

        :param name: the name of the flag
        :param id: the id of the flag
        :param dir: the directory
        :param path: the path of the flag
        :param requires_root: whether the flag requires root or not
        :param score: the score of the flag
        """
        self.name = name
        self.id = id
        self.path = path
        self.requires_root = requires_root
        self.score = score
        self.dir = dir

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "name:{}, id:{}, path:{}, requires_root:{}, score:{}, dir:{}".format(
            self.name, self.id, self.path, self.requires_root, self.score, self.dir
        )

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Flag":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = Flag(
            name=d["name"], dir=d["dir"], id=d["id"], path=d["path"], requires_root=d["requires_root"],
            score=d["score"]
        )
        return obj

    def to_dict(self) -> Dict[str, Union[str, int, bool]]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, int, bool]] = {}
        d["name"] = self.name
        d["dir"] = self.dir
        d["id"] = self.id
        d["path"] = self.path
        d["requires_root"] = self.requires_root
        d["score"] = self.score
        return d

    def __hash__(self) -> int:
        """
        :return: a hash representation of the object
        """
        return hash(self.id)

    def __eq__(self, other) -> bool:
        """
        Tests equality with another flag

        :param other: the flag to compare with
        :return: True if equal otherwise False
        """
        if not isinstance(other, Flag):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.id == other.id and self.name == other.name and self.path == other.path

    @staticmethod
    def from_json_file(json_file_path: str) -> "Flag":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return Flag.from_dict(json.loads(json_str))

    def copy(self) -> "Flag":
        """
        :return: a copy of the DTO
        """
        return Flag.from_dict(self.to_dict())

    @staticmethod
    def schema() -> "Flag":
        """
        :return: get the schema of the DTO
        """
        return Flag(name="", dir="", id=-1, path="", requires_root=True, score=-1)
