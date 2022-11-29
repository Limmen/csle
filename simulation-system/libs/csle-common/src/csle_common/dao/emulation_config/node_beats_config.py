from typing import List, Dict, Any
from csle_common.util.general_util import GeneralUtil


class NodeBeatsConfig:
    """
    A DTO object representing the beats configuration of an individual container in an emulation
    """

    def __init__(self, ip: str, log_files_paths: List[str], filebeat_modules: List[str], kafka_input: bool = False):
        """
        Intializes the DTO

        :param ip: the ip of the nod
        :param log_files_paths: list of log files to ingest to elastic through filebeat
        :param filebeat_modules: list of filebeat modules to enable
        :param kafka_input: boolean indicating whether the kafka log should be ingested from this node or not
        """
        self.ip = ip
        self.log_files_paths = log_files_paths
        self.filebeat_modules = filebeat_modules
        self.kafka_input = kafka_input

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeBeatsConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NodeBeatsConfig(
            ip=d["ip"], log_files_paths=d["log_files_paths"], filebeat_modules=d["filebeat_modules"],
            kafka_input=d["kafka_input"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["log_files_paths"] = self.log_files_paths
        d["filebeat_modules"] = self.filebeat_modules
        d["kafka_input"] = self.kafka_input
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, log_files_paths: {self.log_files_paths}, filebeat_modules: {self.filebeat_modules}, " \
               f"kafka_input: {self.kafka_input}"

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

    def copy(self) -> "NodeBeatsConfig":
        """
        :return: a copy of the DTO
        """
        return NodeBeatsConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "NodeBeatsConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.ip = GeneralUtil.replace_first_octet_of_ip(ip=config.ip, ip_first_octet=ip_first_octet)
        return config
