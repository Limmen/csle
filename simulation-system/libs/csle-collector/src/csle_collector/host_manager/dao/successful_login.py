import datetime
from csle_base.json_serializable import JSONSerializable
from typing import Dict, Any


class SuccessfulLogin(JSONSerializable):
    """
    DTO Class representing a parsed successful login event from a server in the emulation
    """

    def __init__(self):
        """
        Initializes the DTO
        """
        self.timestamp = None
        self.ip = ""
        self.user = ""

    @staticmethod
    def parse_from_str(login_attempt_str: str, year: int):
        """
        Parses a login event from a string

        :param login_attempt_str: the string to parse
        :param year: the current year
        :return: the parsed login event
        """
        successful_login_attempt_dto = SuccessfulLogin()
        parts = login_attempt_str.split()
        if len(parts) > 6:
            successful_login_attempt_dto.user = parts[0]
            successful_login_attempt_dto.ip = parts[2]
            date_str = " ".join(parts[3:7])
            date_str = str(year) + " " + date_str
            successful_login_attempt_dto.timestamp = \
                datetime.datetime.strptime(date_str, '%Y %a %b %d %H:%M').timestamp()
        return successful_login_attempt_dto

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, user:{}, timestamp:{}".format(self.ip, self.user, self.timestamp)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["timestamp"] = self.timestamp
        d["ip"] = self.ip
        d["user"] = self.user
        return d

    @staticmethod
    def from_dict(parsed_stats_dict: Dict[str, Any]) -> "SuccessfulLogin":
        """
        Parses a FailedLoginAttempt object from a dict

        :param parsed_stats_dict: the dict to parse
        :return: the parsed FailedLoginAttempt object
        """
        successful_login_dto = SuccessfulLogin()
        successful_login_dto.timestamp = parsed_stats_dict["timestamp"]
        successful_login_dto.ip = parsed_stats_dict["ip"]
        successful_login_dto.user = parsed_stats_dict["user"]
        return successful_login_dto

    @staticmethod
    def from_json_file(json_file_path: str) -> "SuccessfulLogin":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SuccessfulLogin.from_dict(json.loads(json_str))
