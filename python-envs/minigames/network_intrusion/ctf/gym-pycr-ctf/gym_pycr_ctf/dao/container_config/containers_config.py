from typing import List
from gym_pycr_ctf.dao.container_config.node_container_config import NodeContainerConfig


class ContainersConfig:
    """
    A DTO representing the configuration of the containers that make up an emulation environment
    """

    def __init__(self, containers : List[NodeContainerConfig], network: str, agent_ip : str, router_ip : str,
                 subnet_mask: str, subnet_prefix: str, ids_enabled :bool, vulnerable_nodes = None):
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