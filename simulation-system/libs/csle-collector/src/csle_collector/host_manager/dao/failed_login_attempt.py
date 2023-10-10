import datetime
from csle_base.json_serializable import JSONSerializable
from typing import Dict, Any


class FailedLoginAttempt(JSONSerializable):
    """
    Class representing a failed login event on some server in the emulation
    """

    def __init__(self):
        """
        Initializes the object
        """
        self.timestamp = None

    @staticmethod
    def parse_from_str(login_attempt_str: str) -> "FailedLoginAttempt":
        """
        Parses a failed login event DTO from a string

        :param login_attempt_str: the string to parse
        :return: the parsed DTO
        """
        failed_login_attempt_dto = FailedLoginAttempt()
        failed_login_attempt_dto.timestamp = \
            datetime.datetime.strptime(login_attempt_str, '%Y %b %d %H:%M:%S').timestamp()
        return failed_login_attempt_dto

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "timestamp:{}".format(self.timestamp)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["timestamp"] = self.timestamp
        return d

    @staticmethod
    def from_dict(parsed_stats_dict: Dict[str, Any]) -> "FailedLoginAttempt":
        """
        Parses a FailedLoginAttempt object from a dict

        :param parsed_stats_dict: the dict to parse
        :return: the parsed FailedLoginAttempt object
        """
        failed_login_attempt_dto = FailedLoginAttempt()
        failed_login_attempt_dto.timestamp = parsed_stats_dict["timestamp"]
        return failed_login_attempt_dto

    @staticmethod
    def from_json_file(json_file_path: str) -> "FailedLoginAttempt":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FailedLoginAttempt.from_dict(json.loads(json_str))
