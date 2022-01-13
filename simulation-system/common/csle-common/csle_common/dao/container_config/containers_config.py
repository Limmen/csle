from typing import List
from csle_common.dao.container_config.node_container_config import NodeContainerConfig


class ContainersConfig:
    """
    A DTO representing the configuration of the containers that make up an emulation environment
    """

    def __init__(self, containers : List[NodeContainerConfig], network: str, agent_ip : str, router_ip : str,
                 subnet_mask: str, subnet_prefix: str, ids_enabled :bool, vulnerable_nodes = None):
        """
        Initializes the DTO

        :param containers: the list of containers
        :param network: the network name
        :param agent_ip: the ip of the agent
        :param router_ip: the ip of the router
        :param subnet_mask: the subnet mask
        :param subnet_prefix: the subnet prefix
        :param ids_enabled: whether the IDS is enabled or nt
        :param vulnerable_nodes: the list of vulnerable nodes
        """
        self.containers = containers
        self.network = network
        self.agent_ip = agent_ip
        self.router_ip = router_ip
        self.subnet_mask = subnet_mask
        self.subnet_prefix = subnet_prefix
        self.ids_enabled = ids_enabled
        self.vulnerable_nodes = vulnerable_nodes

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "containers:{},network:{},agent_ip:{},router_ip:{},subnet_mask:{},subnet_prefix:{}," \
               "ids_enabled:{},vulnerable_nodes:{}".format(
            self.containers, self.network, self.agent_ip, self.router_ip, self.subnet_mask, self.subnet_prefix,
            self.ids_enabled, self.vulnerable_nodes)