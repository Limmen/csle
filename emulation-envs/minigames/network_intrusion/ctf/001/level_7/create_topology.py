import os
from gym_pycr_ctf.dao.container_config.topology import Topology
from gym_pycr_ctf.dao.container_config.node_firewall_config import NodeFirewallConfig
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs_model.config.generator.topology_generator import TopologyGenerator

def default_topology() -> Topology:
    node_1 = NodeFirewallConfig(ip="172.18.7.10",
                           output_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79",
                                              "172.18.7.191", "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.19",
                                              "172.18.7.31",
                                              "172.18.7.42", "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71",
                                              "172.18.7.11"]),
                           input_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79",
                                             "172.18.7.191", "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.19",
                                             "172.18.7.31",
                                             "172.18.7.42", "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71",
                                             "172.18.7.11"]),
                           forward_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79",
                                             "172.18.7.191", "172.18.7.1", "172.18.7.254", "172.18.7.19", "172.18.7.31",
                                               "172.18.7.42",
                                               "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71",
                                               "172.18.7.11"]),
                           output_drop = set(), input_drop = set(), forward_drop = set(), routes=set(),
                           default_input = "DROP", default_output = "DROP", default_forward="DROP",
                           default_gw=None
                           )
    node_2 = NodeFirewallConfig(ip="172.18.7.2",
                       output_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                          "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.19", "172.18.7.31",
                                          "172.18.7.42",
                                          "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71",
                                          "172.18.7.11"]),
                       input_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                         "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.19", "172.18.7.31",
                                         "172.18.7.42",
                                         "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71",
                                         "172.18.7.11"]),
                       forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set(),
                       default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                       )
    node_3 = NodeFirewallConfig(ip="172.18.7.3",
                           output_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                              "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.19", "172.18.7.31",
                                              "172.18.7.42",
                                              "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71",
                                              "172.18.7.11"]),
                           input_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                             "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.19", "172.18.7.31",
                                             "172.18.7.42",
                                             "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71",
                                             "172.18.7.11"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                            default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_4 = NodeFirewallConfig(ip="172.18.7.21",
                           output_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                                "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.1", "172.18.7.254",
                                              "172.18.7.19", "172.18.7.31", "172.18.7.42",
                                              "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71",
                                              "172.18.7.11"]),
                           input_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                             "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.19", "172.18.7.31",
                                             "172.18.7.42",
                                             "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                           default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                           )
    node_5 = NodeFirewallConfig(ip="172.18.7.79",
                           output_accept=set(
                               ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.19", "172.18.7.31",
                                "172.18.7.42", "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71",
                                "172.18.7.11"]),
                           input_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                             "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.19", "172.18.7.31",
                                             "172.18.7.42", "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71",
                                             "172.18.7.11"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                           default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_6 = NodeFirewallConfig(ip="172.18.7.19",
                                output_accept=set(
                                    ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                     "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.31",
                                     "172.18.7.42", "172.18.7.37", "172.18.7.82", "172.18.7.75","172.18.7.71",
                                     "172.18.7.11"]),
                                input_accept=set(
                                    ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                     "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.31",
                                     "172.18.7.42", "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71",
                                     "172.18.7.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_7 = NodeFirewallConfig(ip="172.18.7.31",
                                output_accept=set(
                                    ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                     "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.42",
                                     "172.18.7.37",
                                     "172.18.7.82", "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                                input_accept=set(
                                    ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                     "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.42",
                                     "172.18.7.37",
                                     "172.18.7.82", "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_8 = NodeFirewallConfig(ip="172.18.7.42",
                                output_accept=set(
                                    ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                     "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.37",
                                     "172.18.7.82",
                                     "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                                input_accept=set(
                                    ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                     "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.37",
                                     "172.18.7.82",
                                     "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_9 = NodeFirewallConfig(ip="172.18.7.37",
                                output_accept=set(
                                    ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                     "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.42",
                                     "172.18.7.82",
                                     "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                                input_accept=set(
                                    ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                     "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.42",
                                     "172.18.7.82",
                                     "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_10 = NodeFirewallConfig(ip="172.18.7.82",
                                output_accept=set(
                                    ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                     "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.42",
                                     "172.18.7.37", "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                                input_accept=set(
                                    ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                     "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.42",
                                     "172.18.7.37",
                                     "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_11 = NodeFirewallConfig(ip="172.18.7.75",
                                 output_accept=set(
                                     ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                      "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.42",
                                      "172.18.7.37", "172.18.7.82", "172.18.7.71", "172.18.7.11"]),
                                 input_accept=set(
                                     ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                      "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.42",
                                      "172.18.7.37",
                                      "172.18.7.82", "172.18.7.71", "172.18.7.11"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_12 = NodeFirewallConfig(ip="172.18.7.71",
                                 output_accept=set(
                                     ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                      "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.42",
                                      "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.11"]),
                                 input_accept=set(
                                     ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                      "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.42",
                                      "172.18.7.37",
                                      "172.18.7.82", "172.18.7.75", "172.18.7.11"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_13 = NodeFirewallConfig(ip="172.18.7.11",
                                 output_accept=set(
                                     ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                      "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.42",
                                      "172.18.7.37", "172.18.7.82", "172.18.7.75", "172.18.7.71"]),
                                 input_accept=set(
                                     ["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                      "172.18.7.10", "172.18.7.1", "172.18.7.254", "172.18.7.79", "172.18.7.42",
                                      "172.18.7.37",
                                      "172.18.7.82", "172.18.7.75", "172.18.7.71"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_14 = NodeFirewallConfig(ip="172.18.7.191",
                       output_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                          "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.1",
                                          "172.18.7.19", "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82",
                                          "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                       input_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                         "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.1",
                                         "172.18.7.19",
                                         "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82", "172.18.7.75",
                                         "172.18.7.71", "172.18.7.11"]),
                       forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                       default_input="DROP", default_output="DROP", default_forward="DROP", default_gw="172.18.7.10")
    node_15 = NodeFirewallConfig(ip="172.18.7.254",
                                 output_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                                    "172.18.7.79", "172.18.7.10", "172.18.7.1",
                                                    "172.18.7.254",
                                                    "172.18.7.19", "172.18.7.31", "172.18.7.42", "172.18.7.37",
                                                    "172.18.7.82",
                                                    "172.18.7.75", "172.18.7.71", "172.18.7.11"]),
                                 input_accept=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                                   "172.18.7.79", "172.18.7.10", "172.18.7.1",
                                                   "172.18.7.254",
                                                   "172.18.7.19",
                                                   "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82",
                                                   "172.18.7.75",
                                                   "172.18.7.71", "172.18.7.11"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.7.10")
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11, node_12,
                    node_13, node_14, node_15]
    topology = Topology(node_configs=node_configs, subnetwork = "172.18.7.0/24")
    return topology


if __name__ == '__main__':
    if not os.path.exists(util.default_topology_path()):
        TopologyGenerator.write_topology(default_topology())
    topology = util.read_topology(util.default_topology_path())
    emulation_config = EmulationConfig(agent_ip="172.18.7.191", agent_username="pycr_admin",
                                     agent_pw="pycr@admin-pw_191", server_connection=False)
    TopologyGenerator.create_topology(topology=topology, emulation_config=emulation_config)