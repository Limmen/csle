import os
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.topology_generator import TopologyGenerator
import csle_common.constants.constants as constants


def default_topology() -> Topology:
    """
    :return: the Topology configuration of the emulation
    """
    node_1 = NodeFirewallConfig(ip="172.18.2.10", hostname="router1",
                                output_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                                   "172.18.2.191", "172.18.2.10", "172.18.2.1", "172.18.2.254"]),
                                input_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                                  "172.18.2.191", "172.18.2.10", "172.18.2.1", "172.18.2.254"]),
                                forward_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                                    "172.18.2.191", "172.18.2.1", "172.18.2.254"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)

    node_2 = NodeFirewallConfig(ip="172.18.2.2", hostname="ssh1",
                                output_accept=set(
                                    ["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79", "172.18.2.191",
                                     "172.18.2.10", "172.18.2.1", "172.18.2.254", "172.18.2.54"]),
                                input_accept=set(
                                    ["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79", "172.18.2.191",
                                     "172.18.2.10", "172.18.2.1", "172.18.2.254", "172.18.2.54"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set([("172.18.2.7", "172.18.2.3"), ("172.18.2.101", "172.18.2.3"),
                                            ("172.18.2.62", "172.18.2.3"), ("172.18.2.61", "172.18.2.3"),
                                            ("172.18.2.74", "172.18.2.3")]),
                                default_input="DROP", default_output="DROP", default_forward="ACCEPT", default_gw=None)

    node_3 = NodeFirewallConfig(ip="172.18.2.3", hostname="telnet1",
                                output_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                                   "172.18.2.191", "172.18.2.10", "172.18.2.74", "172.18.2.1", "172.18.2.254",
                                                   "172.18.2.61"]),
                                input_accept=set(
                                    ["172.18.2.74", "172.18.2.7", "172.18.2.21", "172.18.2.79", "172.18.2.191",
                                     "172.18.2.10", "172.18.2.1", "172.18.2.254", "172.18.2.101", "172.18.2.61"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(),
                                forward_drop=set(["172.18.2.54"]),
                                routes=set([("172.18.2.54", "172.18.2.2"), ("172.18.2.7", "172.18.2.74"),
                                            ("172.18.2.62", "172.18.2.74"), ("172.18.2.101", "172.18.2.74")]),
                                default_input="ACCEPT", default_output="DROP", default_forward="ACCEPT",
                                default_gw=None)

    node_4 = NodeFirewallConfig(ip="172.18.2.21", hostname="honeypot1",
                                output_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21",
                                                   "172.18.2.79", "172.18.2.191", "172.18.2.10", "172.18.2.1", "172.18.2.254"]),
                                input_accept=set(
                                    ["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79", "172.18.2.191",
                                     "172.18.2.10", "172.18.2.1", "172.18.2.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(
                                    [("172.18.2.7", "172.18.2.3"), ("172.18.2.101", "172.18.2.3"),
                                     ("172.18.2.62", "172.18.2.3"),
                                     ("172.18.2.61", "172.18.2.3"), ("172.18.2.74", "172.18.2.3"),
                                     ("172.18.2.54", "172.18.2.2")]
                                ),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                )

    node_5 = NodeFirewallConfig(ip="172.18.2.79", hostname="ftp1",
                                output_accept=set(
                                    ["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79", "172.18.2.191",
                                     "172.18.2.10", "172.18.2.1", "172.18.2.254"]),
                                input_accept=set(
                                    ["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79", "172.18.2.191",
                                     "172.18.2.10", "172.18.2.1", "172.18.2.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(
                                    [("172.18.2.7", "172.18.2.3"), ("172.18.2.101", "172.18.2.3"),
                                     ("172.18.2.62", "172.18.2.3"), ("172.18.2.61", "172.18.2.3"),
                                     ("172.18.2.74", "172.18.2.3"), ("172.18.2.54", "172.18.2.2")]
                                ),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)

    node_6 = NodeFirewallConfig(ip="172.18.2.191", hostname="hacker_kali1",
                                output_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21",
                                                   "172.18.2.79", "172.18.2.191", "172.18.2.10", "172.18.2.1"]),
                                input_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21",
                                                  "172.18.2.79", "172.18.2.191", "172.18.2.10", "172.18.2.1"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.2.10")

    node_7 = NodeFirewallConfig(ip="172.18.2.54", hostname="ssh2",
                                output_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                                   "172.18.2.191", "172.18.2.10", "172.18.2.54", "172.18.2.1", "172.18.2.254"]),
                                input_accept=set(["172.18.2.2", "172.18.2.1", "172.18.2.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.2.2"
                                )

    node_8 = NodeFirewallConfig(ip="172.18.2.74", hostname="ssh3",
                                output_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                                   "172.18.2.191", "172.18.2.10", "172.18.2.61", "172.18.2.74",
                                                   "172.18.2.101", "172.18.2.62", "172.18.2.1", "172.18.2.254"]),
                                input_accept=set(["172.18.2.3", "172.18.2.61", "172.18.2.62", "172.18.2.74",
                                                  "172.18.2.7", "172.18.2.101", "172.18.2.1", "172.18.2.254"]),
                                forward_accept=set(["172.18.2.101", "172.18.2.62", "172.18.2.61"]),
                                output_drop=set(), input_drop=set(),
                                forward_drop=set(["172.18.2.7", "172.18.2.101", "172.18.2.62"]),
                                routes=set([
                                    ("172.18.2.2", "172.18.2.3"), ("172.18.2.21", "172.18.2.3"),
                                    ("172.18.2.54", "172.18.2.3"), ("172.18.2.79", "172.18.2.3"),
                                    ("172.18.2.10", "172.18.2.3"), ("172.18.2.191", "172.18.2.3"),
                                    ("172.18.2.61", "172.18.2.3"), ("172.18.2.7", "172.18.2.62")
                                ]),
                                default_input="DROP", default_output="DROP", default_forward="ACCEPT",
                                default_gw=None)

    node_9 = NodeFirewallConfig(ip="172.18.2.61", hostname="telnet2",
                                output_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                                   "172.18.2.191", "172.18.2.10", "172.18.2.61", "172.18.2.74",
                                                   "172.18.2.1", "172.18.2.254"]),
                                input_accept=set(["172.18.2.3", "172.18.2.61", "172.18.2.62", "172.18.2.74",
                                                  "172.18.2.7", "172.18.2.101", "172.18.2.1", "172.18.2.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.2.3")

    node_10 = NodeFirewallConfig(ip="172.18.2.62", hostname="telnet3",
                                output_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                                   "172.18.2.191", "172.18.2.10", "172.18.2.61", "172.18.2.74",
                                                   "172.18.2.1", "172.18.2.254",
                                                   "172.18.2.101", "172.18.2.62", "172.18.2.7"]),
                                input_accept=set(["172.18.2.74", "172.18.2.7", "172.18.2.101", "172.18.2.1", "172.18.2.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(),
                                routes=set([("172.18.2.2", "172.18.2.74"), ("172.18.2.21", "172.18.2.74"),
                                            ("172.18.2.54", "172.18.2.74"), ("172.18.2.79", "172.18.2.74"),
                                            ("172.18.2.10", "172.18.2.74"), ("172.18.2.191", "172.18.2.74"),
                                            ("172.18.2.61", "172.18.2.74"), ("172.18.2.101", "172.18.2.74")]),
                                forward_drop=set(["172.18.2.7"]), default_input="DROP", default_output="DROP",
                                default_forward="ACCEPT", default_gw=None)

    node_11 = NodeFirewallConfig(ip="172.18.2.101", hostname="honeypot2",
                                 output_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                                    "172.18.2.191", "172.18.2.10", "172.18.2.61", "172.18.2.74",
                                                    "172.18.2.101", "172.18.2.62", "172.18.2.1", "172.18.2.254"]),
                                 input_accept=set(["172.18.2.74", "172.18.2.7", "172.18.2.62", "172.18.2.1", "172.18.2.254"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.2.74")

    node_12 = NodeFirewallConfig(ip="172.18.2.7", hostname="ftp2",
                                 output_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                                    "172.18.2.191", "172.18.2.10", "172.18.2.61", "172.18.2.74",
                                                    "172.18.2.101", "172.18.2.62", "172.18.2.7", "172.18.2.1", "172.18.2.254"]),
                                 input_accept=set(["172.18.2.62", "172.18.2.1", "172.18.2.254"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.2.62")
    node_13 = NodeFirewallConfig(ip="172.18.2.254", hostname="client1",
                                output_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21",
                                                   "172.18.2.79", "172.18.2.10", "172.18.2.1", "172.18.2.254"]),
                                input_accept=set(["172.18.2.2", "172.18.2.3", "172.18.2.21",
                                                  "172.18.2.79", "172.18.2.10", "172.18.2.1", "172.18.2.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.2.10")
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11, node_12,
                    node_13]
    topology = Topology(node_configs=node_configs, subnetwork="172.18.2.0/24")
    return topology

# Generates the topology.json configuration file
if __name__ == '__main__':
    if not os.path.exists(util.default_topology_path()):
        TopologyGenerator.write_topology(default_topology())
    topology = util.read_topology(util.default_topology_path())
    emulation_config = EmulationConfig(agent_ip="172.18.2.191", agent_username=constants.csle_ADMIN.USER,
                                     agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    TopologyGenerator.create_topology(topology=topology, emulation_config=emulation_config)
