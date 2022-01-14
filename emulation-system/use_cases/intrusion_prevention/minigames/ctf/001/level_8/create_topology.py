import os
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.topology_generator import TopologyGenerator
import csle_common.constants.constants as constants


def default_topology() -> Topology:
    """
    :return: the Topology of the emulation
    """
    node_1 = NodeFirewallConfig(ip="172.18.8.10", hostname="router_2_1",
                           output_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                                              "172.18.8.191", "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.19",
                                              "172.18.8.31",
                                              "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                              "172.18.8.11",
                                              "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54", "172.18.8.55",
                                              "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59", "172.18.8.60",
                                              "172.18.8.61", "172.18.8.62"]),
                           input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                                             "172.18.8.191", "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.19",
                                             "172.18.8.31",
                                             "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                             "172.18.8.11",
                                             "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54", "172.18.8.55",
                                             "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59", "172.18.8.60",
                                             "172.18.8.61", "172.18.8.62"
                                             ]),
                           forward_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                                             "172.18.8.191", "172.18.8.1", "172.18.8.254", "172.18.8.19", "172.18.8.31",
                                               "172.18.8.42",
                                               "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                               "172.18.8.11",
                                               "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54",
                                               "172.18.8.55",
                                               "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59",
                                               "172.18.8.60",
                                               "172.18.8.61", "172.18.8.62"
                                               ]),
                           output_drop = set(), input_drop = set(), forward_drop = set(), routes=set(),
                           default_input = "DROP", default_output = "DROP", default_forward="DROP",
                           default_gw=None
                           )
    node_2 = NodeFirewallConfig(ip="172.18.8.2", hostname="ssh_1_1",
                       output_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                          "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.19", "172.18.8.31",
                                          "172.18.8.42",
                                          "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                          "172.18.8.11", "172.18.8.52"]),
                       input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                         "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.19", "172.18.8.31",
                                         "172.18.8.42",
                                         "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                         "172.18.8.11", "172.18.8.52"]),
                       forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set(),
                       default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                       )
    node_3 = NodeFirewallConfig(ip="172.18.8.3", hostname="telnet_1_1",
                           output_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                              "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.19", "172.18.8.31",
                                              "172.18.8.42",
                                              "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                              "172.18.8.11"]),
                           input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                             "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.19", "172.18.8.31",
                                             "172.18.8.42",
                                             "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                             "172.18.8.11"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                            default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_4 = NodeFirewallConfig(ip="172.18.8.21", hostname="honeypot_1_1",
                           output_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21",
                                                "172.18.8.79", "172.18.8.191", "172.18.8.10", "172.18.8.1",
                                              "172.18.8.254",
                                              "172.18.8.19", "172.18.8.31", "172.18.8.42",
                                              "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                              "172.18.8.11"]),
                           input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                             "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.19", "172.18.8.31",
                                             "172.18.8.42",
                                             "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                           default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                           )
    node_5 = NodeFirewallConfig(ip="172.18.8.79", hostname="ftp_1_1",
                           output_accept=set(
                               ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.19", "172.18.8.31",
                                "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                "172.18.8.11", "172.18.8.51"]),
                           input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                             "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.19", "172.18.8.31",
                                             "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                             "172.18.8.11", "172.18.8.51"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                           default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_6 = NodeFirewallConfig(ip="172.18.8.19", hostname="samba_1_1",
                                output_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.31",
                                     "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75","172.18.8.71",
                                     "172.18.8.11"]),
                                input_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.31",
                                     "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                     "172.18.8.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_7 = NodeFirewallConfig(ip="172.18.8.31", hostname="shellshock_1_1",
                                output_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.42",
                                     "172.18.8.37",
                                     "172.18.8.82", "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                                input_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.42",
                                     "172.18.8.37",
                                     "172.18.8.82", "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_8 = NodeFirewallConfig(ip="172.18.8.42", hostname="sql_injection_1_1",
                                output_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.37",
                                     "172.18.8.82",
                                     "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                                input_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.37",
                                     "172.18.8.82",
                                     "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_9 = NodeFirewallConfig(ip="172.18.8.37", hostname="cve_2015_3306_1_1",
                                output_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.42",
                                     "172.18.8.82",
                                     "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                                input_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.42",
                                     "172.18.8.82",
                                     "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_10 = NodeFirewallConfig(ip="172.18.8.82", hostname="cve_2015_1427_1_1",
                                output_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.42",
                                     "172.18.8.37", "172.18.8.75", "172.18.8.71", "172.18.8.11", "172.18.8.53",
                                     "172.18.8.51"]),
                                input_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.42",
                                     "172.18.8.37",
                                     "172.18.8.75", "172.18.8.71", "172.18.8.11", "172.18.8.53", "172.18.8.51"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_11 = NodeFirewallConfig(ip="172.18.8.75", hostname="cve_2016_10033_1_1",
                                 output_accept=set(
                                     ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                      "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.42",
                                      "172.18.8.37", "172.18.8.82", "172.18.8.71", "172.18.8.11"]),
                                 input_accept=set(
                                     ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                      "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.42",
                                      "172.18.8.37",
                                      "172.18.8.82", "172.18.8.71", "172.18.8.11"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_12 = NodeFirewallConfig(ip="172.18.8.71", hostname="cve_2010_0426_1_1",
                                 output_accept=set(
                                     ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                      "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.42",
                                      "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.11"]),
                                 input_accept=set(
                                     ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                      "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.42",
                                      "172.18.8.37",
                                      "172.18.8.82", "172.18.8.75", "172.18.8.11"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_13 = NodeFirewallConfig(ip="172.18.8.11", hostname="cve_2015_5602_1_2",
                                 output_accept=set(
                                     ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                      "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.42",
                                      "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71"]),
                                 input_accept=set(
                                     ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                      "172.18.8.10", "172.18.8.1", "172.18.8.254", "172.18.8.79", "172.18.8.42",
                                      "172.18.8.37",
                                      "172.18.8.82", "172.18.8.75", "172.18.8.71"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_14 = NodeFirewallConfig(ip="172.18.8.51", hostname="ssh_1_2",
                                 output_accept=set(
                                     ["172.18.8.79", "172.18.8.1", "172.18.8.254", "172.18.8.82"]),
                                 input_accept=set(
                                     ["172.18.8.79", "172.18.8.1", "172.18.8.254", "172.18.8.82"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_15 = NodeFirewallConfig(ip="172.18.8.52", hostname="ssh_1_3",
                                output_accept=set(
                                    ["172.18.8.2", "172.18.8.1", "172.18.8.254", "172.18.8.54"]),
                                input_accept=set(
                                    ["172.18.8.2", "172.18.8.1", "172.18.8.254", "172.18.8.54"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                forward_drop=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                )
    node_16 = NodeFirewallConfig(ip="172.18.8.53", hostname="honeypot_1_2",
                                 output_accept=set(
                                     ["172.18.8.82", "172.18.8.1", "172.18.8.254"]),
                                 input_accept=set(
                                     ["172.18.8.82", "172.18.8.1", "172.18.8.254"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_17 = NodeFirewallConfig(ip="172.18.8.54", hostname="samba_1_2",
                                 output_accept=set(
                                     ["172.18.8.52", "172.18.8.1", "172.18.8.254", "172.18.8.55"]),
                                 input_accept=set(
                                     ["172.18.8.52", "172.18.8.1", "172.18.8.254", "172.18.8.55"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_18 = NodeFirewallConfig(ip="172.18.8.55", hostname="shellshock_1_2",
                                 output_accept=set(
                                     ["172.18.8.54", "172.18.8.1", "172.18.8.254", "172.18.8.56"]),
                                 input_accept=set(
                                     ["172.18.8.54", "172.18.8.1", "172.18.8.254", "172.18.8.56"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_19 = NodeFirewallConfig(ip="172.18.8.56", hostname="sql_injection_1_2",
                                 output_accept=set(
                                     ["172.18.8.55", "172.18.8.1", "172.18.8.254", "172.18.8.57"]),
                                 input_accept=set(
                                     ["172.18.8.55", "172.18.8.1", "172.18.8.254", "172.18.8.57"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_20 = NodeFirewallConfig(ip="172.18.8.57", hostname="cve_2015_3306_1_2",
                                 output_accept=set(
                                     ["172.18.8.56", "172.18.8.1", "172.18.8.254", "172.18.8.58"]),
                                 input_accept=set(
                                     ["172.18.8.56", "172.18.8.1", "172.18.8.254", "172.18.8.58"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_21 = NodeFirewallConfig(ip="172.18.8.58", hostname="cve_2015_1427_1_2",
                                 output_accept=set(
                                     ["172.18.8.57", "172.18.8.1", "172.18.8.254", "172.18.8.59"]),
                                 input_accept=set(
                                     ["172.18.8.57", "172.18.8.1", "172.18.8.254", "172.18.8.59"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_22 = NodeFirewallConfig(ip="172.18.8.59", hostname="cve_2016_10033_1_2",
                                 output_accept=set(
                                     ["172.18.8.58", "172.18.8.1", "172.18.8.254", "172.18.8.60"]),
                                 input_accept=set(
                                     ["172.18.8.58", "172.18.8.1", "172.18.8.254", "172.18.8.60"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_23 = NodeFirewallConfig(ip="172.18.8.60", hostname="cve_2010_0426_1_2",
                                 output_accept=set(
                                     ["172.18.8.59", "172.18.8.1", "172.18.8.254", "172.18.8.61"]),
                                 input_accept=set(
                                     ["172.18.8.59", "172.18.8.1", "172.18.8.254", "172.18.8.61"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_24 = NodeFirewallConfig(ip="172.18.8.61", hostname="cve_2015_5602_1_1",
                                 output_accept=set(
                                     ["172.18.8.60", "172.18.8.1", "172.18.8.254", "172.18.8.62"]),
                                 input_accept=set(
                                     ["172.18.8.60", "172.18.8.1", "172.18.8.254", "172.18.8.62"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_25 = NodeFirewallConfig(ip="172.18.8.62", hostname="ssh_1_4",
                                 output_accept=set(
                                     ["172.18.8.61", "172.18.8.1", "172.18.8.254"]),
                                 input_accept=set(
                                     ["172.18.8.61", "172.18.8.1", "172.18.8.254"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_26 = NodeFirewallConfig(ip="172.18.8.191", hostname="hacker_kali_1_1",
                       output_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21",
                                          "172.18.8.79", "172.18.8.191", "172.18.8.10", "172.18.8.1"
                                          "172.18.8.19", "172.18.8.31", "172.18.8.42", "172.18.8.37", "172.18.8.82",
                                          "172.18.8.75", "172.18.8.71", "172.18.8.11",
                                          "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54", "172.18.8.55",
                                          "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59", "172.18.8.60",
                                          "172.18.8.61", "172.18.8.62"
                                          ]),
                       input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21",
                                         "172.18.8.79", "172.18.8.191", "172.18.8.10", "172.18.8.1"
                                         "172.18.8.19",
                                         "172.18.8.31", "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75",
                                         "172.18.8.71", "172.18.8.11",
                                         "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54", "172.18.8.55",
                                         "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59", "172.18.8.60",
                                         "172.18.8.61", "172.18.8.62"
                                         ]),
                       forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                       default_input="DROP", default_output="DROP", default_forward="DROP", default_gw="172.18.8.10")
    node_27 = NodeFirewallConfig(ip="172.18.8.254", hostname="client_1_1",
                                 output_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21",
                                                    "172.18.8.79", "172.18.8.10", "172.18.8.1",
                                                    "172.18.8.254",
                                                    "172.18.8.19", "172.18.8.31", "172.18.8.42", "172.18.8.37",
                                                    "172.18.8.82",
                                                    "172.18.8.75", "172.18.8.71", "172.18.8.11",
                                                    "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54",
                                                    "172.18.8.55",
                                                    "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59",
                                                    "172.18.8.60",
                                                    "172.18.8.61", "172.18.8.62"
                                                    ]),
                                 input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21",
                                                   "172.18.8.79", "172.18.8.10", "172.18.8.1",
                                                   "172.18.8.254",
                                                   "172.18.8.19",
                                                   "172.18.8.31", "172.18.8.42", "172.18.8.37", "172.18.8.82",
                                                   "172.18.8.75",
                                                   "172.18.8.71", "172.18.8.11",
                                                   "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54",
                                                   "172.18.8.55",
                                                   "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59",
                                                   "172.18.8.60",
                                                   "172.18.8.61", "172.18.8.62"
                                                   ]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.8.10")
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11, node_12,
                    node_13, node_14, node_15, node_16, node_17, node_18, node_19, node_20, node_21, node_22, node_23,
                    node_24, node_25, node_26, node_27]
    topology = Topology(node_configs=node_configs, subnetwork = "172.18.8.0/24")
    return topology

# Generates the topology.json configuration file
if __name__ == '__main__':
    if not os.path.exists(util.default_topology_path()):
        TopologyGenerator.write_topology(default_topology())
    topology = util.read_topology(util.default_topology_path())
    emulation_config = EmulationConfig(agent_ip="172.18.8.191", agent_username=constants.csle_ADMIN.USER,
                                     agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    TopologyGenerator.create_topology(topology=topology, emulation_config=emulation_config)