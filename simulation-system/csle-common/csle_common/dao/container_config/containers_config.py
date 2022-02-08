from typing import List
from csle_common.dao.container_config.node_container_config import NodeContainerConfig
from csle_common.dao.container_config.container_network import ContainerNetwork
import csle_common.constants.constants as constants


class ContainersConfig:
    """
    A DTO representing the configuration of the containers that make up an emulation environment
    """

    def __init__(self, containers : List[NodeContainerConfig], agent_ip : str, router_ip : str,
                 networks: List[ContainerNetwork],
                 ids_enabled :bool, vulnerable_nodes = None):
        """
        Initializes the DTO

        :param containers: the list of containers
        :param agent_ip: the ip of the agent
        :param router_ip: the ip of the router
        :param ids_enabled: whether the IDS is enabled or nt
        :param vulnerable_nodes: the list of vulnerable nodes
        :param networks: list of subnetworks
        """
        self.containers = containers
        self.agent_ip = agent_ip
        self.router_ip = router_ip
        self.ids_enabled = ids_enabled
        self.vulnerable_nodes = vulnerable_nodes
        self.networks = networks


    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"containers:{self.containers},networks:{self.networks},agent_ip:{self.agent_ip}, " \
               f"router_ip:{self.router_ip}" \
               f"ids_enabled:{self.ids_enabled},vulnerable_nodes:{self.vulnerable_nodes}"