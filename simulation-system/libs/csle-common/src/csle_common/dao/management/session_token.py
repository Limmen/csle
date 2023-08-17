import time
from typing import Dict, Any, Union
from csle_base.json_serializable import JSONSerializable


class SessionToken(JSONSerializable):
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

    def to_dict(self) -> Dict[str, Union[str, float]]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, float]] = {}
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

    def expired(self, valid_length_hours: int) -> bool:
        """
        Checks if the token has expired or not

        :param valid_length_hours: the number of hours that a token is valid
        :return: True if the token has expired otherwise False
        """
        return ((time.time() - self.timestamp) / (60) / (60)) > valid_length_hours

    @staticmethod
    def from_json_file(json_file_path: str) -> "SessionToken":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SessionToken.from_dict(json.loads(json_str))
