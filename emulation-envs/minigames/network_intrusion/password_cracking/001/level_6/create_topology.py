import os
from gym_pycr_pwcrack.dao.container_config.topology import Topology
from gym_pycr_pwcrack.dao.container_config.node_firewall_config import NodeFirewallConfig
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.envs.config.generator.topology_generator import TopologyGenerator


def default_topology() -> Topology:
    node_1 = NodeFirewallConfig(ip="172.18.6.10",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                   "172.18.6.191", "172.18.6.10", "172.18.6.1",
                                                   "172.18.6.4", "172.18.6.5", "172.18.6.6", "172.18.6.8",
                                                   "172.18.6.9", "172.18.6.178"
                                                   ]),
                                input_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                  "172.18.6.191", "172.18.6.10", "172.18.6.1",
                                                  "172.18.6.4", "172.18.6.5", "172.18.6.6", "172.18.6.8",
                                                  "172.18.6.9", "172.18.6.178"]),
                                forward_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                    "172.18.6.191", "172.18.6.1", "172.18.6.4", "172.18.6.5",
                                                    "172.18.6.6", "172.18.6.8", "172.18.6.9", "172.18.6.178"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)

    node_2 = NodeFirewallConfig(ip="172.18.6.2",
                                output_accept=set(
                                    ["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79", "172.18.6.191",
                                     "172.18.6.10", "172.18.6.1", "172.18.6.54"]),
                                input_accept=set(
                                    ["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79", "172.18.6.191",
                                     "172.18.6.10", "172.18.6.1", "172.18.6.54"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set([("172.18.6.7", "172.18.6.3"), ("172.18.6.101", "172.18.6.3"),
                                            ("172.18.6.62", "172.18.6.3"), ("172.18.6.61", "172.18.6.3"),
                                            ("172.18.6.74", "172.18.6.3")]),
                                default_input="DROP", default_output="DROP", default_forward="ACCEPT", default_gw=None)

    node_3 = NodeFirewallConfig(ip="172.18.6.3",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                   "172.18.6.191", "172.18.6.10", "172.18.6.74", "172.18.6.1",
                                                   "172.18.6.61"]),
                                input_accept=set(
                                    ["172.18.6.74", "172.18.6.7", "172.18.6.21", "172.18.6.79", "172.18.6.191",
                                     "172.18.6.10", "172.18.6.1", "172.18.6.101", "172.18.6.61"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(),
                                forward_drop=set(["172.18.6.54"]),
                                routes=set([("172.18.6.54", "172.18.6.2"), ("172.18.6.7", "172.18.6.74"),
                                            ("172.18.6.62", "172.18.6.74"), ("172.18.6.101", "172.18.6.74")]),
                                default_input="ACCEPT", default_output="DROP", default_forward="ACCEPT",
                                default_gw=None)

    node_4 = NodeFirewallConfig(ip="172.18.6.21",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21",
                                                   "172.18.6.79", "172.18.6.191", "172.18.6.10", "172.18.6.1"]),
                                input_accept=set(
                                    ["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79", "172.18.6.191",
                                     "172.18.6.10", "172.18.6.1"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(
                                    [("172.18.6.7", "172.18.6.3"), ("172.18.6.101", "172.18.6.3"),
                                     ("172.18.6.62", "172.18.6.3"),
                                     ("172.18.6.61", "172.18.6.3"), ("172.18.6.74", "172.18.6.3"),
                                     ("172.18.6.54", "172.18.6.2")]
                                ),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                )

    node_5 = NodeFirewallConfig(ip="172.18.6.79",
                                output_accept=set(
                                    ["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79", "172.18.6.191",
                                     "172.18.6.10", "172.18.6.1"]),
                                input_accept=set(
                                    ["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79", "172.18.6.191",
                                     "172.18.6.10", "172.18.6.1"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(
                                    [("172.18.6.7", "172.18.6.3"), ("172.18.6.101", "172.18.6.3"),
                                     ("172.18.6.62", "172.18.6.3"), ("172.18.6.61", "172.18.6.3"),
                                     ("172.18.6.74", "172.18.6.3"), ("172.18.6.54", "172.18.6.2")]
                                ),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)

    node_6 = NodeFirewallConfig(ip="172.18.6.191",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21",
                                                   "172.18.6.79", "172.18.6.191", "172.18.6.10", "172.18.6.1"]),
                                input_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21",
                                                  "172.18.6.79", "172.18.6.191", "172.18.6.10", "172.18.6.1"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.6.10")

    node_7 = NodeFirewallConfig(ip="172.18.6.54",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                   "172.18.6.191", "172.18.6.10", "172.18.6.54", "172.18.6.1",
                                                   "172.18.6.11", "172.18.6.12", "172.18.6.13", "172.18.6.14"]),
                                input_accept=set(["172.18.6.2", "172.18.6.1", "172.18.6.11", "172.18.6.12",
                                                  "172.18.6.13", "172.18.6.14"]),
                                forward_accept=set(["172.18.6.11", "172.18.6.12", "172.18.6.13", "172.18.6.14"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set([
                                    ("172.18.6.1", "172.18.6.2"), ("172.18.6.10", "172.18.6.2"),
                                    ("172.18.6.191", "172.18.6.2"), ("172.18.6.3", "172.18.6.2"),
                                    ("172.18.6.21", "172.18.6.2"), ("172.18.6.21", "172.18.6.2")
                                ]), default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw=None
                                )

    node_8 = NodeFirewallConfig(ip="172.18.6.74",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                   "172.18.6.191", "172.18.6.10", "172.18.6.61", "172.18.6.74",
                                                   "172.18.6.101", "172.18.6.62", "172.18.6.1"]),
                                input_accept=set(["172.18.6.3", "172.18.6.61", "172.18.6.62", "172.18.6.74",
                                                  "172.18.6.7", "172.18.6.101", "172.18.6.1"]),
                                forward_accept=set(["172.18.6.101", "172.18.6.62", "172.18.6.61"]),
                                output_drop=set(), input_drop=set(),
                                forward_drop=set(["172.18.6.7", "172.18.6.101", "172.18.6.62"]),
                                routes=set([
                                    ("172.18.6.2", "172.18.6.3"), ("172.18.6.21", "172.18.6.3"),
                                    ("172.18.6.54", "172.18.6.3"), ("172.18.6.79", "172.18.6.3"),
                                    ("172.18.6.10", "172.18.6.3"), ("172.18.6.191", "172.18.6.3"),
                                    ("172.18.6.61", "172.18.6.3"), ("172.18.6.7", "172.18.6.62")
                                ]),
                                default_input="DROP", default_output="DROP", default_forward="ACCEPT",
                                default_gw=None)

    node_9 = NodeFirewallConfig(ip="172.18.6.61",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                   "172.18.6.191", "172.18.6.10", "172.18.6.61", "172.18.6.74",
                                                   "172.18.6.1",
                                                   "172.18.6.19", "172.18.6.20", "172.18.6.21", "172.18.6.22",
                                                   "172.18.6.23", "172.18.6.24", "172.18.6.25", "172.18.6.28"]),
                                input_accept=set(["172.18.6.3", "172.18.6.61", "172.18.6.62", "172.18.6.74",
                                                  "172.18.6.7", "172.18.6.101", "172.18.6.1",
                                                  "172.18.6.19", "172.18.6.20", "172.18.6.21", "172.18.6.22",
                                                  "172.18.6.23", "172.18.6.24", "172.18.6.25", "172.18.6.28"
                                                  ]),
                                forward_accept=set(["172.18.6.19", "172.18.6.20", "172.18.6.21", "172.18.6.22",
                                                   "172.18.6.23", "172.18.6.24", "172.18.6.25", "172.18.6.28"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.6.3")

    node_10 = NodeFirewallConfig(ip="172.18.6.62",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                   "172.18.6.191", "172.18.6.10", "172.18.6.61", "172.18.6.74",
                                                   "172.18.6.1",
                                                   "172.18.6.101", "172.18.6.62", "172.18.6.7",
                                                   "172.18.6.15", "172.18.6.16", "172.18.6.17", "172.18.6.18"]),
                                input_accept=set(["172.18.6.74", "172.18.6.7", "172.18.6.101", "172.18.6.1",
                                                  "172.18.6.15", "172.18.6.16", "172.18.6.17", "172.18.6.18"]),
                                forward_accept=set(["172.18.6.15", "172.18.6.16", "172.18.6.17", "172.18.6.18"]),
                                output_drop=set(), input_drop=set(),
                                routes=set([("172.18.6.2", "172.18.6.74"), ("172.18.6.21", "172.18.6.74"),
                                            ("172.18.6.54", "172.18.6.74"), ("172.18.6.79", "172.18.6.74"),
                                            ("172.18.6.10", "172.18.6.74"), ("172.18.6.191", "172.18.6.74"),
                                            ("172.18.6.61", "172.18.6.74"), ("172.18.6.101", "172.18.6.74")]),
                                forward_drop=set(["172.18.6.7"]), default_input="DROP", default_output="DROP",
                                default_forward="ACCEPT", default_gw=None)

    node_11 = NodeFirewallConfig(ip="172.18.6.101",
                                 output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                    "172.18.6.191", "172.18.6.10", "172.18.6.61", "172.18.6.74",
                                                    "172.18.6.101", "172.18.6.62", "172.18.6.1"]),
                                 input_accept=set(["172.18.6.74", "172.18.6.7", "172.18.6.62", "172.18.6.1"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.6.74")

    node_12 = NodeFirewallConfig(ip="172.18.6.7",
                                 output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                    "172.18.6.191", "172.18.6.10", "172.18.6.61", "172.18.6.74",
                                                    "172.18.6.101", "172.18.6.62", "172.18.6.7", "172.18.6.1"]),
                                 input_accept=set(["172.18.6.62", "172.18.6.1"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.6.62")
    node_13 = NodeFirewallConfig(ip="172.18.6.4", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT", default_forward="ACCEPT",
                                 default_gw=None)
    node_14 = NodeFirewallConfig(ip="172.18.6.5", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_15 = NodeFirewallConfig(ip="172.18.6.6", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_16 = NodeFirewallConfig(ip="172.18.6.8", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_17 = NodeFirewallConfig(ip="172.18.6.9", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_18 = NodeFirewallConfig(ip="172.18.6.178", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_19 = NodeFirewallConfig(ip="172.18.6.11", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_20 = NodeFirewallConfig(ip="172.18.6.12", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_21 = NodeFirewallConfig(ip="172.18.6.13", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_22 = NodeFirewallConfig(ip="172.18.6.14", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_23 = NodeFirewallConfig(ip="172.18.6.15", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_24 = NodeFirewallConfig(ip="172.18.6.16", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_25 = NodeFirewallConfig(ip="172.18.6.17", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_26 = NodeFirewallConfig(ip="172.18.6.18", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_27 = NodeFirewallConfig(ip="172.18.6.19", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_28 = NodeFirewallConfig(ip="172.18.6.20", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_29 = NodeFirewallConfig(ip="172.18.6.22", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_30 = NodeFirewallConfig(ip="172.18.6.23", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_31 = NodeFirewallConfig(ip="172.18.6.24", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_32 = NodeFirewallConfig(ip="172.18.6.25", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_33 = NodeFirewallConfig(ip="172.18.6.28", output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11,
                    node_12, node_13, node_14, node_15, node_16, node_17, node_18, node_19, node_20, node_20,
                    node_21, node_22, node_23, node_24, node_25, node_26, node_27, node_28, node_29, node_30,
                    node_31, node_32, node_33]
    topology = Topology(node_configs=node_configs, subnetwork="172.18.6.0/24")
    return topology


if __name__ == '__main__':
    if not os.path.exists(util.default_topology_path()):
        TopologyGenerator.write_topology(default_topology())
    topology = util.read_topology(util.default_topology_path())
    cluster_config = ClusterConfig(agent_ip="172.18.6.191", agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    TopologyGenerator.create_topology(topology=topology, cluster_config=cluster_config)
