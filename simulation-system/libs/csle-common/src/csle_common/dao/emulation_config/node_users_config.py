from typing import List, Dict, Any
from csle_common.dao.emulation_config.user import User
from csle_common.util.general_util import GeneralUtil
from csle_base.json_serializable import JSONSerializable


class NodeUsersConfig(JSONSerializable):
    """
    A DTO object representing the users of a container in an emulation environment
    """

    def __init__(self, ip: str, users: List[User], docker_gw_bridge_ip: str = "", physical_host_ip: str = ""):
        """
        Initializes the DTO

        :param ip: the ip of the node
        :param users: the list of users
        :param docker_gw_bridge_ip: IP to reach the container from the host network
        :param physical_host_ip: IP of the physical host where the container is running
        """
        self.ip = ip
        self.users = users
        self.docker_gw_bridge_ip = docker_gw_bridge_ip
        self.physical_host_ip = physical_host_ip

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeUsersConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NodeUsersConfig(
            ip=d["ip"], users=list(map(lambda x: User.from_dict(x), d["users"])),
            docker_gw_bridge_ip=d["docker_gw_bridge_ip"],
            physical_host_ip=d["physical_host_ip"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["ip"] = self.ip
        d["users"] = list(map(lambda x: x.to_dict(), self.users))
        d["docker_gw_bridge_ip"] = self.docker_gw_bridge_ip
        d["physical_host_ip"] = self.physical_host_ip
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, docker_gw_bridge_ip:{self.docker_gw_bridge_ip}, " \
               f"users:{','.join(list(map(lambda x: str(x), self.users)))}, physical_host_ip: {self.physical_host_ip}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "NodeUsersConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NodeUsersConfig.from_dict(json.loads(json_str))

    def copy(self) -> "NodeUsersConfig":
        """
        :return: a copy of the DTO
        """
        return NodeUsersConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "NodeUsersConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.ip = GeneralUtil.replace_first_octet_of_ip(ip=config.ip, ip_first_octet=ip_first_octet)
        return config
