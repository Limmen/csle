import csle_common.constants.constants as constants
from csle_common.dao.network.node_type import NodeType
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.dao.container_config.users_config import UsersConfig
from csle_common.dao.container_config.flags_config import FlagsConfig
from csle_common.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.traffic_config import TrafficConfig
from csle_common.dao.container_config.resources_config import ResourcesConfig
from csle_common.dao.container_config.log_sink_config import LogSinkConfig
from csle_common.dao.network.network_config import NetworkConfig
from csle_common.dao.container_config.services_config import ServicesConfig
from csle_common.dao.network.credential import Credential
from csle_common.dao.network.node import Node


class EmulationEnvConfig:
    """
    Class representing the configuration of an emulation
    """

    def __init__(self, name: str, containers_config: ContainersConfig, users_config: UsersConfig,
                 flags_config: FlagsConfig,
                 vuln_config: VulnerabilitiesConfig, topology_config: Topology, traffic_config: TrafficConfig,
                 resources_config: ResourcesConfig, log_sink_config: LogSinkConfig, services_config: ServicesConfig):
        """
        Initializes the object

        :param name: the name of the emulation
        :param containers_config: the containers configuration
        :param users_config: the users configuration
        :param flags_config: the flags configuration
        :param vuln_config: the vulnerabilities configuration
        :param topology_config: the topology configuration
        :param traffic_config: the traffic configuration
        :param resources_config: the resources configuration
        :param services_config: the services configuration
        """
        self.name = name
        self.containers_config = containers_config
        self.users_config = users_config
        self.flags_config = flags_config
        self.vuln_config = vuln_config
        self.topology_config = topology_config
        self.traffic_config = traffic_config
        self.resources_config = resources_config
        self.log_sink_config = log_sink_config
        self.services_config = services_config

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["name"] = self.name
        d["containers_config"] = self.containers_config.to_dict()
        d["users_config"] = self.users_config.to_dict()
        d["flags_config"] = self.flags_config.to_dict()
        d["vuln_config"] = len(self.vuln_config.to_dict())
        d["topology_config"] = self.topology_config.to_dict()
        d["traffic_config"] = self.traffic_config.to_dict()
        d["resources_config"] = self.resources_config.to_dict()
        d["log_sink_config"] = self.log_sink_config.to_dict()
        d["services_config"] = self.services_config.to_dict()
        return d

    def __str__(self) -> str:
        """
        :return:  a string representation of the object
        """
        return f"name: {self.name}, containers_config: {self.containers_config}, users_config: {self.users_config}, " \
               f"flags_config: {self.flags_config}, vuln_config: {self.vuln_config}, " \
               f"topology_config: {self.topology_config}, traffic_config: {self.traffic_config}, " \
               f"resources_config: {self.resources_config}, log_sink_config:{self.log_sink_config}, " \
               f"services_config: {self.services_config}"


    def network_config(self):
        nodes = []
        vulnerable_nodes = []
        for c in self.containers_config.containers:
            ip_ids = list(map(lambda ip: int(ip.rsplit(".", 1)[-1]), c.get_ips()))
            node_type = NodeType.SERVER
            for router_img in constants.CONTAINER_IMAGES.ROUTER_IMAGES:
                if router_img in c.name:
                    node_type = NodeType.ROUTER
            for hacker_img in constants.CONTAINER_IMAGES.HACKER_IMAGES:
                if hacker_img in c.name:
                    node_type = NodeType.HACKER

            flags = []
            for node_flags_cfg in self.flags_config.flags:
                if node_flags_cfg.ip in c.get_ips():
                    flags = node_flags_cfg.flags

            level = c.level
            vulnerabilities = self.vuln_config.vulnerabilities

            services = []
            for node_services_cfg in self.services_config.services_configs:
                if node_services_cfg.ip in c.get_ips():
                    services = node_services_cfg.services

            os = c.os

            credentials = []
            for vuln in vulnerabilities:
                credentials = credentials + vuln.credentials
            for serv in services:
                credentials = credentials + serv.credentials

            for user_cfg in self.users_config.users:
                if user_cfg.ip in c.get_ips():
                    for user in user_cfg.users:
                        credentials.append(Credential(username=user[0], pw=user[1], root=user[2]))

            root_usernames = []
            for cred in credentials:
                if cred.root:
                    root_usernames.append(cred.username)
            visible = True
            reachable_nodes = []
            network_names = list(map(lambda x: x[1].name, c.ips_and_networks))
            for c2 in self.containers_config.containers:
                reachable = False
                if c2.name != c.name:
                    for ip_net in c2.ips_and_networks:
                        if ip_net[1].name in network_names:
                            reachable = True
                if reachable:
                    reachable_nodes = reachable_nodes + c2.get_ips()
            node = Node(
                ips = c.get_ips(),
                ip_ids = ip_ids, id = ip_ids[0], type=node_type, flags=flags, level=int(level),
                vulnerabilities=vulnerabilities, services=services, os=os, credentials=credentials,
                root_usernames=root_usernames, visible=visible, reachable_nodes=reachable_nodes, firewall=False
            )
            nodes.append(node)




        net_conf = NetworkConfig(subnet_masks=self.topology_config.subnetwork_masks,
                                 vulnerable_nodes=self.containers_config.vulnerable_nodes, nodes=nodes,
                                 agent_reachable=self.containers_config.agent_reachable_nodes)
