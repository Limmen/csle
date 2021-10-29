import os
from pycr_common.dao.container_config.topology import Topology
from pycr_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from pycr_common.util.experiments_util import util
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.config.generator.topology_generator import TopologyGenerator


def default_topology() -> Topology:
    node_1 = NodeFirewallConfig(ip="172.18.9.10", hostname="router2",
                                output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79",
                                                   "172.18.9.191", "172.18.9.10", "172.18.9.1", "172.18.9.254",
                                                   "172.18.9.253", "172.18.9.252",
                                                   "172.18.9.4", "172.18.9.5", "172.18.9.6", "172.18.9.8",
                                                   "172.18.9.9", "172.18.9.178"
                                                   ]),
                                input_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79",
                                                  "172.18.9.191", "172.18.9.10", "172.18.9.1", "172.18.9.254",
                                                  "172.18.9.253", "172.18.9.252",
                                                  "172.18.9.4", "172.18.9.5", "172.18.9.6", "172.18.9.8",
                                                  "172.18.9.9", "172.18.9.178"]),
                                forward_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79",
                                                    "172.18.9.191", "172.18.9.1", "172.18.9.254", "172.18.9.253",
                                                    "172.18.9.252",
                                                    "172.18.9.4", "172.18.9.5",
                                                    "172.18.9.6", "172.18.9.8", "172.18.9.9", "172.18.9.178"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)

    node_2 = NodeFirewallConfig(ip="172.18.9.2", hostname="ssh1",
                                output_accept=set(
                                    ["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79", "172.18.9.191",
                                     "172.18.9.10", "172.18.9.1", "172.18.9.254", "172.18.9.253", "172.18.9.252",
                                     "172.18.9.54"]),
                                input_accept=set(
                                    ["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79", "172.18.9.191",
                                     "172.18.9.10", "172.18.9.1", "172.18.9.254", "172.18.9.253", "172.18.9.252",
                                     "172.18.9.54"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set([("172.18.9.7", "172.18.9.3"), ("172.18.9.101", "172.18.9.3"),
                                            ("172.18.9.62", "172.18.9.3"), ("172.18.9.61", "172.18.9.3"),
                                            ("172.18.9.74", "172.18.9.3")]),
                                default_input="DROP", default_output="DROP", default_forward="ACCEPT", default_gw=None)

    node_3 = NodeFirewallConfig(ip="172.18.9.3", hostname="samba2_1",
                                output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79",
                                                   "172.18.9.191", "172.18.9.10", "172.18.9.74", "172.18.9.1",
                                                   "172.18.9.254", "172.18.9.253", "172.18.9.252",
                                                   "172.18.9.61"]),
                                input_accept=set(
                                    ["172.18.9.74", "172.18.9.7", "172.18.9.21", "172.18.9.79", "172.18.9.191",
                                     "172.18.9.10", "172.18.9.1", "172.18.9.254", "172.18.9.253", "172.18.9.252",
                                     "172.18.9.101", "172.18.9.61"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(),
                                forward_drop=set(["172.18.9.54"]),
                                routes=set([("172.18.9.54", "172.18.9.2"), ("172.18.9.7", "172.18.9.74"),
                                            ("172.18.9.62", "172.18.9.74"), ("172.18.9.101", "172.18.9.74")]),
                                default_input="ACCEPT", default_output="DROP", default_forward="ACCEPT",
                                default_gw=None)

    node_4 = NodeFirewallConfig(ip="172.18.9.21", hostname="honeypot1_1",
                                output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21",
                                                   "172.18.9.79", "172.18.9.191", "172.18.9.10", "172.18.9.1",
                                                   "172.18.9.254", "172.18.9.253", "172.18.9.252"]),
                                input_accept=set(
                                    ["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79", "172.18.9.191",
                                     "172.18.9.10", "172.18.9.1", "172.18.9.254", "172.18.9.253", "172.18.9.252"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(
                                    [("172.18.9.7", "172.18.9.3"), ("172.18.9.101", "172.18.9.3"),
                                     ("172.18.9.62", "172.18.9.3"),
                                     ("172.18.9.61", "172.18.9.3"), ("172.18.9.74", "172.18.9.3"),
                                     ("172.18.9.54", "172.18.9.2")]
                                ),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                )

    node_5 = NodeFirewallConfig(ip="172.18.9.79", hostname="ftp1",
                                output_accept=set(
                                    ["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79", "172.18.9.191",
                                     "172.18.9.10", "172.18.9.1", "172.18.9.254", "172.18.9.253", "172.18.9.252"]),
                                input_accept=set(
                                    ["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79", "172.18.9.191",
                                     "172.18.9.10", "172.18.9.1", "172.18.9.254", "172.18.9.253", "172.18.9.252"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(
                                    [("172.18.9.7", "172.18.9.3"), ("172.18.9.101", "172.18.9.3"),
                                     ("172.18.9.62", "172.18.9.3"), ("172.18.9.61", "172.18.9.3"),
                                     ("172.18.9.74", "172.18.9.3"), ("172.18.9.54", "172.18.9.2")]
                                ),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)

    node_6 = NodeFirewallConfig(ip="172.18.9.191", hostname="hacker_kali1",
                                output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21",
                                                   "172.18.9.79", "172.18.9.191", "172.18.9.10", "172.18.9.1"]),
                                input_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21",
                                                  "172.18.9.79", "172.18.9.191", "172.18.9.10", "172.18.9.1"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.9.10")

    node_7 = NodeFirewallConfig(ip="172.18.9.54", hostname="shellshock1_1",
                                output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79",
                                                   "172.18.9.191", "172.18.9.10", "172.18.9.54", "172.18.9.1",
                                                   "172.18.9.254", "172.18.9.253", "172.18.9.252",
                                                   "172.18.9.11", "172.18.9.12", "172.18.9.13", "172.18.9.14"]),
                                input_accept=set(["172.18.9.2", "172.18.9.1", "172.18.9.254", "172.18.9.253",
                                                  "172.18.9.252",
                                                  "172.18.9.11", "172.18.9.12",
                                                  "172.18.9.13", "172.18.9.14"]),
                                forward_accept=set(["172.18.9.11", "172.18.9.12", "172.18.9.13", "172.18.9.14"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set([
                                    ("172.18.9.1", "172.18.9.2"), ("172.18.9.10", "172.18.9.2"),
                                    ("172.18.9.191", "172.18.9.2"), ("172.18.9.3", "172.18.9.2"),
                                    ("172.18.9.21", "172.18.9.2"), ("172.18.9.21", "172.18.9.2")
                                ]), default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw=None
                                )

    node_8 = NodeFirewallConfig(ip="172.18.9.74", hostname="sql_injection1_1",
                                output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79",
                                                   "172.18.9.191", "172.18.9.10", "172.18.9.61", "172.18.9.74",
                                                   "172.18.9.101", "172.18.9.62", "172.18.9.1", "172.18.9.254",
                                                   "172.18.9.253", "172.18.9.252"]),
                                input_accept=set(["172.18.9.3", "172.18.9.61", "172.18.9.62", "172.18.9.74",
                                                  "172.18.9.7", "172.18.9.101", "172.18.9.1", "172.18.9.254",
                                                  "172.18.9.253", "172.18.9.252"]),
                                forward_accept=set(["172.18.9.101", "172.18.9.62", "172.18.9.61"]),
                                output_drop=set(), input_drop=set(),
                                forward_drop=set(["172.18.9.7", "172.18.9.101", "172.18.9.62"]),
                                routes=set([
                                    ("172.18.9.2", "172.18.9.3"), ("172.18.9.21", "172.18.9.3"),
                                    ("172.18.9.54", "172.18.9.3"), ("172.18.9.79", "172.18.9.3"),
                                    ("172.18.9.10", "172.18.9.3"), ("172.18.9.191", "172.18.9.3"),
                                    ("172.18.9.61", "172.18.9.3"), ("172.18.9.7", "172.18.9.62")
                                ]),
                                default_input="DROP", default_output="DROP", default_forward="ACCEPT",
                                default_gw=None)

    node_9 = NodeFirewallConfig(ip="172.18.9.61", hostname="cve_2010_0426_1_1",
                                output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79",
                                                   "172.18.9.191", "172.18.9.10", "172.18.9.61", "172.18.9.74",
                                                   "172.18.9.1", "172.18.9.254", "172.18.9.253", "172.18.9.252",
                                                   "172.18.9.19", "172.18.9.20", "172.18.9.21", "172.18.9.22",
                                                   "172.18.9.23", "172.18.9.24", "172.18.9.25", "172.18.9.28"]),
                                input_accept=set(["172.18.9.3", "172.18.9.61", "172.18.9.62", "172.18.9.74",
                                                  "172.18.9.7", "172.18.9.101", "172.18.9.1", "172.18.9.254",
                                                  "172.18.9.253", "172.18.9.252",
                                                  "172.18.9.19", "172.18.9.20", "172.18.9.21", "172.18.9.22",
                                                  "172.18.9.23", "172.18.9.24", "172.18.9.25", "172.18.9.28"
                                                  ]),
                                forward_accept=set(["172.18.9.19", "172.18.9.20", "172.18.9.21", "172.18.9.22",
                                                   "172.18.9.23", "172.18.9.24", "172.18.9.25", "172.18.9.28"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.9.3")

    node_10 = NodeFirewallConfig(ip="172.18.9.62", hostname="cve_2015_1427_1_1",
                                output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79",
                                                   "172.18.9.191", "172.18.9.10", "172.18.9.61", "172.18.9.74",
                                                   "172.18.9.1", "172.18.9.254", "172.18.9.253", "172.18.9.252",
                                                   "172.18.9.101", "172.18.9.62", "172.18.9.7",
                                                   "172.18.9.15", "172.18.9.16", "172.18.9.17", "172.18.9.18"]),
                                input_accept=set(["172.18.9.74", "172.18.9.7", "172.18.9.101", "172.18.9.1",
                                                  "172.18.9.254", "172.18.9.253", "172.18.9.252",
                                                  "172.18.9.15", "172.18.9.16", "172.18.9.17", "172.18.9.18"]),
                                forward_accept=set(["172.18.9.15", "172.18.9.16", "172.18.9.17", "172.18.9.18"]),
                                output_drop=set(), input_drop=set(),
                                routes=set([("172.18.9.2", "172.18.9.74"), ("172.18.9.21", "172.18.9.74"),
                                            ("172.18.9.54", "172.18.9.74"), ("172.18.9.79", "172.18.9.74"),
                                            ("172.18.9.10", "172.18.9.74"), ("172.18.9.191", "172.18.9.74"),
                                            ("172.18.9.61", "172.18.9.74"), ("172.18.9.101", "172.18.9.74")]),
                                forward_drop=set(["172.18.9.7"]), default_input="DROP", default_output="DROP",
                                default_forward="ACCEPT", default_gw=None)

    node_11 = NodeFirewallConfig(ip="172.18.9.101", hostname="honeypot2_1",
                                 output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79",
                                                    "172.18.9.191", "172.18.9.10", "172.18.9.61", "172.18.9.74",
                                                    "172.18.9.101", "172.18.9.62", "172.18.9.1", "172.18.9.254",
                                                    "172.18.9.253", "172.18.9.252"]),
                                 input_accept=set(["172.18.9.74", "172.18.9.7", "172.18.9.62", "172.18.9.1",
                                                   "172.18.9.254", "172.18.9.253", "172.18.9.252"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.9.74")

    node_12 = NodeFirewallConfig(ip="172.18.9.7", hostname="samba1_1",
                                 output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21", "172.18.9.79",
                                                    "172.18.9.191", "172.18.9.10", "172.18.9.61", "172.18.9.74",
                                                    "172.18.9.101", "172.18.9.62", "172.18.9.7", "172.18.9.1",
                                                    "172.18.9.254", "172.18.9.253", "172.18.9.252"]),
                                 input_accept=set(["172.18.9.62", "172.18.9.1", "172.18.9.254", "172.18.9.253",
                                                   "172.18.9.252"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.9.62")
    node_13 = NodeFirewallConfig(ip="172.18.9.4", hostname="honeypot1_2",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT", default_forward="ACCEPT",
                                 default_gw=None)
    node_14 = NodeFirewallConfig(ip="172.18.9.5", hostname="honeypot1_3",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_15 = NodeFirewallConfig(ip="172.18.9.6", hostname="honeypot1_4",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_16 = NodeFirewallConfig(ip="172.18.9.8", hostname="honeypot1_5",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_17 = NodeFirewallConfig(ip="172.18.9.9", hostname="honeypot1_6",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_18 = NodeFirewallConfig(ip="172.18.9.178", hostname="cve_2015_3306_1_1",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_19 = NodeFirewallConfig(ip="172.18.9.11", hostname="honeypot2_2",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_20 = NodeFirewallConfig(ip="172.18.9.12", hostname="honeypot2_3",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_21 = NodeFirewallConfig(ip="172.18.9.13", hostname="honeypot2_4",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_22 = NodeFirewallConfig(ip="172.18.9.14", hostname="honeypot2_5",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_23 = NodeFirewallConfig(ip="172.18.9.15", hostname="honeypot2_6",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_24 = NodeFirewallConfig(ip="172.18.9.16", hostname="honeypot2_7",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_25 = NodeFirewallConfig(ip="172.18.9.17", hostname="honeypot2_8",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_26 = NodeFirewallConfig(ip="172.18.9.18", hostname="honeypot2_9",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_27 = NodeFirewallConfig(ip="172.18.9.19", hostname="honeypot2_10",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_28 = NodeFirewallConfig(ip="172.18.9.20", hostname="honeypot2_11",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_29 = NodeFirewallConfig(ip="172.18.9.22", hostname="honeypot2_12",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_30 = NodeFirewallConfig(ip="172.18.9.23", hostname="honeypot2_13",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_31 = NodeFirewallConfig(ip="172.18.9.24", hostname="honeypot2_14",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_32 = NodeFirewallConfig(ip="172.18.9.25", hostname="cve_2015_5602_1_1",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_33 = NodeFirewallConfig(ip="172.18.9.28", hostname="cve_2016_10033_1_1",
                                 output_accept=set(), input_accept=set(), forward_accept=set(),
                                 output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="ACCEPT", default_output="ACCEPT",
                                 default_forward="ACCEPT",
                                 default_gw=None)
    node_34 = NodeFirewallConfig(ip="172.18.9.254", hostname="client1_1",
                                output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21",
                                                   "172.18.9.79", "172.18.9.10", "172.18.9.1",
                                                   "172.18.9.254"]),
                                input_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21",
                                                  "172.18.9.79", "172.18.9.10", "172.18.9.1",
                                                  "172.18.9.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.9.10")
    node_35 = NodeFirewallConfig(ip="172.18.9.253", hostname="client1_2",
                                 output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21",
                                                    "172.18.9.79", "172.18.9.10", "172.18.9.1",
                                                    "172.18.9.253"]),
                                 input_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21",
                                                   "172.18.9.79", "172.18.9.10", "172.18.9.1",
                                                   "172.18.9.253"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.9.10")
    node_36 = NodeFirewallConfig(ip="172.18.9.252", hostname="client1_3",
                                 output_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21",
                                                    "172.18.9.79", "172.18.9.10", "172.18.9.1",
                                                    "172.18.9.252"]),
                                 input_accept=set(["172.18.9.2", "172.18.9.3", "172.18.9.21",
                                                   "172.18.9.79", "172.18.9.10", "172.18.9.1",
                                                   "172.18.9.252"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.9.10")
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11,
                    node_12, node_13, node_14, node_15, node_16, node_17, node_18, node_19, node_20, node_20,
                    node_21, node_22, node_23, node_24, node_25, node_26, node_27, node_28, node_29, node_30,
                    node_31, node_32, node_33, node_34, node_35, node_36]
    topology = Topology(node_configs=node_configs, subnetwork="172.18.9.0/24")
    return topology


if __name__ == '__main__':
    if not os.path.exists(util.default_topology_path()):
        TopologyGenerator.write_topology(default_topology())
    topology = util.read_topology(util.default_topology_path())
    emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="pycr_admin",
                                     agent_pw="pycr@admin-pw_191", server_connection=False)
    TopologyGenerator.create_topology(topology=topology, emulation_config=emulation_config)
