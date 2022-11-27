from typing import Dict, Any


class User:
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
    def from_dict(d: Dict[str, Any]):
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

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["username"] = self.username
        d["pw"] = self.pw
        d["root"] = self.root
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"username:{self.username}, pw:{self.pw}, root:{self.root}"

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

    def copy(self) -> "User":
        """
        :return: a copy of the DTO
        """
        return User.from_dict(self.to_dict())
