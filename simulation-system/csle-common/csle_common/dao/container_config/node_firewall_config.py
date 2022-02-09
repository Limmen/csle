from typing import Set, List
from csle_common.dao.container_config.default_network_firewall_config import DefaultNetworkFirewallConfig

class NodeFirewallConfig:
    """
    A DTO object representing a firewall configuration of a container in an emulation environment
    """

    def __init__(self, ips_gw_default_policy_networks: List[DefaultNetworkFirewallConfig],
                 hostname: str, output_accept: Set[str], input_accept: Set[str],
                 forward_accept: Set[str], output_drop: Set[str], input_drop: Set[str],
                 forward_drop: Set[str],
                 routes: Set[str]
                 ):
        """
        Initializes the DTO

        :param ips_gw_default_policy_networks: List of ip,gw,default policy, network
        :param ip: the ip of the node
        :param hostname: the hostname of the node
        :param output_accept: the list of ips to accept output
        :param input_accept: the list of ips to accept input
        :param forward_accept: the list of ips to accept forward
        :param output_drop: the list of ips to drop output
        :param input_drop: the list of ips to drop input
        :param forward_drop: the list of ips to drop forward
        :param routes: the set of custom routes for the routing table
        """
        self.ips_gw_default_policy_networks = ips_gw_default_policy_networks
        self.hostname = hostname
        self.output_accept = output_accept
        self.input_accept = input_accept
        self.forward_accept = forward_accept
        self.output_drop = output_drop
        self.input_drop = input_drop
        self.forward_drop = forward_drop
        self.routes = routes


    def get_ips(self):
        """
        :return: list of ip addresses
        """
        return list(filter(lambda x: x is not None, map(lambda x: x.ip, self.ips_gw_default_policy_networks)))

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["hostname"] = self.hostname
        d["ips_gw_default_policy_networks"] = list(map(lambda x: x.to_dict(), self.ips_gw_default_policy_networks))
        d["output_accept"] = self.output_accept
        d["input_accept"] = self.input_accept
        d["forward_accept"] = self.forward_accept
        d["output_drop"] = self.output_drop
        d["input_drop"] = self.input_drop
        d["forward_drop"] = self.forward_drop
        d["routes"] = self.routes
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ips_gw_default_policy_networks:{self.ips_gw_default_policy_networks}, " \
               f"output_accept:{self.output_accept}, " \
               f"input_accept:{self.input_accept}, forward_accept:{self.forward_accept}, " \
               f"output_drop:{self.output_drop}, " \
               f"input_drop:{self.input_drop}, forward_drop:{self.forward_drop}, " \
               f"routers:{self.routes}, hostname: {self.hostname}"
