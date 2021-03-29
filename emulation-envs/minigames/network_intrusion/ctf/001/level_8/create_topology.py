import os
from gym_pycr_ctf.dao.container_config.topology import Topology
from gym_pycr_ctf.dao.container_config.node_firewall_config import NodeFirewallConfig
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.envs.config.generator.topology_generator import TopologyGenerator

def default_topology() -> Topology:
    node_1 = NodeFirewallConfig(ip="172.18.8.10",
                           output_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                                              "172.18.8.191", "172.18.8.10", "172.18.8.1", "172.18.8.19", "172.18.8.31",
                                              "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                              "172.18.8.11",
                                              "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54", "172.18.8.55",
                                              "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59", "172.18.8.60",
                                              "172.18.8.61", "172.18.8.62"]),
                           input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                                             "172.18.8.191", "172.18.8.10", "172.18.8.1", "172.18.8.19", "172.18.8.31",
                                             "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                             "172.18.8.11",
                                             "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54", "172.18.8.55",
                                             "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59", "172.18.8.60",
                                             "172.18.8.61", "172.18.8.62"
                                             ]),
                           forward_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79",
                                             "172.18.8.191", "172.18.8.1", "172.18.8.19", "172.18.8.31", "172.18.8.42",
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
    node_2 = NodeFirewallConfig(ip="172.18.8.2",
                       output_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                          "172.18.8.10", "172.18.8.1", "172.18.8.19", "172.18.8.31", "172.18.8.42",
                                          "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                          "172.18.8.11", "172.18.8.52"]),
                       input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                         "172.18.8.10", "172.18.8.1", "172.18.8.19", "172.18.8.31", "172.18.8.42",
                                         "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                         "172.18.8.11", "172.18.8.52"]),
                       forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set(),
                       default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                       )
    node_3 = NodeFirewallConfig(ip="172.18.8.3",
                           output_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                              "172.18.8.10", "172.18.8.1", "172.18.8.19", "172.18.8.31", "172.18.8.42",
                                              "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                              "172.18.8.11"]),
                           input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                             "172.18.8.10", "172.18.8.1", "172.18.8.19", "172.18.8.31", "172.18.8.42",
                                             "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                             "172.18.8.11"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                            default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_4 = NodeFirewallConfig(ip="172.18.8.21",
                           output_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21",
                                                "172.18.8.79", "172.18.8.191", "172.18.8.10", "172.18.8.1",
                                              "172.18.8.19", "172.18.8.31", "172.18.8.42",
                                              "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                              "172.18.8.11"]),
                           input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                             "172.18.8.10", "172.18.8.1", "172.18.8.19", "172.18.8.31", "172.18.8.42",
                                             "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                           default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                           )
    node_5 = NodeFirewallConfig(ip="172.18.8.79",
                           output_accept=set(
                               ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                "172.18.8.10", "172.18.8.1", "172.18.8.19", "172.18.8.31",
                                "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                "172.18.8.11", "172.18.8.51"]),
                           input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                             "172.18.8.10", "172.18.8.1", "172.18.8.19", "172.18.8.31",
                                             "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                             "172.18.8.11", "172.18.8.51"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                           default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_6 = NodeFirewallConfig(ip="172.18.8.19",
                                output_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.31",
                                     "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75","172.18.8.71",
                                     "172.18.8.11"]),
                                input_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.31",
                                     "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71",
                                     "172.18.8.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_7 = NodeFirewallConfig(ip="172.18.8.31",
                                output_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.42", "172.18.8.37",
                                     "172.18.8.82", "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                                input_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.42", "172.18.8.37",
                                     "172.18.8.82", "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_8 = NodeFirewallConfig(ip="172.18.8.42",
                                output_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.37", "172.18.8.82",
                                     "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                                input_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.37", "172.18.8.82",
                                     "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_9 = NodeFirewallConfig(ip="172.18.8.37",
                                output_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.42", "172.18.8.82",
                                     "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                                input_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.42", "172.18.8.82",
                                     "172.18.8.75", "172.18.8.71", "172.18.8.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_10 = NodeFirewallConfig(ip="172.18.8.82",
                                output_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.42",
                                     "172.18.8.37", "172.18.8.75", "172.18.8.71", "172.18.8.11", "172.18.8.53",
                                     "172.18.8.51"]),
                                input_accept=set(
                                    ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                     "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.42", "172.18.8.37",
                                     "172.18.8.75", "172.18.8.71", "172.18.8.11", "172.18.8.53", "172.18.8.51"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_11 = NodeFirewallConfig(ip="172.18.8.75",
                                 output_accept=set(
                                     ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                      "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.42",
                                      "172.18.8.37", "172.18.8.82", "172.18.8.71", "172.18.8.11"]),
                                 input_accept=set(
                                     ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                      "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.42", "172.18.8.37",
                                      "172.18.8.82", "172.18.8.71", "172.18.8.11"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_12 = NodeFirewallConfig(ip="172.18.8.71",
                                 output_accept=set(
                                     ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                      "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.42",
                                      "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.11"]),
                                 input_accept=set(
                                     ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                      "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.42", "172.18.8.37",
                                      "172.18.8.82", "172.18.8.75", "172.18.8.11"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_13 = NodeFirewallConfig(ip="172.18.8.11",
                                 output_accept=set(
                                     ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                      "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.42",
                                      "172.18.8.37", "172.18.8.82", "172.18.8.75", "172.18.8.71"]),
                                 input_accept=set(
                                     ["172.18.8.2", "172.18.8.3", "172.18.8.21", "172.18.8.79", "172.18.8.191",
                                      "172.18.8.10", "172.18.8.1", "172.18.8.79", "172.18.8.42", "172.18.8.37",
                                      "172.18.8.82", "172.18.8.75", "172.18.8.71"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_14 = NodeFirewallConfig(ip="172.18.8.51",
                                 output_accept=set(
                                     ["172.18.8.79", "172.18.8.1", "172.18.8.82"]),
                                 input_accept=set(
                                     ["172.18.8.79", "172.18.8.1", "172.18.8.82"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_15 = NodeFirewallConfig(ip="172.18.8.52",
                                output_accept=set(
                                    ["172.18.8.2", "172.18.8.1", "172.18.8.54"]),
                                input_accept=set(
                                    ["172.18.8.2", "172.18.8.1", "172.18.8.54"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                forward_drop=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                )
    node_16 = NodeFirewallConfig(ip="172.18.8.53",
                                 output_accept=set(
                                     ["172.18.8.82", "172.18.8.1"]),
                                 input_accept=set(
                                     ["172.18.8.82", "172.18.8.1"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_17 = NodeFirewallConfig(ip="172.18.8.54",
                                 output_accept=set(
                                     ["172.18.8.52", "172.18.8.1", "172.18.8.55"]),
                                 input_accept=set(
                                     ["172.18.8.52", "172.18.8.1", "172.18.8.55"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_18 = NodeFirewallConfig(ip="172.18.8.55",
                                 output_accept=set(
                                     ["172.18.8.54", "172.18.8.1", "172.18.8.56"]),
                                 input_accept=set(
                                     ["172.18.8.54", "172.18.8.1", "172.18.8.56"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_19 = NodeFirewallConfig(ip="172.18.8.56",
                                 output_accept=set(
                                     ["172.18.8.55", "172.18.8.1", "172.18.8.57"]),
                                 input_accept=set(
                                     ["172.18.8.55", "172.18.8.1", "172.18.8.57"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_20 = NodeFirewallConfig(ip="172.18.8.57",
                                 output_accept=set(
                                     ["172.18.8.56", "172.18.8.1", "172.18.8.58"]),
                                 input_accept=set(
                                     ["172.18.8.56", "172.18.8.1", "172.18.8.58"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_21 = NodeFirewallConfig(ip="172.18.8.58",
                                 output_accept=set(
                                     ["172.18.8.57", "172.18.8.1", "172.18.8.59"]),
                                 input_accept=set(
                                     ["172.18.8.57", "172.18.8.1", "172.18.8.59"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_22 = NodeFirewallConfig(ip="172.18.8.59",
                                 output_accept=set(
                                     ["172.18.8.58", "172.18.8.1", "172.18.8.60"]),
                                 input_accept=set(
                                     ["172.18.8.58", "172.18.8.1", "172.18.8.60"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_23 = NodeFirewallConfig(ip="172.18.8.60",
                                 output_accept=set(
                                     ["172.18.8.59", "172.18.8.1", "172.18.8.61"]),
                                 input_accept=set(
                                     ["172.18.8.59", "172.18.8.1", "172.18.8.61"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_24 = NodeFirewallConfig(ip="172.18.8.61",
                                 output_accept=set(
                                     ["172.18.8.60", "172.18.8.1", "172.18.8.62"]),
                                 input_accept=set(
                                     ["172.18.8.60", "172.18.8.1", "172.18.8.62"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_25 = NodeFirewallConfig(ip="172.18.8.62",
                                 output_accept=set(
                                     ["172.18.8.61", "172.18.8.1"]),
                                 input_accept=set(
                                     ["172.18.8.61", "172.18.8.1"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                 forward_drop=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                 )
    node_26 = NodeFirewallConfig(ip="172.18.8.191",
                       output_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21",
                                          "172.18.8.79", "172.18.8.191", "172.18.8.10", "172.18.8.1",
                                          "172.18.8.19", "172.18.8.31", "172.18.8.42", "172.18.8.37", "172.18.8.82",
                                          "172.18.8.75", "172.18.8.71", "172.18.8.11",
                                          "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54", "172.18.8.55",
                                          "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59", "172.18.8.60",
                                          "172.18.8.61", "172.18.8.62"
                                          ]),
                       input_accept=set(["172.18.8.2", "172.18.8.3", "172.18.8.21",
                                         "172.18.8.79", "172.18.8.191", "172.18.8.10", "172.18.8.1", "172.18.8.19",
                                         "172.18.8.31", "172.18.8.42", "172.18.8.37", "172.18.8.82", "172.18.8.75",
                                         "172.18.8.71", "172.18.8.11",
                                         "172.18.8.51", "172.18.8.52", "172.18.8.53", "172.18.8.54", "172.18.8.55",
                                         "172.18.8.56", "172.18.8.57", "172.18.8.58", "172.18.8.59", "172.18.8.60",
                                         "172.18.8.61", "172.18.8.62"
                                         ]),
                       forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                       default_input="DROP", default_output="DROP", default_forward="DROP", default_gw="172.18.8.10")
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11, node_12,
                    node_13, node_14, node_15, node_16, node_17, node_18, node_19, node_20, node_21, node_22, node_23,
                    node_24, node_25, node_26]
    topology = Topology(node_configs=node_configs, subnetwork = "172.18.8.0/24")
    return topology


if __name__ == '__main__':
    if not os.path.exists(util.default_topology_path()):
        TopologyGenerator.write_topology(default_topology())
    topology = util.read_topology(util.default_topology_path())
    cluster_config = ClusterConfig(agent_ip="172.18.8.191", agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    TopologyGenerator.create_topology(topology=topology, cluster_config=cluster_config)