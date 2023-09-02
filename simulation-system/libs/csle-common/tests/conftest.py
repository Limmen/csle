import time
import pytest
import csle_collector.constants.constants as collector_constants
import csle_common.constants.constants as constants
from csle_collector.client_manager.dao.client import Client
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_config.beats_config import BeatsConfig
from csle_common.dao.emulation_config.client_population_config import ClientPopulationConfig
from csle_common.dao.emulation_config.cluster_config import ClusterConfig
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_common.dao.emulation_config.docker_stats_manager_config import DockerStatsManagerConfig
from csle_common.dao.emulation_config.elk_config import ElkConfig
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.dao.emulation_config.flag import Flag
from csle_common.dao.emulation_config.flags_config import FlagsConfig
from csle_common.dao.emulation_config.host_manager_config import HostManagerConfig
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic
from csle_common.dao.emulation_config.network_service import NetworkService
from csle_common.dao.emulation_config.node_beats_config import NodeBeatsConfig
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.node_flags_config import NodeFlagsConfig
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.node_services_config import NodeServicesConfig
from csle_common.dao.emulation_config.node_traffic_config import NodeTrafficConfig
from csle_common.dao.emulation_config.node_users_config import NodeUsersConfig
from csle_common.dao.emulation_config.node_vulnerability_config import NodeVulnerabilityConfig
from csle_common.dao.emulation_config.ossec_ids_manager_config import OSSECIDSManagerConfig
from csle_common.dao.emulation_config.ovs_config import OVSConfig
from csle_common.dao.emulation_config.ovs_switch_config import OvsSwitchConfig
from csle_common.dao.emulation_config.packet_delay_distribution_type import PacketDelayDistributionType
from csle_common.dao.emulation_config.packet_loss_type import PacketLossType
from csle_common.dao.emulation_config.resources_config import ResourcesConfig
from csle_common.dao.emulation_config.sdn_controller_config import SDNControllerConfig
from csle_common.dao.emulation_config.sdn_controller_type import SDNControllerType
from csle_common.dao.emulation_config.services_config import ServicesConfig
from csle_common.dao.emulation_config.snort_ids_manager_config import SnortIDSManagerConfig
from csle_common.dao.emulation_config.topology_config import TopologyConfig
from csle_common.dao.emulation_config.traffic_config import TrafficConfig
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.user import User
from csle_common.dao.emulation_config.users_config import UsersConfig
from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.emulation_config.vulnerability_type import VulnType
from csle_common.dao.datasets.statistics_dataset import StatisticsDataset
from csle_common.dao.datasets.traces_dataset import TracesDataset
from csle_common.dao.docker.docker_container_metadata import DockerContainerMetadata
from csle_common.dao.docker.docker_env_metadata import DockerEnvMetadata
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import EmulationDefenderActionOutcome
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_config import EmulationAttackerActionConfig
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_config import EmulationDefenderActionConfig
from csle_common.dao.emulation_action_result.nikto_scan_result import NiktoScanResult
from csle_common.dao.emulation_action_result.nikto_vuln import NiktoVuln
from csle_common.dao.emulation_action_result.nmap_brute_credentials import NmapBruteCredentials
from csle_common.dao.emulation_action_result.nmap_hop import NmapHop
from csle_common.dao.emulation_action_result.nmap_http_enum import NmapHttpEnum
from csle_common.dao.emulation_action_result.nmap_http_grep import NmapHttpGrep
from csle_common.dao.emulation_action_result.nmap_os import NmapOs
from csle_common.dao.emulation_action_result.nmap_port import NmapPort
from csle_common.dao.emulation_action_result.nmap_port_status import NmapPortStatus
from csle_common.dao.emulation_action_result.nmap_host_status import NmapHostStatus
from csle_common.dao.emulation_action_result.nmap_vulscan import NmapVulscan
from csle_common.dao.emulation_action_result.nmap_trace import NmapTrace
from csle_common.dao.emulation_action_result.nmap_vuln import NmapVuln
from csle_common.dao.emulation_action_result.nmap_host_result import NmapHostResult
from csle_common.dao.emulation_action_result.nmap_scan_result import NmapScanResult


@pytest.fixture
def example_credential() -> Credential:
    """
    Fixture that returns an example Credential object

    :return: an example Credential object
    """
    return Credential(username="testuser", pw="testpw", port=2911, protocol=TransportProtocol.UDP,
                      service="myservice", root=False)


@pytest.fixture
def example_config() -> Config:
    """
    Help function that returns a config class when making fixtures and testing

    :return: Config class
    """
    c_node = ClusterNode(ip="123.456.78.99", leader=True, cpus=1, gpus=2, RAM=3)
    config = Config(
        management_admin_username_default="admin",
        management_admin_password_default="admin",
        management_admin_first_name_default="Admin",
        management_admin_last_name_default="Adminson",
        management_admin_email_default="admin@CSLE.com",
        management_admin_organization_default="CSLE",
        management_guest_username_default="guest",
        management_guest_password_default="guest",
        management_guest_first_name_default="Guest",
        management_guest_last_name_default="Guestson",
        management_guest_email_default="guest@CSLE.com",
        management_guest_organization_default="CSLE",
        ssh_admin_username="null",
        ssh_admin_password="null",
        ssh_agent_username="null",
        ssh_agent_password="null",
        metastore_user="null",
        metastore_password="null",
        metastore_database_name="null",
        metastore_ip="null",
        node_exporter_port=1,
        grafana_port=1,
        management_system_port=1,
        cadvisor_port=1,
        prometheus_port=1,
        node_exporter_pid_file="null",
        pgadmin_port=1,
        csle_mgmt_webapp_pid_file="null",
        docker_stats_manager_log_file="null",
        docker_stats_manager_log_dir="null",
        docker_stats_manager_port=1,
        docker_stats_manager_max_workers=1,
        docker_stats_manager_outfile="null",
        docker_stats_manager_pidfile="null",
        prometheus_pid_file="null",
        prometheus_log_file="null",
        prometheus_config_file="null",
        default_log_dir="null",
        cluster_config=ClusterConfig([c_node]),
        node_exporter_log_file="null",
        allow_registration=True,
        grafana_username="null",
        grafana_password="null",
        pgadmin_username="null",
        pgadmin_password="null",
        postgresql_log_dir="null",
        nginx_log_dir="null",
        flask_log_file="null",
        cluster_manager_log_file="null",
    )
    return config


@pytest.fixture
def example_emulation_env_config() -> EmulationEnvConfig:
    """
    Fixture that returns an example EmulationEnvConfig object

    :return: example EmulationEnvConfig object
    """
    c_net = ContainerNetwork(name="Network1", subnet_mask="Subnet1", bitmask="null",
                             subnet_prefix="null", interface="eth0")
    nc_config = NodeContainerConfig(name="Container1",
                                    ips_and_networks=[("123.456.78.99", c_net)],
                                    version="null", level="null",
                                    restart_policy="JDoePolicy", suffix="null",
                                    os="null", execution_ip_first_octet=-1,
                                    docker_gw_bridge_ip="123.456.78.99",
                                    physical_host_ip="123.456.78.99")
    c_config = ContainersConfig(containers=[nc_config],
                                agent_ip="123.456.78.99",
                                router_ip="123.456.78.99",
                                networks=[c_net],
                                ids_enabled=False,
                                vulnerable_nodes=None,
                                agent_reachable_nodes=None)
    n_u_config = NodeUsersConfig(ip="123.456.78.99",
                                 users=[User(username="JDoe", pw="JDoe", root=True)],
                                 docker_gw_bridge_ip="null",
                                 physical_host_ip="123.456.78.99")
    u_config = UsersConfig(users_configs=[n_u_config])
    flag = Flag(name="JohnDoe", dir="null", id=1, path="null", requires_root=False, score=1)
    nf_conf = NodeFlagsConfig(ip="123.456.78.99", flags=[flag], docker_gw_bridge_ip="null",
                              physical_host_ip="123.456.78.99")
    cred = Credential(username="JDoe", pw="JDoe", port=-1, protocol=None, service="null", root=False)
    nv_conf = NodeVulnerabilityConfig(ip="123.456.78.99", vuln_type=VulnType.WEAK_PW, name="JohnDoe", port=1,
                                      protocol=TransportProtocol.TCP, credentials=[cred], cvss=2.0,
                                      cve=None, service="null", root=False, docker_gw_bridge_ip="123.456.78.99",
                                      physical_host_ip="123.456.78.99")
    dfn_conf = DefaultNetworkFirewallConfig(ip=None, default_gw="null", default_input="null",
                                            default_output="null", default_forward="null", network=c_net)
    n_fire_conf = NodeFirewallConfig(ips_gw_default_policy_networks=[dfn_conf],
                                     hostname="JohnDoe", output_accept={"null"},
                                     input_accept={"null"}, forward_accept={"null"},
                                     output_drop={"null"}, input_drop={"null"},
                                     forward_drop={"null"}, routes={("null", "null")},
                                     docker_gw_bridge_ip="123.456.78.99",
                                     physical_host_ip="123.456.78.99")
    top_conf = TopologyConfig(node_configs=[n_fire_conf],
                              subnetwork_masks=["null"])
    node_traf_conf = NodeTrafficConfig(ip="123.456.78.99",
                                       commands=["JDoeCommands"],
                                       traffic_manager_log_file="null",
                                       traffic_manager_log_dir="null",
                                       traffic_manager_max_workers=5,
                                       traffic_manager_port=50043,
                                       docker_gw_bridge_ip="123.456.78.99",
                                       physical_host_ip="123.456.78.99")
    nn_config = NodeNetworkConfig(interface=constants.NETWORKING.ETH0, limit_packets_queue=30000,
                                  packet_delay_ms=0.1, packet_delay_jitter_ms=0.025,
                                  packet_delay_correlation_percentage=25.5,
                                  packet_delay_distribution=PacketDelayDistributionType.PARETONORMAL,
                                  packet_loss_type=PacketLossType.GEMODEL,
                                  packet_loss_rate_random_percentage=2.3,
                                  packet_loss_random_correlation_percentage=25.6,
                                  loss_state_markov_chain_p13=0.1,
                                  loss_state_markov_chain_p31=0.1,
                                  loss_state_markov_chain_p32=0.1,
                                  loss_state_markov_chain_p23=0.1,
                                  loss_state_markov_chain_p14=0.1,
                                  loss_gemodel_p=0.0001,
                                  loss_gemodel_r=0.999,
                                  loss_gemodel_h=0.0001,
                                  loss_gemodel_k=0.9999,
                                  packet_corrupt_percentage=0.00001,
                                  packet_corrupt_correlation_percentage=25.7,
                                  packet_duplicate_percentage=0.00001,
                                  packet_duplicate_correlation_percentage=25,
                                  packet_reorder_percentage=0.0025,
                                  packet_reorder_correlation_percentage=25,
                                  packet_reorder_gap=5,
                                  rate_limit_mbit=100,
                                  packet_overhead_bytes=0,
                                  cell_overhead_bytes=0)
    node_res_conf = NodeResourcesConfig(container_name="Johndoe",
                                        num_cpus=5, available_memory_gb=5,
                                        ips_and_network_configs=[("null", nn_config)],
                                        docker_gw_bridge_ip="123.456.78.99",
                                        physical_host_ip="123.456.78.99")
    client = Client(id=1, workflow_distribution=[1.0],
                    arrival_config=ConstantArrivalConfig(lamb=1.0),
                    mu=4, exponential_service_time=False)
    wf_m_chain = WorkflowMarkovChain(transition_matrix=[[1.0]], initial_state=1, id=1)
    wf_service = WorkflowService(ips_and_commands=[("null", ["null"])], id=1)
    wf_config = WorkflowsConfig(workflow_markov_chains=[wf_m_chain],
                                workflow_services=[wf_service])
    cp_config = ClientPopulationConfig(ip="123.456.78.99",
                                       networks=[c_net],
                                       client_manager_port=5,
                                       client_manager_log_file="null",
                                       client_manager_log_dir="null",
                                       client_manager_max_workers=5,
                                       clients=[client],
                                       workflows_config=wf_config,
                                       client_time_step_len_seconds=1,
                                       docker_gw_bridge_ip="null",
                                       physical_host_ip="123.456.78.99")
    res_conf = ResourcesConfig(node_resources_configurations=[node_res_conf])
    traf_conf = TrafficConfig(node_traffic_configs=[node_traf_conf],
                              client_population_config=cp_config)
    kafka_top = KafkaTopic(name="JohhnDoe", num_partitions=3, num_replicas=5, attributes=["null"],
                           retention_time_hours=3)
    kafka_conf = KafkaConfig(container=nc_config, resources=node_res_conf, firewall_config=n_fire_conf,
                             topics=[kafka_top], kafka_manager_log_file="null", kafka_manager_log_dir="null",
                             kafka_manager_max_workers=9, kafka_port=9092, kafka_port_external=9292,
                             time_step_len_seconds=15, kafka_manager_port=50051, version="0.0.1")
    network_service = NetworkService(protocol=TransportProtocol.TCP, port=1, name="JohnDoe", credentials=None)
    n_service_conf = NodeServicesConfig(ip="123.456.78.99", services=[network_service])
    service_conf = ServicesConfig(services_configs=[n_service_conf])
    e_a_action = EmulationAttackerAction(id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
                                         name="JohnDoe",
                                         cmds=["JohnDoeCommands"],
                                         type=EmulationAttackerActionType.RECON, descr="null",
                                         ips=["null"], index=10,
                                         action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                         vulnerability="null", alt_cmds=["null"], backdoor=False,
                                         execution_time=0.0, ts=1.1)
    ovs_switch = OvsSwitchConfig(container_name="JohnDoe", ip="123.456.78.99", openflow_protocols=["null"],
                                 controller_ip="123.456.78.99", controller_port=2,
                                 controller_transport_protocol="null",
                                 docker_gw_bridge_ip="null", physical_host_ip="123.456.78.99")
    sdc_ctrl = SDNControllerConfig(container=nc_config, resources=node_res_conf, firewall_config=n_fire_conf,
                                   controller_port=4, controller_type=SDNControllerType.RYU,
                                   controller_module_name="null", controller_web_api_port=5,
                                   manager_log_file="null", manager_log_dir="null", manager_max_workers=10,
                                   time_step_len_seconds=15, version="0.0.1", manager_port=50042)
    host_mng = HostManagerConfig(host_manager_log_file="null", host_manager_log_dir="null",
                                 host_manager_max_workers=5, time_step_len_seconds=15, host_manager_port=50049,
                                 version="0.0.1")
    snort_mng = SnortIDSManagerConfig(snort_ids_manager_log_file="null", snort_ids_manager_log_dir="null",
                                      snort_ids_manager_max_workers=5, time_step_len_seconds=15,
                                      snort_ids_manager_port=50048, version="0.0.1")
    ossec_mng = OSSECIDSManagerConfig(ossec_ids_manager_log_file="null", ossec_ids_manager_log_dir="null",
                                      ossec_ids_manager_max_workers=5, time_step_len_seconds=15,
                                      ossec_ids_manager_port=50047, version="0.0.1")
    docker_mng = DockerStatsManagerConfig(docker_stats_manager_log_file="null",
                                          docker_stats_manager_log_dir="null",
                                          docker_stats_manager_max_workers=5, time_step_len_seconds=15,
                                          docker_stats_manager_port=50046, version="0.0.1")
    elk = ElkConfig(container=nc_config, resources=node_res_conf, firewall_config=n_fire_conf,
                    elk_manager_log_file="null", elk_manager_log_dir="null", elk_manager_max_workers=5,
                    elastic_port=9200, kibana_port=5601, logstash_port=5044, time_step_len_seconds=15,
                    elk_manager_port=50045, version="0.0.1")
    nb_config = NodeBeatsConfig(ip="123.456.78.99", log_files_paths=["null"], filebeat_modules=["null"],
                                metricbeat_modules=["null"], heartbeat_hosts_to_monitor=["null"],
                                kafka_input=False, start_filebeat_automatically=False,
                                start_packetbeat_automatically=False, start_metricbeat_automatically=False,
                                start_heartbeat_automatically=False)
    beats = BeatsConfig(node_beats_configs=[nb_config], num_elastic_shards=3, reload_enabled=True)
    em_env = EmulationEnvConfig(name="Johndoe", containers_config=c_config, users_config=u_config,
                                flags_config=FlagsConfig(node_flag_configs=[nf_conf]),
                                vuln_config=VulnerabilitiesConfig(node_vulnerability_configs=[nv_conf]),
                                topology_config=top_conf, traffic_config=traf_conf, resources_config=res_conf,
                                kafka_config=kafka_conf, services_config=service_conf, descr="null",
                                static_attacker_sequences={"E_A_action": [e_a_action]},
                                ovs_config=OVSConfig(switch_configs=[ovs_switch]),
                                sdn_controller_config=sdc_ctrl, host_manager_config=host_mng,
                                snort_ids_manager_config=snort_mng, ossec_ids_manager_config=ossec_mng,
                                docker_stats_manager_config=docker_mng, elk_config=elk, beats_config=beats,
                                level=5, version="null", execution_id=10,
                                csle_collector_version=collector_constants.LATEST_VERSION,
                                csle_ryu_version=collector_constants.LATEST_VERSION)
    return em_env


@pytest.fixture
def example_emulation_execution(get_ex_em_env: EmulationEnvConfig) -> EmulationExecution:
    """
    Fixture that returns an example EmulationExecution object

    :param get_ex_em_env: fixture returning an example EmulationEnvConfig
    :return: an example EmulationExecution object
    """
    em_env = get_ex_em_env
    em_ex = EmulationExecution(emulation_name="JohbnDoeEmulation", timestamp=1.5, ip_first_octet=-1,
                               emulation_env_config=em_env, physical_servers=["JohnDoeServer"])
    return em_ex


@pytest.fixture
def example_traces_dataset() -> TracesDataset:
    """
    Fixture that returns an example TracesDataset object

    :return: an example TracesDataset object
    """
    return TracesDataset(name="test_dataset", description="test_descr", download_count=100,
                            file_path="test_path", url="test_url", date_added=time.time(),
                            size_in_gb=5, compressed_size_in_gb=17, citation="test_citation",
                            num_files=50, file_format="json", added_by="testadded", columns="col1,col2",
                            data_schema={}, num_attributes_per_time_step=10, num_traces=15)


@pytest.fixture
def example_statistics_dataset() -> StatisticsDataset:
    """
    Fixture that returns an example StatisticsDataset object

    :return: an example StatisticsDataset object
    """
    return StatisticsDataset(name="test_dataset", description="test_descr", download_count=100,
                             file_path="test_path", url="test_url", date_added=time.time(), num_measurements=100,
                             num_metrics=10, size_in_gb=5, compressed_size_in_gb=17, citation="test_citation",
                             num_files=50, file_format="json", added_by="testadded", conditions="cond1,cond2",
                             metrics="metric1,metric2", num_conditions=10)

@pytest.fixture
def example_docker_container_metadata() -> DockerContainerMetadata:
    """
    Fixture that returns an example DockerContainerMetadata object

    :return: an example DockerContainerMetadata object
    """
    return DockerContainerMetadata(
        name="cont1", status="test", short_id="shortid", image_short_id="imgshort", image_tags=[], id="testid",
        created="1 Aug", ip="testIp", network_id=5, gateway="gw", mac="mymac", ip_prefix_len=16,
        name2="secondname", level="level1", hostname="host1", image_name="img1", net="mynet", dir="mydir",
        config_path="mycfg", container_handle=None, kafka_container="kafkacont", emulation="myem")


@pytest.fixture
def example_docker_env_metadata(example_docker_container_metadata: DockerContainerMetadata) \
        -> DockerEnvMetadata:
    """
    Fixture that returns an example DockerEnvMetadata object

    :param example_docker_container_metadata: an example DAO
    :return: an example DockerEnvMetadata object
    """
    return DockerEnvMetadata(
        containers=[example_docker_container_metadata], name="myenv", subnet_prefix="myprefix", subnet_mask="mymask",
        level="mylevel", config=None, kafka_config=None)


@pytest.fixture
def example_emulation_attacker_action() -> EmulationAttackerAction:
    """
    Fixture that returns an example DockerContainerMetadata object

    :return: an example EmulationAttackerAction object
    """
    return EmulationAttackerAction(
        id=EmulationAttackerActionId.CONTINUE, name="test", cmds=["cmd1"],
        type=EmulationAttackerActionType.CONTINUE, descr="testtest", ips=["ip1"], index=0,
        action_outcome=EmulationAttackerActionOutcome.CONTINUE, vulnerability="test", alt_cmds=["altcmd1"],
        backdoor=False, execution_time=0.0, ts=0.0
    )


@pytest.fixture
def example_emulation_attacker_action_config(example_emulation_attacker_action: EmulationAttackerAction) \
        -> EmulationAttackerActionConfig:
    """
    Fixture that returns an example EmulationAttackerActionConfig object

    :param example_emulation_attacker_action: an example DAO
    :return: an example EmulationAttackerActionConfig object
    """
    return EmulationAttackerActionConfig(
        num_indices=10, actions=[example_emulation_attacker_action],
        nmap_action_ids=[EmulationAttackerActionId.NMAP_VULNERS_ALL],
        network_service_action_ids=[EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST],
        shell_action_ids=[EmulationAttackerActionId.CVE_2015_1427_EXPLOIT],
        nikto_action_ids=[EmulationAttackerActionId.NIKTO_WEB_HOST_SCAN],
        masscan_action_ids=[EmulationAttackerActionId.MASSCAN_ALL_SCAN],
        stopping_action_ids=[EmulationAttackerActionId.STOP, EmulationAttackerActionId.CONTINUE])


@pytest.fixture
def example_emulation_defender_action() -> EmulationDefenderAction:
    """
    Fixture that returns an example EmulationDefenderAction object

    :return: an example EmulationDefenderAction object
    """
    return EmulationDefenderAction(
        id=EmulationDefenderActionId.STOP, name="testname", cmds=["cmd1"],
        type=EmulationDefenderActionType.CONTINUE, ips=["ip1", "ip2"], index=0,
        action_outcome=EmulationDefenderActionOutcome.CONTINUE, alt_cmds=["alt1"], execution_time=0.0,
        ts=0.0, descr="testdescr")


@pytest.fixture
def example_emulation_defender_action_config(example_emulation_defender_action: EmulationDefenderAction) \
        -> EmulationDefenderActionConfig:
    """
    Fixture that returns an example EmulationAttackerActionConfig object

    :param example_emulation_defender_action: an example DAO
    :return: an example EmulationAttackerActionConfig object
    """
    return EmulationDefenderActionConfig(
        num_indices=10, actions=[example_emulation_defender_action],
        stopping_action_ids=[EmulationDefenderActionId.STOP, EmulationDefenderActionId.CONTINUE],
        multiple_stop_actions=[],
        multiple_stop_actions_ids=[EmulationDefenderActionId.STOP, EmulationDefenderActionId.CONTINUE])


@pytest.fixture
def example_nikto_vuln() -> NiktoVuln:
    """
    Fixture that returns an example NiktoVuln object

    :return: an example NiktoVuln object
    """
    return NiktoVuln(id="testid", osvdb_id=15, method="test", iplink="test2", namelink="test3", uri="test4",
                     description="test5")


@pytest.fixture
def example_nikto_scan_result(example_nikto_vuln: NiktoVuln) -> NiktoScanResult:
    """
    Fixture that returns an example NiktoScanResult object

    :param example_nikto_vuln: an example DAO
    :return: an example NiktoScanResult object
    """
    return NiktoScanResult(port=3333, ip="192.168.1.1", sitename="test", vulnerabilities=[example_nikto_vuln])


@pytest.fixture
def example_nmap_brute_credentials() -> NmapBruteCredentials:
    """
    Fixture that returns an example NmapBruteCredentials object

    :return: an example NmapBruteCredentials object
    """
    return NmapBruteCredentials(
        username="testuser", pw="testpw", state="teststate", port=3333, protocol=TransportProtocol.TCP,
        service="testservice")


@pytest.fixture
def example_nmap_hop() -> NmapHop:
    """
    Fixture that returns an example NmapHop object

    :return: an example NmapHop object
    """
    return NmapHop(ttl=20, ipaddr="testip", rtt=0.0, host="testhost")


@pytest.fixture
def example_nmap_http_enum() -> NmapHttpEnum:
    """
    Fixture that returns an example NmapHttpEnum object

    :return: an example NmapHttpEnum object
    """
    return NmapHttpEnum(output="testout")


@pytest.fixture
def example_nmap_http_grep() -> NmapHttpGrep:
    """
    Fixture that returns an example NmapHttpEnum object

    :return: an example NmapHttpEnum object
    """
    return NmapHttpGrep(output="testout")


@pytest.fixture
def example_nmap_vulscan() -> NmapVulscan:
    """
    Fixture that returns an example NmapVulscan object

    :return: an example NmapVulscan object
    """
    return NmapVulscan(output="testout")


@pytest.fixture
def example_nmap_os() -> NmapOs:
    """
    Fixture that returns an example NmapOs object

    :return: an example NmapOs object
    """
    return NmapOs(name="testosName", vendor="osvendor", osfamily="osfam", accuracy=5)


@pytest.fixture
def example_nmap_port(example_nmap_http_grep: NmapHttpGrep, example_nmap_http_enum: NmapHttpEnum,
                      example_nmap_vulscan: NmapVulscan) -> NmapPort:
    """
    Fixture that returns an example NmapPort object

    :param example_nmap_http_grep: an example DAO
    :param example_nmap_http_enum: an example DAO
    :param example_nmap_vulscan: an example DAO
    :return: an example NmapPort object
    """
    return NmapPort(port_id=1, protocol=TransportProtocol.UDP, status=NmapPortStatus.UP,
                    service_version="testservice", http_enum=example_nmap_http_enum, http_grep=example_nmap_http_grep,
                    service_fp="test_fp", vulscan=example_nmap_vulscan, service_name="testervicename")


@pytest.fixture
def example_nmap_trace(example_nmap_hop: NmapHop) -> NmapTrace:
    """
    Fixture that returns an example NmapTrace object

    :param example_nmap_hop: an example DAO
    :return: an example NmapTrace object
    """
    return NmapTrace(hops=[example_nmap_hop])


@pytest.fixture
def example_nmap_vuln(example_credential: Credential) -> NmapVuln:
    """
    Fixture that returns an example NmapVuln object

    :param example_credential: an example DAO
    :return: an example NmapVuln object
    """
    return NmapVuln(name="vuln_name", port=4443, protocol=TransportProtocol.TCP, cvss=0.1,
                    service="testservice", credentials=[example_credential])


@pytest.fixture
def example_nmap_host_result(example_nmap_port: NmapPort, example_nmap_os: NmapOs,
                             example_nmap_vuln: NmapVuln,
                             example_nmap_brute_credentials: NmapBruteCredentials,
                             example_nmap_trace: NmapTrace) -> NmapHostResult:
    """
    Fixture that returns an example NmapHostResult object

    :param example_nmap_port: an example DAO
    :param example_nmap_os: an example DAO
    :param example_nmap_vuln: an example DAO
    :param example_nmap_brute_credentials: an example DAO
    :param example_nmap_trace: an example DAO
    :return: an example NmapHostResult object
    """
    return NmapHostResult(
        status=NmapHostStatus.UP, ips=["172.151.51.2"], mac_addr="00-B0-D0-63-C2-26", hostnames=["testhost"],
        ports=[example_nmap_port], os=example_nmap_os, os_matches=[example_nmap_os],
        vulnerabilities=[example_nmap_vuln], credentials=[example_nmap_brute_credentials], trace=example_nmap_trace)


@pytest.fixture
def example_nmap_scan_result(example_nmap_host_result: NmapHostResult) -> NmapScanResult:
    """
    Fixture that returns an example NmapScanResult object

    :param example_nmap_host_result: an example DAO
    :return: an example NmapScanResult object
    """
    return NmapScanResult(hosts=[example_nmap_host_result], ips=["192.168.5.1"])