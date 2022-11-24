from typing import Dict, Any


class SnortIDSManagerConfig:
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

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
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
