from typing import Dict, Any


class ManagementUser:
    """
    DTO representing a management user
    """

    def __init__(self, username: str, password: str, admin: bool, salt: str) -> None:
        """
        Initializes the DTO

        :param username: the username of the user
        :param password: the password of the user
        :param admin: boolean flag whether the user is an admin or not
        :param salt: the password salt of the user
        """
        self.username = username
        self.password = password
        self.admin = admin
        self.salt = salt
        self.id = -1

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["username"] = self.username
        d["password"] = self.password
        d["salt"] = self.salt
        d["admin"] = self.admin
        d["id"] = self.id
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ManagementUser":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ManagementUser(
            username=d["username"], password=d["password"], admin=d["admin"], salt=d["salt"]
        )
        if "id" in d:
            obj.id = d["id"]
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"username: {self.username}, password: {self.password}, admin: {self.admin}, id: {self.id}, " \
               f"salt: {self.salt}"

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