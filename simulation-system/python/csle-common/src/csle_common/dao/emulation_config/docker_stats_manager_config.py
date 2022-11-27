from typing import Dict, Any


class DockerStatsManagerConfig:
    """
    Represents the configuration of the docker stats managers in a CSLE emulation
    """

    def __init__(self, docker_stats_manager_log_file: str, docker_stats_manager_log_dir: str,
                 docker_stats_manager_max_workers: int,
                 time_step_len_seconds: int = 15, docker_stats_manager_port: int = 50046,
                 version: str = "0.0.1") -> None:
        """
        Initializes the DTO

        :param time_step_len_seconds: the length of a time-step (period for logging)
        :param version: the version
        :param docker_stats_manager_port: the GRPC port of the docker stats manager
        :param docker_stats_manager_log_file: log file of the docker stats manager
        :param docker_stats_manager_log_dir: log dir of the docker stats manager
        :param docker_stats_manager_max_workers: max number of gRPC workers of the docker stats manager
        """
        self.time_step_len_seconds = time_step_len_seconds
        self.version = version
        self.docker_stats_manager_port = docker_stats_manager_port
        self.docker_stats_manager_log_file = docker_stats_manager_log_file
        self.docker_stats_manager_log_dir = docker_stats_manager_log_dir
        self.docker_stats_manager_max_workers = docker_stats_manager_max_workers

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DockerStatsManagerConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = DockerStatsManagerConfig(time_step_len_seconds=d["time_step_len_seconds"],
                                       version=d["version"], docker_stats_manager_port=d["docker_stats_manager_port"],
                                       docker_stats_manager_log_file=d["docker_stats_manager_log_file"],
                                       docker_stats_manager_log_dir=d["docker_stats_manager_log_dir"],
                                       docker_stats_manager_max_workers=d["docker_stats_manager_max_workers"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["docker_stats_manager_port"] = self.docker_stats_manager_port
        d["time_step_len_seconds"] = self.time_step_len_seconds
        d["version"] = self.version
        d["docker_stats_manager_log_file"] = self.docker_stats_manager_log_file
        d["docker_stats_manager_log_dir"] = self.docker_stats_manager_log_dir
        d["docker_stats_manager_max_workers"] = self.docker_stats_manager_max_workers
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"docker_stats_manager_port: {self.docker_stats_manager_port}, " \
               f"time_step_len_seconds: {self.time_step_len_seconds}," \
               f" version: {self.version}, docker_stats_manager_log_dir: {self.docker_stats_manager_log_dir}, " \
               f"docker_stats_manager_log_file: {self.docker_stats_manager_log_file}, " \
               f"docker_stats_manager_max_workers: {self.docker_stats_manager_max_workers}"

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

    def copy(self) -> "DockerStatsManagerConfig":
        """
        :return: a copy of the DTO
        """
        return DockerStatsManagerConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "DockerStatsManagerConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        return config

    @staticmethod
    def schema() -> "DockerStatsManagerConfig":
        """
        :return: get the schema of the DTO
        """
        return DockerStatsManagerConfig(docker_stats_manager_log_file="docker_stats_manager.log",
                                        docker_stats_manager_log_dir="/var/log/csle/", docker_stats_manager_port=50046,
                                        docker_stats_manager_max_workers=10)
