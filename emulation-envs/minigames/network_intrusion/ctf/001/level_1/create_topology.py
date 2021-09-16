import os
from gym_pycr_ctf.dao.container_config.topology import Topology
from gym_pycr_ctf.dao.container_config.node_firewall_config import NodeFirewallConfig
from gym_pycr_ctf.util.experiments_util import util
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.config.generator.topology_generator import TopologyGenerator

def default_topology() -> Topology:
    node_1 = NodeFirewallConfig(ip="172.18.1.10",
                           output_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79",
                                                "172.18.1.191", "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79",
                                             "172.18.1.191", "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           forward_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79",
                                             "172.18.1.191", "172.18.1.1", "172.18.1.254"]),
                           output_drop = set(), input_drop = set(), forward_drop = set(), routes=set(),
                           default_input = "DROP", default_output = "DROP", default_forward="DROP",
                           default_gw=None
                           )
    node_2 = NodeFirewallConfig(ip="172.18.1.2",
                       output_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                          "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                       input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                         "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                       forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set(),
                       default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                       )
    node_3 = NodeFirewallConfig(ip="172.18.1.3",
                           output_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                         "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                             "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                            default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_4 = NodeFirewallConfig(ip="172.18.1.21",
                           output_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21",
                                                "172.18.1.79", "172.18.1.191", "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                             "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                           default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                           )
    node_5 = NodeFirewallConfig(ip="172.18.1.79",
                           output_accept=set(
                               ["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                             "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                           default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_6 = NodeFirewallConfig(ip="172.18.1.191",
                       output_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21",
                                          "172.18.1.79", "172.18.1.191", "172.18.1.10", "172.18.1.1"]),
                       input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21",
                                         "172.18.1.79", "172.18.1.191", "172.18.1.10", "172.18.1.1"]),
                       forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                       default_input="DROP", default_output="DROP", default_forward="DROP", default_gw="172.18.1.10")
    node_7 = NodeFirewallConfig(ip="172.18.1.254",
                                output_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21",
                                                   "172.18.1.79", "172.18.1.10", "172.18.1.1"]),
                                input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21",
                                                  "172.18.1.79", "172.18.1.10", "172.18.1.1"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.1.10")
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7]
    topology = Topology(node_configs=node_configs, subnetwork = "172.18.1.0/24")
    return topology


if __name__ == '__main__':
    if not os.path.exists(util.default_topology_path()):
        TopologyGenerator.write_topology(default_topology())
    topology = util.read_topology(util.default_topology_path())
    emulation_config = EmulationConfig(agent_ip="172.18.1.191", agent_username="pycr_admin",
                                     agent_pw="pycr@admin-pw_191", server_connection=False)
    TopologyGenerator.create_topology(topology=topology, emulation_config=emulation_config)