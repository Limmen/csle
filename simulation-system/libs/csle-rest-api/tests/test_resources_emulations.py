import json
import logging
from typing import Any, Dict, List, Tuple

import csle_collector.constants.constants as collector_constants
import csle_common.constants.constants as constants
import pytest
import pytest_mock
from csle_cluster.cluster_manager.cluster_manager_pb2 import (
    OperationOutcomeDTO,
    RunningEmulationsDTO,
)
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig
from csle_collector.client_manager.dao.client import Client
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import (
    EmulationAttackerAction,
)
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import (
    EmulationAttackerActionId,
)
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import (
    EmulationAttackerActionOutcome,
)
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import (
    EmulationAttackerActionType,
)
from csle_common.dao.emulation_config.beats_config import BeatsConfig
from csle_common.dao.emulation_config.client_population_config import (
    ClientPopulationConfig,
)
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_config.default_network_firewall_config import (
    DefaultNetworkFirewallConfig,
)
from csle_common.dao.emulation_config.docker_stats_manager_config import (
    DockerStatsManagerConfig,
)
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
from csle_common.dao.emulation_config.node_vulnerability_config import (
    NodeVulnerabilityConfig,
)
from csle_common.dao.emulation_config.ossec_ids_manager_config import (
    OSSECIDSManagerConfig,
)
from csle_common.dao.emulation_config.ovs_config import OVSConfig
from csle_common.dao.emulation_config.ovs_switch_config import OvsSwitchConfig
from csle_common.dao.emulation_config.packet_delay_distribution_type import (
    PacketDelayDistributionType,
)
from csle_common.dao.emulation_config.packet_loss_type import PacketLossType
from csle_common.dao.emulation_config.resources_config import ResourcesConfig
from csle_common.dao.emulation_config.sdn_controller_config import SDNControllerConfig
from csle_common.dao.emulation_config.sdn_controller_type import SDNControllerType
from csle_common.dao.emulation_config.services_config import ServicesConfig
from csle_common.dao.emulation_config.snort_ids_manager_config import (
    SnortIDSManagerConfig,
)
from csle_common.dao.emulation_config.topology_config import TopologyConfig
from csle_common.dao.emulation_config.traffic_config import TrafficConfig
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.user import User
from csle_common.dao.emulation_config.users_config import UsersConfig
from csle_common.dao.emulation_config.vulnerabilities_config import (
    VulnerabilitiesConfig,
)
from csle_common.dao.emulation_config.vulnerability_type import VulnType

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app

logger = logging.getLogger("logger")


class TestResourcesEmulationsSuite:
    """
    Test suite for /system-identification-jobs resource
    """
    @pytest.fixture
    def flask_app(self):
        """
        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

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
    def emulations(self, mocker):
        """
        Pytest fixture for mocking the list_emulations function
        :param mocker: the pytest mocker object
        :return: the mocked function
        TODO: Lägg in i conftest.
        """
        def list_emulations() -> List[EmulationEnvConfig]:
            em_env = TestResourcesEmulationsSuite.get_ex_em_env()
            return [em_env]
        list_emulations_mocker = mocker.MagicMock(side_effect=list_emulations)
        return list_emulations_mocker

    @pytest.fixture
    def emulations_images(self, mocker):
        """
        Pytest fixture for mocking the list_emulation_images function
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_emulation_images() -> List[Tuple[str, bytes]]:  # OBS: kan bli fel
            em_im_list = [("Emulation1", bytes("Emulation1", "utf-8"))]
            return em_im_list
        list_emulation_images_mocker = mocker.MagicMock(side_effect=list_emulation_images)
        return list_emulation_images_mocker

    @pytest.fixture
    def running_emulations(self, mocker):
        """
        Pytest fixture for mocking the list_all_running_emulations fixture
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_all_running_emulations(ip: str, port: int) -> RunningEmulationsDTO:
            return RunningEmulationsDTO(runningEmulations="abcdef")
        list_all_running_emulations_mocker = mocker.MagicMock(side_effect=list_all_running_emulations)
        return list_all_running_emulations_mocker

    @pytest.fixture
    def given_emulation(self, mocker):

        def list_emulation_executions_for_a_given_emulation(emulation_name: str) -> List[EmulationExecution]:
            em_env = TestResourcesEmulationsSuite.get_ex_em_env()
            em_ex = EmulationExecution(emulation_name="JohbnDoeEmulation", timestamp=1.5, ip_first_octet=-1,
                                       emulation_env_config=em_env, physical_servers=["JohnDoeServer"])
            return em_ex
        list_emulation_executions_for_a_given_emulation_mocker = \
            mocker.MagicMock(side_effect=list_emulation_executions_for_a_given_emulation)
        return list_emulation_executions_for_a_given_emulation_mocker

    @pytest.fixture
    def uninstall(self, mocker):
        """Pytest fixture for mocking the uninstall_emulation function
        :param mocker: The pytest mocker object
        :return: The mocked function        
        """
        def uninstall_emulation(config: EmulationEnvConfig) -> None:
            return None
        uninstall_emulation_mocker = mocker.MagicMock(side_effect=uninstall_emulation)
        return uninstall_emulation_mocker

    @pytest.fixture
    def clean(self, mocker):
        """
        Pytest fixture for mocking the clean_all_executions_of_emulation function
        :param mocker: The pytest mocker object
        :return: The mocked function
        """
        def clean_all_executions_of_emulation(ip: str, port: int, emulation: str) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)
        clean_all_executions_of_emulation_mocker = mocker.MagicMock(side_effect=clean_all_executions_of_emulation)
        return clean_all_executions_of_emulation_mocker

    @pytest.fixture
    def emulations_ids_in_names(self, mocker):
        """Pytest fixture for mocking the list_emulations_ids function
        :param mocker: the pytest mocker object
        :return: The mocked function
        """
        def list_emulations_ids() -> List[Tuple]:
            list_dict = [(10, "a")]
            return list_dict
        list_emulations_ids_mocker = mocker.MagicMock(side_effect=list_emulations_ids
                                                      )
        return list_emulations_ids_mocker

    @pytest.fixture
    def emulations_ids_not_in_names(self, mocker):
        """Pytest fixture for mocking the list_emulations_ids function
        :param mocker: the pytest mocker object
        :return: The mocked function
        """
        def list_emulations_ids() -> List[Tuple]:
            list_dict = [(10, "q")]
            return list_dict
        list_emulations_ids_mocker = mocker.MagicMock(side_effect=list_emulations_ids
                                                      )
        return list_emulations_ids_mocker


    @staticmethod
    def get_ex_em_env():
        """
        Static help method for fetching an example EmulationEnvConfig class
        :return: example EmulationEnvConfig class
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
                        arrival_config=ArrivalConfig(client_arrival_type=ClientArrivalType(0)),
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
        em_env = EmulationEnvConfig(name="Johndoe", containers_config=c_config, users_config=u_config,
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
        return em_env

    def test_emulations_get(self, mocker, flask_app, not_logged_in, logged_in,
                            logged_in_as_admin, config, emulations,
                            emulations_images, running_emulations,
                            given_emulation, uninstall,
                            clean, emulations_ids_not_in_names,
                            emulations_ids_in_names):
        """
        Testing the HTTPS GET method for the /emulations resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param cofig: the config fixture 
        :param emulations: the emulations fixture
        :param emulation_images: the emulations_images fixture
        :param running_emulation: the running_emulations fixture
        :param given_emulation: the given_emulation fixture¨
        :param uninstall: the uninstall fixture¨
        :param clean: the clean fixturefvf
        :param emulations_ids: the emulations_ids
        :param get_ex_em_env: the get_ex_em_env fixture
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations_ids",
                     side_effect=emulations_ids_not_in_names)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_all_running_emulations",
                     side_effect=running_emulations)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        # logger.info(response.status_code)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        repsonse_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == "q"
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is False
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations_ids",
                     side_effect=emulations_ids_in_names)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        repsonse_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == "a"
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations_ids",
                     side_effect=emulations_ids_not_in_names)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        repsonse_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == "q"
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is False
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations_ids",
                     side_effect=emulations_ids_in_names)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        repsonse_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == "a"
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations",
                     side_effect=emulations)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_images",
                     side_effect=emulations_images)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_executions_for_a_given_emulation",
                     side_effect=given_emulation)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        logger.info(response_data_list)
        # TODO: Kolla varför arrival config inte har någon funktion to_dict().
