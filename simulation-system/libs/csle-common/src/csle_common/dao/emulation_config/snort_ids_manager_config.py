from typing import Dict, Any, Union
from csle_base.json_serializable import JSONSerializable


class SnortIDSManagerConfig(JSONSerializable):
    """
    Represents the configuration of the Snort IDS managers in a CSLE emulation
    """

    def __init__(self, snort_ids_manager_log_file: str, snort_ids_manager_log_dir: str,
                 snort_ids_manager_max_workers: int,
                 time_step_len_seconds: int = 15, snort_ids_manager_port: int = 50048, version: str = "0.0.1") -> None:
        """
        Initializes the DTO

        :param time_step_len_seconds: the length of a time-step (period for logging)
        :param version: the version
        :param snort_ids_manager_port: the GRPC port of the snort IDS manager
        :param snort_ids_manager_log_file: the log file of the snort IDS manager
        :param snort_ids_manager_log_dir: the log dir of the snort IDS manager
        """
        self.time_step_len_seconds = time_step_len_seconds
        self.version = version
        self.snort_ids_manager_port = snort_ids_manager_port
        self.snort_ids_manager_log_file = snort_ids_manager_log_file
        self.snort_ids_manager_log_dir = snort_ids_manager_log_dir
        self.snort_ids_manager_max_workers = snort_ids_manager_max_workers

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SnortIDSManagerConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = SnortIDSManagerConfig(time_step_len_seconds=d["time_step_len_seconds"],
                                    version=d["version"], snort_ids_manager_port=d["snort_ids_manager_port"],
                                    snort_ids_manager_max_workers=d["snort_ids_manager_max_workers"],
                                    snort_ids_manager_log_dir=d["snort_ids_manager_log_dir"],
                                    snort_ids_manager_log_file=d["snort_ids_manager_log_file"])
        return obj

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, int]] = {}
        d["snort_ids_manager_port"] = self.snort_ids_manager_port
        d["time_step_len_seconds"] = self.time_step_len_seconds
        d["version"] = self.version
        d["snort_ids_manager_max_workers"] = self.snort_ids_manager_max_workers
        d["snort_ids_manager_log_dir"] = self.snort_ids_manager_log_dir
        d["snort_ids_manager_log_file"] = self.snort_ids_manager_log_file
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"snort_ids_manager_port: {self.snort_ids_manager_port}, " \
               f"time_step_len_seconds: {self.time_step_len_seconds}," \
               f" version: {self.version}, snort_ids_manager_max_workers: {self.snort_ids_manager_max_workers}," \
               f"snort_ids_manager_log_file: {self.snort_ids_manager_log_file}, " \
               f"snort_ids_manager_log_dir: {self.snort_ids_manager_log_dir}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "SnortIDSManagerConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SnortIDSManagerConfig.from_dict(json.loads(json_str))

    def copy(self) -> "SnortIDSManagerConfig":
        """
        :return: a copy of the DTO
        """
        return SnortIDSManagerConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "SnortIDSManagerConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        return config

    @staticmethod
    def schema() -> "SnortIDSManagerConfig":
        """
        :return: get the schema of the DTO
        """
        return SnortIDSManagerConfig(snort_ids_manager_log_file="snort_ids_manager.log", snort_ids_manager_log_dir="/",
                                     snort_ids_manager_max_workers=10)
