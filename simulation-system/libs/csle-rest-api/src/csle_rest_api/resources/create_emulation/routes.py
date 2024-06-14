"""
Routes and sub-resources for the /create-emulation resource
"""
from typing import Dict, List, Union, Tuple, Any
from flask import Blueprint, jsonify, request, Response
import json
import csle_rest_api.constants.constants as api_constants
import csle_rest_api.util.rest_api_util as rest_api_util
import csle_common.constants.constants as constants
import csle_collector.constants.constants as collector_constants
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.client import Client
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
from csle_common.dao.emulation_config.traffic_config import TrafficConfig
from csle_common.dao.emulation_config.node_traffic_config import NodeTrafficConfig
from csle_common.dao.emulation_config.users_config import UsersConfig
from csle_common.dao.emulation_config.node_users_config import NodeUsersConfig
from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.client_population_config import ClientPopulationConfig
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic
from csle_common.dao.emulation_config.flag import Flag
from csle_common.dao.emulation_config.node_vulnerability_config import NodeVulnerabilityConfig
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.node_services_config import NodeServicesConfig
from csle_common.dao.emulation_config.services_config import ServicesConfig
from csle_common.dao.emulation_config.network_service import NetworkService
from csle_common.dao.emulation_config.ovs_config import OVSConfig
from csle_common.dao.emulation_config.sdn_controller_config import SDNControllerConfig
from csle_common.dao.emulation_config.user import User
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_config.host_manager_config import HostManagerConfig
from csle_common.dao.emulation_config.snort_ids_manager_config import SnortIDSManagerConfig
from csle_common.dao.emulation_config.ossec_ids_manager_config import OSSECIDSManagerConfig
from csle_common.dao.emulation_config.docker_stats_manager_config import DockerStatsManagerConfig
from csle_common.dao.emulation_config.elk_config import ElkConfig
from csle_common.dao.emulation_config.beats_config import BeatsConfig
from csle_common.dao.emulation_config.node_beats_config import NodeBeatsConfig
from csle_common.dao.emulation_config.credential import Credential

# Creates a blueprint "sub application" of the main REST app
create_emulation_bp = Blueprint(
    api_constants.MGMT_WEBAPP.CREATE_EMULATION_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.CREATE_EMULATION_RESOURCE}")


@create_emulation_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def create_emulation() -> Tuple[Response, int]:
    """
    The /create-emulation resource.

    :return: The given policy or deletes the policy
    """
    requires_admin = True
    authorized = rest_api_util.check_if_user_is_authorized(request=request, requires_admin=requires_admin)
    if authorized is not None:
        return authorized
    emulation_data = json.loads(request.data)
    config = convert_json_data_to_emulation_config(emulation_data)
    response = jsonify(config.to_dict())
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response, constants.HTTPS.OK_STATUS_CODE


def convert_json_data_to_emulation_config(emulation_data: Dict[str, Any]) -> EmulationEnvConfig:
    """
    Converts the json emulation data to an emulation environment configuration object.

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: the emulation environment configuration
    """

    name = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_NAME]
    level = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_LEVEL]
    version = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_VERSION]
    descr = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_DESCRIPTION]
    containers_cfg = convert_json_data_to_containers_config(emulation_data=emulation_data)
    flags_cfg = convert_json_data_to_flags_config(emulation_data=emulation_data)
    resources_cfg = convert_json_data_to_resource_constraints_config(emulation_data=emulation_data)
    topology_cfg = convert_json_data_to_topology_config(emulation_data=emulation_data)
    traffic_cfg = convert_json_data_to_traffic_config(emulation_data=emulation_data)
    users_cfg = convert_json_data_to_users_config(emulation_data=emulation_data)
    services_cfg = convert_json_data_to_services_config(emulation_data=emulation_data)
    vuln_cfg = convert_json_data_to_vulns_config(emulation_data=emulation_data)
    kafka_cfg = convert_json_data_to_kafka_config(emulation_data=emulation_data)
    static_attackers_cfg = convert_json_data_to_static_attacker_sequences(topology_cfg.subnetwork_masks)
    ovs_cfg = convert_json_data_to_ovs_config(emulation_data=emulation_data)
    sdn_controller_cfg = convert_json_data_to_sdn_controller_config(emulation_data=emulation_data)
    host_manager_cfg = convert_json_data_to_host_manager_config(emulation_data=emulation_data)
    snort_ids_manager_cfg = convert_json_data_to_snort_ids_manager_config(emulation_data=emulation_data)
    ossec_ids_manager_cfg = convert_json_data_to_ossec_ids_manager_config(emulation_data=emulation_data)
    docker_stats_manager_cfg = convert_json_data_to_docker_stats_manager_config(emulation_data=emulation_data)
    elk_cfg = convert_json_data_to_elk_config(emulation_data=emulation_data)
    beats_cfg = convert_json_data_to_beats_config(emulation_data=emulation_data)
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


def convert_json_data_to_containers_config(emulation_data: Dict[str, Any]) -> ContainersConfig:
    """
    Converts the json emulation data to a containers configuration object.

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: the ContainersConfig of the emulation
    """
    containers = []
    vulnerable_nodes: List[str] = []
    # *** We need to define the agent reachable nodes
    agent_reachable_nodes: List[str] = []
    # *** We need to check with Kim what is networks? Which interfaces are considered here?
    networks: List[Tuple[str, ContainerNetwork]] = []
    agent_ip = ""
    router_ip = ""
    emulation_ids_enabled = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_IDS_ENABLED]
    emulation_containers = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_CONTAINER]
    for container in emulation_containers:
        container_name = container[api_constants.CREATE_EMULATION_PAGE.NAME]
        container_os = container[api_constants.CREATE_EMULATION_PAGE.OS]
        container_version = container[api_constants.CREATE_EMULATION_PAGE.VERSION]
        containers_level = container[api_constants.CREATE_EMULATION_PAGE.LEVEL]
        container_restart_policy = container[api_constants.CREATE_EMULATION_PAGE.RESTART_POLICY]
        container_interfaces = container[api_constants.CREATE_EMULATION_PAGE.INTERFACES]
        ips_and_networks = []
        for interfaces in container_interfaces:
            interface_name = interfaces[api_constants.CREATE_EMULATION_PAGE.NAME]
            interface_ip = interfaces[api_constants.CREATE_EMULATION_PAGE.IP]
            interface_subnet_mask = interfaces[api_constants.CREATE_EMULATION_PAGE.SUBNET_MASK]
            interface_subnet_prefix = interfaces[api_constants.CREATE_EMULATION_PAGE.SUBNET_PREFIX]
            interface_physical_interface = interfaces[api_constants.CREATE_EMULATION_PAGE.PHYSICAL_INTERFACE]
            interface_bit_mask = interfaces[api_constants.CREATE_EMULATION_PAGE.BITMASK]
            ips_and_networks.append((interface_ip,
                                     ContainerNetwork(
                                         name=interface_name,
                                         subnet_mask=interface_subnet_mask,
                                         subnet_prefix=interface_subnet_prefix,
                                         interface=interface_physical_interface,
                                         bitmask=interface_bit_mask
                                     )))
            if (api_constants.CREATE_EMULATION_PAGE.HACKER in container_name):
                agent_ip = interface_ip
            if (api_constants.CREATE_EMULATION_PAGE.ROUTER in container_name):
                router_ip = interface_ip
        # container_vulns = container[api_constants.CREATE_EMULATION_PAGE.VULNS]
        # for vuln in container_vulns:
        #     vuln_service = vuln[api_constants.CREATE_EMULATION_PAGE.VULN_SERVICE]
        #     vuln_service_ip = vuln[api_constants.CREATE_EMULATION_PAGE.VULN_SERVICE][
        #         api_constants.CREATE_EMULATION_PAGE.SERVICE_IP]
        #     vulnerable_nodes.append(vuln_service_ip)

        node = NodeContainerConfig(
            name=container_name,
            os=container_os,
            ips_and_networks=ips_and_networks,
            version=container_version, level=containers_level, restart_policy=container_restart_policy, suffix="_1")
        containers.append(node)
    containers_cfg = ContainersConfig(containers=containers, agent_ip=agent_ip, router_ip=router_ip,
                                      ids_enabled=emulation_ids_enabled, vulnerable_nodes=vulnerable_nodes,
                                      agent_reachable_nodes=agent_reachable_nodes, networks=networks)

    return containers_cfg


def convert_json_data_to_flags_config(emulation_data: Dict[str, Any]) -> FlagsConfig:
    """
    Converts the json emulation data to a flags configuration object.

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: The flags confguration
    """
    flags: List[NodeFlagsConfig] = []
    interface_ip = "0.0.0.0"
    emulation_containers = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_CONTAINER]
    for containers in emulation_containers:
        container_falg_id = containers[api_constants.CREATE_EMULATION_PAGE.FLAG_ID]
        container_flag_score = containers[api_constants.CREATE_EMULATION_PAGE.FLAG_SCORE]
        container_flag_permission = containers[api_constants.CREATE_EMULATION_PAGE.FLAG_PERMISSION]
        container_interfaces = containers[api_constants.CREATE_EMULATION_PAGE.INTERFACES]
        for interfaces in container_interfaces:
            interface_ip = interfaces[api_constants.CREATE_EMULATION_PAGE.IP]
        flags_config = NodeFlagsConfig(ip=interface_ip,
                                       flags=[Flag(
                                           name=f"{constants.COMMON.FLAG_FILENAME_PREFIX}{container_falg_id}",
                                           path=f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}"
                                                f"{container_falg_id}"
                                                f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                                           dir=f"/{constants.COMMANDS.TMP_DIR}/",
                                           id=container_falg_id, requires_root=container_flag_permission,
                                           score=container_flag_score
                                       )])
        flags.append(flags_config)
    flags_config = FlagsConfig(node_flag_configs=flags)
    return flags_config


def convert_json_data_to_static_attacker_sequences(subnet_masks: List[str]) -> Dict[str, List[EmulationAttackerAction]]:
    """
    Generates Converts the json emulation data to the attacker sequences config

    :param subnetmasks: list of subnet masks for the emulation
    :return: the default static attacker sequences configuration
    """
    return {}


def convert_json_data_to_ovs_config(emulation_data: Dict[str, Any]) -> OVSConfig:
    """
    Converts the json emulation data to the OVS config

    :param emulation_data: the emulation data in JSON format received from front-end
    """

    ovs_config = OVSConfig(switch_configs=[])
    return ovs_config


def convert_json_data_to_sdn_controller_config(emulation_data: Dict[str, Any]) -> Union[None, SDNControllerConfig]:
    """
    Generates the Converts the json emulation data to the SDN controller config

    :param emulation_data: the emulation data in JSON format received from front-end
    """
    return None


def convert_json_data_to_host_manager_config(emulation_data: Dict[str, Any]) -> HostManagerConfig:
    """
    Converts the json emulation data to the host manager configuration

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: the host manager configuration
    """
    version = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_VERSION]
    time_step_len_seconds = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_TIME_STEP_LENGTH]
    config = HostManagerConfig(version=version, time_step_len_seconds=time_step_len_seconds,
                               host_manager_port=collector_constants.MANAGER_PORTS.HOST_MANAGER_DEFAULT_PORT,
                               host_manager_log_file=collector_constants.LOG_FILES.HOST_MANAGER_LOG_FILE,
                               host_manager_log_dir=collector_constants.LOG_FILES.HOST_MANAGER_LOG_DIR,
                               host_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS)
    return config


def convert_json_data_to_snort_ids_manager_config(emulation_data: Dict[str, Any]) -> SnortIDSManagerConfig:
    """
    Converts the json emulation data to the Snort IDS manager configuration

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: the Snort IDS manager configuration
    """

    version = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_VERSION]
    time_step_len_seconds = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_TIME_STEP_LENGTH]

    config = SnortIDSManagerConfig(
        version=version, time_step_len_seconds=time_step_len_seconds,
        snort_ids_manager_port=collector_constants.MANAGER_PORTS.SNORT_IDS_MANAGER_DEFAULT_PORT,
        snort_ids_manager_log_dir=collector_constants.LOG_FILES.SNORT_IDS_MANAGER_LOG_DIR,
        snort_ids_manager_log_file=collector_constants.LOG_FILES.SNORT_IDS_MANAGER_LOG_FILE,
        snort_ids_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS)
    return config


def convert_json_data_to_ossec_ids_manager_config(emulation_data: Dict[str, Any]) -> OSSECIDSManagerConfig:
    """
    Converts the json emulation data to the OSSEC IDS manager configuration

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: the OSSEC IDS manager configuration
    """
    version = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_VERSION]
    time_step_len_seconds = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_TIME_STEP_LENGTH]
    config = OSSECIDSManagerConfig(
        version=version, time_step_len_seconds=time_step_len_seconds,
        ossec_ids_manager_port=collector_constants.MANAGER_PORTS.OSSEC_IDS_MANAGER_DEFAULT_PORT,
        ossec_ids_manager_log_file=collector_constants.LOG_FILES.OSSEC_IDS_MANAGER_LOG_FILE,
        ossec_ids_manager_log_dir=collector_constants.LOG_FILES.OSSEC_IDS_MANAGER_LOG_DIR,
        ossec_ids_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS)
    return config


def convert_json_data_to_docker_stats_manager_config(emulation_data: Dict[str, Any]) -> DockerStatsManagerConfig:
    """
    Converts the json emulation data to the docker stats manager configuration

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: the docker stats manager configuration
    """
    version = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_VERSION]
    time_step_len_seconds = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_TIME_STEP_LENGTH]
    config = DockerStatsManagerConfig(
        version=version, time_step_len_seconds=time_step_len_seconds,
        docker_stats_manager_port=collector_constants.MANAGER_PORTS.DOCKER_STATS_MANAGER_DEFAULT_PORT,
        docker_stats_manager_log_file=collector_constants.LOG_FILES.DOCKER_STATS_MANAGER_LOG_FILE,
        docker_stats_manager_log_dir=collector_constants.LOG_FILES.DOCKER_STATS_MANAGER_LOG_DIR,
        docker_stats_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS)
    return config


def convert_json_data_to_elk_config(emulation_data: Dict[str, Any]) -> ElkConfig:
    """
    Converts the json emulation data to the default ELK configuration

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: the ELK configuration
    """

    # *** This function I am not sure if we have already collected all the paramters needed.

    network_id = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_NETWORK_ID]
    level = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_LEVEL]
    version = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_VERSION]
    time_step_len_seconds = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_TIME_STEP_LENGTH]
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


def convert_json_data_to_beats_config(emulation_data: Dict[str, Any]) -> BeatsConfig:
    """
    Converts the json emulation data to the beats config

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: the beats configuration
    """
    # *** This file I am not very sure if all the parameters are set correctly
    # *** Compared to other files this one seems incomplete.
    network_id = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_NETWORK_ID]
    node_beats_configs = []
    emulation_containers = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_CONTAINER]
    for containers in emulation_containers:
        container_interfaces = containers[api_constants.CREATE_EMULATION_PAGE.INTERFACES]
        for interfaces in container_interfaces:
            interface_ip = interfaces[api_constants.CREATE_EMULATION_PAGE.IP]
        node_beats = NodeBeatsConfig(ip=interface_ip,
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
                                         f"{collector_constants.ELK_CONFIG.NETWORK_ID_FOURTH_OCTET}"
                                     ])
        node_beats_configs.append(node_beats)
    beats_conf = BeatsConfig(node_beats_configs=node_beats_configs, num_elastic_shards=1, reload_enabled=False)
    return beats_conf


def convert_json_data_to_kafka_config(emulation_data: Dict[str, Any]) -> KafkaConfig:
    """
    Converts the json emulation data to the kafka configuration

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: the kafka configuration
    """

    network_id = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_NETWORK_ID]
    level = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_LEVEL]
    version = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_VERSION]
    time_step_len_seconds = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_TIME_STEP_LENGTH]

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
             )),
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

    config = KafkaConfig(container=container, resources=resources, topics=topics, firewall_config=firewall_config,
                         version=version,
                         kafka_port=collector_constants.KAFKA.PORT,
                         kafka_port_external=collector_constants.KAFKA.EXTERNAL_PORT,
                         kafka_manager_port=collector_constants.MANAGER_PORTS.KAFKA_MANAGER_DEFAULT_PORT,
                         time_step_len_seconds=time_step_len_seconds,
                         kafka_manager_log_file=collector_constants.LOG_FILES.KAFKA_MANAGER_LOG_FILE,
                         kafka_manager_log_dir=collector_constants.LOG_FILES.KAFKA_MANAGER_LOG_DIR,
                         kafka_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS)
    return config


def convert_json_data_to_resource_constraints_config(emulation_data: Dict[str, Any]) -> ResourcesConfig:
    """
    Converts the json emulation data to the resource constraints config

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: generates the ResourcesConfig
    """
    node_resources_configurations = []
    emulation_containers = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_CONTAINER]
    for containers in emulation_containers:
        container_name = containers[api_constants.CREATE_EMULATION_PAGE.NAME]
        container_cpu = containers[api_constants.CREATE_EMULATION_PAGE.CPU]
        container_memory = containers[api_constants.CREATE_EMULATION_PAGE.MEM]
        container_interfaces = containers[api_constants.CREATE_EMULATION_PAGE.INTERFACES]
        ips_and_network_configs = []
        for interfaces in container_interfaces:
            interface_ip = interfaces[api_constants.CREATE_EMULATION_PAGE.IP]
            interface_physical_interface = interfaces[api_constants.CREATE_EMULATION_PAGE.PHYSICAL_INTERFACE]
            interface_limit_packet_queue = interfaces[api_constants.CREATE_EMULATION_PAGE.LIMIT_PACKETS_QUEUE]
            interface_packet_delay_ms = interfaces[api_constants.CREATE_EMULATION_PAGE.PACKET_DELAY_MS]
            interface_packet_delay_jitter_ms = interfaces[api_constants.CREATE_EMULATION_PAGE.PACKET_DELAY_JITTER_MS]
            interface_packet_delay_correlation_percentage = interfaces[
                api_constants.CREATE_EMULATION_PAGE.PACKET_DELAY_CORRELATION_PERCENTAGE]
            interfaces_packet_delay_distribution = interfaces[
                api_constants.CREATE_EMULATION_PAGE.PACKET_DELAY_DISTRIBUTION]
            interface_packet_loss_type = interfaces[api_constants.CREATE_EMULATION_PAGE.PACKET_LOSS_TYPE]
            interface_loss_gmodel_p = interfaces[api_constants.CREATE_EMULATION_PAGE.LOSS_GE_MODEL_P]
            interface_loss_gmodel_r = interfaces[api_constants.CREATE_EMULATION_PAGE.LOSS_GE_MODEL_R]
            interface_loss_gmodel_k = interfaces[api_constants.CREATE_EMULATION_PAGE.LOSS_GE_MODEL_K]
            interface_loss_gmodel_h = interfaces[api_constants.CREATE_EMULATION_PAGE.LOSS_GE_MODEL_H]
            interface_packet_corruption_percentage = interfaces[
                api_constants.CREATE_EMULATION_PAGE.PACKET_CORRUPT_PERCENTAGE]
            interface_packet_corruption_correlation_percentage = interfaces[
                api_constants.CREATE_EMULATION_PAGE.PACKET_CORRUPT_CORRELATION_PERCENTAGE]
            interface_packet_duplication_percentage = interfaces[
                api_constants.CREATE_EMULATION_PAGE.PACKET_DUPLICATE_PERCENTAGE]
            interface_packet_duplicate_correlation_percentage = interfaces[
                api_constants.CREATE_EMULATION_PAGE.PACKET_DUPLICATE_CORRELATION_PERCENTAGE]
            interface_packet_reorder_percentage = interfaces[
                api_constants.CREATE_EMULATION_PAGE.PACKET_REORDER_PERCENTAGE]
            interface_packet_reorder_correlation_percentage = interfaces[
                api_constants.CREATE_EMULATION_PAGE.PACKET_REORDER_CORRELATION_PERCENTAGE]
            interface_packet_reorder_gap = interfaces[api_constants.CREATE_EMULATION_PAGE.PACKET_REORDER_GAP]
            interface_rate_limit_m_bit = interfaces[api_constants.CREATE_EMULATION_PAGE.RATE_LIMIT_MBIT]
            interface_packet_overhead_bytes = interfaces[api_constants.CREATE_EMULATION_PAGE.PACKET_OVERHEAD_BYTES]
            interface_cell_overhead_bytes = interfaces[api_constants.CREATE_EMULATION_PAGE.CELL_OVERHEAD_BYTES]
            ips_and_network_configs.append(
                (interface_ip, NodeNetworkConfig(
                    interface=interface_physical_interface,
                    limit_packets_queue=interface_limit_packet_queue, packet_delay_ms=interface_packet_delay_ms,
                    packet_delay_jitter_ms=interface_packet_delay_jitter_ms,
                    packet_delay_correlation_percentage=interface_packet_delay_correlation_percentage,
                    packet_delay_distribution=interfaces_packet_delay_distribution,
                    packet_loss_type=interface_packet_loss_type,
                    loss_gemodel_p=interface_loss_gmodel_p,
                    loss_gemodel_r=interface_loss_gmodel_r,
                    loss_gemodel_k=interface_loss_gmodel_k,
                    loss_gemodel_h=interface_loss_gmodel_h,
                    packet_corrupt_percentage=interface_packet_corruption_percentage,
                    packet_corrupt_correlation_percentage=interface_packet_corruption_correlation_percentage,
                    packet_duplicate_percentage=interface_packet_duplication_percentage,
                    packet_duplicate_correlation_percentage=interface_packet_duplicate_correlation_percentage,
                    packet_reorder_percentage=interface_packet_reorder_percentage,
                    packet_reorder_correlation_percentage=interface_packet_reorder_correlation_percentage,
                    packet_reorder_gap=interface_packet_reorder_gap,
                    rate_limit_mbit=interface_rate_limit_m_bit,
                    packet_overhead_bytes=interface_packet_overhead_bytes,
                    cell_overhead_bytes=interface_cell_overhead_bytes
                ))
            )

        node_resource_config = NodeResourcesConfig(
            container_name=container_name,
            num_cpus=container_cpu, available_memory_gb=container_memory,
            ips_and_network_configs=ips_and_network_configs)
        node_resources_configurations.append(node_resource_config)
    resources_config = ResourcesConfig(node_resources_configurations=node_resources_configurations)
    return resources_config


def convert_json_data_to_topology_config(emulation_data: Dict[str, Any]) -> TopologyConfig:
    """
    Converts the json emulation data to the topology config

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: the Topology configuration
    """
    node_configs = []
    emulation_containers = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_CONTAINER]
    for containers in emulation_containers:
        subnetwork_masks = []
        container_name = containers[api_constants.CREATE_EMULATION_PAGE.NAME]
        ips_gw_default_policy_networks = []
        container_interfaces = containers[api_constants.CREATE_EMULATION_PAGE.INTERFACES]
        for interfaces in container_interfaces:
            interface_default_gateway = interfaces[api_constants.CREATE_EMULATION_PAGE.DEFAULT_GATEWAY]
            interface_default_input = interfaces[api_constants.CREATE_EMULATION_PAGE.DEFAULT_INPUT]
            interface_default_output = interfaces[api_constants.CREATE_EMULATION_PAGE.DEFAULT_OUTPUT]
            interface_default_forward = interfaces[api_constants.CREATE_EMULATION_PAGE.DEFAULT_FORWARD]
            interface_ip = interfaces[api_constants.CREATE_EMULATION_PAGE.IP]
            interface_name = interfaces[api_constants.CREATE_EMULATION_PAGE.NAME]
            interface_subnet_mask = interfaces[api_constants.CREATE_EMULATION_PAGE.SUBNET_MASK]
            interface_subnet_prefix = interfaces[api_constants.CREATE_EMULATION_PAGE.SUBNET_PREFIX]
            interface_bit_mask = interfaces[api_constants.CREATE_EMULATION_PAGE.BITMASK]
            subnetwork_masks.append(interface_subnet_mask)
            default_network_firewall_config = DefaultNetworkFirewallConfig(
                ip=interface_ip,
                default_gw=interface_default_gateway,
                default_input=interface_default_input,
                default_output=interface_default_output,
                default_forward=interface_default_forward,
                network=ContainerNetwork(
                    name=interface_name,
                    subnet_mask=interface_subnet_mask,
                    subnet_prefix=interface_subnet_prefix,
                    bitmask=interface_bit_mask
                )
            )
            ips_gw_default_policy_networks.append(default_network_firewall_config)
        node_configs.append(NodeFirewallConfig(
            hostname=container_name,
            ips_gw_default_policy_networks=ips_gw_default_policy_networks,
            output_accept=set([]),
            input_accept=set([]),
            forward_accept=set([]),
            output_drop=set(), input_drop=set(), forward_drop=set(), routes=set()))

        topology = TopologyConfig(node_configs=node_configs,
                                  subnetwork_masks=subnetwork_masks)
        return topology


def convert_json_data_to_traffic_config(emulation_data: Dict[str, Any]) -> TrafficConfig:
    """
    Converts the json emulation data to the traffic config

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: the traffic configuration
    """
    traffic_generators = []
    emulation_containers = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_CONTAINER]
    emulation_time_step_length = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_TIME_STEP_LENGTH]
    client_ip = ""
    client_name = ""
    client_subnet_mask = ""
    client_subnet_prefix = ""
    client_bit_mask = ""
    for containers in emulation_containers:
        container_name = containers[api_constants.CREATE_EMULATION_PAGE.NAME]
        container_interfaces = containers[api_constants.CREATE_EMULATION_PAGE.INTERFACES]
        interface_ip = ""
        interface_name = ""
        interface_subnet_mask = ""
        interface_subnet_prefix = ""
        interface_bit_mask = ""
        for interfaces in container_interfaces:
            interface_ip = interfaces[api_constants.CREATE_EMULATION_PAGE.IP]
            interface_name = interfaces[api_constants.CREATE_EMULATION_PAGE.NAME]
            interface_subnet_prefix = interfaces[api_constants.CREATE_EMULATION_PAGE.SUBNET_PREFIX]
            interface_subnet_mask = interfaces[api_constants.CREATE_EMULATION_PAGE.SUBNET_MASK]
            interface_bit_mask = interfaces[api_constants.CREATE_EMULATION_PAGE.BITMASK]

        traffic_generators.append(NodeTrafficConfig(
            ip=interface_ip, commands=(constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[container_name]
                                       + constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[
                                           constants.TRAFFIC_COMMANDS.GENERIC_COMMANDS]),
            traffic_manager_port=collector_constants.MANAGER_PORTS.TRAFFIC_MANAGER_DEFAULT_PORT,
            traffic_manager_log_file=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_FILE,
            traffic_manager_log_dir=collector_constants.LOG_FILES.TRAFFIC_MANAGER_LOG_DIR,
            traffic_manager_max_workers=collector_constants.GRPC_WORKERS.DEFAULT_MAX_NUM_WORKERS))
        if (api_constants.CREATE_EMULATION_PAGE.CLIENT in container_name):
            client_ip = interface_ip
            client_name = interface_name
            client_subnet_mask = interface_subnet_mask
            client_subnet_prefix = interface_subnet_prefix
            client_bit_mask = interface_bit_mask

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
            name=client_name,
            subnet_mask=client_subnet_mask,
            subnet_prefix=client_subnet_prefix,
            bitmask=client_bit_mask
        )],
        ip=client_ip,
        client_manager_port=collector_constants.MANAGER_PORTS.CLIENT_MANAGER_DEFAULT_PORT,
        client_time_step_len_seconds=emulation_time_step_length,
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


def convert_json_data_to_users_config(emulation_data: Dict[str, Any]) -> UsersConfig:
    """
    Converts the json emulation data to the users config

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: generates the UsersConfig
    """
    emulation_containers = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_CONTAINER]
    users = []
    interface_ip = "0.0.0.0"
    for containers in emulation_containers:
        container_users = containers[api_constants.CREATE_EMULATION_PAGE.USERS]
        container_interfaces = containers[api_constants.CREATE_EMULATION_PAGE.INTERFACES]
        for interfaces in container_interfaces:
            # interface_name = interfaces[api_constants.CREATE_EMULATION_PAGE.NAME]
            interface_ip = interfaces[api_constants.CREATE_EMULATION_PAGE.IP]
        all_users = []
        for user in container_users:
            user_name = user[api_constants.CREATE_EMULATION_PAGE.USER_NAME]
            user_pw = user[api_constants.CREATE_EMULATION_PAGE.PW]
            user_access = user[api_constants.CREATE_EMULATION_PAGE.ROOT]
            all_users.append(User(username=user_name, pw=user_pw, root=user_access))
        users.append(NodeUsersConfig(ip=interface_ip, users=all_users))

    users_conf = UsersConfig(users_configs=users)
    return users_conf


def convert_json_data_to_vulns_config(emulation_data: Dict[str, Any]) -> VulnerabilitiesConfig:
    """
    Converts the json emulation data to the vulnerabilities config

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: the vulnerability config
    """
    emulation_containers = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_CONTAINER]
    vulns = []
    for containers in emulation_containers:
        container_vulns = containers[api_constants.CREATE_EMULATION_PAGE.VULNS]
        for vuln in container_vulns:
            vuln_name = vuln[api_constants.CREATE_EMULATION_PAGE.VULN_NAME]
            vuln_type = vuln[api_constants.CREATE_EMULATION_PAGE.VULN_TYPE]
            vuln_service_name = vuln[api_constants.CREATE_EMULATION_PAGE.VULN_SERVICE]
            # vuln_service_protocol = vuln[api_constants.CREATE_EMULATION_PAGE.VULN_SERVICE][
            #     api_constants.CREATE_EMULATION_PAGE.PROTOCOL]
            # vuln_service_protocol = TransportProtocol(int(vuln_service_protocol))
            # vuln_service_port = vuln[api_constants.CREATE_EMULATION_PAGE.VULN_SERVICE][
            #     api_constants.CREATE_EMULATION_PAGE.PORT]
            # vuln_service_ip = vuln[api_constants.CREATE_EMULATION_PAGE.VULN_SERVICE][
            #     api_constants.CREATE_EMULATION_PAGE.SERVICE_IP]
            vuln_root_access = vuln[api_constants.CREATE_EMULATION_PAGE.VULN_ROOT]
            vuln_credentials = vuln[api_constants.CREATE_EMULATION_PAGE.VULN_CREDENTIALS]
            cred = []
            for credentials in vuln_credentials:
                cred.append(Credential(username=credentials[api_constants.CREATE_EMULATION_PAGE.VULN_CRED_USERNAME],
                                       pw=credentials[api_constants.CREATE_EMULATION_PAGE.VULN_CRED_PW],
                                       root=credentials[api_constants.CREATE_EMULATION_PAGE.VULN_CRED_ROOT],
                                       service=vuln_service_name,
                                       protocol=TransportProtocol.TCP,
                                       port=80))

            vulns.append(NodeVulnerabilityConfig(
                name=vuln_name,
                # *** I think we can also use service ip instead of interface ip, it will be the same.
                # If it is not true we can use interface ip
                ip="0.0.0.0",
                vuln_type=vuln_type,
                # *** We should define credentials in the front end
                credentials=cred,
                # *** We should define cvss in the front end
                cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
                cve=None,
                root=vuln_root_access, port=80,
                protocol=TransportProtocol.TCP, service=vuln_service_name))
    vulns_config = VulnerabilitiesConfig(node_vulnerability_configs=vulns)
    return vulns_config


def convert_json_data_to_services_config(emulation_data: Dict[str, Any]) -> ServicesConfig:
    """
    Converts the json emulation data to the services config

    :param emulation_data: the emulation data in JSON format received from front-end
    :return: The services configuration
    """
    emulation_containers = emulation_data[api_constants.CREATE_EMULATION_PAGE.EMULATION_CONTAINER]
    services_configs = []
    service_ip = "0.0.0.0"
    for containers in emulation_containers:
        container_services = containers[api_constants.CREATE_EMULATION_PAGE.SERVICES]
        services = []
        for service in container_services:
            service_name = service[api_constants.CREATE_EMULATION_PAGE.NAME]
            service_protocol = service[api_constants.CREATE_EMULATION_PAGE.PROTOCOL]
            service_port = service[api_constants.CREATE_EMULATION_PAGE.PORT]
            service_ip = service[api_constants.CREATE_EMULATION_PAGE.SERVICE_IP]
            services.append(NetworkService(protocol=service_protocol, port=service_port,
                                           name=service_name, credentials=[]))
    # *** for NodeServicesConfig the ip can be also the interface ip. I think it should be the same unless the node
    # has two or more interfaces
    services_configs.append(NodeServicesConfig(
        ip=service_ip,
        services=[
            NetworkService(protocol=TransportProtocol.TCP, port=constants.SSH.DEFAULT_PORT,
                           name=constants.SSH.SERVICE_NAME, credentials=[])
        ]
    ))

    service_cfg = ServicesConfig(
        services_configs=services_configs
    )
    return service_cfg
