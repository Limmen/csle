from typing import Dict, Any, List
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_base.json_serializable import JSONSerializable


class EmulationExecution(JSONSerializable):
    """
    A DTO representing an execution of an emulation
    """

    def __init__(self, emulation_name: str, timestamp: float, ip_first_octet: int,
                 emulation_env_config: EmulationEnvConfig, physical_servers: List[str]):
        """
        Initializes the DTO

        :param emulation_name: the emulation name
        :param timestamp: the timestamp the execution started
        :param ip_first_octet: the first octet in the ip
        :param emulation_env_config: the emulation env config
        :param id: the id of the execution
        :param physical_servers: list of physical server IPs where the execution is running
        """
        self.emulation_name = emulation_name
        self.timestamp = timestamp
        self.emulation_env_config = emulation_env_config
        self.ip_first_octet = ip_first_octet
        self.physical_servers = physical_servers

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationExecution":
        """
        Converts a dict representation to a DTO

        :param d: the dict to convert
        :return: the DTO
        """
        return EmulationExecution(emulation_name=d["emulation_name"], timestamp=d["timestamp"],
                                  ip_first_octet=d["ip_first_octet"],
                                  emulation_env_config=EmulationEnvConfig.from_dict(d["emulation_env_config"]),
                                  physical_servers=d["physical_servers"])

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["emulation_name"] = self.emulation_name
        d["timestamp"] = self.timestamp
        d["emulation_env_config"] = self.emulation_env_config.to_dict()
        d["ip_first_octet"] = self.ip_first_octet
        d["physical_servers"] = self.physical_servers
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"emulation_name:{self.emulation_name}, timestamp: {self.timestamp}, " \
               f"emulation_env_config: {self.emulation_env_config}," \
               f"ip_first_octet:{self.ip_first_octet}, physical_servers: {self.physical_servers}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationExecution":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationExecution.from_dict(json.loads(json_str))
