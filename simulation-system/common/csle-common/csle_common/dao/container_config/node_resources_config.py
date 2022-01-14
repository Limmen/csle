from csle_common.dao.container_config.node_network_config import NodeNetworkConfig


class NodeResourcesConfig:
    """
    A DTO object representing the resources of a specific container in an emulation environment
    """

    def __init__(self, ip: str, container_name: str,
                 num_cpus: int, available_memory_gb :int, network_config: NodeNetworkConfig):
        """
        Initializes the DTO

        :param ip: the IP-address of the container
        :param container_name: the name of the container
        :param num_cpus: the number of CPUs available to the node
        :param available_memory_gb: the number of RAM GB available to the node
        :param network_config: the network configuration of the node
        """
        self.ip = ip
        self.container_name = container_name
        self.num_cpus = num_cpus
        self.available_memory_gb = available_memory_gb
        self.network_config = network_config

    def __str__(self) -> str:
        """
        :return: a string representation of the node's resources
        """
        return f"ip: {self.ip}, num_cpus: {self.num_cpus}, available_memory_gb:{self.available_memory_gb}, " \
               f"network_config:{str(self.network_config)}, container_name:{self.container_name}"
