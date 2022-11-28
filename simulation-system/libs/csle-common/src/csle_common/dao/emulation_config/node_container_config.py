from typing import List, Tuple, Dict, Any
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.util.general_util import GeneralUtil


class NodeContainerConfig:
    """
    A DTO object representing an individual container in an emulation environment
    """

    def __init__(self, name: str, ips_and_networks: List[Tuple[str, ContainerNetwork]],
                 version: str, level: str, restart_policy: str,
                 suffix: str, os: str, execution_ip_first_octet: int = -1):
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
        execution_ip_first_octet = -1
        if "execution_ip_first_octet" in d:
            execution_ip_first_octet = d["execution_ip_first_octet"]
        obj = NodeContainerConfig(
            name=d["name"],
            ips_and_networks=list(map(lambda x: (x[0], ContainerNetwork.from_dict(x[1])), d["ips_and_networks"])),
            version=d["version"], level=d["level"],
            restart_policy=d["restart_policy"], suffix=d["suffix"], os=d["os"],
            execution_ip_first_octet=execution_ip_first_octet
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["name"] = self.name
        d["ips_and_networks"] = list(map(lambda x: (x[0], x[1].to_dict()), self.ips_and_networks))
        d["version"] = self.version
        d["restart_policy"] = self.restart_policy
        d["suffix"] = self.suffix
        d["os"] = self.os
        d["level"] = self.level
        d["full_name_str"] = self.get_full_name()
        d["execution_ip_first_octet"] = self.execution_ip_first_octet
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name{self.name}, ips and networks: {self.ips_and_networks}, version: {self.version}, " \
               f"level:{self.level}, restart_policy: {self.restart_policy}, " \
               f"suffix:{self.suffix}, os:{self.os}, full_name:{self.full_name_str}, " \
               f"execution_ip_first_octet: {self.execution_ip_first_octet}"

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

    def copy(self) -> "NodeContainerConfig":
        """
        :return: a copy of the DTO
        """
        return NodeContainerConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "NodeContainerConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.execution_ip_first_octet = ip_first_octet
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
