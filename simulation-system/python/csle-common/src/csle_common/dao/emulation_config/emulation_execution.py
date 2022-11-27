from typing import Dict, Any
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig


class EmulationExecution:
    """
    A DTO representing an execution of an emulation
    """

    def __init__(self, emulation_name: str, timestamp: float, ip_first_octet: int,
                 emulation_env_config: EmulationEnvConfig):
        """
        Initializes the DTO

        :param emulation_name: the emulation name
        :param timestamp: the timestamp the execution started
        :param ip_first_octet: the first octet in the ip
        :param emulation_env_config: the emulation env config
        :param id: the id of the execution
        """
        self.emulation_name = emulation_name
        self.timestamp = timestamp
        self.emulation_env_config = emulation_env_config
        self.ip_first_octet = ip_first_octet

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationExecution":
        """
        Converts a dict representation to a DTO

        :param d: the dict to convert
        :return: the DTO
        """
        return EmulationExecution(emulation_name=d["emulation_name"], timestamp=d["timestamp"],
                                  ip_first_octet=d["ip_first_octet"],
                                  emulation_env_config=EmulationEnvConfig.from_dict(d["emulation_env_config"]))

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["emulation_name"] = self.emulation_name
        d["timestamp"] = self.timestamp
        d["emulation_env_config"] = self.emulation_env_config.to_dict()
        d["ip_first_octet"] = self.ip_first_octet
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"emulation_name:{self.emulation_name}, timestamp: {self.timestamp}, " \
               f"emulation_env_config: {self.emulation_env_config}" \
               f"ip_first_octet:{self.ip_first_octet}"
