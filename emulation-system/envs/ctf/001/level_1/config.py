import argparse
import os
import multiprocessing
import csle_common.constants.constants as constants
import csle_collector.constants.constants as collector_constants
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
from csle_common.dao.container_config.node_vulnerability_config import NodeVulnerabilityConfig
from csle_common.dao.network.credential import Credential
from csle_common.dao.container_config.vulnerability_type import VulnType
from csle_common.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.container_config.emulation_env_config import EmulationEnvConfig
from csle_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from csle_common.dao.container_config.client_population_config import ClientPopulationConfig
from csle_common.dao.container_config.client_population_process_type import ClientPopulationProcessType
from csle_common.dao.container_config.log_sink_config import LogSinkConfig
from csle_common.dao.container_config.kafka_topic import KafkaTopic
from csle_common.util.experiments_util import util
from csle_common.dao.network.flag import Flag
from csle_common.dao.network.transport_protocol import TransportProtocol


def default_config(name: str, network_id: int = 1, level: int = 1, version: str = "0.0.1") -> EmulationEnvConfig:
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
    log_sink_cfg = default_log_sink_config(network_id=network_id, level=level, version=version)
    emulation_env_cfg = EmulationEnvConfig(
        name=name, containers_config=containers_cfg, users_config=users_cfg, flags_config=flags_cfg,
        vuln_config=vuln_cfg, topology_config=topology_cfg, traffic_config=traffic_cfg, resources_config=resources_cfg,
        log_sink_config=log_sink_cfg
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
        NodeContainerConfig(
            name=f"{constants.CONTAINER_IMAGES.CLIENT_1}",
            ips_and_networks=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.254",
                 ContainerNetwork(
                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                 f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                 )),
            ],
            minigame=constants.CSLE.CTF_MINIGAME,
            version=version, level=str(level), restart_policy=constants.DOCKER.ON_FAILURE_3, suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.FTP_1}",
                            ips_and_networks=[
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
                            ips_and_networks=[
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
                            ips_and_networks=[
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
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.ROUTER_1}",
                            ips_and_networks=[
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
                            ips_and_networks=[
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
                            ips_and_networks=[
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
                            suffix="_1")
    ]
    containers_cfg = ContainersConfig(
        containers=containers,
        agent_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
        router_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
        ids_enabled=False, vulnerable_nodes=[
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3"
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
            )
        ]
    )
    return containers_cfg


def default_log_sink_config(network_id: int, level: int, version: str) -> LogSinkConfig:
    """
    Generates the default log sink configuration
    :param network_id: the id of the emulation network
    :param level: the level of the emulation
    :param version: the version of the emulation
    :return: the log sink configuration
    """
    container = NodeContainerConfig(
        name=f"{constants.CONTAINER_IMAGES.KAFKA_1}",
        ips_and_networks=[
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{collector_constants.LOG_SINK.NETWORK_ID_THIRD_OCTET}.{collector_constants.LOG_SINK.NETWORK_ID_FOURTH_OCTET}",
             ContainerNetwork(
                 name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_{collector_constants.LOG_SINK.NETWORK_ID_THIRD_OCTET}",
                 subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                             f"{network_id}.{collector_constants.LOG_SINK.NETWORK_ID_THIRD_OCTET}"
                             f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                 subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
             )),
        ],
        minigame=constants.CSLE.CTF_MINIGAME,
        version=version, level=str(level),
        restart_policy=constants.DOCKER.ON_FAILURE_3, suffix=collector_constants.LOG_SINK.SUFFIX)

    resources = NodeResourcesConfig(
        container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                       f"{constants.CONTAINER_IMAGES.KAFKA_1}_1-{constants.CSLE.LEVEL}{level}",
        num_cpus=1, available_memory_gb=4,
        ips_and_network_configs=[
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{collector_constants.LOG_SINK.NETWORK_ID_THIRD_OCTET}.{collector_constants.LOG_SINK.NETWORK_ID_FOURTH_OCTET}",
             None)])

    topics = [
        KafkaTopic(
            name=collector_constants.LOG_SINK.CLIENT_POPULATION_TOPIC_NAME,
            num_replicas=1,
            num_partitions=1,
            attributes=collector_constants.LOG_SINK.CLIENT_POPULATION_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.LOG_SINK.IDS_LOG_TOPIC_NAME,
            num_replicas=1,
            num_partitions=1,
            attributes=collector_constants.LOG_SINK.IDS_LOG_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.LOG_SINK.HOST_METRICS_TOPIC_NAME,
            num_replicas=1,
            num_partitions=1,
            attributes=collector_constants.LOG_SINK.HOST_METRICS_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.LOG_SINK.DOCKER_STATS_TOPIC_NAME,
            num_replicas=1,
            num_partitions=1,
            attributes=collector_constants.LOG_SINK.DOCKER_STATS_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.LOG_SINK.ATTACKER_ACTIONS_TOPIC_NAME,
            num_replicas=1,
            num_partitions=1,
            attributes=collector_constants.LOG_SINK.ATTACKER_ACTIONS_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.LOG_SINK.DEFENDER_ACTIONS_TOPIC_NAME,
            num_replicas=1,
            num_partitions=1,
            attributes=collector_constants.LOG_SINK.DEFENDER_ACTIONS_ATTRIBUTES
        )
    ]

    config = LogSinkConfig(container=container, resources=resources, topics=topics,
                           version=version, kafka_port=9092, default_grpc_port=50051,
                           secondary_grpc_port=50049, time_step_len_seconds=15)
    return config


def default_flags_config(network_id: int) -> FlagsConfig:
    """
    :param network_id: the network id
    :return: The flags confguration
    """
    flags = [
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                        flags=[
                            Flag(
                                name=f"{constants.COMMON.FLAG_FILENAME_PREFIX}3",
                                path=f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}3"
                                     f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                                dir=f"/{constants.COMMANDS.TMP_DIR}/",
                                id=3, requires_root=True, score=1
                            )]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                        flags=[
                            Flag(
                                name=f"{constants.COMMON.FLAG_FILENAME_PREFIX}2",
                                path=f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}2"
                                     f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                                dir=f"/{constants.COMMANDS.TMP_DIR}/",
                                id=2, requires_root=True, score=1
                            )]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                        flags=[
                            Flag(
                                name=f"{constants.COMMON.FLAG_FILENAME_PREFIX}1",
                                path=f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}1"
                                     f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                                dir=f"/{constants.COMMANDS.TMP_DIR}/",
                                id=1, requires_root=True, score=1
                            )])
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
            num_cpus=min(16, multiprocessing.cpu_count()), available_memory_gb=4,
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
                     rate_limit_mbit=10000, packet_overhead_bytes=0,
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
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7]
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
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.HONEYPOT_1]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS])
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.ROUTER_1]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS])
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.SSH_1]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS])
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.TELNET_1]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS])
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.FTP_1]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS])
                          )
    ]
    client_population_config = ClientPopulationConfig(
        networks=[ContainerNetwork(
            name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
            subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                        f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
            subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
        )],
        ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.254",
        client_process_type=ClientPopulationProcessType.POISSON,
        lamb=0.025, mu=1, client_manager_port=50051, num_commands=2, client_time_step_len_seconds=15
    )
    traffic_conf = TrafficConfig(node_traffic_configs=traffic_generators,
                                 client_population_config=client_population_config)
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
        ])
    ]
    users_conf = UsersConfig(users=users)
    return users_conf


def default_vulns_config(network_id: int) -> VulnerabilitiesConfig:
    """
    :param network_id: the network id
    :return: the vulnerability config
    """
    vulns = [
        NodeVulnerabilityConfig(
            name=constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS,
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
            vuln_type=VulnType.WEAK_PW,
            credentials=[Credential(username="l_hopital", pw="l_hopital", root=True,
                                    service=constants.FTP.SERVICE_NAME,
                                    protocol=TransportProtocol.TCP,
                                    port=constants.FTP.DEFAULT_PORT),
                         Credential(username="euler", pw="euler", root=False,
                                    service=constants.FTP.SERVICE_NAME,
                                    protocol=TransportProtocol.TCP,
                                    port=constants.FTP.DEFAULT_PORT),
                         Credential(username="pi", pw="pi", root=True,
                                    service=constants.FTP.SERVICE_NAME,
                                    protocol=TransportProtocol.TCP,
                                    port=constants.FTP.DEFAULT_PORT)],
            cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
            cve=None,
            root=True, port=constants.FTP.DEFAULT_PORT,
            protocol=TransportProtocol.TCP, service=constants.FTP.SERVICE_NAME),
        NodeVulnerabilityConfig(
            name=constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS,
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
            vuln_type=VulnType.WEAK_PW,
            credentials=[Credential(username="puppet", pw="puppet", root=False,
                                    service=constants.SSH.SERVICE_NAME,
                                    protocol=TransportProtocol.TCP,
                                    port=constants.SSH.DEFAULT_PORT)],
            cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
            cve=None,
            root=True, port=constants.SSH.DEFAULT_PORT, protocol=TransportProtocol.TCP, 
            service=constants.SSH.SERVICE_NAME),
        NodeVulnerabilityConfig(
            name=constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS,
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
            vuln_type=VulnType.WEAK_PW,
            credentials=[Credential(username="admin", pw="admin", root=True,
                                    service=constants.TELNET.SERVICE_NAME,
                                    protocol=TransportProtocol.TCP,
                                    port=constants.TELNET.DEFAULT_PORT)],
            cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
            cve=None,
            root=True, port=constants.TELNET.DEFAULT_PORT, protocol=TransportProtocol.TCP,
            service=constants.TELNET.SERVICE_NAME)
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
        config = default_config(name="csle-ctf-level1-001", network_id=1, level=1, version="0.0.1")
        util.write_emulation_config_file(config, util.default_emulation_config_path())
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
