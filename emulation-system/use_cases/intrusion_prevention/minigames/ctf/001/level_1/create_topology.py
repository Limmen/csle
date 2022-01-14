import os
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.topology_generator import TopologyGenerator
import csle_common.constants.constants as constants


def default_topology() -> Topology:
    """
    :return: the Topology configuration
    """
    node_1 = NodeFirewallConfig(
        ip="172.18.1.10", hostname="router_1_1",
        output_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79",
                                             "172.18.1.191", "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
        input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79",
                                             "172.18.1.191", "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
        forward_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79",
                                             "172.18.1.191", "172.18.1.1", "172.18.1.254"]),
        output_drop = set(), input_drop = set(), forward_drop = set(), routes=set(),
        default_input = "DROP", default_output = "DROP", default_forward="DROP", default_gw=None)
    node_2 = NodeFirewallConfig(ip="172.18.1.2", hostname="ssh_1_1",
                       output_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                          "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                       input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                         "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                       forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set(),
                       default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                       )
    node_3 = NodeFirewallConfig(ip="172.18.1.3", hostname="telnet_1_1",
                           output_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                         "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                             "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                            default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_4 = NodeFirewallConfig(ip="172.18.1.21", hostname="honeypot_1_1",
                           output_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21",
                                                "172.18.1.79", "172.18.1.191", "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                             "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                           default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                           )
    node_5 = NodeFirewallConfig(ip="172.18.1.79", hostname="ftp_1_1",
                           output_accept=set(
                               ["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.191",
                                             "172.18.1.10", "172.18.1.1", "172.18.1.254"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                           default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_6 = NodeFirewallConfig(ip="172.18.1.191", hostname="hacker_kali_1_1",
                       output_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21",
                                          "172.18.1.79", "172.18.1.191", "172.18.1.10", "172.18.1.1"]),
                       input_accept=set(["172.18.1.2", "172.18.1.3", "172.18.1.21",
                                         "172.18.1.79", "172.18.1.191", "172.18.1.10", "172.18.1.1"]),
                       forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                       default_input="DROP", default_output="DROP", default_forward="DROP", default_gw="172.18.1.10")
    node_7 = NodeFirewallConfig(ip="172.18.1.254", hostname="client_1_1",
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

# Generates the topology.json configuration file
if __name__ == '__main__':
    if not os.path.exists(util.default_topology_path()):
        TopologyGenerator.write_topology(default_topology())
    topology = util.read_topology(util.default_topology_path())
    emulation_config = EmulationConfig(agent_ip="172.18.1.191", agent_username=constants.csle_ADMIN.USER,
                                     agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    TopologyGenerator.create_topology(topology=topology, emulation_config=emulation_config)