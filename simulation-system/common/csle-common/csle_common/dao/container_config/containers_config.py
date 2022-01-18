from typing import List
from csle_common.dao.container_config.node_container_config import NodeContainerConfig


class ContainersConfig:
    """
    A DTO representing the configuration of the containers that make up an emulation environment
    """

    def __init__(self, containers : List[NodeContainerConfig], internal_network: str, agent_ip : str, router_ip : str,
                 internal_subnet_mask: str, internal_subnet_prefix: str, ids_enabled :bool,
                 external_network: str, external_subnet_mask: str, external_subnet_prefix: str, vulnerable_nodes = None):
        """
        Initializes the DTO

        :param containers: the list of containers
        :param internal_network: the network name
        :param agent_ip: the ip of the agent
        :param router_ip: the ip of the router
        :param internal_subnet_mask: the subnet mask
        :param internal_subnet_prefix: the subnet prefix
        :param ids_enabled: whether the IDS is enabled or nt
        :param vulnerable_nodes: the list of vulnerable nodes
        """
        self.containers = containers
        self.internal_network = internal_network
        self.agent_ip = agent_ip
        self.router_ip = router_ip
        self.internal_subnet_mask = internal_subnet_mask
        self.internal_subnet_prefix = internal_subnet_prefix
        self.ids_enabled = ids_enabled
        self.vulnerable_nodes = vulnerable_nodes
        self.external_network = external_network
        self.external_subnet_mask = external_subnet_mask
        self.external_subnet_prefix = external_subnet_prefix

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "containers:{},network:{},agent_ip:{},router_ip:{},subnet_mask:{},subnet_prefix:{}," \
               "ids_enabled:{},vulnerable_nodes:{}, external_network:{}, external_subnet_mask:{}, " \
               "external_subnet_prefix:{}".format(
            self.containers, self.internal_network, self.agent_ip, self.router_ip, self.internal_subnet_mask,
            self.internal_subnet_prefix,
            self.ids_enabled, self.vulnerable_nodes, self.external_network, self.external_subnet_mask,
            self.external_subnet_prefix)