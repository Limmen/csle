from typing import List
import random
import numpy as np
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from csle_common.envs_model.config.generator.generator_util import GeneratorUtil
from csle_common.util.experiments_util import util
import csle_common.constants.constants as constants


class TopologyGenerator:
    """
    A Utility Class for generating topology configuration files
    """

    @staticmethod
    def generate(num_nodes: int, subnet_prefix: str) -> Topology:
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
        for i in range(num_nodes - 2):
            ip_suffix = TopologyGenerator.__generate_random_ip(nodes_ip_suffixes)
            nodes_ip_suffixes.append(ip_suffix)

        node_id_d = {}
        node_id_d_inv = {}
        for i in range(len(nodes_ip_suffixes)):
            node_id_d[nodes_ip_suffixes[i]] = i
            node_id_d_inv[i] = nodes_ip_suffixes[i]

        adj_matrix = np.zeros((len(nodes_ip_suffixes) + 1, len(nodes_ip_suffixes) + 1))

        reachable = set()
        reachable.add(agent_ip_suffix)

        gateways = {}

        # Attach all nodes to the topology randomly
        for i in range(len(nodes_ip_suffixes)):
            if nodes_ip_suffixes[i] not in reachable:
                l = list(reachable)
                attach = random.randint(0, len(l) - 1)
                adj_matrix[node_id_d[l[attach]]][node_id_d[nodes_ip_suffixes[i]]] = 1
                adj_matrix[node_id_d[nodes_ip_suffixes[i]]][node_id_d[l[attach]]] = 1
                reachable.add(nodes_ip_suffixes[i])
                gateways[nodes_ip_suffixes[i]] = l[attach]

        # Create some random links
        for i in range(adj_matrix.shape[0] - 1):
            for j in range(adj_matrix.shape[1] - 1):
                if j == i:
                    adj_matrix[i][j] = 1
                if np.random.rand() < 0.1:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1

        router_ip_suffix = TopologyGenerator.__generate_random_ip(nodes_ip_suffixes)
        adj_matrix[node_id_d[agent_ip_suffix]][-1] = 1
        adj_matrix[-1][node_id_d[agent_ip_suffix]] = 1

        # gw and agent same connections
        adj_matrix[-1] = adj_matrix[node_id_d[agent_ip_suffix]]
        for i in range(len(nodes_ip_suffixes)):
            if not nodes_ip_suffixes[i] == agent_ip_suffix:
                if adj_matrix[node_id_d[nodes_ip_suffixes[i]]][node_id_d[agent_ip_suffix]] == 1:
                    adj_matrix[node_id_d[nodes_ip_suffixes[i]]][-1] = 1

        gateways[agent_ip_suffix] = router_ip_suffix

        nodes_ip_suffixes.append(router_ip_suffix)
        node_id_d_inv[len(nodes_ip_suffixes) - 1] = router_ip_suffix
        node_id_d[router_ip_suffix] = len(nodes_ip_suffixes) - 1

        node_fw_configs = []
        for i in range(len(nodes_ip_suffixes)):
            ip = subnet_prefix + str(nodes_ip_suffixes[i])
            net_gw = subnet_prefix + "1"
            output_accept = set()
            input_accept = set()
            forward_accept = set()
            output_accept.add(net_gw)
            input_accept.add(net_gw)
            forward_accept.add(net_gw)
            output_drop = set()
            input_drop = set()
            forward_drop = set()
            routes = set()
            for j in range(adj_matrix.shape[1]):
                if adj_matrix[i][j] == 1:
                    input_accept.add(subnet_prefix + str(node_id_d_inv[j]))
                    output_accept.add(subnet_prefix + str(node_id_d_inv[j]))
                    forward_accept.add(subnet_prefix + str(node_id_d_inv[j]))
                else:
                    input_drop.add(subnet_prefix + str(node_id_d_inv[j]))
                    output_drop.add(subnet_prefix + str(node_id_d_inv[j]))
                    forward_drop.add(subnet_prefix + str(node_id_d_inv[j]))

            default_gw = None
            if nodes_ip_suffixes[i] == agent_ip_suffix:
                default_gw = subnet_prefix + str(router_ip_suffix)

            node_cfg = NodeFirewallConfig(
                ip=ip, output_accept=output_accept, input_accept=input_accept,
                forward_accept=forward_accept, output_drop=set(), input_drop=set(), forward_drop=set(),
                routes=set(), default_internal_input=constants.FIREWALL.DROP,
                default_internal_output=constants.FIREWALL.DROP, default_internal_forward=constants.FIREWALL.DROP,
                default_internal_gw=default_gw)
            node_fw_configs.append(node_cfg)

        topology = Topology(node_configs=node_fw_configs, subnetwork=subnet_prefix + "0/24")
        agent_ip = subnet_prefix + str(agent_ip_suffix)
        router_ip = subnet_prefix + str(router_ip_suffix)

        return adj_matrix, gateways, topology, agent_ip, router_ip, node_id_d, node_id_d_inv

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
            print("Connecting to node:{}".format(node.ip))
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=node.ip)

            for route in node.routes:
                target, gw = route
                cmd = f"{constants.COMMANDS.SUDO_ADD_ROUTE} {target} gw {gw}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            # Set default internal gw
            if node.default_internal_gw is not None:
                cmd = f"{constants.COMMANDS.SUDO_ADD_ROUTE} " \
                      f"-net {node.internal_subnetwork_mask.replace('/24', '')} " \
                      f"{constants.COMMANDS.NETMASK} {constants.CSLE.CSLE_SUBNETMASK_DIGITS} " \
                      f"gw {node.default_internal_gw}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            # Set default external gw
            if node.default_external_gw is not None:
                cmd = f"{constants.COMMANDS.SUDO_ADD_ROUTE} " \
                      f"-net {node.external_subnetwork_mask.replace('/24', '')} " \
                      f"{constants.COMMANDS.NETMASK} {constants.CSLE.CSLE_SUBNETMASK_DIGITS} " \
                      f"gw {node.default_external_gw}"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            cmd = constants.COMMANDS.CLEAR_IPTABLES
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            # Setup /etc/hosts
            cmd = f"{constants.COMMANDS.ECHO} '" + node.ip + " " + \
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
                if node2.ip != node.ip:
                    cmd = f"{constants.COMMANDS.ECHO} '" + node2.ip + " " + node2.hostname \
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

            # Default rules on internal network
            cmd = f"{constants.COMMANDS.IPTABLES_APPEND_OUTPUT} -d {node.internal_subnetwork_mask} -j " \
                  f"{node.default_internal_output}"
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
            cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_OUTPUT} -d {node.internal_subnetwork_mask} -j " \
                  f"{node.default_internal_output}"
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            cmd = f"{constants.COMMANDS.IPTABLES_APPEND_INPUT} -d {node.internal_subnetwork_mask} -j " \
                  f"{node.default_internal_input}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
            cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_INPUT} -d {node.internal_subnetwork_mask} -j " \
                  f"{node.default_internal_input}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            cmd = f"{constants.COMMANDS.IPTABLES_APPEND_FORWARD} -d {node.internal_subnetwork_mask} -j " \
                  f"{node.default_internal_forward}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
            cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_FORWARD} -d {node.internal_subnetwork_mask} -j " \
                  f"{node.default_internal_forward}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            # Default rules on external network
            cmd = f"{constants.COMMANDS.IPTABLES_APPEND_OUTPUT} -d {node.external_subnetwork_mask} -j " \
                  f"{node.default_external_output}"
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
            cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_OUTPUT} -d {node.external_subnetwork_mask} -j " \
                  f"{node.default_external_output}"
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            cmd = f"{constants.COMMANDS.IPTABLES_APPEND_INPUT} -d {node.external_subnetwork_mask} -j " \
                  f"{node.default_external_input}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
            cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_INPUT} -d {node.external_subnetwork_mask} -j " \
                  f"{node.default_external_input}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)

            cmd = f"{constants.COMMANDS.IPTABLES_APPEND_FORWARD} -d {node.external_subnetwork_mask} -j " \
                  f"{node.default_external_forward}"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn, wait_for_completion=True)
            cmd = f"{constants.COMMANDS.ARPTABLES_APPEND_FORWARD} -d {node.external_subnetwork_mask} -j " \
                  f"{node.default_external_forward}"
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
    adj_matrix, gws, topology = TopologyGenerator.generate(num_nodes=10,
                                                           subnet_prefix=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}2.")
    print(adj_matrix)
    print(gws)
    print(topology)
