from typing import List, Dict, Any
from csle_common.dao.emulation_config.flag import Flag
from csle_common.util.general_util import GeneralUtil
from csle_base.json_serializable import JSONSerializable


class NodeFlagsConfig(JSONSerializable):
    """
    A DTO object representing the set of flags at a specific container in an emulation environment
    """

    def __init__(self, ip: str, flags: List[Flag], docker_gw_bridge_ip: str = "", physical_host_ip: str = ""):
        """
        Initializes the DTO

        :param ip: the ip of the node
        :param flags: the list of flags
        :param docker_gw_bridge_ip: IP to reach the container from the host network
        :param physical_host_ip: IP of the physical host where the container is running
        """
        self.ip = ip
        self.flags = flags
        self.docker_gw_bridge_ip = docker_gw_bridge_ip
        self.physical_host_ip = physical_host_ip

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["ip"] = self.ip
        d["flags"] = list(map(lambda x: x.to_dict(), self.flags))
        d["docker_gw_bridge_ip"] = self.docker_gw_bridge_ip
        d["physical_host_ip"] = self.physical_host_ip
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeFlagsConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        return NodeFlagsConfig(ip=d["ip"], flags=list(map(lambda x: Flag.from_dict(x), d["flags"])),
                               docker_gw_bridge_ip=d["docker_gw_bridge_ip"], physical_host_ip=d["physical_host_ip"])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, docker_gw_bridge_ip:{self.docker_gw_bridge_ip}, " \
               f"flags:{','.join(list(map(lambda x: str(x), self.flags)))}, physical_host_ip: {self.physical_host_ip}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "NodeFlagsConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NodeFlagsConfig.from_dict(json.loads(json_str))

    def copy(self) -> "NodeFlagsConfig":
        """
        :return: a copy of the DTO
        """
        return NodeFlagsConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "NodeFlagsConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.ip = GeneralUtil.replace_first_octet_of_ip(ip=config.ip, ip_first_octet=ip_first_octet)
        return config
