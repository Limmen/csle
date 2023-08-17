from typing import Any, Dict
import json
import csle_collector.constants.constants as collector_constants
import csle_common.constants.constants as constants
import pytest
import pytest_mock
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.client import Client
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_config.beats_config import BeatsConfig
from csle_common.dao.emulation_config.client_population_config import ClientPopulationConfig
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
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesLogsSuite:
    """
    Test suite for /login resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def csle_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_csle_log_files function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_csle_log_files(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}": 654321}

        get_csle_log_files_mocker = mocker.MagicMock(side_effect=get_csle_log_files)
        return get_csle_log_files_mocker

    @pytest.fixture
    def dsm_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_docker_statsmanager_logs function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_docker_statsmanager_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}": 654321}

        get_docker_statsmanager_logs_mocker = mocker.MagicMock(side_effect=get_docker_statsmanager_logs)
        return get_docker_statsmanager_logs_mocker

    @pytest.fixture
    def prom_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_prometheus_logs function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_prometheus_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE}": 654321}

        get_prometheus_logs_mocker = mocker.MagicMock(side_effect=get_prometheus_logs)
        return get_prometheus_logs_mocker

    @pytest.fixture
    def nginx_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_nginx_logs function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_nginx_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.NGINX_RESOURCE}": 654321}

        get_nginx_logs_mocker = mocker.MagicMock(side_effect=get_nginx_logs)
        return get_nginx_logs_mocker

    @pytest.fixture
    def postgresql_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_postgresql_logs function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_postgresql_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.POSTGRESQL_RESOURCE}": 654321}

        get_postgresql_logs_mocker = mocker.MagicMock(side_effect=get_postgresql_logs)
        return get_postgresql_logs_mocker

    @pytest.fixture
    def flask_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_flask_logs function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_flask_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.FLASK_RESOURCE}": 654321}

        get_flask_logs_mocker = mocker.MagicMock(side_effect=get_flask_logs)
        return get_flask_logs_mocker

    @pytest.fixture
    def cluster_manager_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_cluster_manager_logs function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_cluster_manager_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.CLUSTERMANAGER_RESOURCE}": 654321}

        get_cluster_manager_logs_mocker = mocker.MagicMock(side_effect=get_cluster_manager_logs)
        return get_cluster_manager_logs_mocker

    @pytest.fixture
    def docker_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_docker_logs function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_docker_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.DOCKER_RESOURCE}": 654321}

        get_docker_logs_mocker = mocker.MagicMock(side_effect=get_docker_logs)
        return get_docker_logs_mocker

    @pytest.fixture
    def container_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_ryu_controller_logs function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_ryu_controller_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE}": 654321}

        get_ryu_controller_logs_mocker = mocker.MagicMock(side_effect=get_ryu_controller_logs)
        return get_ryu_controller_logs_mocker

    @pytest.fixture
    def client_manager_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_client_manager function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_client_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.CLIENT_MANAGER_SUBRESOURCE}": 654321}

        get_client_manager_logs_mocker = mocker.MagicMock(side_effect=get_client_manager_logs)
        return get_client_manager_logs_mocker

    @pytest.fixture
    def kafka_manager_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_kafka_manager function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_kafka_manager_logs(ip: str, port: int, emulation, ip_first_octet: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}": 654321}

        get_kafka_manager_logs_mocker = mocker.MagicMock(side_effect=get_kafka_manager_logs)
        return get_kafka_manager_logs_mocker

    @pytest.fixture
    def kafka_logs(self, mocker):
        """
        Pytest fixture for mocking the get_kafka_logs function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_kafka_logs(ip: str, port: int, emulation: str, ip_first_octet: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}": 654321}

        get_kafka_logs_mocker = mocker.MagicMock(side_effect=get_kafka_logs)
        return get_kafka_logs_mocker

    @pytest.fixture
    def snort_ids_manager_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_snort_ids_manager_logs function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_snort_ids_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: int) \
                -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}": 654321}

        get_snort_ids_manager_logs_mocker = mocker.MagicMock(side_effect=get_snort_ids_manager_logs)
        return get_snort_ids_manager_logs_mocker

    @pytest.fixture
    def snort_ids_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_snort_ids_logs function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_snort_ids_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}": 654321}

        get_snort_ids_logs_mocker = mocker.MagicMock(side_effect=get_snort_ids_logs)
        return get_snort_ids_logs_mocker

    @pytest.fixture
    def ossec_ids_manager_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_ossec_ids_manager_logs function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_ossec_ids_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MANAGER_SUBRESOURCE}": 654321}

        get_ossec_ids_manager_logs_mocker = mocker.MagicMock(side_effect=get_ossec_ids_manager_logs)
        return get_ossec_ids_manager_logs_mocker

    @pytest.fixture
    def ossec_ids_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_ossec_ids_logs function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_ossec_ids_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_SUBRESOURCE}": 654321}

        get_ossec_ids_logs_mocker = mocker.MagicMock(side_effect=get_ossec_ids_logs)
        return get_ossec_ids_logs_mocker

    @pytest.fixture
    def host_manager_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_host_manager_logs function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_host_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.HOST_MANAGER_SUBRESOURCE}": 654321}

        get_host_manager_logs_mocker = mocker.MagicMock(side_effect=get_host_manager_logs)
        return get_host_manager_logs_mocker

    @pytest.fixture
    def traffic_manager_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_traffic_manager_logs function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_traffic_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.TRAFFIC_MANAGER_SUBRESOURCE}": 654321}

        get_traffic_manager_logs_mocker = mocker.MagicMock(side_effect=get_traffic_manager_logs)
        return get_traffic_manager_logs_mocker

    @pytest.fixture
    def elk_manager_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_elk_manager_logs function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_elk_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.ELK_MANAGER_SUBRESOURCE}": 654321}

        get_elk_manager_logs_mocker = mocker.MagicMock(side_effect=get_elk_manager_logs)
        return get_elk_manager_logs_mocker

    @pytest.fixture
    def elk_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_elk_logs function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_elk_logs(ip: str, port: int, emulation: str, ip_first_octet: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.ELK_STACK_SUBRESOURCE}": 654321}

        get_elk_logs_mocker = mocker.MagicMock(side_effect=get_elk_logs)
        return get_elk_logs_mocker

    @pytest.fixture
    def ryu_manager_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_ryu_manger_logs function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_ryu_manager_logs(ip: str, port: int, emulation: str, ip_first_octet: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.RYU_MANAGER_SUBRESOURCE}": 654321}

        get_ryu_manager_logs_mocker = mocker.MagicMock(side_effect=get_ryu_manager_logs)
        return get_ryu_manager_logs_mocker

    @pytest.fixture
    def ryu_controller_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_ryu_controller_logs function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_ryu_controller_logs(ip: str, port: int, emulation: str, ip_first_octet: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.RYU_CONTROLLER_SUBRESOURCE}": 654321}

        get_ryu_controller_logs_mocker = mocker.MagicMock(side_effect=get_ryu_controller_logs)
        return get_ryu_controller_logs_mocker

    @pytest.fixture
    def get_em_ex(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_emulation_execution function

        :param mocker: The pytest mocker object
        :return: the mocked function
        """

        def get_emulation_execution(ip_first_octet: int, emulation_name: str) -> EmulationExecution:
            c_net = ContainerNetwork(name="Network1", subnet_mask="Subnet1", bitmask="null",
                                     subnet_prefix="null", interface="eth0")
            nc_config = NodeContainerConfig(name="Container1",
                                            ips_and_networks=[("123.456.78.99", c_net)],
                                            version="null", level="null",
                                            restart_policy="JDoePolicy", suffix="null",
                                            os="null", execution_ip_first_octet=ip_first_octet,
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
            cred = Credential(username="JDoe", pw="JDoe", port=None, protocol=None, service="null", root=False)
            nv_conf = NodeVulnerabilityConfig(ip="123.456.78.99", vuln_type=VulnType(0), name="JohnDoe", port=1,
                                              protocol=TransportProtocol(0), credentials=[cred], cvss=2.0,
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
                                          packet_delay_distribution=PacketDelayDistributionType.PARETO,
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
                            arrival_config=ConstantArrivalConfig(lamb=10),
                            mu=4, exponential_service_time=False)
            wf_m_chain = WorkflowMarkovChain(transition_matrix=[[1.0]], initial_state=1, id=1)
            wf_service = WorkflowService(ips_and_commands=[("null", "null")], id=1)
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
                                               physical_host_ip="null")
            res_conf = ResourcesConfig(node_resources_configurations=[node_res_conf])
            traf_conf = TrafficConfig(node_traffic_configs=[node_traf_conf],
                                      client_population_config=cp_config)
            kafka_top = KafkaTopic(name="JohhnDoe", num_partitions=3, num_replicas=5, attributes=["null"],
                                   retention_time_hours=3)
            kafka_conf = KafkaConfig(container=nc_config, resources=node_res_conf, firewall_config=n_fire_conf,
                                     topics=[kafka_top], kafka_manager_log_file="null", kafka_manager_log_dir="null",
                                     kafka_manager_max_workers=9, kafka_port=9092, kafka_port_external=9292,
                                     time_step_len_seconds=15, kafka_manager_port=50051, version="0.0.1")
            network_service = NetworkService(protocol=TransportProtocol(0), port=1, name="JohnDoe", credentials=None)
            n_service_conf = NodeServicesConfig(ip="123.456.78.99", services=[network_service])
            service_conf = ServicesConfig(services_configs=[n_service_conf])
            e_a_action = EmulationAttackerAction(id=EmulationAttackerActionId(0), name="JohnDoe",
                                                 cmds=["JohnDoeCommands"],
                                                 type=EmulationAttackerActionType(0), descr="null",
                                                 ips=["null"], index=10,
                                                 action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                                 vulnerability="null", alt_cmds=["null"], backdoor=False,
                                                 execution_time=0.0, ts=1.1)
            ovs_switch = OvsSwitchConfig(container_name="JohnDoe", ip="123.456.78.99", openflow_protocols=["null"],
                                         controller_ip="123.456.78.99", controller_port=2,
                                         controller_transport_protocol="null",
                                         docker_gw_bridge_ip="null", physical_host_ip="123.456.78.99")
            sdc_ctrl = SDNControllerConfig(container=nc_config, resources=node_res_conf, firewall_config=n_fire_conf,
                                           controller_port=4, controller_type=SDNControllerType(0),
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
            em_env = EmulationEnvConfig(name=emulation_name, containers_config=c_config, users_config=u_config,
                                        flags_config=FlagsConfig(node_flag_configs=[nf_conf]),
                                        vuln_config=VulnerabilitiesConfig(node_vulnerability_configs=[nv_conf]),
                                        topology_config=top_conf, traffic_config=traf_conf, resources_config=res_conf,
                                        kafka_config=kafka_conf, services_config=service_conf, descr="null",
                                        static_attacker_sequences={str: [e_a_action]},
                                        ovs_config=OVSConfig(switch_configs=[ovs_switch]),
                                        sdn_controller_config=sdc_ctrl, host_manager_config=host_mng,
                                        snort_ids_manager_config=snort_mng, ossec_ids_manager_config=ossec_mng,
                                        docker_stats_manager_config=docker_mng, elk_config=elk, beats_config=beats,
                                        level=5, version="null", execution_id=10,
                                        csle_collector_version=collector_constants.LATEST_VERSION,
                                        csle_ryu_version=collector_constants.LATEST_VERSION)
            em_ex = EmulationExecution(emulation_name=emulation_name, timestamp=1.5, ip_first_octet=ip_first_octet,
                                       emulation_env_config=em_env, physical_servers=["JohnDoeServer"])
            return em_ex

        get_emulation_execution_mocker = mocker.MagicMock(side_effect=get_emulation_execution)
        return get_emulation_execution_mocker

    @pytest.fixture
    def config(self, mocker: pytest_mock.MockFixture, example_config: Config):
        """
        Pytest fixture for mocking the get_config function

        :param mocker: the pytest mocker object
        :param example_config: The example_config function fetched from conftest.py
        :return: the mocked function
        """

        def get_config(id: int) -> Config:
            config = example_config
            return config

        get_config_mocker = mocker.MagicMock(side_effect=get_config)
        return get_config_mocker

    @pytest.fixture
    def node_exporter_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_node_exporter_logs function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_node_exporter_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE}": 654321}

        get_node_exporter_logs_mocker = mocker.MagicMock(side_effect=get_node_exporter_logs)
        return get_node_exporter_logs_mocker

    @pytest.fixture
    def cadvisor_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_cadvisor_logs function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_cadvisor_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE}": 654321}

        get_cadvisor_logs_mocker = mocker.MagicMock(side_effect=get_cadvisor_logs)
        return get_cadvisor_logs_mocker

    @pytest.fixture
    def pgadmin_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_pgadmin_logs function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_pgadmin_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.PGADMIN_RESOURCE}": 654321}

        get_pgadmin_logs_mocker = mocker.MagicMock(side_effect=get_pgadmin_logs)
        return get_pgadmin_logs_mocker

    @pytest.fixture
    def grafana_logs(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_grafana_logs function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_grafana_logs(ip: str, port: int) -> Dict[str, Any]:
            return {f"{api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE}": 654321}

        get_grafana_logs_mocker = mocker.MagicMock(side_effect=get_grafana_logs)
        return get_grafana_logs_mocker

    def test_logs_post_cluster(self, flask_app, not_logged_in, logged_in, logged_in_as_admin,
                               mocker: pytest_mock.MockFixture, example_config, csle_logs, dsm_logs, prom_logs,
                               nginx_logs,
                               postgresql_logs, flask_logs, cluster_manager_logs, docker_logs, node_exporter_logs,
                               cadvisor_logs, pgadmin_logs, grafana_logs) -> None:
        """
        Tests the POST HTTPS method for the /logs resource

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param database: the database fixture
        :param token: the token fixture
        :param save: the save fixture
        :param update: the update fixture
        :return: None
        """
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "get_csle_log_files", side_effect=csle_logs)
        mocker_list = [dsm_logs, prom_logs, nginx_logs, postgresql_logs,
                       flask_logs, cluster_manager_logs, docker_logs,
                       node_exporter_logs, cadvisor_logs, pgadmin_logs,
                       grafana_logs]
        corr_func_names = ["get_docker_statsmanager_logs",
                           "get_prometheus_logs", "get_nginx_logs", "get_postgresql_logs",
                           "get_flask_logs", "get_cluster_manager_logs",
                           "get_docker_logs", "get_node_exporter_logs",
                           "get_cadvisor_logs", "get_pgadmin_logs",
                           "get_grafana_logs"]
        constants_list = [api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.PROMETHEUS_RESOURCE, api_constants.MGMT_WEBAPP.NGINX_RESOURCE,
                          api_constants.MGMT_WEBAPP.POSTGRESQL_RESOURCE, api_constants.MGMT_WEBAPP.FLASK_RESOURCE,
                          api_constants.MGMT_WEBAPP.CLUSTERMANAGER_RESOURCE, api_constants.MGMT_WEBAPP.DOCKER_RESOURCE,
                          api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE, api_constants.MGMT_WEBAPP.CADVISOR_RESOURCE,
                          api_constants.MGMT_WEBAPP.PGADMIN_RESOURCE, api_constants.MGMT_WEBAPP.GRAFANA_RESOURCE]
        for i in range(len(mocker_list)):
            mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
            path = f"csle_cluster.cluster_manager.cluster_controller.ClusterController.{corr_func_names[i]}"
            mocker.patch(path, side_effect=mocker_list[i])
            response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}"
                                                    f"{constants.COMMANDS.SLASH_DELIM}"
                                                    f"{constants_list[i]}",
                                                    data=json.dumps({}))
            response_data = response.data.decode("utf-8")
            response_data_dict = json.loads(response_data)
            assert response_data_dict == {}
            assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
            mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
            response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}"
                                                    f"{constants.COMMANDS.SLASH_DELIM}{constants_list[i]}",
                                                    data=json.dumps({}))
            response_data = response.data.decode("utf-8")
            response_data_dict = json.loads(response_data)
            assert response_data_dict == {}
            assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
            config = example_config
            config_cluster_dict = config.cluster_config.to_dict()['cluster_nodes'][0]
            mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
            response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}"
                                                    f"{constants.COMMANDS.SLASH_DELIM}{constants_list[i]}",
                                                    data=json.dumps(config_cluster_dict))
            response_data = response.data.decode("utf-8")
            response_data_dict = json.loads(response_data)
            assert response.status_code == constants.HTTPS.OK_STATUS_CODE
            assert response_data_dict == {f"{constants_list[i]}": 654321}
            del config_cluster_dict[api_constants.MGMT_WEBAPP.IP_PROPERTY]
            response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}"
                                                    f"{constants.COMMANDS.SLASH_DELIM}"
                                                    f"{constants_list[i]}",
                                                    data=json.dumps(config_cluster_dict))

            response_data = response.data.decode("utf-8")
            response_data_dict = json.loads(response_data)
            assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
            assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict

    def test_logs_post_metastore(self, flask_app, not_logged_in, logged_in, logged_in_as_admin,
                                 mocker: pytest_mock.MockFixture, csle_logs,
                                 get_em_ex, container_logs, client_manager_logs, kafka_manager_logs, kafka_logs,
                                 snort_ids_manager_logs, snort_ids_logs, ossec_ids_manager_logs,
                                 ossec_ids_logs, host_manager_logs, traffic_manager_logs, elk_manager_logs,
                                 elk_logs, ryu_manager_logs, ryu_controller_logs, config) -> None:
        """
        Tests the POST HTTPS method for the /logs resource

        :param flask_app: the flask app representing the web server
        :param mocker: the mocker object for mocking functions
        :param csle_logs: the csle_logs fixture
        :param container_logs: the container_logs fixture
        :param client_manager_logs: the client_manager_logs fixture
        :param kafka_manager_logs: the kafka_manager_logs fixture
        :param kafka_logs: the kafka_logs fixture
        :param snort_ids_manager_logs: the snort_ids_manager fixture
        :param snort_ids_logs: the snort_ids_logs fixture
        :param ossec_ids_manager_logs: the ossec_ids_manager_logs fixture
        :param ossec_ids_logs: the ossec_ids_logs_ fixture
        :param host_manager_logs: the host_manager_logs fixture
        :param traffic_manager_logs: the traffic_manager_logs fixture
        :param elk_manager_logs: the elk_manager_logs fixture
        :param elk_logs: the elk_logs fixture
        :param ryu_manager_logs: the ryu_manager_logs fixture
        :param tyu_controller_logs: the ryu_controller_logs fixture
        :return: None
        """
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_csle_log_files",
                     side_effect=csle_logs)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker_list = [container_logs, client_manager_logs, kafka_manager_logs, kafka_logs, snort_ids_manager_logs,
                       snort_ids_logs, ossec_ids_manager_logs, ossec_ids_logs, host_manager_logs,
                       traffic_manager_logs, elk_manager_logs, elk_logs, ryu_manager_logs, ryu_controller_logs]
        corr_func_names = ["get_container_logs", "get_client_manager_logs", "get_kafka_manager_logs", "get_kafka_logs",
                           "get_snort_ids_manager_logs", "get_snort_ids_logs", "get_ossec_ids_manager_logs",
                           "get_ossec_ids_logs", "get_host_manager_logs", "get_traffic_manager_logs",
                           "get_elk_manager_logs", "get_elk_logs", "get_ryu_manager_logs", "get_ryu_controller_logs"]
        constants_list = [api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.CLIENT_MANAGER_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.OSSEC_IDS_MANAGER_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.OSSEC_IDS_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.HOST_MANAGER_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.TRAFFIC_MANAGER_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.ELK_MANAGER_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.ELK_STACK_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.RYU_MANAGER_SUBRESOURCE,
                          api_constants.MGMT_WEBAPP.RYU_CONTROLLER_SUBRESOURCE]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        k = 0
        for i in range(len(mocker_list)):
            k += 1
            mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
            path = f"csle_cluster.cluster_manager.cluster_controller.ClusterController.{corr_func_names[i]}"
            mocker.patch(path, side_effect=mocker_list[i])
            response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}"
                                                    f"{constants.COMMANDS.SLASH_DELIM}"
                                                    f"{constants_list[i]}"
                                                    f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}=emulation1"
                                                    f"&{api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM}=10",
                                                    data=json.dumps({}))
            response_data = response.data.decode("utf-8")
            response_data_dict = json.loads(response_data)
            assert response_data_dict == {}
            assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
            mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
            response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}"
                                                    f"{constants.COMMANDS.SLASH_DELIM}"
                                                    f"{constants_list[i]}"
                                                    f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}=emulation1"
                                                    f"&{api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM}=10",
                                                    data=json.dumps({}))
            response_data = response.data.decode("utf-8")
            response_data_dict = json.loads(response_data)
            assert response_data_dict == {}
            assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
            mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
            response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}"
                                                    f"{constants.COMMANDS.SLASH_DELIM}"
                                                    f"{constants_list[i]}"
                                                    f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}=emulation1"
                                                    f"&{api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM}=10",
                                                    data=json.dumps({}))
            response_data = response.data.decode("utf-8")
            response_data_dict = json.loads(response_data)
            assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
            assert response_data_dict == {}
            indata_dict = {api_constants.MGMT_WEBAPP.NAME_PROPERTY: "123.456.78.99"}
            if corr_func_names[i] == "get_container_logs":
                indata_dict[api_constants.MGMT_WEBAPP.NAME_PROPERTY] = "Container1null-levelnull-10"
            response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.LOGS_RESOURCE}"
                                                    f"{constants.COMMANDS.SLASH_DELIM}"
                                                    f"{constants_list[i]}"
                                                    f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}=emulation1"
                                                    f"&{api_constants.MGMT_WEBAPP.EXECUTION_ID_QUERY_PARAM}=10",
                                                    data=json.dumps(indata_dict))
            response_data = response.data.decode("utf-8")
            response_data_dict = json.loads(response_data)
            assert response.status_code == constants.HTTPS.OK_STATUS_CODE
            assert response_data_dict == {constants_list[i]: 654321}
