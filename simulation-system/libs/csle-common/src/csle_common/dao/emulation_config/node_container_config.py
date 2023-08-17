from typing import List, Tuple, Dict, Any
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.util.general_util import GeneralUtil
from csle_base.json_serializable import JSONSerializable


class NodeContainerConfig(JSONSerializable):
    """
    A DTO object representing an individual container in an emulation environment
    """

    def __init__(self, name: str, ips_and_networks: List[Tuple[str, ContainerNetwork]],
                 version: str, level: str, restart_policy: str,
                 suffix: str, os: str, execution_ip_first_octet: int = -1, docker_gw_bridge_ip: str = "",
                 physical_host_ip: str = ""):
        """
        Initializes the DTO

        :param name: the name of the node container
        :param ips_and_networks: the list of ips and networks that the container is connected to
        :param version: the version of the container
        :param level: the level of the container
        :param restart_policy: the restart policy of the container
        :param suffix: the suffix of the container id
        :param os: the operating system of the container
        :param execution_ip_first_octet: the first octet in the IP address (depends on the execution)
        :param docker_gw_bridge_ip: IP to reach the container from the host network
        :param physical_host_ip: IP of the physical host where the container is running
        """
        self.name = name
        self.ips_and_networks = ips_and_networks
        self.version = version
        self.level = level
        self.restart_policy = restart_policy
        self.suffix = suffix
        self.os = os
        self.execution_ip_first_octet = execution_ip_first_octet
        self.full_name_str = self.get_full_name()
        self.docker_gw_bridge_ip = docker_gw_bridge_ip
        self.physical_host_ip = physical_host_ip

    def get_ips(self) -> List[str]:
        """
        :return: a list of ips that this container has
        """
        return list(filter(lambda x: x is not None, map(lambda x: x[0], self.ips_and_networks)))

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeContainerConfig":
        """
        Converts a dict representation to an instance
        :param d:  the dict to convert
        :return: the created instance
        """
        obj = NodeContainerConfig(
            name=d["name"],
            ips_and_networks=list(map(lambda x: (x[0], ContainerNetwork.from_dict(x[1])), d["ips_and_networks"])),
            version=d["version"], level=d["level"],
            restart_policy=d["restart_policy"], suffix=d["suffix"], os=d["os"],
            execution_ip_first_octet=d["execution_ip_first_octet"],
            docker_gw_bridge_ip=d["docker_gw_bridge_ip"], physical_host_ip=d["physical_host_ip"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["name"] = self.name
        d["ips_and_networks"] = list(map(lambda x: (x[0], x[1].to_dict()), self.ips_and_networks))
        d["version"] = self.version
        d["restart_policy"] = self.restart_policy
        d["suffix"] = self.suffix
        d["os"] = self.os
        d["level"] = self.level
        d["full_name_str"] = self.get_full_name()
        d["execution_ip_first_octet"] = self.execution_ip_first_octet
        d["docker_gw_bridge_ip"] = self.docker_gw_bridge_ip
        d["physical_host_ip"] = self.physical_host_ip
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name{self.name}, ips and networks: {self.ips_and_networks}, version: {self.version}, " \
               f"level:{self.level}, restart_policy: {self.restart_policy}, " \
               f"suffix:{self.suffix}, os:{self.os}, full_name:{self.full_name_str}, " \
               f"execution_ip_first_octet: {self.execution_ip_first_octet}," \
               f"docker_gw_bridge_ip: {self.docker_gw_bridge_ip}, physical_host_ip: {self.physical_host_ip}"

    def reachable(self, reachable_ips: List[str]) -> bool:
        """
        Check if container is reachable given a list of reachable ips

        :param reachable_ips: the list of reachable ips
        :return: True if the container is reachable, false otherwise
        """
        for ip in self.get_ips():
            if ip in reachable_ips:
                return True
        return False

    def get_full_name(self) -> str:
        """
        :return: the full name
        """
        return f"{self.name}{self.suffix}-{constants.CSLE.LEVEL}{self.level}-" \
               f"{self.execution_ip_first_octet}"

    def get_readable_name(self) -> str:
        """
        :return: the readable name
        """
        return f"csle-{self.name}{self.suffix}-{constants.CSLE.LEVEL}{self.level}_" \
               f"{self.execution_ip_first_octet}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "NodeContainerConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NodeContainerConfig.from_dict(json.loads(json_str))

    def copy(self) -> "NodeContainerConfig":
        """
        :return: a copy of the DTO
        """
        return NodeContainerConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int, physical_servers: List[str]) -> "NodeContainerConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :param physical_servers: the list of physical servers of the execution
        :return: the new config
        """
        config = self.copy()
        config.execution_ip_first_octet = ip_first_octet
        config.physical_host_ip = physical_servers[0]  # TODO Update this
        config.ips_and_networks = list(map(lambda x: (
            GeneralUtil.replace_first_octet_of_ip(ip=x[0], ip_first_octet=ip_first_octet),
            x[1].create_execution_config(ip_first_octet=ip_first_octet)), config.ips_and_networks))
        return config

    @staticmethod
    def schema() -> "NodeContainerConfig":
        """
        :return: get the schema of the DTO
        """
        return NodeContainerConfig(name="", ips_and_networks=[("", ContainerNetwork.schema())], version="", level="",
                                   restart_policy="", suffix="", os="", execution_ip_first_octet=-1)
