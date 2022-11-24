import time
from typing import Dict, Any


class SessionToken:
    """
    DTO representing a session token
    """

    def __init__(self, token: str, timestamp: float, username: str) -> None:
        """
        Initializes the DTO

        :param token: the token string
        :param timestamp: the time the token was created
        :param username: the username of the user that the token is given to
        """
        self.token = token
        self.timestamp = timestamp
        self.username = username

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["username"] = self.username
        d["timestamp"] = self.timestamp
        d["token"] = self.token
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SessionToken":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = SessionToken(
            username=d["username"], token=d["token"], timestamp=d["timestamp"]
        )
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"username: {self.username}, token: {self.token}, timestamp: {self.timestamp}"

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

    def expired(self, valid_length_hours: int) -> bool:
        """
        Checks if the token has expired or not

        :param valid_length_hours: the number of hours that a token is valid
        :return: True if the token has expired otherwise False
        """
        return ((time.time() - self.timestamp) / (60) / (60)) > valid_length_hours
