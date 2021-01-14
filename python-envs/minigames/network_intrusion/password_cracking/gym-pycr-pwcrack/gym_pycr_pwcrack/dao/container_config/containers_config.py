from typing import List
from gym_pycr_pwcrack.dao.container_config.node_container_config import NodeContainerConfig


class ContainersConfig:

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