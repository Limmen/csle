import os
from pycr_common.dao.container_config.topology import Topology
from pycr_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from pycr_common.util.experiments_util import util
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.config.generator.topology_generator import TopologyGenerator
import pycr_common.constants.constants as constants


def default_topology() -> Topology:
    """
    :return: the Topology of the emulation
    """
    node_1 = NodeFirewallConfig(ip="172.18.6.10", hostname="router2",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                   "172.18.6.191", "172.18.6.10", "172.18.6.1", "172.18.6.254",
                                                   "172.18.6.4", "172.18.6.5", "172.18.6.6", "172.18.6.8",
                                                   "172.18.6.9", "172.18.6.178"
                                                   ]),
                                input_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                  "172.18.6.191", "172.18.6.10", "172.18.6.1", "172.18.6.254",
                                                  "172.18.6.4", "172.18.6.5", "172.18.6.6", "172.18.6.8",
                                                  "172.18.6.9", "172.18.6.178"]),
                                forward_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                    "172.18.6.191", "172.18.6.1", "172.18.6.254", "172.18.6.4", "172.18.6.5",
                                                    "172.18.6.6", "172.18.6.8", "172.18.6.9", "172.18.6.178"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)

    node_2 = NodeFirewallConfig(ip="172.18.6.2", hostname="ssh1",
                                output_accept=set(
                                    ["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79", "172.18.6.191",
                                     "172.18.6.10", "172.18.6.1", "172.18.6.254", "172.18.6.54"]),
                                input_accept=set(
                                    ["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79", "172.18.6.191",
                                     "172.18.6.10", "172.18.6.1", "172.18.6.254", "172.18.6.54"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set([("172.18.6.7", "172.18.6.3"), ("172.18.6.101", "172.18.6.3"),
                                            ("172.18.6.62", "172.18.6.3"), ("172.18.6.61", "172.18.6.3"),
                                            ("172.18.6.74", "172.18.6.3")]),
                                default_input="DROP", default_output="DROP", default_forward="ACCEPT", default_gw=None)

    node_3 = NodeFirewallConfig(ip="172.18.6.3", hostname="telnet1",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                   "172.18.6.191", "172.18.6.10", "172.18.6.74", "172.18.6.1", "172.18.6.254",
                                                   "172.18.6.61"]),
                                input_accept=set(
                                    ["172.18.6.74", "172.18.6.7", "172.18.6.21", "172.18.6.79", "172.18.6.191",
                                     "172.18.6.10", "172.18.6.1", "172.18.6.254", "172.18.6.101", "172.18.6.61"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(),
                                forward_drop=set(["172.18.6.54"]),
                                routes=set([("172.18.6.54", "172.18.6.2"), ("172.18.6.7", "172.18.6.74"),
                                            ("172.18.6.62", "172.18.6.74"), ("172.18.6.101", "172.18.6.74")]),
                                default_input="ACCEPT", default_output="DROP", default_forward="ACCEPT",
                                default_gw=None)

    node_4 = NodeFirewallConfig(ip="172.18.6.21", hostname="honeypot1_1",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21",
                                                   "172.18.6.79", "172.18.6.191", "172.18.6.10", "172.18.6.1", "172.18.6.254"]),
                                input_accept=set(
                                    ["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79", "172.18.6.191",
                                     "172.18.6.10", "172.18.6.1", "172.18.6.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(
                                    [("172.18.6.7", "172.18.6.3"), ("172.18.6.101", "172.18.6.3"),
                                     ("172.18.6.62", "172.18.6.3"),
                                     ("172.18.6.61", "172.18.6.3"), ("172.18.6.74", "172.18.6.3"),
                                     ("172.18.6.54", "172.18.6.2")]
                                ),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                )

    node_5 = NodeFirewallConfig(ip="172.18.6.79", hostname="ftp1",
                                output_accept=set(
                                    ["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79", "172.18.6.191",
                                     "172.18.6.10", "172.18.6.1", "172.18.6.254"]),
                                input_accept=set(
                                    ["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79", "172.18.6.191",
                                     "172.18.6.10", "172.18.6.1", "172.18.6.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(
                                    [("172.18.6.7", "172.18.6.3"), ("172.18.6.101", "172.18.6.3"),
                                     ("172.18.6.62", "172.18.6.3"), ("172.18.6.61", "172.18.6.3"),
                                     ("172.18.6.74", "172.18.6.3"), ("172.18.6.54", "172.18.6.2")]
                                ),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)

    node_6 = NodeFirewallConfig(ip="172.18.6.191", hostname="hacker_kali1",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21",
                                                   "172.18.6.79", "172.18.6.191", "172.18.6.10", "172.18.6.1"]),
                                input_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21",
                                                  "172.18.6.79", "172.18.6.191", "172.18.6.10", "172.18.6.1"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.6.10")

    node_7 = NodeFirewallConfig(ip="172.18.6.54", hostname="ssh2",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                   "172.18.6.191", "172.18.6.10", "172.18.6.54", "172.18.6.1", "172.18.6.254",
                                                   "172.18.6.11", "172.18.6.12", "172.18.6.13", "172.18.6.14"]),
                                input_accept=set(["172.18.6.2", "172.18.6.1", "172.18.6.254", "172.18.6.11", "172.18.6.12",
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

    node_8 = NodeFirewallConfig(ip="172.18.6.74", hostname="ssh3",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                   "172.18.6.191", "172.18.6.10", "172.18.6.61", "172.18.6.74",
                                                   "172.18.6.101", "172.18.6.62", "172.18.6.1", "172.18.6.254"]),
                                input_accept=set(["172.18.6.3", "172.18.6.61", "172.18.6.62", "172.18.6.74",
                                                  "172.18.6.7", "172.18.6.101", "172.18.6.1", "172.18.6.254"]),
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

    node_9 = NodeFirewallConfig(ip="172.18.6.61", hostname="telnet2",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                   "172.18.6.191", "172.18.6.10", "172.18.6.61", "172.18.6.74",
                                                   "172.18.6.1", "172.18.6.254",
                                                   "172.18.6.19", "172.18.6.20", "172.18.6.21", "172.18.6.22",
                                                   "172.18.6.23", "172.18.6.24", "172.18.6.25", "172.18.6.28"]),
                                input_accept=set(["172.18.6.3", "172.18.6.61", "172.18.6.62", "172.18.6.74",
                                                  "172.18.6.7", "172.18.6.101", "172.18.6.1", "172.18.6.254",
                                                  "172.18.6.19", "172.18.6.20", "172.18.6.21", "172.18.6.22",
                                                  "172.18.6.23", "172.18.6.24", "172.18.6.25", "172.18.6.28"
                                                  ]),
                                forward_accept=set(["172.18.6.19", "172.18.6.20", "172.18.6.21", "172.18.6.22",
                                                   "172.18.6.23", "172.18.6.24", "172.18.6.25", "172.18.6.28"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.6.3")

    node_10 = NodeFirewallConfig(ip="172.18.6.62", hostname="telnet3",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                   "172.18.6.191", "172.18.6.10", "172.18.6.61", "172.18.6.74",
                                                   "172.18.6.1", "172.18.6.254",
                                                   "172.18.6.101", "172.18.6.62", "172.18.6.7",
                                                   "172.18.6.15", "172.18.6.16", "172.18.6.17", "172.18.6.18"]),
                                input_accept=set(["172.18.6.74", "172.18.6.7", "172.18.6.101", "172.18.6.1", "172.18.6.254",
                                                  "172.18.6.15", "172.18.6.16", "172.18.6.17", "172.18.6.18"]),
                                forward_accept=set(["172.18.6.15", "172.18.6.16", "172.18.6.17", "172.18.6.18"]),
                                output_drop=set(), input_drop=set(),
                                routes=set([("172.18.6.2", "172.18.6.74"), ("172.18.6.21", "172.18.6.74"),
                                            ("172.18.6.54", "172.18.6.74"), ("172.18.6.79", "172.18.6.74"),
                                            ("172.18.6.10", "172.18.6.74"), ("172.18.6.191", "172.18.6.74"),
                                            ("172.18.6.61", "172.18.6.74"), ("172.18.6.101", "172.18.6.74")]),
                                forward_drop=set(["172.18.6.7"]), default_input="DROP", default_output="DROP",
                                default_forward="ACCEPT", default_gw=None)

    node_11 = NodeFirewallConfig(ip="172.18.6.101", hostname="honeypot2_1",
                                 output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                    "172.18.6.191", "172.18.6.10", "172.18.6.61", "172.18.6.74",
                                                    "172.18.6.101", "172.18.6.62", "172.18.6.1", "172.18.6.254"]),
                                 input_accept=set(["172.18.6.74", "172.18.6.7", "172.18.6.62", "172.18.6.1", "172.18.6.254"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.6.74")

    node_12 = NodeFirewallConfig(ip="172.18.6.7", hostname="ftp2",
                                 output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21", "172.18.6.79",
                                                    "172.18.6.191", "172.18.6.10", "172.18.6.61", "172.18.6.74",
                                                    "172.18.6.101", "172.18.6.62", "172.18.6.7", "172.18.6.1", "172.18.6.254"]),
                                 input_accept=set(["172.18.6.62", "172.18.6.1", "172.18.6.254"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.6.62")
    node_13 = NodeFirewallConfig(ip="172.18.6.4", hostname="honeypot1_2",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT", default_forward="ACCEPT",
                                 default_gw=None)
    node_14 = NodeFirewallConfig(ip="172.18.6.5", hostname="honeypot1_3",
                                output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_15 = NodeFirewallConfig(ip="172.18.6.6", hostname="honeypot1_4",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_16 = NodeFirewallConfig(ip="172.18.6.8", hostname="honeypot1_5",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_17 = NodeFirewallConfig(ip="172.18.6.9", hostname="honeypot1_6",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_18 = NodeFirewallConfig(ip="172.18.6.178", hostname="honeypot1_7",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_19 = NodeFirewallConfig(ip="172.18.6.11", hostname="honeypot2_2",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_20 = NodeFirewallConfig(ip="172.18.6.12", hostname="honeypot2_3",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_21 = NodeFirewallConfig(ip="172.18.6.13", hostname="honeypot2_4",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_22 = NodeFirewallConfig(ip="172.18.6.14", hostname="honeypot2_5",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_23 = NodeFirewallConfig(ip="172.18.6.15", hostname="honeypot2_6",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_24 = NodeFirewallConfig(ip="172.18.6.16", hostname="honeypot2_7",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_25 = NodeFirewallConfig(ip="172.18.6.17",
                                 output_accept=set(), hostname="honeypot2_8",
                                 input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_26 = NodeFirewallConfig(ip="172.18.6.18", hostname="honeypot2_9",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_27 = NodeFirewallConfig(ip="172.18.6.19", hostname="honeypot2_10",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_28 = NodeFirewallConfig(ip="172.18.6.20", hostname="honeypot2_11",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_29 = NodeFirewallConfig(ip="172.18.6.22", hostname="honeypot2_12",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_30 = NodeFirewallConfig(ip="172.18.6.23", hostname="honeypot2_13",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_31 = NodeFirewallConfig(ip="172.18.6.24", hostname="honeypot2_14",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_32 = NodeFirewallConfig(ip="172.18.6.25", hostname="honeypot2_15",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_33 = NodeFirewallConfig(ip="172.18.6.28", hostname="honeypot2_16",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_34 = NodeFirewallConfig(ip="172.18.6.254", hostname="client1",
                                output_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21",
                                                   "172.18.6.79", "172.18.6.10", "172.18.6.1",
                                                   "172.18.6.254"]),
                                input_accept=set(["172.18.6.2", "172.18.6.3", "172.18.6.21",
                                                  "172.18.6.79", "172.18.6.10", "172.18.6.1",
                                                  "172.18.6.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.6.10")
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11,
                    node_12, node_13, node_14, node_15, node_16, node_17, node_18, node_19, node_20, node_20,
                    node_21, node_22, node_23, node_24, node_25, node_26, node_27, node_28, node_29, node_30,
                    node_31, node_32, node_33, node_34]
    topology = Topology(node_configs=node_configs, subnetwork="172.18.6.0/24")
    return topology

# Generates the topology.json configuration file
if __name__ == '__main__':
    if not os.path.exists(util.default_topology_path()):
        TopologyGenerator.write_topology(default_topology())
    topology = util.read_topology(util.default_topology_path())
    emulation_config = EmulationConfig(agent_ip="172.18.6.191", agent_username=constants.PYCR_ADMIN.USER,
                                     agent_pw=constants.PYCR_ADMIN.PW, server_connection=False)
    TopologyGenerator.create_topology(topology=topology, emulation_config=emulation_config)
