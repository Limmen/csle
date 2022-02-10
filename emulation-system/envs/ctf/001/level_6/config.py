import argparse
import os
import csle_common.constants.constants as constants
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.container_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.dao.container_config.node_container_config import NodeContainerConfig
from csle_common.dao.container_config.container_network import ContainerNetwork
from csle_common.dao.container_config.flags_config import FlagsConfig
from csle_common.dao.container_config.node_flags_config import NodeFlagsConfig
from csle_common.dao.container_config.resources_config import ResourcesConfig
from csle_common.dao.container_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.container_config.node_network_config import NodeNetworkConfig
from csle_common.dao.container_config.packet_loss_type import PacketLossType
from csle_common.dao.container_config.packet_delay_distribution_type import PacketDelayDistributionType
from csle_common.dao.container_config.traffic_config import TrafficConfig
from csle_common.dao.container_config.node_traffic_config import NodeTrafficConfig
from csle_common.dao.container_config.users_config import UsersConfig
from csle_common.dao.container_config.node_users_config import NodeUsersConfig
from csle_common.dao.container_config.pw_vulnerability_config import PwVulnerabilityConfig
from csle_common.dao.container_config.vulnerability_type import VulnType
from csle_common.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.container_config.emulation_env_config import EmulationEnvConfig
from csle_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from csle_common.util.experiments_util import util


def default_config(name: str, network_id: int = 6, level: int = 6, version: str = "0.0.1") -> EmulationEnvConfig:
    """
    Returns the default configuration of the emulation environment

    :param name: the name of the emulation
    :param network_id: the network id of the emulation
    :param level: the level of the emulation
    :param version: the version of the emulation
    :return: the emulation environment configuration
    """
    containers_cfg = default_containers_config(network_id=network_id, level=level, version=version)
    flags_cfg = default_flags_config(network_id=network_id)
    resources_cfg = default_resource_constraints_config(network_id=network_id, level=level)
    topology_cfg = default_topology_config(network_id=network_id)
    traffic_cfg = default_traffic_config(network_id=network_id)
    users_cfg = default_users_config(network_id=network_id)
    vuln_cfg = default_vulns_config(network_id=network_id)
    emulation_env_cfg = EmulationEnvConfig(
        name=name, containers_config=containers_cfg, users_config=users_cfg, flags_config=flags_cfg,
        vuln_config=vuln_cfg, topology_config=topology_cfg, traffic_config=traffic_cfg, resources_config=resources_cfg
    )
    return emulation_env_cfg


def default_containers_config(network_id: int, level: int, version: str) -> ContainersConfig:
    """
    :param version: the version of the containers to use
    :param level: the level parameter of the emulation
    :param network_id: the network id
    :return: the ContainersConfig of the emulation
    """
    containers = [
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.CLIENT_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.254",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 )),
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.FTP_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HACKER_KALI_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.ROUTER_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.10",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.SSH_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.2",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.TELNET_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.FTP_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 )),
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.101",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_7",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.7{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.SSH_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_9",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.9{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.SSH_3}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.TELNET_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.TELNET_3}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.62",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_7",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.7{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_2"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_3"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_4"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_5"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_6"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_7"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_9",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.9{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_2"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_9",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.9{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_3"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_9",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.9{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_4"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_9",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.9{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_5"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_7",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.7{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_6"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_7",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.7{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_7"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_7",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.7{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_8"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_7",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.7{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_9"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_10"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_11"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_12"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_13"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_14"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME, version=version,
                            level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_15")
    ]
    containers_cfg = ContainersConfig(
        containers=containers,
        agent_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
        router_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
        ids_enabled=False, vulnerable_nodes=[
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7"
        ],
        networks=[
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_7",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.7{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_9",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.9{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
            )
        ]
    )
    return containers_cfg


def default_flags_config(network_id: int) -> FlagsConfig:
    """
    :param network_id: the network id
    :return: The flags confguration
    """
    flags = [
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                        flags=[(
                            f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}3"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}3", f"/{constants.COMMANDS.TMP_DIR}/", 3, True,
                            1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                        flags=[(
                            f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}2"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}2", f"/{constants.COMMANDS.TMP_DIR}/", 2, True,
                            1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                        flags=[(
                            f"/{constants.COMMANDS.ROOT_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}1"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}1", f"/{constants.COMMANDS.ROOT_DIR}/", 1, True,
                            1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54",
                        flags=[(
                            f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}4"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}4", f"/{constants.COMMANDS.TMP_DIR}/", 4, True,
                            1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
                        flags=[(
                            f"/{constants.COMMANDS.ROOT_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}5"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}5", f"/{constants.COMMANDS.ROOT_DIR}/", 5, True,
                            1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7",
                        flags=[(
                            f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}6"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}6", f"/{constants.COMMANDS.TMP_DIR}/", 6, True,
                            1)])
    ]
    flags_config = FlagsConfig(flags=flags)
    return flags_config


def default_resource_constraints_config(network_id: int, level: int) -> ResourcesConfig:
    """
    :param level: the level parameter of the emulation
    :param network_id: the network id
    :return: generates the ResourcesConfig
    """
    node_resources_configurations = [
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.ROUTER_2}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 )),
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.10", NodeNetworkConfig(
                    interface=constants.NETWORKING.ETH1,
                    limit_packets_queue=30000, packet_delay_ms=2,
                    packet_delay_jitter_ms=0.5, packet_delay_correlation_percentage=25,
                    packet_delay_distribution=PacketDelayDistributionType.PARETO,
                    packet_loss_type=PacketLossType.GEMODEL,
                    loss_gemodel_p=0.02, loss_gemodel_r=0.97,
                    loss_gemodel_k=0.98, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.02,
                    packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                    packet_duplicate_correlation_percentage=25, packet_reorder_percentage=2,
                    packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                    rate_limit_mbit=100, packet_overhead_bytes=0,
                    cell_overhead_bytes=0
                ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.SSH_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 )),
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.2",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH1,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))
            ]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.TELNET_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 )),
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH1,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))
            ]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.FTP_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HACKER_KALI_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=2,
                     packet_delay_jitter_ms=0.5, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.02, loss_gemodel_r=0.97,
                     loss_gemodel_k=0.98, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.02,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=2,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=100, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.SSH_2}_1-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH1,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 ))
                            ]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.SSH_3}_1-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH1,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 ))]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.TELNET_2}_1-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH1,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 ))
                            ]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.TELNET_3}_1-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.62",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH1,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH2,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 ))
                            ]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_1-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.101",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH1,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 )),
                            ]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.FTP_2}_1-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 ))]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_2-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
                                     limit_packets_queue=30000, packet_delay_ms=0.1,
                                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                     packet_loss_type=PacketLossType.GEMODEL,
                                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                                     cell_overhead_bytes=0
                                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_3-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_4-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_5-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_6-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_7-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_2-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_3-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_4-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_5-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_6-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_7-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_8-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_9-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_10-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_11-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_12-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_13-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_14-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_15-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=0.1,
                     packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                     loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=1000, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.CLIENT_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.254",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
                     limit_packets_queue=30000, packet_delay_ms=2,
                     packet_delay_jitter_ms=0.5, packet_delay_correlation_percentage=25,
                     packet_delay_distribution=PacketDelayDistributionType.PARETO,
                     packet_loss_type=PacketLossType.GEMODEL,
                     loss_gemodel_p=0.02, loss_gemodel_r=0.97,
                     loss_gemodel_k=0.98, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.02,
                     packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                     packet_duplicate_correlation_percentage=25, packet_reorder_percentage=2,
                     packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                     rate_limit_mbit=100, packet_overhead_bytes=0,
                     cell_overhead_bytes=0
                 ))])
    ]
    resources_config = ResourcesConfig(node_resources_configurations=node_resources_configurations)
    return resources_config


def default_topology_config(network_id: int) -> Topology:
    """
    :param network_id: the network id
    :return: the Topology configuration
    """
    node_1 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.ROUTER_2}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.10",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set([]),
        output_drop=set(), input_drop=set(), forward_drop=set(), routes=set())

    node_2 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.SSH_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.2",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set()
    )

    node_3 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.TELNET_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())

    node_4 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())

    node_5 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.FTP_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())

    node_6 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HACKER_KALI_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())

    node_7 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.SSH_2}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())

    node_8 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.SSH_3}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())

    node_9 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.TELNET_2}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())

    node_10 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.TELNET_3}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.62",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())

    node_11 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())

    node_12 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.FTP_2}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_13 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_2",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_14 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_3",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_15 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_4",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_16 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_5",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_17 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_6",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_18 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_7",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_19 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_2",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_9",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.9{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_20 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_3",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_9",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.9{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_21 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_4",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_9",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.9{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_22 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_5",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_9",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.9{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_23 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_6",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_7",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.7{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_24 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_7",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_7",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.7{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_25 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_8",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_7",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.7{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_26 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_9",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_7",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.7{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_27 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_10",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_28 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_11",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_29 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_12",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_30 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_13",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_31 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_14",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_32 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_15",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_8",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_33 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.CLIENT_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.254",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11,
                    node_12, node_13, node_14, node_15, node_16, node_17, node_18, node_19, node_20,
                    node_21, node_22, node_23, node_24, node_25, node_26, node_27, node_28, node_29, node_30,
                    node_31, node_32, node_33]
    topology = Topology(node_configs=node_configs,
                        subnetwork_masks=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.7{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.8{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.9{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}"
                        ])
    return topology


def default_traffic_config(network_id: int) -> TrafficConfig:
    """
    :param network_id: the network id
    :return: the traffic configuration
    """
    traffic_generators = [
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.254",
                          commands=[
                              # f"timeout 120 sudo nmap -sS -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sP --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sU -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sT -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sF -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sN -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sX -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -O --osscan-guess --max-os-tries 1 --min-rate 100000
                              # --max-retries 1 -T5 -n {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{
                              # network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap --script=http-grep --min-rate 100000 --max-retries 1 -T5 -n
                              # {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sv -sC --script=finger --min-rate 100000 --max-retries 1 -T5
                              # -n {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}2.2 "
                              f"> /dev/null 2>&1 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}2.2:80 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | "
                              f"telnet {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-p 5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 "
                              f"> /dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 "
                              f"> /dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                          commands=[],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10"
                          ],
                          target_hosts=[]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-p 5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-p 5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54 > /dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2:80 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-p 5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61:8080 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | "
                              f"telnet {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 psql -h "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p 5432 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.2",
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.2"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | "
                              f"telnet {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 "
                              f"-c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 "
                              f"-p 5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' "
                              f"ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61:8080 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | "
                              f"telnet {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62:8080 "
                              f"> /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | "
                              f"telnet {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | "
                              f"telnet {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74 "
                              f"> /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62",
                          commands=[
                              f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 -c csle_ctf1234 > "
                              f"/dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 > /dev/null 2>&1",
                              f"timeout 5 psql -h "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 -p 5432 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74 "
                              f"> /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62:8080 "
                              f"> /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62",
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}6.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.62:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.62 > /dev/null "
                              f"2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.62"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.62"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.12 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.12 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.13 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.13 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.14 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.14 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.11 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.11 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.13 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.13 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.14 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.14 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.11 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.11 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.12 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.12 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.14 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.14 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.11 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.11 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.12 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.12 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.13 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.13 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.16 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.16 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.17 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.17 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.18 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.18 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.15 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.15 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.17 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.17 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.18 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.18 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.15 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.15 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.16 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.16 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.18 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.18 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.15 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.15 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.16 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.16 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.17 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.17 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19"],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19"]
                          )
    ]
    traffic_conf = TrafficConfig(node_traffic_configs=traffic_generators)
    return traffic_conf


def default_users_config(network_id: int) -> UsersConfig:
    """
    :param network_id: the network id
    :return: generates the UsersConfig
    """
    users = [
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191", users=[
            ("agent", "agent", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21", users=[
            ("admin", "admin31151x", True),
            ("test", "qwerty", True),
            ("oracle", "abc123", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10", users=[
            ("admin", "admin1235912", True),
            ("jessica", "water", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2", users=[
            ("admin", "test32121", False),
            ("user1", "123123", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3", users=[
            ("john", "doe", True),
            ("vagrant", "test_pw1", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54", users=[
            ("trent", "xe125@41!341", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101", users=[
            ("zidane", "1b12ha9", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7", users=[
            ("zlatan", "pi12195e", True),
            ("kennedy", "eul1145x", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4", users=[
            ("user1", "1235121", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5", users=[
            ("user2", "1235121", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6", users=[
            ("user3", "1bsae235121", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8", users=[
            ("user4", "1bsae235121", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9", users=[
            ("user5", "1gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178", users=[
            ("user6", "1gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11", users=[
            ("user7", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12", users=[
            ("user8", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13", users=[
            ("user9", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14", users=[
            ("user10", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15", users=[
            ("user11", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16", users=[
            ("user12", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17", users=[
            ("user13", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18", users=[
            ("user14", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19", users=[
            ("user15", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20", users=[
            ("user16", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22", users=[
            ("user18", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23", users=[
            ("user19", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24", users=[
            ("user20", "081gxq2", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25", users=[
            ("user20", "081gxq2", True)
        ])
    ]
    users_conf = UsersConfig(users=users)
    return users_conf


def default_vulns_config(network_id : int) -> VulnerabilitiesConfig:
    """
    :param network_id: the network id
    :return: the vulnerability config
    """
    vulns = [
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              vuln_type=VulnType.WEAK_PW, username="l_hopital", pw="l_hopital",
                              root=True),
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              vuln_type=VulnType.WEAK_PW, username="euler", pw="euler",
                              root=False),
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              vuln_type=VulnType.WEAK_PW, username="pi", pw="pi",
                              root=True),
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              vuln_type=VulnType.WEAK_PW, username="puppet", pw="puppet",
                              root=True),
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              vuln_type=VulnType.WEAK_PW, username="admin", pw="admin",
                              root=True),
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54",
                              vuln_type=VulnType.WEAK_PW, username="vagrant", pw="vagrant",
                              root=True),
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74",
                              vuln_type=VulnType.WEAK_PW, username="administrator", pw="administrator",
                              root=True),
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
                              vuln_type=VulnType.WEAK_PW, username="adm",
                              pw="adm", root=True),
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62",
                              vuln_type=VulnType.WEAK_PW, username="guest", pw="guest", root=True),
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7",
                              vuln_type=VulnType.WEAK_PW, username="ec2-user", pw="ec2-user",
                              root=True)
    ]
    vulns_config = VulnerabilitiesConfig(vulnerabilities=vulns)
    return vulns_config

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--run", help="Boolean parameter, if true, run containers",
                        action="store_true")
    parser.add_argument("-s", "--stop", help="Boolean parameter, if true, stop containers",
                        action="store_true")
    parser.add_argument("-c", "--clean", help="Boolean parameter, if true, remove containers",
                        action="store_true")
    parser.add_argument("-a", "--apply", help="Boolean parameter, if true, apply config",
                        action="store_true")
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
                        action="store_true")
    args = parser.parse_args()
    if not os.path.exists(util.default_emulation_config_path()):
        config = default_config(name="csle-ctf-level6-001", network_id=6, level=6, version="0.0.1")
        EnvConfigGenerator.materialize_emulation_env_config(emulation_env_config=config)
    config = util.read_emulation_env_config(util.default_emulation_config_path())

    if args.install:
        EnvConfigGenerator.install_emulation(config=config)
    if args.uninstall:
        EnvConfigGenerator.uninstall_emulation(config=config)
    if args.run:
        EnvConfigGenerator.run_containers(emulation_env_config=config)
    if args.stop:
        EnvConfigGenerator.stop_containers(emulation_env_config=config)
    if args.clean:
        EnvConfigGenerator.stop_containers(emulation_env_config=config)
        EnvConfigGenerator.rm_containers(emulation_env_config=config)
        EnvConfigGenerator.delete_networks_of_emulation_env_config(emulation_env_config=config)
    if args.apply:
        EnvConfigGenerator.apply_emulation_env_config(emulation_env_config=config)