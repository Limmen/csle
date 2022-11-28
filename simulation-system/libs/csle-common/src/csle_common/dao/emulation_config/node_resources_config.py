from typing import List, Tuple, Dict, Any
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.util.general_util import GeneralUtil


class NodeResourcesConfig:
    """
    A DTO object representing the resources of a specific container in an emulation environment
    """

    def __init__(self, container_name: str,
                 num_cpus: int, available_memory_gb: int,
                 ips_and_network_configs: List[Tuple[str, NodeNetworkConfig]]):
        """
        Initializes the DTO

        :param container_name: the name of the container
        :param num_cpus: the number of CPUs available to the node
        :param available_memory_gb: the number of RAM GB available to the node
        :param ips_and_network_configs: list of ip adresses and network configurations
        """
        self.container_name = container_name
        self.num_cpus = num_cpus
        self.available_memory_gb = available_memory_gb
        self.ips_and_network_configs = ips_and_network_configs

    def get_ips(self) -> List[str]:
        """
        :return: a list of ips
        """
        return list(map(lambda x: x[0], self.ips_and_network_configs))

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeResourcesConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NodeResourcesConfig(
            container_name=d["container_name"],
            ips_and_network_configs=list(map(lambda x: (x[0], NodeNetworkConfig.from_dict(x[1])),
                                             d["ips_and_network_configs"])),
            num_cpus=d["num_cpus"], available_memory_gb=d["available_memory_gb"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["container_name"] = self.container_name
        d["ips_and_network_configs"] = list(map(lambda x: (x[0], None if x[1] is None else x[1].to_dict()),
                                                self.ips_and_network_configs))
        d["num_cpus"] = self.num_cpus
        d["available_memory_gb"] = self.available_memory_gb
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the node's resources
        """
        return f"num_cpus: {self.num_cpus}, available_memory_gb:{self.available_memory_gb}, " \
               f"container_name:{self.container_name}, ips_and_network_configs: {self.ips_and_network_configs}"

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

    def copy(self) -> "NodeResourcesConfig":
        """
        :return: a copy of the DTO
        """
        return NodeResourcesConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "NodeResourcesConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.container_name = config.container_name + f"_{ip_first_octet}"
        config.ips_and_network_configs = list(map(lambda x: (GeneralUtil.replace_first_octet_of_ip(
            ip=x[0], ip_first_octet=ip_first_octet), x[1]), config.ips_and_network_configs))
        return config

    @staticmethod
    def schema() -> "NodeResourcesConfig":
        """
        :return: get the schema of the DTO
        """
        return NodeResourcesConfig(container_name="", num_cpus=1, available_memory_gb=1,
                                   ips_and_network_configs=[("", NodeNetworkConfig.schema())])
