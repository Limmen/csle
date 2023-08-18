from typing import List, Union, Dict, Any
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.util.general_util import GeneralUtil
from csle_base.json_serializable import JSONSerializable


class ContainersConfig(JSONSerializable):
    """
    A DTO representing the configuration of the containers that make up an emulation environment
    """

    def __init__(self, containers: List[NodeContainerConfig], agent_ip: str, router_ip: str,
                 networks: List[ContainerNetwork], ids_enabled: bool,
                 vulnerable_nodes=None, agent_reachable_nodes=None):
        """
        Initializes the DTO

        :param containers: the list of containers
        :param agent_ip: the ip of the agent
        :param router_ip: the ip of the router
        :param ids_enabled: whether the IDS is enabled or nt
        :param vulnerable_nodes: the list of vulnerable nodes
        :param networks: list of subnetworks
        :param agent_reachable_nodes: nodes directly reachable by the attacker
        """
        self.containers = containers
        self.agent_ip = agent_ip
        self.router_ip = router_ip
        self.ids_enabled = ids_enabled
        self.vulnerable_nodes = vulnerable_nodes
        self.networks = networks
        self.agent_reachable_nodes = agent_reachable_nodes

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainersConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ContainersConfig(
            containers=list(map(lambda x: NodeContainerConfig.from_dict(x), d["containers"])),
            agent_ip=d["agent_ip"], router_ip=d["router_ip"],
            networks=list(map(lambda x: ContainerNetwork.from_dict(x), d["networks"])),
            ids_enabled=d["ids_enabled"], vulnerable_nodes=d["vulnerable_nodes"],
            agent_reachable_nodes=d["agent_reachable_nodes"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["agent_ip"] = self.agent_ip
        d["router_ip"] = self.router_ip
        d["networks"] = list(map(lambda x: x.to_dict(), self.networks))
        d["ids_enabled"] = self.ids_enabled
        d["vulnerable_nodes"] = self.vulnerable_nodes
        d["containers"] = list(map(lambda x: x.to_dict(), self.containers))
        d["agent_reachable_nodes"] = self.agent_reachable_nodes
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"containers:{self.containers},networks:{self.networks},agent_ip:{self.agent_ip}, " \
               f"router_ip:{self.router_ip}" \
               f"ids_enabled:{self.ids_enabled},vulnerable_nodes:{self.vulnerable_nodes}, " \
               f"agent_reachable_nodes: {self.agent_reachable_nodes}"

    def get_reachable_ips(self, container: NodeContainerConfig) -> List[str]:
        """
        Get list of IP addresses reachable from a given container

        :param container: the container to get reachable IPs from
        :return:
        """
        reachable_ips = []
        for c in self.containers:
            for ip_net in c.ips_and_networks:
                ip, net = ip_net
                for container_ip_net in container.ips_and_networks:
                    container_ip, container_net = container_ip_net
                    if net.name == container_net.name:
                        reachable_ips.append(ip)
        return reachable_ips

    def get_agent_container(self) -> Union[NodeContainerConfig, None]:
        """
        :return: get container of the attacker agent
        """
        for container in self.containers:
            if self.agent_ip in container.get_ips():
                return container
        return None

    def get_agent_reachable_ips(self) -> List[str]:
        """
        :return: list of ips reachable for the attacker agent
        """
        agent_container = self.get_agent_container()
        if agent_container is None:
            raise ValueError("Agent container is None")
        return self.get_reachable_ips(container=agent_container)

    def get_container_from_ip(self, ip: str) -> Union[NodeContainerConfig, None]:
        """
        Utility function for getting the container

        :param ip: the ip of the container
        :return: the container with the given ip or None
        """
        for c in self.containers:
            if ip in c.get_ips() or ip == c.docker_gw_bridge_ip:
                return c
        return None

    def get_container_from_full_name(self, name: str) -> Union[NodeContainerConfig, None]:
        """
        Utility function for getting the container

        :param name: the full name of the container
        :return: the container with the given ip or None
        """
        for c in self.containers:
            if name == c.full_name_str:
                return c
        return None

    @staticmethod
    def from_json_file(json_file_path: str) -> "ContainersConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ContainersConfig.from_dict(json.loads(json_str))

    def copy(self) -> "ContainersConfig":
        """
        :return: a copy of the DTO
        """
        return ContainersConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int, physical_servers: List[str]) -> "ContainersConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :param physical_servers: the physical servers where the execution will be deployed
        :return: the new config
        """
        config = self.copy()
        config.containers = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet,
                                                                         physical_servers=physical_servers),
                                     config.containers))
        config.networks = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet),
                                   config.networks))
        config.agent_ip = GeneralUtil.replace_first_octet_of_ip(ip=config.agent_ip, ip_first_octet=ip_first_octet)
        config.router_ip = GeneralUtil.replace_first_octet_of_ip(ip=config.router_ip, ip_first_octet=ip_first_octet)
        config.vulnerable_nodes = list(map(lambda x: GeneralUtil.replace_first_octet_of_ip(
            ip=x, ip_first_octet=ip_first_octet), config.vulnerable_nodes))
        config.agent_reachable_nodes = list(map(lambda x: GeneralUtil.replace_first_octet_of_ip(
            ip=x, ip_first_octet=ip_first_octet), config.agent_reachable_nodes))
        return config
