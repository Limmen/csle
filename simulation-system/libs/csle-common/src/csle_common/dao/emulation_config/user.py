from typing import Dict, Any, Union
from csle_base.json_serializable import JSONSerializable


class User(JSONSerializable):
    """
    DTO class representing a user in an emulation
    """

    def __init__(self, username: str, pw: str, root: bool):
        """
        Initializes the DTO

        :param username: the username of the user
        :param pw: the password of the user
        :param root: whether the user has root access or not
        """
        self.username = username
        self.pw = pw
        self.root = root

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "User":
        """
        Converts a dict representation of the object into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = User(
            username=d["username"],
            pw=d["pw"],
            root=d["root"]
        )
        return obj

    def to_dict(self) -> Dict[str, Union[str, bool]]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, bool]] = {}
        d["username"] = self.username
        d["pw"] = self.pw
        d["root"] = self.root
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"username:{self.username}, pw:{self.pw}, root:{self.root}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "User":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return User.from_dict(json.loads(json_str))

    def copy(self) -> "User":
        """
        :return: a copy of the DTO
        """
        return User.from_dict(self.to_dict())
