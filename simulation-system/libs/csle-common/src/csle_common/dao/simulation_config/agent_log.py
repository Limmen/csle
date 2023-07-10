from typing import Dict, Any
from csle_base.json_serializable import JSONSerializable


class AgentLog(JSONSerializable):
    """
    DTO Representing the Agent Log
    """

    def __init__(self):
        """
        Initializes the log
        """
        self.log = []

    def add_entry(self, msg) -> None:
        """
        Adds an entry to the log

        :param msg: the msg to add to the log
        :return: None
        """
        self.log.append(msg)

    def reset(self) -> None:
        """
        Resets the log

        :return: None
        """
        self.log = []

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AgentLog":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = AgentLog()
        obj.log = d["log"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d = {}
        d["log"] = self.log
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "AgentLog":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return AgentLog.from_dict(json.loads(json_str))
