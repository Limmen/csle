from typing import List, Tuple
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig


class NodeResourcesConfig:
    """
    A DTO object representing the resources of a specific container in an emulation environment
    """

    def __init__(self, container_name: str,
                 num_cpus: int, available_memory_gb :int,
                 ips_and_network_configs = List[Tuple[str, NodeNetworkConfig]]):
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
    def from_dict(d: dict) -> "NodeResourcesConfig":
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

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["container_name"] = self.container_name
        d["ips_gw_default_policy_networks"] = list(map(lambda x: (x[0], x[1].to_dict()), self.ips_and_network_configs))
        d["num_cpus"] = self.num_cpus
        d["available_memory_gb"] = self.available_memory_gb
        return d


    def __str__(self) -> str:
        """
        :return: a string representation of the node's resources
        """
        return f"num_cpus: {self.num_cpus}, available_memory_gb:{self.available_memory_gb}, " \
               f"container_name:{self.container_name}, ips_and_network_configs: {self.ips_and_network_configs}"
