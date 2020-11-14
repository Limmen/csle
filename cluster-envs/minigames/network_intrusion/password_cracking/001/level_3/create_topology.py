import os
from gym_pycr_pwcrack.dao.container_config.topology import Topology
from gym_pycr_pwcrack.dao.container_config.node_firewall_config import NodeFirewallConfig
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.envs.logic.cluster.cluster_util import ClusterUtil


def connect_admin(cluster_config: ClusterConfig, ip: str):
    cluster_config.agent_ip = ip
    cluster_config.connect_agent()


def disconnect_admin(cluster_config: ClusterConfig):
    cluster_config.close()


def default_topology() -> Topology:
    node_1 = NodeFirewallConfig(ip="172.18.3.10",
                                output_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79",
                                                   "172.18.3.191", "172.18.3.10", "172.18.3.1",
                                                   "172.18.3.4", "172.18.3.5", "172.18.3.6", "172.18.3.7",
                                                   "172.18.3.8", "172.18.3.9"
                                                   ]),
                                input_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79",
                                                  "172.18.3.191", "172.18.3.10", "172.18.3.1",
                                                  "172.18.3.4", "172.18.3.5", "172.18.3.6", "172.18.3.7",
                                                  "172.18.3.8", "172.18.3.9"]),
                                forward_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79",
                                                    "172.18.3.191", "172.18.3.1", "172.18.3.4", "172.18.3.5",
                                                    "172.18.3.6", "172.18.3.7", "172.18.3.8", "172.18.3.9"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)

    node_2 = NodeFirewallConfig(ip="172.18.3.2",
                                output_accept=set(
                                    ["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79", "172.18.3.191",
                                     "172.18.3.10", "172.18.3.1", "172.18.3.54"]),
                                input_accept=set(
                                    ["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79", "172.18.3.191",
                                     "172.18.3.10", "172.18.3.1", "172.18.3.54"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set([("172.18.3.7", "172.18.3.3"), ("172.18.3.101", "172.18.3.3"),
                                            ("172.18.3.62", "172.18.3.3"), ("172.18.3.61", "172.18.3.3"),
                                            ("172.18.3.74", "172.18.3.3")]),
                                default_input="DROP", default_output="DROP", default_forward="ACCEPT", default_gw=None)

    node_3 = NodeFirewallConfig(ip="172.18.3.3",
                                output_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79",
                                                   "172.18.3.191", "172.18.3.10", "172.18.3.74", "172.18.3.1",
                                                   "172.18.3.61"]),
                                input_accept=set(
                                    ["172.18.3.74", "172.18.3.7", "172.18.3.21", "172.18.3.79", "172.18.3.191",
                                     "172.18.3.10", "172.18.3.1", "172.18.3.101", "172.18.3.61"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(),
                                forward_drop=set(["172.18.3.54"]),
                                routes=set([("172.18.3.54", "172.18.3.2"), ("172.18.3.7", "172.18.3.74"),
                                            ("172.18.3.62", "172.18.3.74"), ("172.18.3.101", "172.18.3.74")]),
                                default_input="ACCEPT", default_output="DROP", default_forward="ACCEPT",
                                default_gw=None)

    node_4 = NodeFirewallConfig(ip="172.18.3.21",
                                output_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21",
                                                   "172.18.3.79", "172.18.3.191", "172.18.3.10", "172.18.3.1"]),
                                input_accept=set(
                                    ["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79", "172.18.3.191",
                                     "172.18.3.10", "172.18.3.1"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(
                                    [("172.18.3.7", "172.18.3.3"), ("172.18.3.101", "172.18.3.3"),
                                     ("172.18.3.62", "172.18.3.3"),
                                     ("172.18.3.61", "172.18.3.3"), ("172.18.3.74", "172.18.3.3"),
                                     ("172.18.3.54", "172.18.3.2")]
                                ),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                )

    node_4 = NodeFirewallConfig(ip="172.18.3.79",
                                output_accept=set(
                                    ["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79", "172.18.3.191",
                                     "172.18.3.10", "172.18.3.1"]),
                                input_accept=set(
                                    ["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79", "172.18.3.191",
                                     "172.18.3.10", "172.18.3.1"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(
                                    [("172.18.3.7", "172.18.3.3"), ("172.18.3.101", "172.18.3.3"),
                                     ("172.18.3.62", "172.18.3.3"), ("172.18.3.61", "172.18.3.3"),
                                     ("172.18.3.74", "172.18.3.3"), ("172.18.3.54", "172.18.3.2")]
                                ),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)

    node_5 = NodeFirewallConfig(ip="172.18.3.191",
                                output_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21",
                                                   "172.18.3.79", "172.18.3.191", "172.18.3.10", "172.18.3.1"]),
                                input_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21",
                                                  "172.18.3.79", "172.18.3.191", "172.18.3.10", "172.18.3.1"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.3.10")

    node_6 = NodeFirewallConfig(ip="172.18.3.54",
                                output_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79",
                                                   "172.18.3.191", "172.18.3.10", "172.18.3.54", "172.18.3.1",
                                                   "172.18.3.11", "172.18.3.12", "172.18.3.13", "172.18.3.14"]),
                                input_accept=set(["172.18.3.2", "172.18.3.1", "172.18.3.11", "172.18.3.12",
                                                  "172.18.3.13", "172.18.3.14"]),
                                forward_accept=set(["172.18.3.11", "172.18.3.12", "172.18.3.13", "172.18.3.14"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.3.2"
                                )

    node_7 = NodeFirewallConfig(ip="172.18.3.74",
                                output_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79",
                                                   "172.18.3.191", "172.18.3.10", "172.18.3.61", "172.18.3.74",
                                                   "172.18.3.101", "172.18.3.62", "172.18.3.1"]),
                                input_accept=set(["172.18.3.3", "172.18.3.61", "172.18.3.62", "172.18.3.74",
                                                  "172.18.3.7", "172.18.3.101", "172.18.3.1"]),
                                forward_accept=set(["172.18.3.101", "172.18.3.62", "172.18.3.61"]),
                                output_drop=set(), input_drop=set(),
                                forward_drop=set(["172.18.3.7", "172.18.3.101", "172.18.3.62"]),
                                routes=set([
                                    ("172.18.3.2", "172.18.3.3"), ("172.18.3.21", "172.18.3.3"),
                                    ("172.18.3.54", "172.18.3.3"), ("172.18.3.79", "172.18.3.3"),
                                    ("172.18.3.10", "172.18.3.3"), ("172.18.3.191", "172.18.3.3"),
                                    ("172.18.3.61", "172.18.3.3"), ("172.18.3.7", "172.18.3.62")
                                ]),
                                default_input="DROP", default_output="DROP", default_forward="ACCEPT",
                                default_gw=None)

    node_8 = NodeFirewallConfig(ip="172.18.3.61",
                                output_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79",
                                                   "172.18.3.191", "172.18.3.10", "172.18.3.61", "172.18.3.74",
                                                   "172.18.3.1",
                                                   "172.18.3.19", "172.18.3.20", "172.18.3.21", "172.18.3.22",
                                                   "172.18.3.23", "172.18.3.24", "172.18.3.25", "172.18.3.28"]),
                                input_accept=set(["172.18.3.3", "172.18.3.61", "172.18.3.62", "172.18.3.74",
                                                  "172.18.3.7", "172.18.3.101", "172.18.3.1",
                                                  "172.18.3.19", "172.18.3.20", "172.18.3.21", "172.18.3.22",
                                                  "172.18.3.23", "172.18.3.24", "172.18.3.25", "172.18.3.28"
                                                  ]),
                                forward_accept=set(["172.18.3.19", "172.18.3.20", "172.18.3.21", "172.18.3.22",
                                                   "172.18.3.23", "172.18.3.24", "172.18.3.25", "172.18.3.28"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.3.3")

    node_9 = NodeFirewallConfig(ip="172.18.3.62",
                                output_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79",
                                                   "172.18.3.191", "172.18.3.10", "172.18.3.61", "172.18.3.74",
                                                   "172.18.3.1",
                                                   "172.18.3.101", "172.18.3.62", "172.18.3.7",
                                                   "172.18.3.15", "172.18.3.16", "172.18.3.17", "172.18.3.18"]),
                                input_accept=set(["172.18.3.74", "172.18.3.7", "172.18.3.101", "172.18.3.1",
                                                  "172.18.3.15", "172.18.3.16", "172.18.3.17", "172.18.3.18"]),
                                forward_accept=set(["172.18.3.15", "172.18.3.16", "172.18.3.17", "172.18.3.18"]),
                                output_drop=set(), input_drop=set(),
                                routes=set([("172.18.3.2", "172.18.3.74"), ("172.18.3.21", "172.18.3.74"),
                                            ("172.18.3.54", "172.18.3.74"), ("172.18.3.79", "172.18.3.74"),
                                            ("172.18.3.10", "172.18.3.74"), ("172.18.3.191", "172.18.3.74"),
                                            ("172.18.3.61", "172.18.3.74"), ("172.18.3.101", "172.18.3.74")]),
                                forward_drop=set(["172.18.3.7"]), default_input="DROP", default_output="DROP",
                                default_forward="ACCEPT", default_gw=None)

    node_10 = NodeFirewallConfig(ip="172.18.3.101",
                                 output_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79",
                                                    "172.18.3.191", "172.18.3.10", "172.18.3.61", "172.18.3.74",
                                                    "172.18.3.101", "172.18.3.62", "172.18.3.1"]),
                                 input_accept=set(["172.18.3.74", "172.18.3.7", "172.18.3.62", "172.18.3.1"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.3.74")

    node_11 = NodeFirewallConfig(ip="172.18.3.7",
                                 output_accept=set(["172.18.3.2", "172.18.3.3", "172.18.3.21", "172.18.3.79",
                                                    "172.18.3.191", "172.18.3.10", "172.18.3.61", "172.18.3.74",
                                                    "172.18.3.101", "172.18.3.62", "172.18.3.7", "172.18.3.1"]),
                                 input_accept=set(["172.18.3.62", "172.18.3.1"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.3.62")
    node_12 = NodeFirewallConfig(ip="172.18.3.4", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT", default_forward="ACCEPT",
                                 default_gw="172.18.3.10")
    node_13 = NodeFirewallConfig(ip="172.18.3.5", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.10")
    node_14 = NodeFirewallConfig(ip="172.18.3.6", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.10")
    node_15 = NodeFirewallConfig(ip="172.18.3.7", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.10")
    node_16 = NodeFirewallConfig(ip="172.18.3.8", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.10")
    node_17 = NodeFirewallConfig(ip="172.18.3.9", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.10")
    node_18 = NodeFirewallConfig(ip="172.18.3.11", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.54")
    node_19 = NodeFirewallConfig(ip="172.18.3.12", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.54")
    node_20 = NodeFirewallConfig(ip="172.18.3.13", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.54")
    node_21 = NodeFirewallConfig(ip="172.18.3.14", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.54")
    node_22 = NodeFirewallConfig(ip="172.18.3.15", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.62")
    node_23 = NodeFirewallConfig(ip="172.18.3.16", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.62")
    node_23 = NodeFirewallConfig(ip="172.18.3.17", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.62")
    node_24 = NodeFirewallConfig(ip="172.18.3.18", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.62")
    node_25 = NodeFirewallConfig(ip="172.18.3.19", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.61")
    node_26 = NodeFirewallConfig(ip="172.18.3.20", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.61")
    node_27 = NodeFirewallConfig(ip="172.18.3.22", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.61")
    node_28 = NodeFirewallConfig(ip="172.18.3.23", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.61")
    node_29 = NodeFirewallConfig(ip="172.18.3.24", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.61")
    node_30 = NodeFirewallConfig(ip="172.18.3.25", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.61")
    node_31 = NodeFirewallConfig(ip="172.18.3.28", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw="172.18.3.61")
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11]
    topology = Topology(node_configs=node_configs, subnetwork="172.18.3.0/24")
    return topology


def write_default_topology(path: str = None) -> None:
    """
    Writes the default configuration to a json file

    :param path: the path to write the configuration to
    :return: None
    """
    if path is None:
        path = util.default_topology_path()
    topology = default_topology()
    util.write_topology_file(topology, path)


def create_topology(topology: Topology, cluster_config: ClusterConfig):
    for node in topology.node_configs:
        print("node:{}".format(node.ip))
        connect_admin(cluster_config=cluster_config, ip=node.ip)

        for route in node.routes:
            target, gw = route
            cmd="sudo route add {} gw {}".format(target, gw)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        if node.default_gw is not None:
            cmd = "sudo route add -net {} netmask 255.255.255.0 gw {}".format(topology.subnetwork.replace("/24", ""),
                                                                                      node.default_gw)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        cmd = "sudo iptables -F"
        ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        for output_node in node.output_accept:
            cmd = "sudo iptables -A OUTPUT -d {} -j ACCEPT".format(output_node)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        for input_node in node.input_accept:
            cmd = "sudo iptables -A INPUT -s {} -j ACCEPT".format(input_node)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        for forward_node in node.forward_accept:
            cmd = "sudo iptables -A FORWARD -d {} -j ACCEPT".format(forward_node)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        for output_node in node.output_drop:
            cmd = "sudo iptables -A OUTPUT -d {} -j DROP".format(output_node)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        for input_node in node.input_drop:
            cmd = "sudo iptables -A INPUT -s {} -j DROP".format(input_node)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        for forward_node in node.forward_drop:
            cmd = "sudo iptables -A FORWARD -d {} -j DROP".format(forward_node)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        cmd = "sudo iptables -A OUTPUT -d {} -j {}".format(topology.subnetwork, node.default_output)
        o, e, _ = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        cmd = "sudo iptables -A INPUT -d {} -j {}".format(topology.subnetwork, node.default_input)
        ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        cmd = "sudo iptables -A FORWARD -d {} -j {}".format(topology.subnetwork, node.default_forward)
        ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        disconnect_admin(cluster_config=cluster_config)


if __name__ == '__main__':
    if not os.path.exists(util.default_topology_path()):
        write_default_topology()
    topology = util.read_topology(util.default_topology_path())
    cluster_config = ClusterConfig(agent_ip="172.18.3.191", agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    create_topology(topology=topology, cluster_config=cluster_config)
