from typing import Dict, List, Union
import argparse
import os
import multiprocessing
import csle_common.constants.constants as constants
import csle_collector.constants.constants as collector_constants
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.client import Client
import csle_ryu.constants.constants as ryu_constants
from csle_common.dao.emulation_config.topology_config import TopologyConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.flags_config import FlagsConfig
from csle_common.dao.emulation_config.node_flags_config import NodeFlagsConfig
from csle_common.dao.emulation_config.resources_config import ResourcesConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.packet_loss_type import PacketLossType
from csle_common.dao.emulation_config.packet_delay_distribution_type import PacketDelayDistributionType
from csle_common.dao.emulation_config.traffic_config import TrafficConfig
from csle_common.dao.emulation_config.node_traffic_config import NodeTrafficConfig
from csle_common.dao.emulation_config.users_config import UsersConfig
from csle_common.dao.emulation_config.node_users_config import NodeUsersConfig
from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.controllers.emulation_env_controller import EmulationEnvController
from csle_common.dao.emulation_config.client_population_config import ClientPopulationConfig
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.dao.emulation_config.flag import Flag
from csle_common.dao.emulation_config.node_vulnerability_config import NodeVulnerabilityConfig
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_config.vulnerability_type import VulnType
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.node_services_config import NodeServicesConfig
from csle_common.dao.emulation_config.services_config import ServicesConfig
from csle_common.dao.emulation_config.network_service import NetworkService
from csle_common.dao.emulation_config.ovs_config import OVSConfig
from csle_common.dao.emulation_config.ovs_switch_config import OvsSwitchConfig
from csle_common.dao.emulation_config.sdn_controller_config import SDNControllerConfig
from csle_common.dao.emulation_config.sdn_controller_type import SDNControllerType
from csle_common.dao.emulation_config.user import User
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_config.host_manager_config import HostManagerConfig
from csle_common.dao.emulation_config.snort_ids_manager_config import SnortIDSManagerConfig
from csle_common.dao.emulation_config.ossec_ids_manager_config import OSSECIDSManagerConfig
from csle_common.dao.emulation_config.docker_stats_manager_config import DockerStatsManagerConfig
from csle_common.dao.emulation_config.elk_config import ElkConfig
from csle_common.dao.emulation_config.beats_config import BeatsConfig
from csle_common.dao.emulation_config.node_beats_config import NodeBeatsConfig


def default_config(name: str, network_id: int = 12, level: int = 12, version: str = "0.5.0",
                   time_step_len_seconds: int = 30) -> EmulationEnvConfig:
    """
    Returns the default configuration of the emulation environment

    :param name: the name of the emulation
    :param network_id: the network id of the emulation
    :param level: the level of the emulation
    :param version: the version of the emulation
    :param time_step_len_seconds: default length of a time-step in the emulation
    :return: the emulation environment configuration
    """
    containers_cfg = default_containers_config(network_id=network_id, level=level, version=version)
    flags_cfg = default_flags_config(network_id=network_id)
    resources_cfg = default_resource_constraints_config(network_id=network_id, level=level)
    topology_cfg = default_topology_config(network_id=network_id)
    traffic_cfg = default_traffic_config(network_id=network_id)
    users_cfg = default_users_config(network_id=network_id)
    vuln_cfg = default_vulns_config(network_id=network_id)
    kafka_cfg = default_kafka_config(network_id=network_id, level=level, version=version,
                                     time_step_len_seconds=time_step_len_seconds)
    services_cfg = default_services_config(network_id=network_id)
    descr = "An emulation environment with a set of nodes that run common networked services " \
            "such as SSH, FTP, Telnet, IRC, Kafka," \
            " etc. Some of the services are vulnerable to simple dictionary attacks as " \
            "they use weak passwords." \
            "The task of an attacker agent is to identify the vulnerabilities and exploit them and " \
            "discover hidden flags" \
            "on the nodes. Conversely, the task of the defender is to harden the defense of the nodes " \
            "and to detect the attacker."
    static_attackers_cfg = default_static_attacker_sequences(topology_cfg.subnetwork_masks)
    ovs_cfg = default_ovs_config(network_id=network_id, level=level, version=version)
    sdn_controller_cfg = default_sdn_controller_config(network_id=network_id, level=level, version=version,
                                                       time_step_len_seconds=time_step_len_seconds)
    host_manager_cfg = default_host_manager_config(network_id=network_id, level=level, version=version,
                                                   time_step_len_seconds=time_step_len_seconds)
    snort_ids_manager_cfg = default_snort_ids_manager_config(network_id=network_id, level=level, version=version,
                                                             time_step_len_seconds=time_step_len_seconds)
    ossec_ids_manager_cfg = default_ossec_ids_manager_config(network_id=network_id, level=level, version=version,
                                                             time_step_len_seconds=time_step_len_seconds)
    docker_stats_manager_cfg = default_docker_stats_manager_config(network_id=network_id, level=level, version=version,
                                                                   time_step_len_seconds=time_step_len_seconds)
    elk_cfg = default_elk_config(network_id=network_id, level=level, version=version,
                                 time_step_len_seconds=time_step_len_seconds)
    beats_cfg = default_beats_config(network_id=network_id)
    emulation_env_cfg = EmulationEnvConfig(
        name=name, containers_config=containers_cfg, users_config=users_cfg, flags_config=flags_cfg,
        vuln_config=vuln_cfg, topology_config=topology_cfg, traffic_config=traffic_cfg, resources_config=resources_cfg,
        kafka_config=kafka_cfg, services_config=services_cfg,
        descr=descr, static_attacker_sequences=static_attackers_cfg, ovs_config=ovs_cfg,
        sdn_controller_config=sdn_controller_cfg, host_manager_config=host_manager_cfg,
        snort_ids_manager_config=snort_ids_manager_cfg, ossec_ids_manager_config=ossec_ids_manager_cfg,
        docker_stats_manager_config=docker_stats_manager_cfg, elk_config=elk_cfg,
        level=level, execution_id=-1, version=version, beats_config=beats_cfg
    )
    return emulation_env_cfg


def default_containers_config(network_id: int, level: int, version: str) -> ContainersConfig:
    """
    Generates default containers config

    :param version: the version of the containers to use
    :param level: the level parameter of the emulation
    :param network_id: the network id
    :return: the ContainersConfig of the emulation
    """
    containers = [
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.HACKER_KALI_1}",
                            os=constants.CONTAINER_OS.HACKER_KALI_1_OS,
                            ips_and_networks=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                                 f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.191",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH0,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.191",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                                          f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}."
                                                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                                 f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH2,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 ))
                            ],
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(
            name=f"{constants.CONTAINER_IMAGES.CLIENT_1}",
            os=constants.CONTAINER_OS.CLIENT_1_OS,
            ips_and_networks=[
                (
                    f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                    f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.254",
                    ContainerNetwork(
                        name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                        subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                    f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                        subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                        interface=constants.NETWORKING.ETH0,
                        bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                    )),
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.254",
                 ContainerNetwork(
                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                          f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                 f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                 f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                     interface=constants.NETWORKING.ETH2,
                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                 ))
            ],
            version=version, level=str(level), restart_policy=constants.DOCKER.ON_FAILURE_3, suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.ROUTER_2}",
                            os=constants.CONTAINER_OS.ROUTER_2_OS,
                            ips_and_networks=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH0,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (
                                    f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                                    f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                                    ContainerNetwork(
                                        name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                                        subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                    f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                        subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                        interface=constants.NETWORKING.ETH2,
                                        bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                    )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.10",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                                          f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}."
                                                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                                 f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH3,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 ))
                            ],
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.OVS_1}",
                            os=constants.CONTAINER_OS.OVS_1_OS,
                            ips_and_networks=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.78",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH0,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.78",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH2,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.78",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH3,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                                 f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                                          f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_2",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78"
                                                 f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                                   f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78",
                                     interface=constants.NETWORKING.ETH4,
                                     bitmask=ryu_constants.RYU.BITMASK
                                 ))
                            ],
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.OVS_1}",
                            os=constants.CONTAINER_OS.OVS_1_OS,
                            ips_and_networks=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.3",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH0,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH2,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                                 f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.10",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                                          f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_3",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.10"
                                                 f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                                   f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.10",
                                     interface=constants.NETWORKING.ETH3,
                                     bitmask=ryu_constants.RYU.BITMASK
                                 ))
                            ],
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_2"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.OVS_1}",
                            os=constants.CONTAINER_OS.OVS_1_OS,
                            ips_and_networks=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.31",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH0,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH2,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                                 f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                                          f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_4",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18"
                                                 f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                                   f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18",
                                     interface=constants.NETWORKING.ETH3,
                                     bitmask=ryu_constants.RYU.BITMASK
                                 ))
                            ],
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_3"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.SSH_1}",
                            os=constants.CONTAINER_OS.SSH_1_OS,
                            ips_and_networks=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.5",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH0,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.5",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                                          f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}."
                                                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                                 f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH2,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 ))
                            ],
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.TELNET_1}",
                            os=constants.CONTAINER_OS.TELNET_1_OS,
                            ips_and_networks=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.8",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH0,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.8",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                                          f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}."
                                                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                                 f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH2,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 ))
                            ],
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.SSH_1}",
                            os=constants.CONTAINER_OS.SSH_1_OS,
                            ips_and_networks=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.41",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH0,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.41",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                                          f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}."
                                                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                                 f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH2,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 ))
                            ],
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_2"),
        NodeContainerConfig(name=f"{constants.CONTAINER_IMAGES.FTP_1}",
                            os=constants.CONTAINER_OS.FTP_1_OS,
                            ips_and_networks=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.42",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}.6"
                                                 f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH0,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.42",
                                 ContainerNetwork(
                                     name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                                          f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                                     subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                                 f"{network_id}."
                                                 f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                                 f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                                     subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                                     interface=constants.NETWORKING.ETH2,
                                     bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                                 ))
                            ],
                            version=version, level=str(level),
                            restart_policy=constants.DOCKER.ON_FAILURE_3,
                            suffix="_1")
    ]
    containers_cfg = ContainersConfig(
        containers=containers,
        agent_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                 f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.191",
        router_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
        ids_enabled=False, vulnerable_nodes=[
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.5",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.8",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.41",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.42"
        ],
        agent_reachable_nodes=[
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.78",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.3",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.5",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.8",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.31",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.41",
            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.42"
        ],
        networks=[
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                bitmask=constants.CSLE.CSLE_EDGE_BITMASK
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                bitmask=constants.CSLE.CSLE_EDGE_BITMASK
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                bitmask=constants.CSLE.CSLE_EDGE_BITMASK
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                bitmask=constants.CSLE.CSLE_EDGE_BITMASK
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                bitmask=constants.CSLE.CSLE_EDGE_BITMASK
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                bitmask=constants.CSLE.CSLE_EDGE_BITMASK
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                     f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                            f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                bitmask=constants.CSLE.CSLE_EDGE_BITMASK
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                     f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_2",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78"
                            f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                              f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78",
                bitmask=ryu_constants.RYU.BITMASK
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                     f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_3",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.10"
                            f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                              f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.10",
                bitmask=ryu_constants.RYU.BITMASK
            ),
            ContainerNetwork(
                name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                     f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_4",
                subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                            f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18"
                            f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                              f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18",
                bitmask=ryu_constants.RYU.BITMASK
            )
        ]
    )
    return containers_cfg


def default_flags_config(network_id: int) -> FlagsConfig:
    """
    Generates default flags config

    :param network_id: the network id
    :return: The flags confguration
    """
    flags = [
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.5",
                        flags=[Flag(
                            name=f"{constants.COMMON.FLAG_FILENAME_PREFIX}1",
                            path=f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}1"
                                 f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            dir=f"/{constants.COMMANDS.TMP_DIR}/",
                            id=1, requires_root=True, score=1
                        )]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.8",
                        flags=[Flag(
                            name=f"{constants.COMMON.FLAG_FILENAME_PREFIX}2",
                            path=f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}2"
                                 f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            dir=f"/{constants.COMMANDS.TMP_DIR}/",
                            id=2, requires_root=True, score=1
                        )]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.41",
                        flags=[Flag(
                            name=f"{constants.COMMON.FLAG_FILENAME_PREFIX}3",
                            path=f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}3"
                                 f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            dir=f"/{constants.COMMANDS.TMP_DIR}/",
                            id=3, requires_root=True, score=1
                        )]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.42",
                        flags=[Flag(
                            name=f"{constants.COMMON.FLAG_FILENAME_PREFIX}4",
                            path=f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}4"
                                 f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                            dir=f"/{constants.COMMANDS.TMP_DIR}/",
                            id=4, requires_root=True, score=1
                        )])
    ]
    flags_config = FlagsConfig(node_flag_configs=flags)
    return flags_config


def default_resource_constraints_config(network_id: int, level: int) -> ResourcesConfig:
    """
    Generates default resource constraints config

    :param level: the level parameter of the emulation
    :param network_id: the network id
    :return: generates the ResourcesConfig
    """
    node_resources_configurations = [
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-"
                           f"{constants.CONTAINER_IMAGES.HACKER_KALI_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                 f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.191",
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
            container_name=f"{constants.CSLE.NAME}-"
                           f"{constants.CONTAINER_IMAGES.CLIENT_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=min(16, multiprocessing.cpu_count()), available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                 f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.254",
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
            container_name=f"{constants.CSLE.NAME}-"
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
                (
                    f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                    f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                    NodeNetworkConfig(
                        interface=constants.NETWORKING.ETH2,
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
            container_name=f"{constants.CSLE.NAME}-"
                           f"{constants.CONTAINER_IMAGES.OVS_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.78",
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
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.78",
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
                 )),
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.78",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH3,
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
            container_name=f"{constants.CSLE.NAME}-"
                           f"{constants.CONTAINER_IMAGES.OVS_1}_2-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.3",
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
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-"
                           f"{constants.CONTAINER_IMAGES.OVS_1}_3-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.31",
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
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
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
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-"
                           f"{constants.CONTAINER_IMAGES.SSH_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.5",
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
                 ))
            ]),

        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-"
                           f"{constants.CONTAINER_IMAGES.TELNET_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.8",
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
                 ))
            ]),

        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-"
                           f"{constants.CONTAINER_IMAGES.FTP_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.42",
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
                 ))
            ]),

        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-"
                           f"{constants.CONTAINER_IMAGES.SSH_1}_2-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.41",
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
                 ))
            ])
    ]
    resources_config = ResourcesConfig(node_resources_configurations=node_resources_configurations)
    return resources_config


def default_topology_config(network_id: int) -> TopologyConfig:
    """
    Generates default topology config

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
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    interface=constants.NETWORKING.ETH0,
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    interface=constants.NETWORKING.ETH2,
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.78",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.78",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.78",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.78",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.10",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set([]),
        output_drop=set(), input_drop=set(), forward_drop=set(), routes=set())
    node_2 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.HACKER_KALI_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.191",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.191",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_3 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.CLIENT_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.254",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.10",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.254",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
        routes=set())
    node_4 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.OVS_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.78",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78"
                                f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                  f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78",
                    bitmask=ryu_constants.RYU.BITMASK
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
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.78",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.78",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.3",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.31",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.3",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set()
    )
    node_5 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.OVS_1}_2",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.3",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
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
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.78",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.78",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.78",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.78",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.10",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.9"
                                f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                  f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.9",
                    bitmask=ryu_constants.RYU.BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.14",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set()
    )
    node_6 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.OVS_1}_3",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.31",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.78",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.78",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.78",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.78",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                   f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18"
                                f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                  f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18",
                    bitmask=ryu_constants.RYU.BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.22",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set()
    )
    node_7 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.SSH_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.5",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.5",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set()
    )
    node_8 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.TELNET_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.8",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.8",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set()
    )
    node_9 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.SSH_1}_2",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.41",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.41",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set()
    )
    node_10 = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.FTP_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.42",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_6",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.6{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.42",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_1",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.1{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.3{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.4{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.31",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.DROP,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_5",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.5{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set()
    )
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10]
    topology = TopologyConfig(node_configs=node_configs,
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
                                  f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                  f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}"
                              ])
    return topology


def default_traffic_config(network_id: int, time_step_len_seconds: int = 15) -> TrafficConfig:
    """
    Generates default traffic config

    :param network_id: the network id
    :param time_step_len_seconds: default length of a time-step in the emulation
    :return: the traffic configuration
    """
    traffic_generators = [
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.ROUTER_2]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS]),
                          traffic_manager_port=collector_constants.MANAGER_PORTS.TRAFFIC_MANAGER_DEFAULT_PORT,
                          traffic_manager_log_file=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_FILE,
                          traffic_manager_log_dir=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_DIR,
                          traffic_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.5",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.SSH_1]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS]),
                          traffic_manager_port=collector_constants.MANAGER_PORTS.TRAFFIC_MANAGER_DEFAULT_PORT,
                          traffic_manager_log_file=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_FILE,
                          traffic_manager_log_dir=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_DIR,
                          traffic_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.8",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.TELNET_1]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS]),
                          traffic_manager_port=collector_constants.MANAGER_PORTS.TRAFFIC_MANAGER_DEFAULT_PORT,
                          traffic_manager_log_file=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_FILE,
                          traffic_manager_log_dir=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_DIR,
                          traffic_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.41",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.SSH_1]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS]),
                          traffic_manager_port=collector_constants.MANAGER_PORTS.TRAFFIC_MANAGER_DEFAULT_PORT,
                          traffic_manager_log_file=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_FILE,
                          traffic_manager_log_dir=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_DIR,
                          traffic_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.42",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.FTP_1]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS]),
                          traffic_manager_port=collector_constants.MANAGER_PORTS.TRAFFIC_MANAGER_DEFAULT_PORT,
                          traffic_manager_log_file=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_FILE,
                          traffic_manager_log_dir=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_DIR,
                          traffic_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.78",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.OVS_1]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS]),
                          traffic_manager_port=collector_constants.MANAGER_PORTS.TRAFFIC_MANAGER_DEFAULT_PORT,
                          traffic_manager_log_file=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_FILE,
                          traffic_manager_log_dir=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_DIR,
                          traffic_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.3",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.OVS_1]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS]),
                          traffic_manager_port=collector_constants.MANAGER_PORTS.TRAFFIC_MANAGER_DEFAULT_PORT,
                          traffic_manager_log_file=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_FILE,
                          traffic_manager_log_dir=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_DIR,
                          traffic_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.31",
                          commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.CONTAINER_IMAGES.OVS_1]
                                    + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                        constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS]),
                          traffic_manager_port=collector_constants.MANAGER_PORTS.TRAFFIC_MANAGER_DEFAULT_PORT,
                          traffic_manager_log_file=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_FILE,
                          traffic_manager_log_dir=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_DIR,
                          traffic_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS),
    ]
    all_ips_and_commands = []
    for i in range(len(traffic_generators)):
        all_ips_and_commands.append((traffic_generators[i].ip, traffic_generators[i].commands))
    workflows_config = WorkflowsConfig(
        workflow_services=[
            WorkflowService(id=0, ips_and_commands=all_ips_and_commands)
        ],
        workflow_markov_chains=[
            WorkflowMarkovChain(
                transition_matrix=[
                    [0.8, 0.2],
                    [0, 1]
                ],
                initial_state=0,
                id=0
            )
        ]
    )
    client_population_config = ClientPopulationConfig(
        networks=[ContainerNetwork(
            name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_2",
            subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                        f"{network_id}.2{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
            subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
            bitmask=constants.CSLE.CSLE_EDGE_BITMASK
        )],
        ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.254",
        client_manager_port=collector_constants.MANAGER_PORTS.CLIENT_MANAGER_DEFAULT_PORT,
        client_time_step_len_seconds=time_step_len_seconds,
        client_manager_log_dir=collector_constants.LOG_FILES.CLIENT_MANAGER_LOG_DIR,
        client_manager_log_file=collector_constants.LOG_FILES.CLIENT_MANAGER_LOG_FILE,
        client_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS,
        clients=[
            Client(id=0, workflow_distribution=[1],
                   arrival_config=ConstantArrivalConfig(lamb=20), mu=4, exponential_service_time=True)
        ],
        workflows_config=workflows_config)
    traffic_conf = TrafficConfig(node_traffic_configs=traffic_generators,
                                 client_population_config=client_population_config)
    return traffic_conf


def default_kafka_config(network_id: int, level: int, version: str, time_step_len_seconds: int) -> KafkaConfig:
    """
    Generates the default kafka configuration

    :param network_id: the id of the emulation network
    :param level: the level of the emulation
    :param version: the version of the emulation
    :param time_step_len_seconds: default length of a time-step in the emulation
    :return: the kafka configuration
    """
    container = NodeContainerConfig(
        name=f"{constants.CONTAINER_IMAGES.KAFKA_1}",
        os=constants.CONTAINER_OS.KAFKA_1_OS,
        ips_and_networks=[
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
             f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
             ContainerNetwork(
                 name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                      f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                 subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                             f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                             f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                 subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                 bitmask=constants.CSLE.CSLE_EDGE_BITMASK
             ))
        ],
        version=version, level=str(level),
        restart_policy=constants.DOCKER.ON_FAILURE_3, suffix=collector_constants.KAFKA_CONFIG.SUFFIX)

    resources = NodeResourcesConfig(
        container_name=f"{constants.CSLE.NAME}-"
                       f"{constants.CONTAINER_IMAGES.KAFKA_1}_1-{constants.CSLE.LEVEL}{level}",
        num_cpus=1, available_memory_gb=4,
        ips_and_network_configs=[
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
             f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
             None)])

    firewall_config = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.KAFKA_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                   f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=None,
                default_gw=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                           f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}",
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                  f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set([]),
        output_drop=set(), input_drop=set(), forward_drop=set(), routes=set())

    topics = [
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.CLIENT_POPULATION_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.CLIENT_POPULATION_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.SNORT_IDS_LOG_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.SNORT_IDS_LOG_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.OSSEC_IDS_LOG_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.OSSEC_IDS_LOG_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.HOST_METRICS_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.HOST_METRICS_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.DOCKER_STATS_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.DOCKER_STATS_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.ATTACKER_ACTIONS_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.ATTACKER_ACTIONS_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.DEFENDER_ACTIONS_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.DEFENDER_ACTIONS_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.DOCKER_HOST_STATS_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.DOCKER_STATS_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.OPENFLOW_FLOW_STATS_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.OPENFLOW_FLOW_STATS_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.OPENFLOW_PORT_STATS_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.OPENFLOW_PORT_STATS_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.AVERAGE_OPENFLOW_FLOW_STATS_PER_SWITCH_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.AVERAGE_OPENFLOW_FLOW_STATS_PER_SWITCH_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.AVERAGE_OPENFLOW_PORT_STATS_PER_SWITCH_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.AVERAGE_OPENFLOW_PORT_STATS_PER_SWITCH_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.OPENFLOW_AGG_FLOW_STATS_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.OPENFLOW_AGG_FLOW_STATS_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.SNORT_IDS_RULE_LOG_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.SNORT_IDS_RULE_LOG_ATTRIBUTES
        ),
        KafkaTopic(
            name=collector_constants.KAFKA_CONFIG.SNORT_IDS_IP_LOG_TOPIC_NAME,
            num_replicas=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_REPLICAS,
            num_partitions=collector_constants.KAFKA_CONFIG.DEFAULT_NUM_PARTITIONS,
            retention_time_hours=collector_constants.KAFKA_CONFIG.DEFAULT_RETENTION_TIME_HOURS,
            attributes=collector_constants.KAFKA_CONFIG.SNORT_IDS_IP_LOG_ATTRIBUTES
        )
    ]

    config = KafkaConfig(container=container, resources=resources, topics=topics,
                         version=version,
                         kafka_port=collector_constants.KAFKA.PORT,
                         kafka_port_external=collector_constants.KAFKA.EXTERNAL_PORT,
                         kafka_manager_port=collector_constants.MANAGER_PORTS.KAFKA_MANAGER_DEFAULT_PORT,
                         time_step_len_seconds=time_step_len_seconds,
                         firewall_config=firewall_config,
                         kafka_manager_log_file=collector_constants.LOG_FILES.KAFKA_MANAGER_LOG_FILE,
                         kafka_manager_log_dir=collector_constants.LOG_FILES.KAFKA_MANAGER_LOG_DIR,
                         kafka_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS)
    return config


def default_users_config(network_id: int) -> UsersConfig:
    """
    Generates default users config

    :param network_id: the network id
    :return: generates the UsersConfig
    """
    users = [
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.191",
                        users=[User(username="agent", pw="agent", root=True)]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10", users=[
            User(username="admin", pw="admin1235912", root=True),
            User(username="jessica", pw="water", root=False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.78", users=[
            User(username="admin", pw="test32121", root=True),
            User(username="user1", pw="123123", root=True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.3", users=[
            User(username="john", pw="doe", root=True),
            User(username="vagrant", pw="test_pw1", root=False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.5", users=[
            User(username="john", pw="doe", root=True),
            User(username="vagrant", pw="test_pw1", root=False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.8", users=[
            User(username="john", pw="doe", root=True),
            User(username="vagrant", pw="test_pw1", root=False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.31", users=[
            User(username="john", pw="doe", root=True),
            User(username="vagrant", pw="test_pw1", root=False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.41", users=[
            User(username="john", pw="doe", root=True),
            User(username="vagrant", pw="test_pw1", root=False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.42", users=[
            User(username="john", pw="doe", root=True),
            User(username="vagrant", pw="test_pw1", root=False)
        ])
    ]
    users_conf = UsersConfig(users_configs=users)
    return users_conf


def default_vulns_config(network_id: int) -> VulnerabilitiesConfig:
    """
    Generates default vulnerabilities config

    :param network_id: the network id
    :return: the vulnerability config
    """
    vulns = [
        NodeVulnerabilityConfig(
            name=constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS,
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.42",
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
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.5",
            vuln_type=VulnType.WEAK_PW,
            credentials=[Credential(username="puppet", pw="puppet", root=True,
                                    service=constants.SSH.SERVICE_NAME,
                                    protocol=TransportProtocol.TCP,
                                    port=constants.SSH.DEFAULT_PORT)],
            cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
            cve=None,
            root=True, port=constants.SSH.DEFAULT_PORT, protocol=TransportProtocol.TCP,
            service=constants.SSH.SERVICE_NAME),
        NodeVulnerabilityConfig(
            name=constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS,
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.8",
            vuln_type=VulnType.WEAK_PW,
            credentials=[Credential(username="admin", pw="admin", root=True,
                                    service=constants.TELNET.SERVICE_NAME,
                                    protocol=TransportProtocol.TCP,
                                    port=constants.TELNET.DEFAULT_PORT)],
            cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
            cve=None,
            root=True, port=constants.TELNET.DEFAULT_PORT, protocol=TransportProtocol.TCP,
            service=constants.TELNET.SERVICE_NAME),
        NodeVulnerabilityConfig(
            name=constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS,
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.41",
            vuln_type=VulnType.WEAK_PW,
            credentials=[Credential(username="puppet", pw="puppet", root=True,
                                    service=constants.SSH.SERVICE_NAME,
                                    protocol=TransportProtocol.TCP,
                                    port=constants.SSH.DEFAULT_PORT)],
            cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
            cve=None,
            root=True, port=constants.SSH.DEFAULT_PORT, protocol=TransportProtocol.TCP,
            service=constants.SSH.SERVICE_NAME)
    ]
    vulns_config = VulnerabilitiesConfig(node_vulnerability_configs=vulns)
    return vulns_config


def default_services_config(network_id: int) -> ServicesConfig:
    """
    Generates default services config

    :param network_id: the network id
    :return: The services configuration
    """
    services_configs = [
        NodeServicesConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
               f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.254",
            services=[
                NetworkService(protocol=TransportProtocol.TCP, port=constants.SSH.DEFAULT_PORT,
                               name=constants.SSH.SERVICE_NAME, credentials=[])
            ]
        ),
        NodeServicesConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.42",
            services=[
                NetworkService(protocol=TransportProtocol.TCP, port=constants.SSH.DEFAULT_PORT,
                               name=constants.SSH.SERVICE_NAME, credentials=[]),
                NetworkService(protocol=TransportProtocol.TCP, port=constants.FTP.DEFAULT_PORT,
                               name=constants.FTP.SERVICE_NAME, credentials=[]),
                NetworkService(protocol=TransportProtocol.TCP, port=constants.MONGO.DEFAULT_PORT,
                               name=constants.MONGO.SERVICE_NAME, credentials=[]),
                NetworkService(protocol=TransportProtocol.TCP, port=constants.TOMCAT.DEFAULT_PORT,
                               name=constants.TOMCAT.SERVICE_NAME, credentials=[]),
                NetworkService(protocol=TransportProtocol.TCP, port=constants.TEAMSPEAK3.DEFAULT_PORT,
                               name=constants.TEAMSPEAK3.SERVICE_NAME, credentials=[])
            ]
        ),
        NodeServicesConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
               f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.191",
            services=[
                NetworkService(protocol=TransportProtocol.TCP, port=constants.SSH.DEFAULT_PORT,
                               name=constants.SSH.SERVICE_NAME, credentials=[])
            ]
        ),
        NodeServicesConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
            services=[
                NetworkService(protocol=TransportProtocol.TCP, port=constants.SSH.DEFAULT_PORT,
                               name=constants.SSH.SERVICE_NAME, credentials=[])
            ]
        ),
        NodeServicesConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.78",
            services=[
                NetworkService(protocol=TransportProtocol.TCP, port=constants.SSH.DEFAULT_PORT,
                               name=constants.SSH.SERVICE_NAME, credentials=[])
            ]
        ),
        NodeServicesConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.3",
            services=[
                NetworkService(protocol=TransportProtocol.TCP, port=constants.SSH.DEFAULT_PORT,
                               name=constants.SSH.SERVICE_NAME, credentials=[])
            ]
        ),
        NodeServicesConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.31",
            services=[
                NetworkService(protocol=TransportProtocol.TCP, port=constants.SSH.DEFAULT_PORT,
                               name=constants.SSH.SERVICE_NAME, credentials=[])
            ]
        ),
        NodeServicesConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.5",
            services=[
                NetworkService(protocol=TransportProtocol.TCP, port=constants.SSH.DEFAULT_PORT,
                               name=constants.SSH.SERVICE_NAME, credentials=[]),
                NetworkService(protocol=TransportProtocol.TCP, port=constants.DNS.DEFAULT_PORT,
                               name=constants.DNS.SERVICE_NAME, credentials=[]),
                NetworkService(protocol=TransportProtocol.TCP, port=constants.HTTP.DEFAULT_PORT,
                               name=constants.HTTP.SERVICE_NAME, credentials=[])
            ]
        ),
        NodeServicesConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.41",
            services=[
                NetworkService(protocol=TransportProtocol.TCP, port=constants.SSH.DEFAULT_PORT,
                               name=constants.SSH.SERVICE_NAME, credentials=[]),
                NetworkService(protocol=TransportProtocol.TCP, port=constants.DNS.DEFAULT_PORT,
                               name=constants.DNS.SERVICE_NAME, credentials=[]),
                NetworkService(protocol=TransportProtocol.TCP, port=constants.HTTP.DEFAULT_PORT,
                               name=constants.HTTP.SERVICE_NAME, credentials=[])
            ]
        ),
        NodeServicesConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.8",
            services=[
                NetworkService(protocol=TransportProtocol.TCP, port=constants.SSH.DEFAULT_PORT,
                               name=constants.SSH.SERVICE_NAME, credentials=[]),
                NetworkService(protocol=TransportProtocol.TCP, port=constants.TELNET.DEFAULT_PORT,
                               name=constants.TELNET.SERVICE_NAME, credentials=[]),
                NetworkService(protocol=TransportProtocol.TCP, port=constants.HTTP.DEFAULT_PORT,
                               name=constants.HTTP.SERVICE_NAME, credentials=[])
            ]
        )
    ]
    service_cfg = ServicesConfig(
        services_configs=services_configs
    )
    return service_cfg


def default_static_attacker_sequences(subnet_masks: List[str]) -> Dict[str, List[EmulationAttackerAction]]:
    """
    Generates default static attacker sequences config

    :param subnetmasks: list of subnet masks for the emulation
    :return: the default static attacker sequences configuration
    """
    return {}


def default_ovs_config(network_id: int, level: int, version: str) -> OVSConfig:
    """
    Generates default OVS config

    :param network_id: the network id of the emulation
    :param level: the level of the emulation
    :param version: the version of the emulation
    :return: the default OVS config
    """
    ovs_config = OVSConfig(switch_configs=[
        OvsSwitchConfig(
            container_name=f"{constants.CSLE.NAME}-"
                           f"{constants.CONTAINER_IMAGES.OVS_1}_1-{constants.CSLE.LEVEL}{level}",
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
               f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78",
            controller_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                          f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}."
                          f"77",
            controller_port=ryu_constants.RYU.DEFAULT_PORT,
            controller_transport_protocol=ryu_constants.RYU.DEFAULT_TRANSPORT_PROTOCOL,
            openflow_protocols=[constants.OPENFLOW.OPENFLOW_V_1_3]
        ),
        OvsSwitchConfig(
            container_name=f"{constants.CSLE.NAME}-"
                           f"{constants.CONTAINER_IMAGES.OVS_1}_2-{constants.CSLE.LEVEL}{level}",
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
               f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.10",
            controller_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                          f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}."
                          f"14",
            controller_port=ryu_constants.RYU.DEFAULT_PORT,
            controller_transport_protocol=ryu_constants.RYU.DEFAULT_TRANSPORT_PROTOCOL,
            openflow_protocols=[constants.OPENFLOW.OPENFLOW_V_1_3]
        ),
        OvsSwitchConfig(
            container_name=f"{constants.CSLE.NAME}-"
                           f"{constants.CONTAINER_IMAGES.OVS_1}_3-{constants.CSLE.LEVEL}{level}",
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
               f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18",
            controller_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                          f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.22",
            controller_port=ryu_constants.RYU.DEFAULT_PORT,
            controller_transport_protocol=ryu_constants.RYU.DEFAULT_TRANSPORT_PROTOCOL,
            openflow_protocols=[constants.OPENFLOW.OPENFLOW_V_1_3]
        )
    ])
    return ovs_config


def default_sdn_controller_config(network_id: int, level: int, version: str, time_step_len_seconds: int) \
        -> Union[None, SDNControllerConfig]:
    """
    Generates the default SDN controller config

    :param network_id: the network id of the emulation
    :param level: the level of the emulation
    :param version: the version of the emulation
    :param time_step_len_seconds: default length of a time-step in the emulation
    :return: the default SDN Controller config
    """
    container = NodeContainerConfig(
        name=f"{constants.CONTAINER_IMAGES.RYU_1}",
        os=constants.CONTAINER_OS.RYU_1_OS,
        ips_and_networks=[
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.77",
             ContainerNetwork(
                 name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                      f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_2",
                 subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                             f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78"
                             f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                 subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                               f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78",
                 bitmask=ryu_constants.RYU.BITMASK,
                 interface=constants.NETWORKING.ETH0
             )),
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.14",
             ContainerNetwork(
                 name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                      f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_3",
                 subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                             f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.9"
                             f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                 subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                               f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.9",
                 bitmask=ryu_constants.RYU.BITMASK,
                 interface=constants.NETWORKING.ETH2
             )),
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.22",
             ContainerNetwork(
                 name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                      f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_4",
                 subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                             f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18"
                             f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                 subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                               f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18",
                 bitmask=ryu_constants.RYU.BITMASK,
                 interface=constants.NETWORKING.ETH3
             )),
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
             f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}",
             ContainerNetwork(
                 name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                      f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                 subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                             f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                             f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                 subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                 interface=constants.NETWORKING.ETH4,
                 bitmask=constants.CSLE.CSLE_EDGE_BITMASK
             ))
        ],
        version=version, level=str(level),
        restart_policy=constants.DOCKER.ON_FAILURE_3, suffix=ryu_constants.RYU.SUFFIX)

    resources = NodeResourcesConfig(
        container_name=f"{constants.CSLE.NAME}-"
                       f"{constants.CONTAINER_IMAGES.RYU_1}{ryu_constants.RYU.SUFFIX}-"
                       f"{constants.CSLE.LEVEL}{level}",
        num_cpus=min(8, multiprocessing.cpu_count()), available_memory_gb=4,
        ips_and_network_configs=[
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.77",
             None),
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.14",
             None),
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.22",
             None)
        ])

    firewall_config = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.RYU_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.77",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_2",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78"
                                f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                  f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.78",
                    bitmask=ryu_constants.RYU.BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.14",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_3",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.9"
                                f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                  f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.9",
                    bitmask=ryu_constants.RYU.BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.22",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}_4",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18"
                                f"{ryu_constants.RYU.SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}"
                                  f"{ryu_constants.RYU.NETWORK_ID_THIRD_OCTET}.18",
                    bitmask=ryu_constants.RYU.BITMASK
                )
            ),
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                   f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    interface=constants.NETWORKING.ETH2,
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set([]),
        output_drop=set(), input_drop=set(), forward_drop=set(), routes=set())

    sdn_controller_config = SDNControllerConfig(
        container=container, resources=resources, version=version, controller_type=SDNControllerType.RYU,
        controller_port=ryu_constants.RYU.DEFAULT_PORT, time_step_len_seconds=time_step_len_seconds,
        controller_web_api_port=8080, controller_module_name=ryu_constants.CONTROLLERS.LEARNING_SWITCH_CONTROLLER,
        firewall_config=firewall_config,
        manager_port=collector_constants.MANAGER_PORTS.SDN_CONTROLLER_MANAGER_DEFAULT_PORT,
        manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS,
        manager_log_dir=collector_constants.LOG_FILES.RYU_MANAGER_LOG_DIR,
        manager_log_file=collector_constants.LOG_FILES.RYU_MANAGER_LOG_FILE)

    return sdn_controller_config


def default_host_manager_config(network_id: int, level: int, version: str,
                                time_step_len_seconds: int) -> HostManagerConfig:
    """
    Generates the default host manager configuration

    :param network_id: the id of the emulation network
    :param level: the level of the emulation
    :param version: the version of the emulation
    :param time_step_len_seconds: default length of a time-step in the emulation
    :return: the host manager configuration
    """
    config = HostManagerConfig(version=version, time_step_len_seconds=time_step_len_seconds,
                               host_manager_port=collector_constants.MANAGER_PORTS.HOST_MANAGER_DEFAULT_PORT,
                               host_manager_log_file=collector_constants.LOG_FILES.HOST_MANAGER_LOG_FILE,
                               host_manager_log_dir=collector_constants.LOG_FILES.HOST_MANAGER_LOG_DIR,
                               host_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS)
    return config


def default_snort_ids_manager_config(network_id: int, level: int, version: str, time_step_len_seconds: int) \
        -> SnortIDSManagerConfig:
    """
    Generates the default Snort IDS manager configuration

    :param network_id: the id of the emulation network
    :param level: the level of the emulation
    :param version: the version of the emulation
    :param time_step_len_seconds: default length of a time-step in the emulation
    :return: the Snort IDS manager configuration
    """
    config = SnortIDSManagerConfig(
        version=version, time_step_len_seconds=time_step_len_seconds,
        snort_ids_manager_port=collector_constants.MANAGER_PORTS.SNORT_IDS_MANAGER_DEFAULT_PORT,
        snort_ids_manager_log_dir=collector_constants.LOG_FILES.SNORT_IDS_MANAGER_LOG_DIR,
        snort_ids_manager_log_file=collector_constants.LOG_FILES.SNORT_IDS_MANAGER_LOG_FILE,
        snort_ids_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS)
    return config


def default_ossec_ids_manager_config(network_id: int, level: int, version: str, time_step_len_seconds: int) \
        -> OSSECIDSManagerConfig:
    """
    Generates the default OSSEC IDS manager configuration

    :param network_id: the id of the emulation network
    :param level: the level of the emulation
    :param version: the version of the emulation
    :param time_step_len_seconds: default length of a time-step in the emulation
    :return: the OSSEC IDS manager configuration
    """
    config = OSSECIDSManagerConfig(
        version=version, time_step_len_seconds=time_step_len_seconds,
        ossec_ids_manager_port=collector_constants.MANAGER_PORTS.OSSEC_IDS_MANAGER_DEFAULT_PORT,
        ossec_ids_manager_log_file=collector_constants.LOG_FILES.OSSEC_IDS_MANAGER_LOG_FILE,
        ossec_ids_manager_log_dir=collector_constants.LOG_FILES.OSSEC_IDS_MANAGER_LOG_DIR,
        ossec_ids_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS)
    return config


def default_docker_stats_manager_config(network_id: int, level: int, version: str, time_step_len_seconds: int) \
        -> DockerStatsManagerConfig:
    """
    Generates the default docker stats manager configuration

    :param network_id: the id of the emulation network
    :param level: the level of the emulation
    :param version: the version of the emulation
    :param time_step_len_seconds: default length of a time-step in the emulation
    :return: the docker stats manager configuration
    """
    config = DockerStatsManagerConfig(
        version=version, time_step_len_seconds=time_step_len_seconds,
        docker_stats_manager_port=collector_constants.MANAGER_PORTS.DOCKER_STATS_MANAGER_DEFAULT_PORT,
        docker_stats_manager_log_file=collector_constants.LOG_FILES.DOCKER_STATS_MANAGER_LOG_FILE,
        docker_stats_manager_log_dir=collector_constants.LOG_FILES.DOCKER_STATS_MANAGER_LOG_DIR,
        docker_stats_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS)
    return config


def default_elk_config(network_id: int, level: int, version: str, time_step_len_seconds: int) -> ElkConfig:
    """
    Generates the default ELK configuration

    :param network_id: the id of the emulation network
    :param level: the level of the emulation
    :param version: the version of the emulation
    :param time_step_len_seconds: default length of a time-step in the emulation
    :return: the ELK configuration
    """
    container = NodeContainerConfig(
        name=f"{constants.CONTAINER_IMAGES.ELK_1}",
        os=constants.CONTAINER_OS.ELK_1_OS,
        ips_and_networks=[
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
             f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
             ContainerNetwork(
                 name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                      f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}",
                 subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                             f"{network_id}.{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}"
                             f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                 subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                 bitmask=constants.CSLE.CSLE_EDGE_BITMASK
             )),
        ],
        version=version, level=str(level),
        restart_policy=constants.DOCKER.ON_FAILURE_3, suffix=collector_constants.ELK_CONFIG.SUFFIX)

    resources = NodeResourcesConfig(
        container_name=f"{constants.CSLE.NAME}-"
                       f"{constants.CONTAINER_IMAGES.ELK_1}_1-{constants.CSLE.LEVEL}{level}",
        num_cpus=2, available_memory_gb=16,
        ips_and_network_configs=[
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
             f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
             f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
             None)])

    firewall_config = NodeFirewallConfig(
        hostname=f"{constants.CONTAINER_IMAGES.ELK_1}_1",
        ips_gw_default_policy_networks=[
            DefaultNetworkFirewallConfig(
                ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                   f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                   f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                default_gw=None,
                default_input=constants.FIREWALL.ACCEPT,
                default_output=constants.FIREWALL.ACCEPT,
                default_forward=constants.FIREWALL.ACCEPT,
                network=ContainerNetwork(
                    name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{network_id}_"
                         f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}",
                    subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                                f"{network_id}.{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}"
                                f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                    subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}",
                    bitmask=constants.CSLE.CSLE_EDGE_BITMASK
                )
            )
        ],
        output_accept=set([]),
        input_accept=set([]),
        forward_accept=set([]),
        output_drop=set(), input_drop=set(), forward_drop=set(), routes=set())

    config = ElkConfig(version=version, time_step_len_seconds=time_step_len_seconds,
                       elastic_port=collector_constants.ELK.ELASTIC_PORT,
                       kibana_port=collector_constants.ELK.KIBANA_PORT,
                       logstash_port=collector_constants.ELK.LOGSTASH_PORT,
                       elk_manager_port=collector_constants.MANAGER_PORTS.ELK_MANAGER_DEFAULT_PORT,
                       container=container,
                       resources=resources, firewall_config=firewall_config,
                       elk_manager_log_file=collector_constants.LOG_FILES.ELK_MANAGER_LOG_FILE,
                       elk_manager_log_dir=collector_constants.LOG_FILES.ELK_MANAGER_LOG_DIR,
                       elk_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS)
    return config


def default_beats_config(network_id: int) -> BeatsConfig:
    """
    Generates default beats config

    :param network_id: the network id
    :return: the beats configuration
    """
    node_beats_configs = [
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE,
                                          collector_constants.FILEBEAT.SNORT_MODULE],
                        kafka_input=False, start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}"
                        ]),
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.5",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE],
                        kafka_input=False, start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}"
                        ]),
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.8",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE],
                        kafka_input=False, start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}"
                        ]),
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.41",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE],
                        kafka_input=False, start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}"
                        ]),
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.42",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE],
                        kafka_input=False, start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}"
                        ]),
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.78",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE],
                        kafka_input=False, start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}"
                        ]),
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.3",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE],
                        kafka_input=False, start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}"
                        ]),
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.31",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE],
                        kafka_input=False, start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}"
                        ]),
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                           f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE,
                                          collector_constants.FILEBEAT.KAFKA_MODULE],
                        kafka_input=True, start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE,
                                            collector_constants.FILEBEAT.KAFKA_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.254",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.191",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.78",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.3",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.21",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.79"
                        ]),
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                           f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE,
                                          collector_constants.FILEBEAT.ELASTICSEARCH_MODULE,
                                          collector_constants.FILEBEAT.KIBANA_MODULE,
                                          collector_constants.FILEBEAT.LOGSTASH_MODULE], kafka_input=False,
                        start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE,
                                            collector_constants.FILEBEAT.ELASTICSEARCH_MODULE,
                                            collector_constants.FILEBEAT.KIBANA_MODULE,
                                            collector_constants.FILEBEAT.LOGSTASH_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.254",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.191",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.78",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.3",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.21",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}.79"
                        ]),
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.254",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE],
                        kafka_input=False, start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}"
                        ]),
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.EXTERNAL_NETWORK.NETWORK_ID_THIRD_OCTET}.191",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE],
                        kafka_input=False, start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}"
                        ]),
        NodeBeatsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                           f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                           f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}",
                        log_files_paths=collector_constants.LOG_FILES.DEFAULT_LOG_FILE_PATHS,
                        filebeat_modules=[collector_constants.FILEBEAT.SYSTEM_MODULE],
                        kafka_input=False, start_filebeat_automatically=False,
                        start_packetbeat_automatically=False,
                        metricbeat_modules=[collector_constants.METRICBEAT.SYSTEM_MODULE,
                                            collector_constants.METRICBEAT.LINUX_MODULE],
                        start_metricbeat_automatically=False,
                        start_heartbeat_automatically=False,
                        heartbeat_hosts_to_monitor=[
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}",
                            f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}."
                            f"{collector_constants.KAFKA_CONFIG.NETWORK_ID_THIRD_OCTET}."
                            f"{ryu_constants.RYU.NETWORK_ID_FOURTH_OCTET}"
                        ]),
    ]
    beats_conf = BeatsConfig(node_beats_configs=node_beats_configs, num_elastic_shards=1, reload_enabled=False)
    return beats_conf


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
                        action="store_true")
    args = parser.parse_args()
    config = default_config(name="csle-level12-070", network_id=12, level=12, version="0.7.0", time_step_len_seconds=30)
    ExperimentUtil.write_emulation_config_file(config, ExperimentUtil.default_emulation_config_path())

    if args.install:
        EmulationEnvController.install_emulation(config=config)
        img_path = ExperimentUtil.default_emulation_picture_path()
        if os.path.exists(img_path):
            encoded_image_str = ExperimentUtil.read_env_picture(img_path)
            EmulationEnvController.save_emulation_image(img=encoded_image_str, emulation_name=config.name)
    if args.uninstall:
        EmulationEnvController.uninstall_emulation(config=config)
