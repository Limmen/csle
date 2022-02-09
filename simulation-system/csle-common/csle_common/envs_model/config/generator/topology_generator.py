from typing import List, Tuple
import random
import numpy as np
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from csle_common.envs_model.config.generator.generator_util import GeneratorUtil
from csle_common.util.experiments_util import util
import csle_common.constants.constants as constants
from csle_common.dao.container_config.container_network import ContainerNetwork
from csle_common.dao.container_config.default_network_firewall_config import DefaultNetworkFirewallConfig


class TopologyGenerator:
    """
    A Utility Class for generating topology configuration files
    """

    @staticmethod
    def generate(num_nodes: int, subnet_prefix: str, subnet_id: int) -> Tuple[Topology, str, str, List]:
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

        topology = Topology(node_configs=node_configs, subnetwork_masks=subnetwork_masks)
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
    def create_topology(topology: Topology, emulation_config: EmulationConfig) -> None:
        """
        Utility function for connecting to a running emulation and creating the configuration

        :param topology: the topology configuration
        :param emulation_config: the emulation configuration
        :return: None
        """
        print("Creating topology")
        for node in topology.node_configs:
            ips = node.get_ips()
            ip = ips[0]
            print("Connecting to node:{}".format(ip))
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=ip)

            for route in node.routes:
                target, gw = route
                cmd = f"{constants.COMMANDS.SUDO_ADD_ROUTE} {target} gw {gw}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            for default_network_fw_config in node.ips_gw_default_policy_networks:
                if default_network_fw_config.default_gw is not None:
                    cmd = f"{constants.COMMANDS.SUDO_ADD_ROUTE} " \
                          f"-net {default_network_fw_config.network.subnet_mask.replace('/24', '')} " \
                          f"{constants.COMMANDS.NETMASK} {constants.CSLE.CSLE_EDGE_BITMASK} " \
                          f"gw {default_network_fw_config.default_gw}"
                    EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            cmd = constants.COMMANDS.CLEAR_IPTABLES
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            # Setup /etc/hosts
            cmd = f"{constants.COMMANDS.ECHO} '" + ip + " " + \
                  node.hostname + f"' | {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            cmd = f"{constants.COMMANDS.ECHO} " \
                  f"{constants.ETC_HOSTS.DEFAULT_HOST_LINE_1} | {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            cmd = f"{constants.COMMANDS.ECHO} {constants.ETC_HOSTS.DEFAULT_HOST_LINE_2} " \
                  f"| {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            cmd = f"{constants.COMMANDS.ECHO} {constants.ETC_HOSTS.DEFAULT_HOST_LINE_3} " \
                  f"| {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            cmd = f"{constants.COMMANDS.ECHO} {constants.ETC_HOSTS.DEFAULT_HOST_LINE_4} " \
                  f"| {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            cmd = f"{constants.COMMANDS.ECHO} {constants.ETC_HOSTS.DEFAULT_HOST_LINE_5} " \
                  f"| {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            cmd = f"{constants.COMMANDS.ECHO} {constants.ETC_HOSTS.DEFAULT_HOST_LINE_6} " \
                  f"| {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            for node2 in topology.node_configs:
                ips2 = node.get_ips()
                if ip not in ips2:
                    cmd = f"{constants.COMMANDS.ECHO} '" + ips2[0] + " " + node2.hostname \
                          + f"' | {constants.ETC_HOSTS.APPEND_TO_ETC_HOSTS}"
                    o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            # Setup iptables and arptables
            for output_node in node.output_accept:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_OUTPUT} -d {output_node} -j {constants.FIREWALL.ACCEPT}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_OUTPUT} -d {output_node} -j {constants.FIREWALL.ACCEPT}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            for input_node in node.input_accept:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_INPUT} -s {input_node} -j {constants.FIREWALL.ACCEPT}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_INPUT} -s {input_node} -j {constants.FIREWALL.ACCEPT}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            for forward_node in node.forward_accept:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_FORWARD} -d {forward_node} -j {constants.FIREWALL.ACCEPT}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            for output_node in node.output_drop:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_OUTPUT} -d {output_node} -j {constants.FIREWALL.DROP}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_OUTPUT} -d {output_node} -j {constants.FIREWALL.DROP}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            for input_node in node.input_drop:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_INPUT} -s {input_node} -j {constants.FIREWALL.DROP}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_INPUT} -s {input_node} -j {constants.FIREWALL.DROP}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            for forward_node in node.forward_drop:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_FORWARD} -d {forward_node} -j {constants.FIREWALL.DROP}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            for default_network_fw_config in node.ips_gw_default_policy_networks:
                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_OUTPUT} -d " \
                      f"{default_network_fw_config.network.subnet_mask} -j " \
                      f"{default_network_fw_config.default_output}"
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_OUTPUT} -d " \
                      f"{default_network_fw_config.network.subnet_mask} -j " \
                      f"{default_network_fw_config.default_output}"
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_INPUT} -d " \
                      f"{default_network_fw_config.network.subnet_mask} -j " \
                      f"{default_network_fw_config.default_input}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_INPUT} -d " \
                      f"{default_network_fw_config.network.subnet_mask} -j " \
                      f"{default_network_fw_config.default_input}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

                cmd = f"{constants.COMMANDS.IPTABLES_APPEND_FORWARD} -d " \
                      f"{default_network_fw_config.network.subnet_mask} -j " \
                      f"{default_network_fw_config.default_input}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
                cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_FORWARD} -d " \
                      f"{default_network_fw_config.network.subnet_mask} -j " \
                      f"{default_network_fw_config.default_input}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            GeneratorUtil.disconnect_admin(emulation_config=emulation_config)

    @staticmethod
    def write_topology(topology: Topology, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param path: the path to write the configuration to
        :return: None
        """
        path = util.default_topology_path(out_dir=path)
        util.write_topology_file(topology, path)


if __name__ == '__main__':
    topology, agent_ip, router_ip, vulnerable_nodes = TopologyGenerator.generate(
        num_nodes=15, subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}2", subnet_id=2)
    print(topology)
