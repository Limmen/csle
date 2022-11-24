from typing import List, Dict, Any
from csle_common.util.general_util import GeneralUtil


class NodeTrafficConfig:
    """
    A DTO object representing the traffic configuration of an individual container in an emulation
    """

    def __init__(self, ip: str, commands: List[str], traffic_manager_log_file: str, traffic_manager_log_dir: str,
                 traffic_manager_max_workers: int, traffic_manager_port: int = 50043):
        """
        Creates a NodeTrafficConfig DTO Object

        :param ip: the ip of the node that generate the traffic
        :param commands: the commands used to generate the traffic
        :param traffic_manager_log_file: the file name to write logs of the traffic manager
        :param traffic_manager_log_dir: the directory to save the log file of the traffic manager
        :param traffic_manager_max_workers: the maximum number of gRPC workers for the traffic manager
        :param traffic_manager_port: the port of the traffic manager
        """
        self.ip = ip
        self.commands = commands
        self.traffic_manager_port = traffic_manager_port
        self.traffic_manager_log_file = traffic_manager_log_file
        self.traffic_manager_log_dir = traffic_manager_log_dir
        self.traffic_manager_max_workers = traffic_manager_max_workers

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeTrafficConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NodeTrafficConfig(
            ip=d["ip"], commands=d["commands"], traffic_manager_port=d["traffic_manager_port"],
            traffic_manager_max_workers=d["traffic_manager_max_workers"],
            traffic_manager_log_file=d["traffic_manager_log_file"],
            traffic_manager_log_dir=d["traffic_manager_log_dir"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["commands"] = self.commands
        d["traffic_manager_port"] = self.traffic_manager_port
        d["traffic_manager_max_workers"] = self.traffic_manager_max_workers
        d["traffic_manager_log_file"] = self.traffic_manager_log_file
        d["traffic_manager_log_dir"] = self.traffic_manager_log_dir
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, commands:{self.commands}, traffic_manager_port: {self.traffic_manager_port}, " \
               f"traffic_manager_log_file: {self.traffic_manager_log_file}, " \
               f"traffic_manager_max_workers: {self.traffic_manager_max_workers}, " \
               f"traffic_manager_log_file_dir: {self.traffic_manager_log_dir}"

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

    def copy(self) -> "NodeTrafficConfig":
        """
        :return: a copy of the DTO
        """
        return NodeTrafficConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "NodeTrafficConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.ip = GeneralUtil.replace_first_octet_of_ip(ip=config.ip, ip_first_octet=ip_first_octet)
        return config
