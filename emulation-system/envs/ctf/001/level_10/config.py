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
from csle_common.dao.container_config.rce_vulnerability_config import RceVulnerabilityConfig
from csle_common.dao.container_config.sql_injection_vulnerability_config import SQLInjectionVulnerabilityConfig
from csle_common.dao.container_config.priv_esc_vulnerability_config import PrivEscVulnerabilityConfig
from csle_common.util.experiments_util import util


def default_config(name: str, network_id: int = 10, level: int = 10, version: str = "0.0.1") -> EmulationEnvConfig:
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
                                 ))
                            ],
                            minigame=constants.CSLE.CTF_MINIGAME,
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.SAMBA_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
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
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.SHELLSHOCK_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
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
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.SQL_INJECTION_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
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
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.CVE_2015_3306_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
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
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.CVE_2015_1427_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
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
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.CVE_2016_10033_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
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
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.CVE_2010_0426_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
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
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.CVE_2015_5602_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
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
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.PENGINE_EXPLOIT_1}",
                            ips_and_networks = [
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104",
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
                            suffix="_1")
    ]
    containers_cfg = ContainersConfig(
        containers=containers,
        agent_ip=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}.1.191",
        router_ip=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}.2.10",
        ids_enabled=True,
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
            )
        ])
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
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}3", f"/{constants.COMMANDS.TMP_DIR}/", 3,
                            False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                        flags=[(
                            f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}2"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}2", f"/{constants.COMMANDS.TMP_DIR}/", 2,
                            False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                        flags=[(
                            f"/{constants.COMMANDS.ROOT_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}1"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}1", f"/{constants.COMMANDS.ROOT_DIR}/", 1,
                            True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                        flags=[(
                            f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}4"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}4", f"/{constants.COMMANDS.TMP_DIR}/", 4,
                            False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                        flags=[(
                            f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}5"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}5", f"/{constants.COMMANDS.TMP_DIR}/", 5,
                            False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                        flags=[(
                            f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}6"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}6", f"/{constants.COMMANDS.TMP_DIR}/", 6,
                            False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                        flags=[(
                            f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}7"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}7", f"/{constants.COMMANDS.TMP_DIR}/", 7,
                            False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                        flags=[(
                            f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}8"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}8", f"/{constants.COMMANDS.TMP_DIR}/", 8,
                            False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                        flags=[(
                            f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}9"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}9",
                            f"/{constants.COMMANDS.TMP_DIR}/", 9, False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                        flags=[(
                            f"/{constants.COMMANDS.ROOT_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}10"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}10", f"/{constants.COMMANDS.ROOT_DIR}/", 10,
                            True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                        flags=[(
                            f"/{constants.COMMANDS.ROOT_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}11"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}11", f"/{constants.COMMANDS.ROOT_DIR}/", 11,
                            True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104",
                        flags=[(
                            f"/{constants.COMMANDS.ROOT_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}12"
                            f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            f"{constants.COMMON.FLAG_FILENAME_PREFIX}12", f"/{constants.COMMANDS.ROOT_DIR}/", 12,
                            True, 1)])
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
                 ))]),
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
                           f"{constants.CONTAINER_IMAGES.ROUTER_1}_1-{constants.CSLE.LEVEL}{level}",
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
                 ))]),
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
                           f"{constants.CONTAINER_IMAGES.SAMBA_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
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
                           f"{constants.CONTAINER_IMAGES.SHELLSHOCK_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
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
                           f"{constants.CONTAINER_IMAGES.SQL_INJECTION_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
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
                           f"{constants.CONTAINER_IMAGES.CVE_2015_3306_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
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
                           f"{constants.CONTAINER_IMAGES.CVE_2015_1427_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
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
                           f"{constants.CONTAINER_IMAGES.CVE_2016_10033_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
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
                           f"{constants.CONTAINER_IMAGES.CVE_2010_0426_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
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
                           f"{constants.CONTAINER_IMAGES.CVE_2015_5602_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
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
                           f"{constants.CONTAINER_IMAGES.PENGINE_EXPLOIT_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104",
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
        hostname=f"{constants.CONTAINER_IMAGES.ROUTER_1}_1",
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

    node_8 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.SAMBA_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
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
    node_9 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.SHELLSHOCK_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
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
    node_10 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.SQL_INJECTION_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
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
    node_11 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.CVE_2015_3306_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
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
    node_12 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.CVE_2015_1427_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
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
    node_13 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.CVE_2016_10033_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
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
        hostname=f"{constants.CONTAINER_IMAGES.CVE_2010_0426_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
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
        hostname=f"{constants.CONTAINER_IMAGES.CVE_2015_5602_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
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
        hostname=f"{constants.CONTAINER_IMAGES.PENGINE_EXPLOIT_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104",
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
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11, node_12,
                    node_13, node_14, node_15, node_16]
    topology = Topology(node_configs=node_configs,
                        subnetwork_masks=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}"
                        ])
    return topology


def default_traffic_config(network_id: int) -> TrafficConfig:
    """
    :param network_id: the network id
    :return: the traffic configuration
    """
    traffic_generators = [
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.254",
            commands=[
                # f"timeout 120 sudo nmap -sS -p- --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sP --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sU -p- --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sT -p- --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sF -p- --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sN -p- --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sX -p- --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -O --osscan-guess --max-os-tries 1 --min-rate 100000
                # --max-retries 1 -T5 -n {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap --script=http-grep --min-rate 100000 --max-retries 1 -T5 -n
                # {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sv -sC --script=finger --min-rate 100000 --max-retries 1 -T5
                # -n {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1 > "
                f"/dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1 > "
                f"/dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > "
                f"/dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 "
                f"> /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191", commands=[],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
                          ],
                          target_hosts=[]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
            commands=
            [
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -c csle_ctf1234 "
                f"> /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > "
                f"/dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p 5432 > /dev/null "
                f"2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 -c csle_ctf1234 "
                f"> /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42/login.php > /dev/null "
                f"2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ], jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ], target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -c csle_ctf1234 > "
                f"/dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null "
                f"2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p 5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 -c csle_ctf1234 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null "
                f"2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -c csle_ctf1234 > "
                f"/dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null "
                f"2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p 5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 -c csle_ctf1234 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null "
                f"2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > "
                f"/dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 "
                f"> /dev/null 2>&1"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11"
            ])
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
            ("admin", "test32121", True),
            ("user1", "123123", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3", users=[
            ("john", "doe", True),
            ("vagrant", "test_pw1", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19", users=[
            ("karl", "gustaf", True),
            ("steven", "carragher", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31", users=[
            ("stefan", "zweig", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42", users=[
            ("roy", "neruda", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37", users=[
            ("john", "conway", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82", users=[
            ("john", "nash", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75", users=[
            ("larry", "samuelson", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71", users=[
            ("robbins", "monro", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11", users=[
            ("rich", "sutton", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104", users=[
            ("abraham", "wald", True)
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
                              root=False),
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              vuln_type=VulnType.WEAK_PW, username="admin", pw="admin",
                              root=True),
        RceVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                               vuln_type=VulnType.RCE),
        RceVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                               vuln_type=VulnType.RCE),
        SQLInjectionVulnerabilityConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
            vuln_type=VulnType.SQL_INJECTION,
            username="pablo", pw="0d107d09f5bbe40cade3de5c71e9e9b7", root=True),
        RceVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                               vuln_type=VulnType.RCE),
        RceVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                               vuln_type=VulnType.RCE),
        RceVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                               vuln_type=VulnType.RCE),
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                              vuln_type=VulnType.WEAK_PW, username="alan", pw="alan", root=False),
        PrivEscVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                                   vuln_type=VulnType.PRIVILEGE_ESCALATION,
                                   username="alan", pw="alan", root=False, cve="2010-1427"),
        PwVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                              vuln_type=VulnType.WEAK_PW, username="donald", pw="donald",
                              root=False),
        PrivEscVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                                   vuln_type=VulnType.PRIVILEGE_ESCALATION,
                                   username="donald", pw="donald", root=False, cve="2015-5602"),
        RceVulnerabilityConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104",
                               vuln_type=VulnType.RCE)
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
        config = default_config(name="csle-ctf-level10-001", network_id=10, level=10, version="0.0.1")
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
    if args.apply:
        EnvConfigGenerator.apply_emulation_env_config(emulation_env_config=config)