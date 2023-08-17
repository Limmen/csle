from typing import Dict, Any, Union
from csle_base.json_serializable import JSONSerializable


class OSSECIDSManagerConfig(JSONSerializable):
    """
    Represents the configuration of the OSSEC IDS managers in a CSLE emulation
    """

    def __init__(self, ossec_ids_manager_log_file: str, ossec_ids_manager_log_dir: str,
                 ossec_ids_manager_max_workers: int,
                 time_step_len_seconds: int = 15, ossec_ids_manager_port: int = 50047,
                 version: str = "0.0.1") -> None:
        """
        Initializes the DTO

        :param time_step_len_seconds: the length of a time-step (period for logging)
        :param version: the version
        :param ossec_ids_manager_port: the GRPC port of the OSSEC IDS manager
        :param ossec_ids_manager_log_file: Log file of the OSSEC IDS manager
        :param ossec_ids_manager_log_dir: Log dir of the OSSEC IDS manager
        :param ossec_ids_manager_max_workers: Max GRPC workers of the OSSEC IDS manager
        """
        self.time_step_len_seconds = time_step_len_seconds
        self.version = version
        self.ossec_ids_manager_port = ossec_ids_manager_port
        self.ossec_ids_manager_log_file = ossec_ids_manager_log_file
        self.ossec_ids_manager_log_dir = ossec_ids_manager_log_dir
        self.ossec_ids_manager_max_workers = ossec_ids_manager_max_workers

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OSSECIDSManagerConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = OSSECIDSManagerConfig(time_step_len_seconds=d["time_step_len_seconds"],
                                    version=d["version"], ossec_ids_manager_port=d["ossec_ids_manager_port"],
                                    ossec_ids_manager_log_dir=d["ossec_ids_manager_log_dir"],
                                    ossec_ids_manager_log_file=d["ossec_ids_manager_log_file"],
                                    ossec_ids_manager_max_workers=d["ossec_ids_manager_max_workers"])
        return obj

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, int]] = {}
        d["ossec_ids_manager_port"] = self.ossec_ids_manager_port
        d["time_step_len_seconds"] = self.time_step_len_seconds
        d["version"] = self.version
        d["ossec_ids_manager_log_file"] = self.ossec_ids_manager_log_file
        d["ossec_ids_manager_log_dir"] = self.ossec_ids_manager_log_dir
        d["ossec_ids_manager_max_workers"] = self.ossec_ids_manager_max_workers
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ossec_ids_manager_port: {self.ossec_ids_manager_port}, " \
               f"time_step_len_seconds: {self.time_step_len_seconds}," \
               f" version: {self.version}, ossec_ids_manager_log_file: {self.ossec_ids_manager_log_file}, " \
               f"ossec_ids_manager_log_dir: {self.ossec_ids_manager_log_dir}, " \
               f"ossec_ids_manager_max_workers: {self.ossec_ids_manager_max_workers}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "OSSECIDSManagerConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return OSSECIDSManagerConfig.from_dict(json.loads(json_str))

    def copy(self) -> "OSSECIDSManagerConfig":
        """
        :return: a copy of the DTO
        """
        return OSSECIDSManagerConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "OSSECIDSManagerConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        return config

    @staticmethod
    def schema() -> "OSSECIDSManagerConfig":
        """
        :return: get the schema of the DTO
        """
        return OSSECIDSManagerConfig(ossec_ids_manager_log_file="ossec_ids_manager.log", ossec_ids_manager_log_dir="/",
                                     ossec_ids_manager_max_workers=10)
