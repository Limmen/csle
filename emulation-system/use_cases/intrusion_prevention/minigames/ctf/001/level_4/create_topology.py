import os
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.topology_generator import TopologyGenerator
import csle_common.constants.constants as constants


def default_topology(network_id: int = 4) -> Topology:
    """
    :param network_id: the network id
    :return: the Topology of the emulation
    """
    node_1 = NodeFirewallConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                hostname=f"{constants.CONTAINER_IMAGES.ROUTER_2}_1",
                                output_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                                                   f"{network_id}.254"]),
                                input_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.254"]),
                                forward_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                    f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                    f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                    f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                    f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                                    f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                                    f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                                                    f"{network_id}.254"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                                default_input=constants.FIREWALL.DROP, default_output=constants.FIREWALL.DROP,
                                default_forward=constants.FIREWALL.DROP,
                                default_gw=None
                                )
    node_2 = NodeFirewallConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                hostname=f"{constants.CONTAINER_IMAGES.SSH_1}_1",
                                output_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                                                   f"{network_id}.254"]),
                                input_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(),
                                forward_drop=set(),
                                default_input=constants.FIREWALL.DROP, default_output=constants.FIREWALL.DROP,
                                default_forward=constants.FIREWALL.DROP, default_gw=None
                                )
    node_3 = NodeFirewallConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                hostname=f"{constants.CONTAINER_IMAGES.TELNET_1}_1",
                                output_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                                                   f"{network_id}.254"]),
                                input_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input=constants.FIREWALL.DROP, default_output=constants.FIREWALL.DROP,
                                default_forward=constants.FIREWALL.DROP, default_gw=None)
    node_4 = NodeFirewallConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_1",
                                output_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                                                   f"{network_id}.254"]),
                                input_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input=constants.FIREWALL.DROP, default_output=constants.FIREWALL.DROP,
                                default_forward=constants.FIREWALL.DROP, default_gw=None
                                )
    node_5 = NodeFirewallConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                hostname=f"{constants.CONTAINER_IMAGES.FTP_1}_1",
                                output_accept=set(
                                    [f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.254"]),
                                input_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input=constants.FIREWALL.DROP, default_output=constants.FIREWALL.DROP,
                                default_forward=constants.FIREWALL.DROP, default_gw=None)
    node_6 = NodeFirewallConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                hostname=f"{constants.CONTAINER_IMAGES.HACKER_KALI_1}_1",
                                output_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1"]),
                                input_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input=constants.FIREWALL.DROP, default_output=constants.FIREWALL.DROP,
                                default_forward=constants.FIREWALL.DROP,
                                default_gw=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10")
    node_7 = NodeFirewallConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.254",
                                hostname=f"{constants.CONTAINER_IMAGES.CLIENT_1}_1",
                                output_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                                   f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.254"]),
                                input_accept=set([f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.1",
                                                  f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input=constants.FIREWALL.DROP, default_output=constants.FIREWALL.DROP,
                                default_forward=constants.FIREWALL.DROP,
                                default_gw=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10")
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7]
    topology = Topology(node_configs=node_configs,
                        subnetwork=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK}")
    return topology


# Generates the topology.json configuration file
if __name__ == '__main__':
    network_id = 4
    if not os.path.exists(util.default_topology_path()):
        TopologyGenerator.write_topology(default_topology())
    topology = util.read_topology(util.default_topology_path(network_id=network_id))
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                       agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    TopologyGenerator.create_topology(topology=topology, emulation_config=emulation_config)
