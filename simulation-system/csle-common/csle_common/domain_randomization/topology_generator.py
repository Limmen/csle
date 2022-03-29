from typing import List, Tuple
import random
import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.topology_config import TopologyConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_common.util.experiment_util import ExperimentsUtil


class TopologyGenerator:
    """
    A Utility Class for generating topology configuration files
    """

    @staticmethod
    def generate(num_nodes: int, subnet_prefix: str, subnet_id: int) -> Tuple[TopologyConfig, str, str, List]:
        """
        Generates a topology configuration

        :param num_nodes: the number of nodes in the topology
        :param subnet_prefix: the prefix of the subnet
        :return: The created topology
        """
        if num_nodes < 3:
            raise ValueError("At least three nodes are required to create a topology")

        agent_ip_suffix = TopologyGenerator.__generate_random_ip(blacklist=[])
        nodes_ip_suffixes = [agent_ip_suffix]
        router_ip_suffix = TopologyGenerator.__generate_random_ip(nodes_ip_suffixes)
        nodes_ip_suffixes.append(router_ip_suffix)
        for i in range(num_nodes - 2):
            ip_suffix = TopologyGenerator.__generate_random_ip(nodes_ip_suffixes)
            nodes_ip_suffixes.append(ip_suffix)

        net_id = 1
        client_net = ContainerNetwork(name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{subnet_id}_{net_id}",
                               subnet_mask=f"{subnet_prefix}.{net_id}{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                               subnet_prefix=f"{subnet_prefix}.{net_id}")
        net_id += 1
        gw_net = ContainerNetwork(name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{subnet_id}_{net_id}",
                                      subnet_mask=f"{subnet_prefix}.{net_id}{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                      subnet_prefix=f"{subnet_prefix}.{net_id}")

        network_mappings = {}
        network_mappings[client_net.name] = (client_net, [f"{client_net.subnet_prefix}.{agent_ip_suffix}"])
        network_mappings[gw_net.name] = (gw_net, [f"{gw_net.subnet_prefix}.{router_ip_suffix}"])
        net_to_attach_to = gw_net.name

        subnetwork_masks = [client_net.subnet_mask, gw_net.subnet_mask]

        node_configs = []
        agent_cfg = NodeFirewallConfig(
            ips_gw_default_policy_networks = [DefaultNetworkFirewallConfig(
                ip=f"{client_net.subnet_prefix}.{agent_ip_suffix}",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT, default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP, network=client_net
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{gw_net.subnet_prefix}.{router_ip_suffix}",
                default_input=constants.FIREWALL.ACCEPT, default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP, network=gw_net
            ),
            ], hostname="", output_accept=set(), input_accept=set(),
            forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
            routes=set())

        router_cfg = NodeFirewallConfig(
            ips_gw_default_policy_networks = [DefaultNetworkFirewallConfig(
                ip=f"{client_net.subnet_prefix}.{router_ip_suffix}",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT, default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT, network=client_net
            ),
                DefaultNetworkFirewallConfig(
                    ip=f"{gw_net.subnet_prefix}.{router_ip_suffix}",
                    default_gw=None,
                    default_input=constants.FIREWALL.ACCEPT, default_output=constants.FIREWALL.ACCEPT,
                    default_forward=constants.FIREWALL.ACCEPT, network=gw_net
                ),
            ], hostname="", output_accept=set(), input_accept=set(),
            forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
            routes=set())
        node_configs.append(agent_cfg)
        node_configs.append(router_cfg)

        vulnerable_nodes = []

        for i in range(len(nodes_ip_suffixes)):
            if nodes_ip_suffixes[i] != agent_ip_suffix and nodes_ip_suffixes[i] != router_ip_suffix:
                network_mappings[net_to_attach_to] = (
                    network_mappings[net_to_attach_to][0],network_mappings[net_to_attach_to][1] +
                    [f"{network_mappings[net_to_attach_to][0].subnet_prefix}.{nodes_ip_suffixes[i]}"])
                node_cfg = NodeFirewallConfig(
                    ips_gw_default_policy_networks = [DefaultNetworkFirewallConfig(
                        ip=f"{network_mappings[net_to_attach_to][0].subnet_prefix}.{nodes_ip_suffixes[i]}",
                        default_gw=None,
                        default_input=constants.FIREWALL.ACCEPT, default_output=constants.FIREWALL.ACCEPT,
                        default_forward=constants.FIREWALL.DROP, network=network_mappings[net_to_attach_to][0]
                    )], hostname="", output_accept=set(), input_accept=set(),
                    forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                    routes=set())
                if np.random.rand() < 0.3:
                    net_id += 1
                    new_net = ContainerNetwork(name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{subnet_id}_{net_id}",
                                          subnet_mask=f"{subnet_prefix}.{net_id}{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                          subnet_prefix=f"{subnet_prefix}.{net_id}")
                    node_cfg.ips_gw_default_policy_networks.append(DefaultNetworkFirewallConfig(
                        ip=f"{new_net.subnet_prefix}.{nodes_ip_suffixes[i]}",
                        default_gw=None,
                        default_input=constants.FIREWALL.ACCEPT, default_output=constants.FIREWALL.ACCEPT,
                        default_forward=constants.FIREWALL.DROP, network=new_net
                    ))
                    net_to_attach_to = new_net.name
                    network_mappings[new_net.name] = (new_net, [f"{new_net.subnet_prefix}.{nodes_ip_suffixes[i]}"])
                    subnetwork_masks.append(new_net.subnet_mask)
                    vulnerable_nodes.append(node_cfg)
                node_configs.append(node_cfg)

        topology = TopologyConfig(node_configs=node_configs, subnetwork_masks=subnetwork_masks)
        agent_ip = f"{client_net.subnet_prefix}.{agent_ip_suffix}"
        router_ip = f"{client_net.subnet_prefix}.{router_ip_suffix}"

        return topology, agent_ip, router_ip, vulnerable_nodes

    @staticmethod
    def __generate_random_ip(blacklist: List) -> int:
        """
        Utility function for generating a random IP address that is not in the given blacklist

        :param blacklist: a list of blacklisted IP address
        :return: The ip (last byte)
        """
        done = False
        ip_suffix = -1
        while not done:
            ip_suffix = random.randint(2, 254)
            if ip_suffix not in blacklist:
                done = True
        return ip_suffix

    @staticmethod
    def write_topology(topology: TopologyConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param path: the path to write the configuration to
        :return: None
        """
        path = ExperimentsUtil.default_topology_path(out_dir=path)
        ExperimentsUtil.write_topology_file(topology, path)


if __name__ == '__main__':
    topology, agent_ip, router_ip, vulnerable_nodes = TopologyGenerator.generate(
        num_nodes=15, subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}2", subnet_id=2)
    print(topology)
