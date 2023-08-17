from typing import Dict, Any, Union
from csle_base.json_serializable import JSONSerializable


class HostManagerConfig(JSONSerializable):
    """
    Represents the configuration of the Host managers in a CSLE emulation
    """

    def __init__(self, host_manager_log_file: str, host_manager_log_dir: str, host_manager_max_workers: int,
                 time_step_len_seconds: int = 15, host_manager_port: int = 50049, version: str = "0.0.1") -> None:
        """
        Initializes the DTO

        :param time_step_len_seconds: the length of a time-step (period for logging)
        :param version: the version
        :param host_manager_port: the GRPC port of the host manager
        :param host_manager_log_file: log file of the host manager
        :param host_manager_log_dir: log dir of the host manager
        :param host_manager_max_workers: max number of GRPC workers of the host manager
        """
        self.time_step_len_seconds = time_step_len_seconds
        self.version = version
        self.host_manager_port = host_manager_port
        self.host_manager_log_dir = host_manager_log_dir
        self.host_manager_log_file = host_manager_log_file
        self.host_manager_max_workers = host_manager_max_workers

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "HostManagerConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = HostManagerConfig(time_step_len_seconds=d["time_step_len_seconds"], version=d["version"],
                                host_manager_port=d["host_manager_port"],
                                host_manager_log_dir=d["host_manager_log_dir"],
                                host_manager_log_file=d["host_manager_log_file"],
                                host_manager_max_workers=d["host_manager_max_workers"])
        return obj

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, int]] = {}
        d["host_manager_port"] = self.host_manager_port
        d["time_step_len_seconds"] = self.time_step_len_seconds
        d["version"] = self.version
        d["host_manager_log_file"] = self.host_manager_log_file
        d["host_manager_log_dir"] = self.host_manager_log_dir
        d["host_manager_max_workers"] = self.host_manager_max_workers
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"host_manager_port: {self.host_manager_port}, time_step_len_seconds: {self.time_step_len_seconds}," \
               f" version: {self.version}, host_manager_log_file: {self.host_manager_log_file}," \
               f" host_manager_log_dir: {self.host_manager_log_dir}, " \
               f"host_manager_max_workers: {self.host_manager_max_workers}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "HostManagerConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return HostManagerConfig.from_dict(json.loads(json_str))

    def copy(self) -> "HostManagerConfig":
        """
        :return: a copy of the DTO
        """
        return HostManagerConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "HostManagerConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        return config

    @staticmethod
    def schema() -> "HostManagerConfig":
        """
        :return: get the schema of the DTO
        """
        return HostManagerConfig(host_manager_log_file="host_manager.log", host_manager_log_dir="/",
                                 host_manager_max_workers=10)
