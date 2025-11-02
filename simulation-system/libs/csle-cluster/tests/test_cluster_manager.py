from typing import Any, List
import pytest
import pytest_mock
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_cluster.cluster_manager.cluster_manager_pb2 import EmulationMetricsTimeSeriesDTO
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import EmulationDefenderActionOutcome
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_collector.snort_ids_manager.dao.snort_ids_ip_alert_counters import SnortIdsIPAlertCounters
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_ryu.dao.agg_flow_statistic import AggFlowStatistic
from csle_ryu.dao.flow_statistic import FlowStatistic
from csle_ryu.dao.port_statistic import PortStatistic
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_common.dao.emulation_config.emulation_metrics_time_series import EmulationMetricsTimeSeries
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_cluster.cluster_manager.cluster_manager_pb2 import ExecutionInfoDTO
from csle_ryu.dao.avg_port_statistic import AvgPortStatistic
from csle_ryu.dao.avg_flow_statistic import AvgFlowStatistic
from csle_cluster.cluster_manager.cluster_manager_pb2 import KibanaTunnelsDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import RyuTunnelsDTO
from csle_common.dao.emulation_config.emulation_execution_info import EmulationExecutionInfo
from csle_cluster.cluster_manager.cluster_manager_pb2 import SnortIdsManagersInfoDTO
from csle_common.dao.emulation_config.snort_managers_info import SnortIdsManagersInfo
from csle_cluster.cluster_manager.cluster_manager_pb2 import SnortIdsMonitorThreadStatusesDTO
from csle_collector.snort_ids_manager.snort_ids_manager_pb2 import SnortIdsMonitorDTO
from csle_common.dao.emulation_config.ryu_managers_info import RyuManagersInfo
from csle_cluster.cluster_manager.cluster_manager_pb2 import OSSECIdsMonitorThreadStatusesDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import RyuManagerStatusDTO
from csle_collector.ossec_ids_manager.ossec_ids_manager_pb2 import OSSECIdsMonitorDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import OSSECIdsManagersInfoDTO
from csle_common.dao.emulation_config.ossec_managers_info import OSSECIDSManagersInfo
from csle_cluster.cluster_manager.cluster_manager_pb2 import KafkaManagersInfoDTO
from csle_common.dao.emulation_config.kafka_managers_info import KafkaManagersInfo
from csle_cluster.cluster_manager.cluster_manager_pb2 import KafkaStatusDTO
from csle_collector.kafka_manager.kafka_manager_pb2 import KafkaDTO
from csle_collector.docker_stats_manager.docker_stats_manager_pb2 import DockerStatsMonitorDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import HostManagerStatusesDTO
from csle_common.dao.emulation_config.host_managers_info import HostManagersInfo
from csle_collector.host_manager.host_manager_pb2 import HostStatusDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import HostManagersInfoDTO
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.elk_managers_info import ELKManagersInfo
from csle_cluster.cluster_manager.cluster_manager_pb2 import ElkManagersInfoDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import DockerStatsManagersInfoDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import DockerStatsMonitorStatusDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import ContainerImagesDTO
from csle_collector.elk_manager.elk_manager_pb2 import ElkDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import ElkStatusDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import RunningContainersDTO
from csle_common.dao.emulation_config.docker_stats_managers_info import DockerStatsManagersInfo
from csle_cluster.cluster_manager.cluster_manager_pb2 import StoppedContainersDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import RunningEmulationsDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import DockerNetworksDTO
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_cluster.cluster_manager.cluster_manager_pb2 import TrafficManagersInfoDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import ClientManagersInfoDTO
from csle_common.dao.emulation_config.traffic_managers_info import TrafficManagersInfo
from csle_collector.traffic_manager.traffic_manager_pb2 import TrafficDTO
from csle_collector.ryu_manager.ryu_manager_pb2 import RyuDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import GetNumClientsDTO
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_cluster.cluster_manager.cluster_manager_pb2 import OperationOutcomeDTO
import csle_common.constants.constants as constants
from csle_cluster.cluster_manager.cluster_manager import ClusterManagerServicer
from csle_cluster.cluster_manager.cluster_manager_pb2 import ServiceStatusDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import LogsDTO
from csle_common.dao.emulation_config.config import Config
from csle_collector.client_manager.client_manager_pb2 import ClientsDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import NodeStatusDTO
import csle_cluster.cluster_manager.query_cluster_manager as query_cluster_manager
import logging


class TestClusterManagerSuite:
    """
    Test suite for cluster_manager.py
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_cluster.cluster_manager.cluster_manager_pb2_grpc import add_ClusterManagerServicer_to_server
        return add_ClusterManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> ClusterManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the host manager servicer
        """
        return ClusterManagerServicer()

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_cluster.cluster_manager.cluster_manager_pb2_grpc import ClusterManagerStub
        return ClusterManagerStub

    @pytest.fixture
    def get_clients(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the TrafficController.get_num_active_clients method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_num_active_clients(emulation_env_config: EmulationEnvConfig, logger: logging.Logger) -> ClientsDTO:
            clients_dto = ClientsDTO(num_clients=4,
                                     client_process_active=True,
                                     producer_active=True,
                                     clients_time_step_len_seconds=4,
                                     producer_time_step_len_seconds=5)
            return clients_dto

        get_num_active_clients_mocker = mocker.MagicMock(side_effect=get_num_active_clients)
        return get_num_active_clients_mocker

    @pytest.fixture
    def empty_clients(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the ClusterManagerUtil.get_empty_get_num_clients_dto method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_empty_get_num_clients_dto() -> GetNumClientsDTO:
            num_clients_dto = GetNumClientsDTO(num_clients=4, client_process_active=True, producer_active=True,
                                               clients_time_step_len_seconds=4, producer_time_step_len_seconds=4)
            return num_clients_dto

        get_empty_get_num_clients_dto_mocker = mocker.MagicMock(side_effect=get_empty_get_num_clients_dto)
        return get_empty_get_num_clients_dto_mocker

    @staticmethod
    def client_mng_info() -> ClientManagersInfo:
        """
        Static help method for obtaining a ClientManagersInfo object

        :return: a ClientManagersInfo object
        """
        clients_dto = ClientsDTO(num_clients=4, client_process_active=True, producer_active=True,
                                 clients_time_step_len_seconds=4, producer_time_step_len_seconds=5)
        client_manage_info = ClientManagersInfo(ips=["123.456.78.99"], ports=[1], emulation_name="JohnDoeEmulation",
                                                execution_id=1, client_managers_statuses=[clients_dto],
                                                client_managers_running=[True])
        return client_manage_info

    @pytest.fixture
    def active_ips(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the ClusterManagerUtil.get_active_ips method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_active_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
            return ["123.456.78.99"]

        get_active_ips_mocker = mocker.MagicMock(side_effect=get_active_ips)
        return get_active_ips_mocker

    @pytest.fixture
    def start_ryu(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ryu method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_ryu(emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.RootLogger) \
                -> RyuDTO:
            ryu = RyuDTO(ryu_running=True, monitor_running=True, port=4, web_port=4, controller="null",
                         kafka_ip="123.456.78.99", kafka_port=7, time_step_len=4)
            return ryu

        start_ryu_mocker = mocker.MagicMock(side_effect=start_ryu)
        return start_ryu_mocker

    @pytest.fixture
    def stop_ryu(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_ryu method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_ryu(emulation_env_config: EmulationEnvConfig, logger: logging.RootLogger) -> RyuDTO:
            ryu = RyuDTO(ryu_running=True, monitor_running=True, port=4, web_port=4, controller="null",
                         kafka_ip="123.456.78.99", kafka_port=7, time_step_len=4)
            return ryu

        stop_ryu_mocker = mocker.MagicMock(side_effect=stop_ryu)
        return stop_ryu_mocker

    @pytest.fixture
    def ryu_status(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_ryu_status method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_ryu_status(emulation_env_config: EmulationEnvConfig, logger: logging.Logger) -> RyuDTO:
            ryu = RyuDTO(ryu_running=True, monitor_running=True, port=4, web_port=4, controller="null",
                         kafka_ip="123.456.78.99", kafka_port=7, time_step_len=4)
            return ryu

        get_ryu_status_mocker = mocker.MagicMock(side_effect=get_ryu_status)
        return get_ryu_status_mocker

    @staticmethod
    def traffic_mng_info():
        """
        Static help method for obtaining a TrafficManagersInfo object

        :return: a TrafficManagersInfo object
        """
        traffic_dto = TrafficDTO(running=True, script="null")
        traffic_manage_info = TrafficManagersInfo(ips=["123.456.78.99"], ports=[1], emulation_name="JohnDoeEmulation",
                                                  execution_id=1, traffic_managers_statuses=[traffic_dto],
                                                  traffic_managers_running=[True])
        return traffic_manage_info

    @staticmethod
    def with_class():
        """
        Auxillary method for mocking the with_class method

        :return: None
        """

        class A:
            """
            Auxillary class for mocking
            """

            def __init__(self):
                pass

            def __enter__(self):
                pass

            def __exit__(self, exc_type, exc_value, traceback):
                pass

        return A()

    @staticmethod
    def get_dsm_info() -> DockerStatsManagersInfo:
        """
        Static help method for obtaining a DockerStatsManagersInfo object
        
        :return: a DockerStatsManagersInfo object
        """
        docker_sm_info = DockerStatsManagersInfo(
            ips=["123.456.78.99"], ports=[1], emulation_name="JDoeEmulation", execution_id=1,
            docker_stats_managers_statuses=[DockerStatsMonitorDTO(
                num_monitors=4, emulations=["JDoeEmulation"], emulation_executions=[4])],
            docker_stats_managers_running=[True])
        return docker_sm_info

    @staticmethod
    def get_elk_mng_info() -> ELKManagersInfo:
        """
        Static help metod for obtaining an ElkManagersInfo object
        
        :return: an ElkManagersInfo object
        """
        elk_mng_info = ELKManagersInfo(
            ips=["123.456.78.99"], ports=[1], emulation_name="JohnDoeEmulation", execution_id=1,
            elk_managers_statuses=[ElkDTO(elasticRunning=True, kibanaRunning=True, logstashRunning=True)],
            elk_managers_running=[True], local_kibana_port=-1, physical_server_ip="123.456.78.99")
        return elk_mng_info

    @staticmethod
    def get_ex_nc_conf() -> NodeContainerConfig:
        """
        Static help method for obtaining a NodeContainerConfig object
        
        :return: a NodeContainerConfig object
        """
        c_net = ContainerNetwork(name="Network1", subnet_mask="Subnet1", bitmask="null", subnet_prefix="null",
                                 interface="eth0")
        nc_conf = NodeContainerConfig(
            name="Container1", ips_and_networks=[("123.456.78.99", c_net)], version="null", level="null",
            restart_policy="JDoePolicy", suffix="null", os="null", execution_ip_first_octet=-1,
            docker_gw_bridge_ip="123.456.78.99", physical_host_ip="123.456.78.99")
        return nc_conf

    @staticmethod
    def host_status_dto() -> List[HostStatusDTO]:
        """
        Staic help method for obtaining a replicated list of host monitor statuses
        """
        host_stat_dto = HostStatusDTO(
            monitor_running=True, filebeat_running=True, packetbeat_running=True, metricbeat_running=True,
            heartbeat_running=True, ip="123.456.78.99")
        return host_stat_dto

    @staticmethod
    def get_host_mng_info() -> HostManagersInfo:
        """
        Static help method for obtaining a HostManagersInfo object
        
        :return: a HostManagersInfo
        """
        h_m_info = HostManagersInfo(
            ips=["123.456.78.99"], ports=[1], emulation_name="JDoeEmulation", execution_id=1,
            host_managers_statuses=[TestClusterManagerSuite.host_status_dto()], host_managers_running=[True])
        return h_m_info

    @staticmethod
    def get_kafka_mng_info():
        """
        static help method for obtaining a KafkaManagersInfo object
        
        :return: a KafkaManagersInfo object
        """
        kafka_mng_info = KafkaManagersInfo(
            ips=["123.456.78.99"], ports=[1], emulation_name="JDoeEmulation", execution_id=1,
            kafka_managers_statuses=[KafkaDTO(running=True, topics=["null"])], kafka_managers_running=[True])
        return kafka_mng_info

    @staticmethod
    def get_ossec_imt_statuses():
        """
        Static help method for obtaining a list of OSSECIdsMonitorDTO object(s)
        
        :return: a list of OSSECIdsMonitorDTO object(s)
        """
        ossec_imn_statuses = [OSSECIdsMonitorDTO(monitor_running=True, ossec_ids_running=True)]
        return ossec_imn_statuses

    @staticmethod
    def get_ossec_mng_info():
        """
        Static help method for obtaining an OSSECIDSManagersInfo object
        
        :return: an OSSECIDSManagersInfo object
        """
        ossec_mng_info = OSSECIDSManagersInfo(
            ips=["123.456.78.99"], ports=[1], emulation_name="JDoeEmulation", execution_id=1,
            ossec_ids_managers_statuses=[OSSECIdsMonitorDTO(monitor_running=True, ossec_ids_running=True)],
            ossec_ids_managers_running=[True])
        return ossec_mng_info

    @staticmethod
    def ryu_mng_info() -> RyuManagersInfo:
        """
        Static help method for obtaining a RyuManagersInfo

        :return: a RyuManagersInfo object
        """
        ryu_mng_info = RyuManagersInfo(
            ips=["123.456.78.99"], ports=[1], emulation_name="JDoeEmulation", execution_id=1,
            ryu_managers_statuses=[RyuDTO(ryu_running=True, monitor_running=True, port=4, web_port=4, controller="null",
                                          kafka_ip="123.456.78.99", kafka_port=7, time_step_len=4)],
            ryu_managers_running=[True], local_controller_web_port=10, physical_server_ip="123.456.78.99")
        return ryu_mng_info

    @staticmethod
    def snort_mng_info():
        """
        Static hetlp method for obtaining a SnortIdsManagersInfo object

        :return: a SnortIdsManagersInfo object
        """
        snort_mng = SnortIdsManagersInfo(
            ips=["123.456.78.99"], ports=[1], emulation_name="JDoeEmulation", execution_id=1,
            snort_ids_managers_statuses=[SnortIdsMonitorDTO(monitor_running=True, snort_ids_running=True)],
            snort_ids_managers_running=[True])
        return snort_mng

    @staticmethod
    def em_exec_info():
        """
        static help metho for ibtaining an EmulationExecutionInfo object
        
        :return: an EmulationExecutionInfo object
        """
        emulation_exec_info = EmulationExecutionInfo(
            emulation_name="JDoeEmulation", execution_id=1,
            snort_ids_managers_info=TestClusterManagerSuite.snort_mng_info(),
            ossec_ids_managers_info=TestClusterManagerSuite.get_ossec_mng_info(),
            kafka_managers_info=TestClusterManagerSuite.get_kafka_mng_info(),
            host_managers_info=TestClusterManagerSuite.get_host_mng_info(),
            client_managers_info=TestClusterManagerSuite.client_mng_info(),
            docker_stats_managers_info=TestClusterManagerSuite.get_dsm_info(),
            running_containers=[TestClusterManagerSuite.get_ex_nc_conf()],
            stopped_containers=[TestClusterManagerSuite.get_ex_nc_conf()],
            traffic_managers_info=TestClusterManagerSuite.traffic_mng_info(),
            active_networks=[ContainerNetwork(name="Network1",
                                              subnet_mask="Subnet1",
                                              bitmask="null",
                                              subnet_prefix="null",
                                              interface="eth0")],
            inactive_networks=[ContainerNetwork(name="Network1",
                                                subnet_mask="Subnet1",
                                                bitmask="null",
                                                subnet_prefix="null",
                                                interface="eth0")],
            elk_managers_info=TestClusterManagerSuite.get_elk_mng_info(),
            ryu_managers_info=TestClusterManagerSuite.ryu_mng_info())
        return emulation_exec_info

    @staticmethod
    def emulation_mts(get_ex_em_env: EmulationEnvConfig):
        """
        Static help method for obtaining an EmulationMetricsTimeSeries object

        :param get_ex_em_env: an example emulation config
        :return: an EmulationMetricsTimeSeries object
        """
        cp_metrics = ClientPopulationMetrics(ip="123.456.78.99", ts=100.0, num_clients=10, rate=2.0, service_time=4.5)
        docker_stats = DockerStats(pids=10.0, timestamp="null", cpu_percent=5.5, mem_current=4.3, mem_total=2.8,
                                   mem_percent=1.7, blk_read=2.3, blk_write=1.2, net_rx=2.4, net_tx=5.3,
                                   container_name="JDoeContainer", ip="123.456.78.99", ts=1.2)
        host_metrics = HostMetrics(num_logged_in_users=10, num_failed_login_attempts=2, num_open_connections=4,
                                   num_login_events=22, num_processes=14, num_users=100, ip="123.456.78.99", ts=15.4)
        e_d_action = EmulationDefenderAction(
            id=EmulationDefenderActionId(0), name="JohnDoe", cmds=["JDoeCommands"],
            type=EmulationDefenderActionType(0), descr="null", ips=["123.456.78.99"], index=1,
            action_outcome=EmulationDefenderActionOutcome.GAME_END, alt_cmds=["JDoeCommands"],
            execution_time=5.6, ts=10.2)
        e_a_action = EmulationAttackerAction(
            id=EmulationAttackerActionId(0), name="JohnDoe", cmds=["JDoeCommands"], type=EmulationAttackerActionType(0),
            descr="null", ips=["123.456.78.99"], index=1,
            action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING, vulnerability="null",
            alt_cmds=["JDoeCommands"], backdoor=False, execution_time=3.3, ts=41.1)
        snort_ids = SnortIdsAlertCounters()
        em_env_conf = get_ex_em_env
        ossec_ids = OSSECIdsAlertCounters()
        flow_stat = FlowStatistic(timestamp=10.5, datapath_id="null", in_port="null", out_port="null",
                                  dst_mac_address="null", num_packets=10, num_bytes=4,
                                  duration_nanoseconds=3, duration_seconds=4, hard_timeout=100,
                                  idle_timeout=12, priority=1, cookie=3)
        port_stat = PortStatistic(timestamp=12.5, datapath_id="null", port=1, num_received_packets=12,
                                  num_received_bytes=34, num_received_errors=21, num_transmitted_packets=13,
                                  num_transmitted_bytes=22, num_transmitted_errors=16, num_received_dropped=41,
                                  num_transmitted_dropped=55, num_received_frame_errors=66,
                                  num_received_overrun_errors=2, num_received_crc_errors=1,
                                  num_collisions=5, duration_nanoseconds=8, duration_seconds=5)
        avg_flow_stat = AvgFlowStatistic(timestamp=1.0, datapath_id="null",
                                         total_num_packets=10, total_num_bytes=10,
                                         avg_duration_nanoseconds=10, avg_duration_seconds=10,
                                         avg_hard_timeout=10, avg_idle_timeout=10,
                                         avg_priority=10, avg_cookie=10)
        avg_port_stat = AvgPortStatistic(timestamp=1.0, datapath_id="null", total_num_received_packets=10,
                                         total_num_received_bytes=10, total_num_received_errors=10,
                                         total_num_transmitted_packets=10, total_num_transmitted_bytes=10,
                                         total_num_transmitted_errors=10, total_num_received_dropped=10,
                                         total_num_transmitted_dropped=10, total_num_received_frame_errors=10,
                                         total_num_received_overrun_errors=10, total_num_received_crc_errors=10,
                                         total_num_collisions=10, avg_duration_nanoseconds=5,
                                         avg_duration_seconds=5)
        agg_flow_stat = AggFlowStatistic(timestamp=4.3, datapath_id="null",
                                         total_num_packets=2, total_num_bytes=10,
                                         total_num_flows=10)
        snort_ipa = SnortIdsIPAlertCounters()
        snort_rule = SnortIdsRuleCounters()
        emulation_metric_time_series = EmulationMetricsTimeSeries(
            client_metrics=[cp_metrics], aggregated_docker_stats=[docker_stats],
            docker_host_stats={"docker_stats": [docker_stats]}, host_metrics={"host_metrics": [host_metrics]},
            aggregated_host_metrics=[host_metrics], defender_actions=[e_d_action], attacker_actions=[e_a_action],
            agg_snort_ids_metrics=[snort_ids], emulation_env_config=em_env_conf,
            ossec_host_alert_counters={"ossec_host": [ossec_ids]}, aggregated_ossec_host_alert_counters=[ossec_ids],
            openflow_flow_stats=[flow_stat], openflow_port_stats=[port_stat],
            avg_openflow_flow_stats=[avg_flow_stat], avg_openflow_port_stats=[avg_port_stat],
            openflow_flow_metrics_per_switch={"openflow_metrics": [flow_stat]},
            openflow_port_metrics_per_switch={"openflow_flow_metrics": [port_stat]},
            openflow_flow_avg_metrics_per_switch={"openflow_avg_metrics": [avg_flow_stat]},
            openflow_port_avg_metrics_per_switch={"openflow_port_avg_metrics": [avg_port_stat]},
            agg_openflow_flow_metrics_per_switch={"agg_openflow_flow_metrics": [agg_flow_stat]},
            agg_openflow_flow_stats=[agg_flow_stat],
            snort_ids_ip_metrics={"snort_ids_ip": [snort_ipa]},
            agg_snort_ids_rule_metrics=[snort_rule],
            snort_alert_metrics_per_ids={"snort_alert_metrics": [snort_ids]},
            snort_rule_metrics_per_ids={"snort_rule_metrics": [snort_rule]})
        return emulation_metric_time_series

    def test_getNodeStatus(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the getNodeStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        ip = "7.7.7.7"
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_host_ip', return_value=ip)
        mocker.patch('csle_common.util.cluster_util.ClusterUtil.get_config', return_value=example_config)
        mocker.patch('csle_common.util.cluster_util.ClusterUtil.am_i_leader', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_cadvisor_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_prometheus_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_grafana_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_pgadmin_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_nginx_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_flask_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_postgresql_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_statsmanager_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_node_exporter_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_docker_engine_running', return_value=True)
        response: NodeStatusDTO = query_cluster_manager.get_node_status(stub=grpc_stub)
        assert response.ip == ip
        assert response.leader
        assert response.cAdvisorRunning
        assert response.prometheusRunning
        assert response.grafanaRunning
        assert response.pgAdminRunning
        assert response.nginxRunning
        assert response.flaskRunning
        assert response.dockerStatsManagerRunning
        assert response.nodeExporterRunning
        assert response.postgreSQLRunning
        assert response.dockerEngineRunning

        mocker.patch('csle_common.util.cluster_util.ClusterUtil.am_i_leader', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_cadvisor_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_prometheus_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_grafana_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_pgadmin_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_nginx_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_flask_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_postgresql_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_statsmanager_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_node_exporter_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_docker_engine_running', return_value=False)
        response = query_cluster_manager.get_node_status(stub=grpc_stub)
        assert response.ip == ip
        assert not response.leader
        assert not response.cAdvisorRunning
        assert not response.prometheusRunning
        assert not response.grafanaRunning
        assert not response.pgAdminRunning
        assert not response.nginxRunning
        assert not response.flaskRunning
        assert not response.dockerStatsManagerRunning
        assert not response.nodeExporterRunning
        assert not response.postgreSQLRunning
        assert not response.dockerEngineRunning

    def test_startPosgtreSQL(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the startPosgtreSQL grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_postgresql', return_value=(False, None, None))
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_postgresql_running', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.start_postgresql(stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_postgresql', return_value=(True, "PIPE", "PIPE"))
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_postgresql_running', return_value=False)
        response = query_cluster_manager.start_postgresql(stub=grpc_stub)
        assert response.running

    def test_stopPostgreSQL(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopPosgtreSQL grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_postgresql', return_value=(False, None, None))
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_postgresql_running', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.stop_postgresql(stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_postgresql', return_value=(True, "PIPE", "PIPE"))
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_postgresql_running', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.stop_postgresql(stub=grpc_stub)
        assert not response.running

    def test_startDockerEngine(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startDockerEngine grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_docker_engine_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_docker_engine', return_value=(False, None, None))
        response: ServiceStatusDTO = query_cluster_manager.start_docker_engine(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_docker_engine_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_docker_engine', return_value=(True, "PIPE", "PIPE"))
        response: ServiceStatusDTO = query_cluster_manager.start_docker_engine(
            stub=grpc_stub)
        assert response.running

    def test_stopDockerEngine(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopDockerEngine grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_docker_engine_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_docker_engine', return_value=(False, None, None))
        response: ServiceStatusDTO = query_cluster_manager.stop_docker_engine(
            stub=grpc_stub)
        assert not response.running

        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_docker_engine_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_docker_engine', return_value=(True, "PIPE", "PIPE"))
        response = query_cluster_manager.stop_docker_engine(stub=grpc_stub)
        assert not response.running

    def test_startNginx(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startNginx grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_nginx_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_nginx', return_value=(False, None, None))
        response: ServiceStatusDTO = query_cluster_manager.start_nginx(stub=grpc_stub)
        assert response.running

        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_nginx_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_nginx', return_value=(True, "PIPE", "PIPE"))
        response: ServiceStatusDTO = query_cluster_manager.start_nginx(stub=grpc_stub)
        assert response.running

    def test_stopNginx(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopNginx grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_nginx_running', return_value=True)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_nginx', return_value=(False, None, None))
        response: ServiceStatusDTO = query_cluster_manager.stop_nginx(stub=grpc_stub)
        assert not response.running

        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_nginx_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_nginx', return_value=(True, "PIPE", "PIPE"))
        response: ServiceStatusDTO = query_cluster_manager.stop_nginx(stub=grpc_stub)
        assert not response.running

    def test_startCAdvisor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startCAdvisor grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_cadvisor', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.start_cadvisor(stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_cadvisor', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.start_cadvisor(stub=grpc_stub)
        assert response.running

    def test_stopCAdvisor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopCAdvisor grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_cadvisor', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.stop_cadvisor(stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_cadvisor', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.stop_cadvisor(stub=grpc_stub)
        assert not response.running

    def test_startNodeExporter(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startNodeExporter grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_node_exporter', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.start_node_exporter(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_node_exporter', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.start_node_exporter(
            stub=grpc_stub)
        assert response.running

    def test_stopNodeExporter(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopNodeExporter grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_node_exporter', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.stop_node_exporter(
            stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_node_exporter', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.stop_node_exporter(
            stub=grpc_stub)
        assert not response.running

    def test_startGrafana(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startGrafana grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_grafana', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.start_grafana(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_grafana', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.start_grafana(
            stub=grpc_stub)
        assert response.running

    def test_stopGrafana(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopGrafana grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_grafana', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.stop_grafana(
            stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_grafana', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.stop_grafana(
            stub=grpc_stub)
        assert not response.running

    def test_startPrometheus(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startPrometheus grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_prometheus', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.start_prometheus(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_prometheus', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.start_prometheus(
            stub=grpc_stub)
        assert response.running

    def test_stopPrometheus(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopPrometheus grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_prometheus', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.stop_prometheus(
            stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_prometheus', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.stop_prometheus(
            stub=grpc_stub)
        assert not response.running

    def test_startPgAdmin(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startPgAdmin grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_pgadmin', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.start_pgadmin(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_pgadmin', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.start_pgadmin(
            stub=grpc_stub)
        assert response.running

    def test_stopPgAdmin(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopPgAdmin grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_pgadmin', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.stop_pgadmin(
            stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_pgadmin', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.stop_pgadmin(
            stub=grpc_stub)
        assert not response.running

    def test_startFlask(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startFlask grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_flask', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.start_flask(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_flask', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.start_flask(
            stub=grpc_stub)
        assert response.running

    def test_stopFlask(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startFlask grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_flask', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.stop_flask(
            stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_flask', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.stop_flask(
            stub=grpc_stub)
        assert not response.running

    def test_startDockerStatsManager(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startDockerStatsManager grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_docker_statsmanager', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.start_docker_statsmanager(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_docker_statsmanager', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.start_docker_statsmanager(
            stub=grpc_stub)
        assert response.running

    def test_stopDockerStatsManager(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopDockerStatsManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_docker_statsmanager', return_value=False)
        response: ServiceStatusDTO = query_cluster_manager.stop_docker_statsmanager(
            stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_docker_statsmanager', return_value=True)
        response: ServiceStatusDTO = query_cluster_manager.stop_docker_statsmanager(
            stub=grpc_stub)
        assert not response.running

    def test_getLogFile(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getLogFile grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail',
                     return_value="abcdef")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        response: LogsDTO = query_cluster_manager.get_log_file(stub=grpc_stub,
                                                               log_file_name="abcdef")
        assert response.logs == ['abcdef']
        mocker.patch('builtins.open', return_value=None)
        response: LogsDTO = query_cluster_manager.get_log_file(stub=grpc_stub,
                                                               log_file_name="abcdef")
        assert response.logs == []

    def test_getFlaskLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the getFlaskLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config',
                     return_value=example_config)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail',
                     return_value="abcdef")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        response: LogsDTO = query_cluster_manager.get_flask_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']
        mocker.patch('builtins.open', return_value=None)
        response: LogsDTO = query_cluster_manager.get_flask_logs(stub=grpc_stub)
        assert response.logs == []

    def test_getPostrgreSQLLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the getPostrgreSQLLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: an example Config object, obtained from the conftest.py file
        :return: None
        """
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config',
                     return_value=example_config)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail',
                     return_value="abcdef")
        mocker.patch("os.listdir", return_value=[constants.FILE_PATTERNS.LOG_SUFFIX])
        mocker.patch("os.path.isfile", return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        response: LogsDTO = query_cluster_manager.get_postgresql_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']
        mocker.patch('builtins.open', return_value=None)
        response: LogsDTO = query_cluster_manager.get_postgresql_logs(stub=grpc_stub)
        assert response.logs == []

    def test_getDockerLogs(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getDockerLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        Popen_mock = mocker.MagicMock()
        mocker.patch('subprocess.Popen', return_value=Popen_mock)
        Popen_mock.configure_mock(**{"communicate.return_value": (b'abcdef', None)})
        response: LogsDTO = query_cluster_manager.get_docker_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']

        Popen_mock.configure_mock(**{"communicate.return_value": (b'', None)})
        response: LogsDTO = query_cluster_manager.get_docker_logs(stub=grpc_stub)
        assert response.logs == ['']

    def test_getNginxLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the getNginxLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        mocker.patch('os.listdir', return_value=[constants.FILE_PATTERNS.LOG_SUFFIX])
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config',
                     return_value=example_config)
        mocker.patch('os.path.isfile', return_value=True)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail',
                     return_value="abcdef")
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        response: LogsDTO = query_cluster_manager.get_nginx_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']
        mocker.patch('os.listdir', return_value="null")
        mocker.patch('os.path.isfile', return_value=False)
        response = query_cluster_manager.get_nginx_logs(stub=grpc_stub)
        assert response.logs == []

    def test_getGrafanaLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the getGrafanaLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        Popen_mock = mocker.MagicMock()
        mocker.patch('subprocess.Popen', return_value=Popen_mock)
        Popen_mock.configure_mock(**{"communicate.return_value": (b'abcdef', None)})
        response: LogsDTO = query_cluster_manager.get_grafana_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']

    def test_getPgAdminLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the getPgAdminLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        Popen_mock = mocker.MagicMock()
        mocker.patch('subprocess.Popen', return_value=Popen_mock)
        Popen_mock.configure_mock(**{"communicate.return_value": (b'abcdef', None)})
        response: LogsDTO = query_cluster_manager.get_pgadmin_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']

    def test_getCadvisorLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the getCadvisorLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        Popen_mock = mocker.MagicMock()
        mocker.patch('subprocess.Popen', return_value=Popen_mock)
        Popen_mock.configure_mock(**{"communicate.return_value": (b'abcdef', None)})
        response: LogsDTO = query_cluster_manager.get_cadvisor_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']

    def test_getNodeExporterLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the getNodeExporterLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        mocker.patch('os.listdir', return_value=[constants.FILE_PATTERNS.LOG_SUFFIX])
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config',
                     return_value=example_config)
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail',
                     return_value="abcdef")
        response: LogsDTO = query_cluster_manager.get_node_exporter_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']
        mocker.patch('os.path.exists', return_value=False)
        response = query_cluster_manager.get_node_exporter_logs(stub=grpc_stub)
        assert response.logs == []

    def test_getPrometheusLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the getPrometheusLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        mocker.patch('os.listdir', return_value=[constants.FILE_PATTERNS.LOG_SUFFIX])
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config',
                     return_value=example_config)
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail',
                     return_value="abcdef")
        response: LogsDTO = query_cluster_manager.get_prometheus_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']
        mocker.patch('os.path.exists', return_value=False)
        response = query_cluster_manager.get_prometheus_logs(stub=grpc_stub)
        assert response.logs == []

    def test_getDockerStatsManagerLogs(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                       example_config: Config) -> None:
        """
        Tests the getDockerStatsManagerLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        mocker.patch('os.listdir', return_value=[constants.FILE_PATTERNS.LOG_SUFFIX])
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config',
                     return_value=example_config)
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail',
                     return_value="abcdef")
        response: LogsDTO = query_cluster_manager.get_docker_statsmanager_logs(
            stub=grpc_stub)
        assert response.logs == ['abcdef']
        mocker.patch('os.path.exists', return_value=False)
        response = query_cluster_manager.get_docker_statsmanager_logs(
            stub=grpc_stub)
        assert response.logs == []

    def test_getCsleLogFiles(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the getCsleLogFiles grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        mocker.patch('os.listdir', return_value=['1', '2', '3', '4', '5', '6', '8', '9', '0', '8', '7',
                                                 '5', '4', '3', '2', '6', '8', '87', '6', '1', '2'])
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config',
                     return_value=example_config)
        mocker.patch('os.path.isfile', return_value=True)
        response: LogsDTO = query_cluster_manager.get_csle_log_files(
            stub=grpc_stub)
        assert len(response.logs) == 20
        mocker.patch('os.listdir', return_value=['abcdef'])
        response: LogsDTO = query_cluster_manager.get_csle_log_files(
            stub=grpc_stub)
        assert response.logs == [f"{example_config.default_log_dir}{constants.COMMANDS.SLASH_DELIM}abcdef"]
        mocker.patch('os.path.isfile', return_value=False)
        response: LogsDTO = query_cluster_manager.get_csle_log_files(
            stub=grpc_stub)
        assert response.logs == []

    def test_startContainersInExecution(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config,
                                        get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startContainersInExecution grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController.run_containers",
                     return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.update_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_containers_in_execution(stub=grpc_stub,
                                          emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_containers_in_execution(stub=grpc_stub, emulation="JohnDoeEmulation",
                                          ip_first_octet=1)
        assert not response.outcome

    def test_attachContainersInExecutionToNetworks(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                                   example_config: Config, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the attachContainersInExecutionToNetworks grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "connect_containers_to_networks", return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.update_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            attach_containers_in_execution_to_networks(stub=grpc_stub, emulation="JohnDoeEmulation",
                                                       ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            attach_containers_in_execution_to_networks(stub=grpc_stub,
                                                       emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_installLibraries(self, grpc_stub, mocker: pytest_mock.MockFixture,
                              get_ex_exec: EmulationExecution) -> None:
        """
        Tests the installLibraries grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "install_csle_collector_and_ryu_libraries", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.install_libraries(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.install_libraries(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_applyKafkaConfig(self, grpc_stub, mocker: pytest_mock.MockFixture,
                              get_ex_exec: EmulationExecution) -> None:
        """
        Tests the applyKafkaConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "apply_kafka_config", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.apply_kafka_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.apply_kafka_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startSdnController(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                                start_ryu: RyuDTO) -> None:
        """
        Tests the startSdnController grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param start_ryu: fixture that gets the return value of the start_ryu method which will be mocked
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.start_ryu",
                     side_effect=start_ryu)
        response: OperationOutcomeDTO = query_cluster_manager.start_sdn_controller(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_sdn_controller(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_applyResourceConstraints(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                      get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startSdnController grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.resource_constraints_controller.ResourceConstraintsController."
                     "apply_resource_constraints", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.apply_resource_constraints(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.apply_resource_constraints(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_createOvsSwitches(self, grpc_stub, mocker: pytest_mock.MockFixture,
                               get_ex_exec: EmulationExecution) -> None:
        """
        Tests the createOvsSwitches grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.ovs_controller.OVSController."
                     "create_virtual_switches_on_container", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.create_ovs_switches(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.create_ovs_switches(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_pingExecution(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the pingExecution grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController.ping_all",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.ping_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.ping_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_configureOvs(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the configureOvs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.ovs_controller.OVSController.apply_ovs_config",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.configure_ovs(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.configure_ovs(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startSdnControllerMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                       get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startSdnControllerMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.start_ryu_monitor",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_sdn_controller_monitor(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_sdn_controller_monitor(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_createUsers(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the createUsers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.users_controller.UsersController.create_users",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.create_users(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.create_users(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_createVulnerabilities(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                   get_ex_exec: EmulationExecution) -> None:
        """
        Tests the createVulnerabilities grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.vulnerabilities_controller.VulnerabilitiesController.create_vulns",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.create_vulnerabilities(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.create_vulnerabilities(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_createFlags(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the createFlags grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.flags_controller.FlagsController.create_flags",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.create_flags(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.create_flags(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_createTopology(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the createTopology grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.topology_controller.TopologyController.create_topology",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.create_topology(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.create_topology(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startTrafficManagers(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                  get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startTrafficManagers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.start_traffic_managers",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_traffic_managers(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_traffic_managers(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startTrafficGenerators(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                    get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startTrafficGenerators grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.start_internal_traffic_generators",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_traffic_generators(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_traffic_generators(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startClientPopulation(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                   get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startClientPopulation grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.start_client_population",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_client_population(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_client_population(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startKafkaClientProducer(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                      get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startKafkaClientProducer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.start_client_producer",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_kafka_client_producer(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_kafka_client_producer(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopKafkaClientProducer(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                     get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopKafkaClientProducer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.stop_client_producer",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_kafka_client_producer(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_kafka_client_producer(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startSnortIdses(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startSnortIdses grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController.start_snort_idses",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_snort_idses(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_snort_idses(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startSnortIdsesMonitorThreads(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                           get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startSnortIdsesMonitorThreads grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "start_snort_idses_monitor_threads", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_snort_idses_monitor_threads(stub=grpc_stub, emulation="JohnDoeEmulation",
                                              ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_snort_idses_monitor_threads(stub=grpc_stub, emulation="JohnDoeEmulation",
                                              ip_first_octet=1)
        assert not response.outcome

    def test_startOssecIdses(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startOssecIdses grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "start_ossec_idses", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_ossec_idses(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_ossec_idses(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startOssecIdsesMonitorThreads(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                           get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startOssecIdsesMonitorThreads grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "start_ossec_idses_monitor_threads", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_idses_monitor_threads(stub=grpc_stub, emulation="JohnDoeEmulation",
                                              ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_idses_monitor_threads(stub=grpc_stub, emulation="JohnDoeEmulation",
                                              ip_first_octet=1)
        assert not response.outcome

    def test_startElkStack(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startElkStack grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.elk_controller.ELKController.start_elk_stack",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_elk_stack(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_elk_stack(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startHostManagers(self, grpc_stub, mocker: pytest_mock.MockFixture,
                               get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startHostManagers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.start_host_monitor_threads",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_host_managers(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_host_managers(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_applyFileBeatsConfig(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                  get_ex_exec: EmulationExecution) -> None:
        """
        Tests the applyFileBeatsConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.config_filebeats",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.apply_filebeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.apply_filebeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_applyPacketBeatsConfig(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                    get_ex_exec: EmulationExecution) -> None:
        """
        Tests the applyPacketBeatsConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.config_packetbeats",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.apply_packetbeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.apply_packetbeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_applyMetricBeatsConfig(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                    get_ex_exec: EmulationExecution) -> None:
        """
        Tests the applyMetricBeatsConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.config_metricbeats",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.apply_metricbeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.apply_metricbeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_applyHeartBeatsConfig(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                   get_ex_exec: EmulationExecution) -> None:
        """
        Tests the applyHeartBeatsConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.config_heartbeats",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.apply_heartbeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.apply_heartbeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startFilebeats(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startFilebeats grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.start_filebeats",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_filebeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_filebeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startPacketbeats(self, grpc_stub, mocker: pytest_mock.MockFixture,
                              get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startPacketbeats grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.start_packetbeats",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_packetbeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_packetbeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startMetricbeats(self, grpc_stub, mocker: pytest_mock.MockFixture,
                              get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startMetricbeats grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.start_metricbeats",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_metricbeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_metricbeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startHeartbeats(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startHeartbeats grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.start_heartbeats",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_heartbeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_heartbeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startDockerStatsManagerThread(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                           get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startDockerStatsManagerThread grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.container_controller.ContainerController.start_docker_stats_thread",
                     return_value=None)
        response: ServiceStatusDTO = query_cluster_manager. \
            start_docker_statsmanager_thread(stub=grpc_stub, emulation="JohnDoeEmulation",
                                             ip_first_octet=1)
        assert response.running
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: ServiceStatusDTO = query_cluster_manager. \
            start_docker_statsmanager_thread(stub=grpc_stub, emulation="JohnDoeEmulation",
                                             ip_first_octet=1)
        assert not response.running

    def test_stopAllExecutionsOfEmulation(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                          get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the stopAllExecutionsOfEmulation grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_em_env: fixture which creates an example emulation configuration
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_by_name",
                     return_value=get_ex_em_env)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "stop_all_executions_of_emulation", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_all_executions_of_emulation(stub=grpc_stub, emulation="JohnDoeEmulation")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_by_name",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_all_executions_of_emulation(stub=grpc_stub, emulation="JohnDoeEmulation")
        assert not response.outcome

    def test_stopExecution(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopExecution grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "stop_execution_of_emulation", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_execution(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_execution(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopAllExecutions(self, grpc_stub, mocker: pytest_mock.MockFixture,
                               get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopAllExecutions grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "stop_all_executions", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_all_executions(stub=grpc_stub)
        assert response.outcome

    def test_cleanAllExecutions(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the cleanAllExecutions grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "clean_all_executions", return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     return_value=example_config)
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.am_i_leader",
                     return_value=True)
        response: OperationOutcomeDTO = query_cluster_manager. \
            clean_all_executions(stub=grpc_stub)
        assert response.outcome
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.am_i_leader",
                     return_value=False)
        response: OperationOutcomeDTO = query_cluster_manager. \
            clean_all_executions(stub=grpc_stub)
        assert response.outcome

    def test_cleanAllExecutionsOfEmulation(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                           get_ex_em_env: EmulationEnvConfig, example_config: Config) -> None:
        """
        Tests the cleanAllExecutionsOfEmulation grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :param get_ex_em_env: fixture which creates an example emulation configuration
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     return_value=example_config)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_by_name",
                     return_value=get_ex_em_env)
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.am_i_leader",
                     return_value=True)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "clean_all_emulation_executions", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            clean_all_executions_of_emulation(stub=grpc_stub, emulation="JohnDoeEmulation")
        assert response.outcome
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.am_i_leader",
                     return_value=False)
        response: OperationOutcomeDTO = query_cluster_manager. \
            clean_all_executions_of_emulation(stub=grpc_stub, emulation="JohnDoeEmulation")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_by_name",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            clean_all_executions_of_emulation(stub=grpc_stub, emulation="JohnDoeEmulation")
        assert not response.outcome

    def test_cleanExecution(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                            example_config: Config) -> None:
        """
        Tests the cleanExecution grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     return_value=example_config)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.am_i_leader",
                     return_value=True)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "clean_emulation_execution", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.clean_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.am_i_leader",
                     return_value=False)
        response: OperationOutcomeDTO = query_cluster_manager.clean_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.clean_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startTrafficManager_(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                  get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startTrafficManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.start_traffic_manager",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_traffic_manager(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1, container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager.start_traffic_manager(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1, container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopTrafficManager_(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                                 example_config: Config) -> None:
        """
        Tests the stopTrafficManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.stop_traffic_manager",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_traffic_manager(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1, container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager.stop_traffic_manager(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1, container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopTrafficManagers(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                                 example_config: Config) -> None:
        """
        Tests the stopTrafficManagers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.stop_traffic_managers",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_traffic_managers(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_traffic_managers(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startClientManager(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                                example_config: Config) -> None:
        """
        Tests the startClientManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.start_client_manager",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_client_manager(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager.start_client_manager(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopClientManager(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                               example_config: Config) -> None:
        """
        Tests the stopClientManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.stop_client_manager",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_client_manager(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager.stop_client_manager(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopClientPopulation(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                  get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopClientPopulation grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.stop_client_population",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_client_population(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager.stop_client_population(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_getNumActiveClients(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                                 get_clients: ClientsDTO, empty_clients: GetNumClientsDTO) -> None:
        """
        Tests the getNumActiveClients grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.get_num_active_clients",
                     side_effect=get_clients)
        response: GetNumClientsDTO = query_cluster_manager.get_num_active_clients(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.client_process_active
        assert response.producer_active
        assert response.clients_time_step_len_seconds == 4
        assert response.producer_time_step_len_seconds == 5
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil."
                     "get_empty_get_num_clients_dto", side_effect=empty_clients)
        response: GetNumClientsDTO = query_cluster_manager.get_num_active_clients(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.num_clients == 4
        assert response.client_process_active
        assert response.producer_active
        assert response.clients_time_step_len_seconds == 4
        assert response.producer_time_step_len_seconds == 4

    def test_stopTrafficGenerators(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                   get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopTrafficGenerators grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController."
                     "stop_internal_traffic_generators", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_traffic_generators(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_traffic_generators(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startTrafficGenerator(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                   get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startTrafficGenerator grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController."
                     "start_internal_traffic_generator", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_traffic_generator(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1, container_ip='123.456.78.99')
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager.start_traffic_generator(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1, container_ip='123.456.78.99')
        assert not response.outcome

    def test_stopTrafficGenerator(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                  get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopTrafficGenerator grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController."
                     "stop_internal_traffic_generator", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_traffic_generator(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1, container_ip='123.456.78.99')
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip", return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager.stop_traffic_generator(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1, container_ip='123.456.78.99')
        assert not response.outcome

    def test_getClientManagersInfo(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                                   active_ips: List[str]) -> None:
        """
        Tests the getClientManagersInfo grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param active_ips: fixture that creates a list of active IPs
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.get_client_managers_info",
                     return_value=TestClusterManagerSuite.client_mng_info())
        mocker.patch("csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_active_ips",
                     side_effect=active_ips)
        response: ClientManagersInfoDTO = query_cluster_manager.get_client_managers_info(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.ips == ["123.456.78.99"]
        assert response.ports == [1]
        assert response.emulationName == "JohnDoeEmulation"
        assert response.executionId == 1
        assert response.clientManagersRunning
        assert response.clientManagersStatuses[0].num_clients == 4
        assert response.clientManagersStatuses[0].client_process_active
        assert response.clientManagersStatuses[0].producer_active
        assert response.clientManagersStatuses[0].clients_time_step_len_seconds == 4
        assert response.clientManagersStatuses[0].producer_time_step_len_seconds == 5
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip", return_value="99.87.654.321")
        response: ClientManagersInfoDTO = query_cluster_manager.get_client_managers_info(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.ips == []
        assert response.ports == []
        assert response.emulationName == ""
        assert response.executionId == -1
        assert not response.clientManagersRunning
        assert response.clientManagersStatuses == []

    def test_getTrafficManagersInfo(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                                    active_ips: List[str]) -> None:
        """
        Tests the getTrafficManagersInfo grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param active_ips: fixture that creates a list of active IPs
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController."
                     "get_traffic_managers_info", return_value=TestClusterManagerSuite.traffic_mng_info())
        mocker.patch("csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_active_ips",
                     side_effect=active_ips)
        response: TrafficManagersInfoDTO = query_cluster_manager.get_traffic_managers_info(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.ips == ['123.456.78.99']
        assert response.ports == [1]
        assert response.emulationName == "JohnDoeEmulation"
        assert response.executionId == 1
        assert response.trafficManagersRunning
        assert response.trafficManagersStatuses[0].running
        assert response.trafficManagersStatuses[0].script == "null"
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: TrafficManagersInfoDTO = query_cluster_manager.get_traffic_managers_info(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.ips == []
        assert response.ports == []
        assert response.emulationName == ""
        assert response.executionId == -1
        assert response.trafficManagersRunning == []
        assert response.trafficManagersStatuses == []

    def test_stopAllRunningContainers(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopAllRunningContainers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "stop_all_running_containers", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_all_running_containers(stub=grpc_stub)
        assert response.outcome

    def test_stopContainer(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopContainer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "stop_container", return_value=True)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_container(stub=grpc_stub, container_name="JohnDoeContainer")
        assert response.outcome
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "stop_container", return_value=False)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_container(stub=grpc_stub, container_name="JohnDoeContainer")
        assert not response.outcome

    def test_removeAllStoppedContainers(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the removeAllStoppedContainers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "rm_all_stopped_containers", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_all_stopped_containers(stub=grpc_stub)
        assert response.outcome

    def test_removeContainer(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the removeContainer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController.rm_container",
                     return_value=True)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_container(stub=grpc_stub, container_name="JohnDoeContainer")
        assert response.outcome
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "rm_container", return_value=False)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_container(stub=grpc_stub, container_name="JohnDoeContainer")
        assert not response.outcome

    def test_removeAllContainerImages(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the removeAllContainerImages grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController.rm_all_images",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_all_container_images(stub=grpc_stub)
        assert response.outcome

    def test_removeContainerImage(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the removeContainerImage grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController.rm_image",
                     return_value=True)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_container_image(stub=grpc_stub, image_name="JohnDoeImage")
        assert response.outcome

        mocker.patch("csle_common.controllers.container_controller.ContainerController.rm_image",
                     return_value=False)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_container_image(stub=grpc_stub, image_name="JohnDoeImage")
        assert not response.outcome

    def test_listAllContainerImages(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the listAllContainerImages grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "list_all_images", return_value=[("null", "null", "null", "null", 1)])
        response: ContainerImagesDTO = query_cluster_manager. \
            list_all_container_images(stub=grpc_stub)
        assert response.images[0].repoTags == "null"
        assert response.images[0].created == "null"
        assert response.images[0].os == "null"
        assert response.images[0].architecture == "null"
        assert response.images[0].size == 1

    def test_listAllDockerNetworks(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the listAllDockerNetworks grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "list_docker_networks", return_value=(["null"], [1]))
        response: DockerNetworksDTO = query_cluster_manager. \
            list_all_docker_networks(stub=grpc_stub)
        response.networks == ["null"]
        response.network_ids == [1]

    def test_startAllStoppedContainers(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startAllStoppedContainers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "start_all_stopped_containers", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_all_stopped_containers(stub=grpc_stub)
        assert response.outcome

    def test_startContainer(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startContainer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "start_container", return_value=True)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_container(stub=grpc_stub, container_name="JohnDoeContainer")
        assert response.outcome
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "start_container", return_value=False)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_container(stub=grpc_stub, container_name="JohnDoeContainer")
        assert not response.outcome

    def test_listAllRunningContainers(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the listAllRunningContainers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "list_all_running_containers", return_value=[("JohnDoe", "null", "123.456.78.99")])
        response: RunningContainersDTO = query_cluster_manager. \
            list_all_running_containers(stub=grpc_stub)
        assert response.runningContainers[0].name == "JohnDoe"
        assert response.runningContainers[0].image == "null"
        assert response.runningContainers[0].ip == "123.456.78.99"

    def test_listAllRunningEmulations(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the listAllRunningEmulations grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "list_running_emulations", return_value=["JDoeEmulation"])
        response: RunningEmulationsDTO = query_cluster_manager. \
            list_all_running_emulations(stub=grpc_stub)
        assert response.runningEmulations == ["JDoeEmulation"]

    def test_listAllStoppedContainers(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the listAllStoppedContainers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "list_all_stopped_containers", return_value=[("JohnDoe", "null", "123.456.78.99")])
        response: StoppedContainersDTO = query_cluster_manager. \
            list_all_stopped_containers(stub=grpc_stub)
        assert response.stoppedContainers[0].name == "JohnDoe"
        assert response.stoppedContainers[0].image == "null"
        assert response.stoppedContainers[0].ip == "123.456.78.99"

    def test_createEmulationNetworks(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config,
                                     get_ex_exec: EmulationExecution) -> None:
        """
        Tests the createEmulationNetworks grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "clean_all_executions", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "create_networks", return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     return_value=example_config)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.am_i_leader",
                     return_value=True)
        response: OperationOutcomeDTO = query_cluster_manager. \
            create_emulation_networks(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.am_i_leader",
                     return_value=False)
        response: OperationOutcomeDTO = query_cluster_manager. \
            create_emulation_networks(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopDockerStatsManagerThread(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                          get_ex_exec) -> None:
        """
        Tests the stopDockerStatsManagerThread grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "stop_docker_stats_thread", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_docker_statsmanager_thread(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=None)
        response = query_cluster_manager. \
            stop_docker_statsmanager_thread(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_getDockerStatsManagerStatus(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getDockerStatsManagerStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "get_docker_stats_manager_status_by_ip_and_port",
                     return_value=DockerStatsMonitorDTO(num_monitors=4,
                                                        emulations=["JDoeEmulation"],
                                                        emulation_executions=[4]))
        response: DockerStatsMonitorStatusDTO = query_cluster_manager. \
            get_docker_stats_manager_status(stub=grpc_stub, port=1)
        assert response.num_monitors == 4
        assert response.emulations == ["JDoeEmulation"]
        assert response.emulation_executions == [4]

    def test_removeDockerNetworks(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the removeDockerNetworks grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """

        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "remove_networks", return_value=True)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_docker_networks(stub=grpc_stub, networks=["JDoeNetworks"])
        assert response.outcome
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "remove_networks", return_value=False)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_docker_networks(stub=grpc_stub, networks=["JDoeNetworks"])
        assert not response.outcome

    def test_removeAllDockerNetworks(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the removeAllDockerNetworks grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """

        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "rm_all_networks", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_all_docker_networks(stub=grpc_stub)
        assert response.outcome

    def test_getDockerStatsManagersInfo(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                        get_ex_exec: EmulationExecution, active_ips: List[str]) -> None:
        """
        Tests the getDockerStatsManagersInfo grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param active_ips: fixture that creates a list of active IPs
        :return: None
        """
        mocker.patch("csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_active_ips",
                     side_effect=active_ips)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "get_docker_stats_managers_info", return_value=TestClusterManagerSuite.get_dsm_info())
        response: DockerStatsManagersInfoDTO = query_cluster_manager. \
            get_docker_stats_manager_info(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ips == ["123.456.78.99"]
        assert response.ports == [1]
        assert response.emulationName == "JDoeEmulation"
        assert response.executionId == 1
        assert response.dockerStatsManagersRunning
        assert response.dockerStatsManagersStatuses[0].num_monitors == 4
        assert response.dockerStatsManagersStatuses[0].emulations == ["JDoeEmulation"]
        assert response.dockerStatsManagersStatuses[0].emulation_executions == [4]

    def test_stopElkManager(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopElkManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.elk_controller.ELKController."
                     "stop_elk_manager", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_elk_manager(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_elk_manager(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startElkManager(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startElkManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.elk_controller.ELKController."
                     "start_elk_manager", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_elk_manager(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_elk_manager(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_getElkStatus(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getElkStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.elk_controller.ELKController.get_elk_status",
                     return_value=ElkDTO(elasticRunning=True,
                                         kibanaRunning=True,
                                         logstashRunning=True))
        response: ElkStatusDTO = query_cluster_manager. \
            get_elk_status(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.kibanaRunning
        assert response.elasticRunning
        assert response.logstashRunning
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: ElkStatusDTO = query_cluster_manager. \
            get_elk_status(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.kibanaRunning
        assert not response.elasticRunning
        assert not response.logstashRunning

    def test_stopElkStack(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopElkStack grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.elk_controller.ELKController."
                     "stop_elk_stack", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_elk_stack(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_elk_stack(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startElastic(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startElastic grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.elk_controller.ELKController."
                     "start_elastic", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_elastic(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_elastic(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopElastic(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopElastic grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.elk_controller.ELKController."
                     "stop_elastic", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_elastic(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_elastic(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startKibana(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startKibana grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.elk_controller.ELKController."
                     "start_kibana", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_kibana(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_kibana(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopKibana(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopKibana grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.elk_controller.ELKController."
                     "stop_kibana", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_kibana(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_kibana(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startLogstash(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startLogstash grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.elk_controller.ELKController."
                     "start_logstash", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_logstash(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_logstash(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopLogstash(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopLogstash grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.elk_controller.ELKController."
                     "stop_logstash", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_logstash(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_logstash(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_getElkManagersInfo(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                                active_ips: List[str]) -> None:
        """
        Tests the getElkManagersInfo grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param active_ips: fixture that creates a list of active IPs
        :return: None
        """
        mocker.patch("csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_active_ips",
                     side_effect=active_ips)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.elk_controller.ELKController.get_elk_managers_info",
                     return_value=TestClusterManagerSuite.get_elk_mng_info())
        response: ElkManagersInfoDTO = query_cluster_manager. \
            get_elk_managers_info(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ips == ["123.456.78.99"]
        assert response.ports == [1]
        assert response.emulationName == "JohnDoeEmulation"
        assert response.executionId == 1
        assert response.elkManagersRunning
        assert response.elkManagersStatuses[0].elasticRunning
        assert response.elkManagersStatuses[0].kibanaRunning
        assert response.elkManagersStatuses[0].logstashRunning

    def test_startContainersOfExecution(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                        get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startContainersOfExecution grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "start_containers_of_execution", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_containers_of_execution(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_emulation_execution", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_containers_of_execution(stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_runContainer(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the runContainer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """

        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "run_container", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            run_container(stub=grpc_stub, image="JDoeImage",
                          name="JohnDoe", memory=1,
                          num_cpus=10, create_network=True,
                          version="null")
        assert response.outcome

    def test_stopContainersOfExecution(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                       get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopContainersOfExecution grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "start_containers_of_execution", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_containers_of_execution(stub=grpc_stub, emulation="JDoeEmulation",
                                         ip_first_octet=1)
        assert response.outcome

    def test_startHostManager(self, grpc_stub, mocker: pytest_mock.MockFixture,
                              get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startHostManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)

        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.start_host_manager", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_host_manager(stub=grpc_stub, emulation="JDoeEmulation",
                               ip_first_octet=1, container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            start_host_manager(stub=grpc_stub, emulation="JDoeEmulation",
                               ip_first_octet=1, container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopHostManager(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopHostManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.stop_host_manager", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")

        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_host_manager(stub=grpc_stub, emulation="JDoeEmulation",
                              ip_first_octet=1, container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            stop_host_manager(stub=grpc_stub, emulation="JDoeEmulation",
                              ip_first_octet=1, container_ip="123.456.78.99")
        assert not response.outcome

    def test_startHostMonitorThreads(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                     get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startHostMonitorThreads grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.start_host_monitor_threads", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_host_monitor_threads(stub=grpc_stub, emulation="JDoeEmulation",
                                       ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            start_host_monitor_threads(stub=grpc_stub, emulation="JDoeEmulation",
                                       ip_first_octet=1)
        assert not response.outcome

    def test_stopFilebeats(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopFilebeats grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.stop_filebeats", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_filebeats(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            stop_filebeats(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopPacketbeats(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopPacketbeats grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.stop_packetbeats", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_packetbeats(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            stop_packetbeats(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopMetricbeats(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopMetricbeats grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.stop_metricbeats", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_metricbeats(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            stop_metricbeats(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopHeartbeats(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopHeartbeats grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.stop_heartbeats", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_heartbeats(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            stop_heartbeats(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startHostMonitorThread(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                    get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startHostMonitorThread grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.start_host_monitor_thread", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_host_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                      container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_host_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                      container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            start_host_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                      container_ip="123.456.78.99")
        assert not response.outcome

    def test_startFilebeat_(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startFilebeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.start_filebeat", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_filebeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                           container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_filebeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                           container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            start_filebeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                           container_ip="123.456.78.99")
        assert not response.outcome

    def test_startPacketbeat(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startPacketbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.start_packetbeat", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_packetbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                             container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_packetbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                             container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            start_packetbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                             container_ip="123.456.78.99")
        assert not response.outcome

    def test_startMetricbeat(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startMetricbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.start_metricbeat", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_metricbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                             container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_metricbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                             container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            start_metricbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                             container_ip="123.456.78.99")
        assert not response.outcome

    def test_startHeartbeat(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startHeartbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.start_heartbeat", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_heartbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                            container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_heartbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                            container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            start_heartbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                            container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopFilebeat(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopFilebeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.stop_filebeat", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_filebeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                          container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_filebeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                          container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            stop_filebeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                          container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopPacketbeat(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopPacketbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.stop_packetbeat", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_packetbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                            container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_packetbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                            container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            stop_packetbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                            container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopMetricbeat(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopMetricbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.stop_metricbeat", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_metricbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                            container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_metricbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                            container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            stop_metricbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                            container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopHeartbeat(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopHeartbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.stop_heartbeat", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_heartbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                           container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_heartbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                           container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            stop_heartbeat(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                           container_ip="123.456.78.99")
        assert not response.outcome

    def test_applyFileBeatConfig(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                 get_ex_exec: EmulationExecution) -> None:
        """
        Tests the applyFileBeatConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.config_filebeat", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            apply_filebeat_config(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                  container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            apply_filebeat_config(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                  container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            apply_filebeat_config(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                  container_ip="123.456.78.99")
        assert not response.outcome

    def test_applyPacketBeatConfig(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                   get_ex_exec: EmulationExecution) -> None:
        """
        Tests the applyPacketBeatConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.config_packetbeat", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            apply_packetbeat_config(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                    container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            apply_packetbeat_config(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                    container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            apply_packetbeat_config(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                    container_ip="123.456.78.99")
        assert not response.outcome

    def test_applyMetricBeatConfig(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                   get_ex_exec: EmulationExecution) -> None:
        """
        Tests the applyMetricBeatConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.config_metricbeat", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            apply_metricbeat_config(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                    container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            apply_metricbeat_config(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                    container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            apply_metricbeat_config(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                    container_ip="123.456.78.99")
        assert not response.outcome

    def test_applyHeartBeatConfig(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                  get_ex_exec: EmulationExecution) -> None:
        """
        Tests the applyHeartBeatConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.config_heartbeat", return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            apply_heartbeat_config(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                   container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            apply_heartbeat_config(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                   container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            apply_heartbeat_config(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                   container_ip="123.456.78.99")
        assert not response.outcome

    def test_getHostMonitorThreadsStatuses(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                           get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getHostMonitorThreadsStatuses grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.get_host_monitor_threads_statuses",
                     return_value=[TestClusterManagerSuite.host_status_dto()])
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: HostManagerStatusesDTO = query_cluster_manager. \
            get_host_monitor_threads_statuses(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.hostManagerStatuses[0].monitor_running
        assert response.hostManagerStatuses[0].filebeat_running
        assert response.hostManagerStatuses[0].packetbeat_running
        assert response.hostManagerStatuses[0].monitor_running
        assert response.hostManagerStatuses[0].ip == "123.456.78.99"
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: HostManagerStatusesDTO = query_cluster_manager. \
            get_host_monitor_threads_statuses(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.hostManagerStatuses == []

    def test_getHostManagersInfo(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                 get_ex_exec: EmulationDefenderActionOutcome, active_ips: List[str]) -> None:
        """
        Tests the getHostManagersInfo grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param active_ips: fixture that creates a list of active IPs
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller."
                     "HostController.get_host_managers_info",
                     return_value=TestClusterManagerSuite.get_host_mng_info())
        mocker.patch("csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_active_ips",
                     side_effect=active_ips)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: HostManagersInfoDTO = query_cluster_manager. \
            get_host_managers_info(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ips == ["123.456.78.99"]
        assert response.ports == [1]
        assert response.emulationName == "JDoeEmulation"
        assert response.executionId == 1
        assert response.hostManagersRunning
        assert response.hostManagersStatuses[0].monitor_running
        assert response.hostManagersStatuses[0].filebeat_running
        assert response.hostManagersStatuses[0].packetbeat_running
        assert response.hostManagersStatuses[0].metricbeat_running
        assert response.hostManagersStatuses[0].heartbeat_running
        assert response.hostManagersStatuses[0].ip == "123.456.78.99"
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: HostManagersInfoDTO = query_cluster_manager. \
            get_host_managers_info(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ips == []
        assert response.ports == []
        assert response.emulationName == ""
        assert response.executionId == -1
        assert response.hostManagersRunning == []
        assert response.hostManagersStatuses == []

    def test_stopKafkaManager(self, grpc_stub, mocker: pytest_mock.MockFixture,
                              get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopKafkaManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.kafka_controller.KafkaController.stop_kafka_manager",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_kafka_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_kafka_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startKafkaManager(self, grpc_stub, mocker: pytest_mock.MockFixture,
                               get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startKafkaManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.kafka_controller.KafkaController.start_kafka_manager",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_kafka_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_kafka_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_createKafkaTopics(self, grpc_stub, mocker: pytest_mock.MockFixture,
                               get_ex_exec: EmulationExecution) -> None:
        """
        Tests the createKafkaTopics grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.kafka_controller.KafkaController.create_topics",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            create_kafka_topics(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            create_kafka_topics(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_getKafkaStatus(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getKafkaStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.kafka_controller.KafkaController.get_kafka_status",
                     return_value=KafkaDTO(running=True, topics=["null"]))
        response: KafkaStatusDTO = query_cluster_manager. \
            get_kafka_status(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.running
        assert response.topics == ["null"]
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: KafkaStatusDTO = query_cluster_manager. \
            get_kafka_status(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.running
        assert response.topics == []

    def test_stopKafkaServer(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopKafkaServer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.kafka_controller.KafkaController.stop_kafka_server",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_kafka_server(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_kafka_server(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startKafkaServer(self, grpc_stub, mocker: pytest_mock.MockFixture,
                              get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startKafkaServer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.kafka_controller.KafkaController.start_kafka_server",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_kafka_server(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_kafka_server(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_getKafkaManagersInfo(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                                  active_ips: List[str]) -> None:
        """
        Tests the getKafkaManagersInfo grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param active_ips: fixture that creates a list of active IPs
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_active_ips",
                     side_effect=active_ips)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.kafka_controller.KafkaController."
                     "get_kafka_managers_info",
                     return_value=TestClusterManagerSuite.get_kafka_mng_info())
        response: KafkaManagersInfoDTO = query_cluster_manager. \
            get_kafka_managers_info(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ips == ["123.456.78.99"]
        assert response.ports == [1]
        assert response.emulationName == "JDoeEmulation"
        assert response.executionId == 1
        assert response.kafkaManagersRunning
        assert response.kafkaManagersStatuses[0].running
        assert response.kafkaManagersStatuses[0].topics == ["null"]

    def test_stopOSSECIDSes(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopOSSECIDSes grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "stop_ossec_idses", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_idses(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_idses(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startOSSECIDSes(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startOSSECIDSes grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "start_ossec_idses", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_idses(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_idses(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopOSSECIDS(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopOSSECIDS grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "stop_ossec_ids", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_ids(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1, container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_ids(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1, container_ip="123.456.78.99")
        assert not response.outcome

    def test_startOSSECIDS(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startOSSECIDS grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "start_ossec_ids", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_ids(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1, container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_ids(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1, container_ip="123.456.78.99")
        assert not response.outcome

    def test_startOSSECIDSManagers(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                   get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startOSSECIDSManagers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "start_ossec_idses_managers", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_ids_managers(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_ids_managers(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopOSSECIDSManagers(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                  get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopOSSECIDSManagers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "stop_ossec_idses_managers", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_ids_managers(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_ids_managers(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startOSSECIDSManager_(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                   get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startOSSECIDSManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "start_ossec_ids_manager", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_ids_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                    container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_ids_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                    container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopOSSECIDSManager_(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                  get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopOSSECIDSManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "stop_ossec_ids_manager", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_ids_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                   container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_ids_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                   container_ip="123.456.78.99")
        assert not response.outcome

    def test_startOSSECIDSMonitorThread(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                        get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startOSSECIDSMonitorThread grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "start_ossec_ids_monitor_thread", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_ids_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                           container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_ids_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                           container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_cluster.cluster_manager.cluster_manager_util."
                     "ClusterManagerUtil.get_container_config",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ossec_ids_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                           container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopOSSECIDSMonitorThread(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                       get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopOSSECIDSMonitorThread grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "stop_ossec_ids_monitor_thread", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_ids_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                          container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_ids_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                          container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_cluster.cluster_manager.cluster_manager_util."
                     "ClusterManagerUtil.get_container_config",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_ids_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                          container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopOSSECIDSMonitorThreads(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                        get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopOSSECIDSMonitorThreads grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "stop_ossec_idses_monitor_threads", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_ids_monitor_threads(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ossec_ids_monitor_threads(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_getOSSECIDSMonitorThreadStatuses(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                              get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getOSSECIDSMonitorThreadStatuses grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "get_ossec_idses_monitor_threads_statuses",
                     return_value=TestClusterManagerSuite.get_ossec_imt_statuses())
        response: OSSECIdsMonitorThreadStatusesDTO = query_cluster_manager. \
            get_ossec_ids_monitor_thread_statuses(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ossecIDSStatuses[0].monitor_running
        assert response.ossecIDSStatuses[0].ossec_ids_running
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OSSECIdsMonitorThreadStatusesDTO = query_cluster_manager. \
            get_ossec_ids_monitor_thread_statuses(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ossecIDSStatuses == []

    def test_getOSSECIdsManagersInfo(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                                     active_ips: List[str]) -> None:
        """
        Tests the getOSSECIdsManagersInfo grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param active_ips: fixture that creates a list of active IPs
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "get_ossec_managers_info",
                     return_value=TestClusterManagerSuite.get_ossec_mng_info())
        mocker.patch("csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_active_ips",
                     side_effect=active_ips)
        response: OSSECIdsManagersInfoDTO = query_cluster_manager. \
            get_ossec_ids_managers_info(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ips == ["123.456.78.99"]
        assert response.ports == [1]
        assert response.emulationName == "JDoeEmulation"
        assert response.executionId == 1
        assert response.ossecIdsManagersRunning
        assert response.ossecIdsManagersStatuses[0].monitor_running
        assert response.ossecIdsManagersStatuses[0].ossec_ids_running

    def test_startRyuManager(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startRyuManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager."
                     "start_ryu_manager", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ryu_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ryu_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopRyuManager(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopRyuManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager."
                     "stop_ryu_manager", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ryu_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ryu_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_getRyuStatus(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                          ryu_status: RyuDTO) -> None:
        """
        Tests the getRyuStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param ryu_status: fixture that gets the return value of the get_ryu_status method which will be mocked
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager."
                     "get_ryu_status", side_effect=ryu_status)
        response: RyuManagerStatusDTO = query_cluster_manager. \
            get_ryu_status(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ryu_running
        assert response.monitor_running
        assert response.port == 4
        assert response.web_port == 4
        assert response.controller == "null"
        assert response.kafka_ip == "123.456.78.99"
        assert response.kafka_port == 7
        assert response.time_step_len == 4
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: RyuManagerStatusDTO = query_cluster_manager. \
            get_ryu_status(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.ryu_running
        assert not response.monitor_running
        assert response.port == -1
        assert response.web_port == -1
        assert response.controller == ""
        assert response.kafka_ip == ""
        assert response.kafka_port == -1
        assert response.time_step_len == -1

    def test_startRyu_(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                       start_ryu: RyuDTO) -> None:
        """
        Tests the startRyu grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param start_ryu: fixture that gets the return value of the start_ryu method which will be mocked
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager."
                     "start_ryu", side_effect=start_ryu)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ryu(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ryu(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopRyu_(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                      stop_ryu: RyuDTO) -> None:
        """
        Tests the stopRyu grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param stop_ryu: fixture that gets the return value of the stop_ryu method which will be mocked
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager."
                     "stop_ryu", side_effect=stop_ryu)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ryu(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ryu(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_getRyuManagersInfo(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                                active_ips: List[str]) -> None:
        """
        Tests the getRyuManagersInfo grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param active_ips: fixture that creates a list of active IPs
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager."
                     "get_ryu_managers_info", return_value=TestClusterManagerSuite.ryu_mng_info())
        mocker.patch("csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_active_ips",
                     side_effect=active_ips)
        response: RyuManagerStatusDTO = query_cluster_manager. \
            get_ryu_managers_info(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ips == ["123.456.78.99"]
        assert response.ports == [1]
        assert response.emulationName == "JDoeEmulation"
        assert response.ryuManagersRunning == [True]
        assert response.ryuManagersStatuses[0].ryu_running
        assert response.ryuManagersStatuses[0].monitor_running
        assert response.ryuManagersStatuses[0].port == 4
        assert response.ryuManagersStatuses[0].web_port == 4
        assert response.ryuManagersStatuses[0].controller == "null"
        assert response.ryuManagersStatuses[0].kafka_ip == "123.456.78.99"
        assert response.ryuManagersStatuses[0].kafka_port == 7
        assert response.ryuManagersStatuses[0].time_step_len == 4
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: RyuManagerStatusDTO = query_cluster_manager. \
            get_ryu_managers_info(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ips == []
        assert response.ports == []
        assert response.emulationName == ""
        assert response.ryuManagersRunning == []
        assert response.ryuManagersStatuses == []

    def test_stopSnortIdses(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopSnortIdses grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "stop_snort_idses", side_effect=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_snort_idses(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_snort_idses(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_getSnortIdsMonitorThreadStatuses(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                              get_ex_exec: EmulationExecution, active_ips: List[str]) -> None:
        """
        Tests the getSnortIdsMonitorThreadStatuses grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param active_ips: fixture that creates a list of active IPs
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "get_snort_idses_monitor_threads_statuses",
                     return_value=[SnortIdsMonitorDTO(monitor_running=True, snort_ids_running=True)])
        response: SnortIdsMonitorThreadStatusesDTO = query_cluster_manager. \
            get_snort_ids_monitor_thread_statuses(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.snortIDSStatuses[0].monitor_running
        assert response.snortIDSStatuses[0].snort_ids_running
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: SnortIdsMonitorThreadStatusesDTO = query_cluster_manager. \
            get_snort_ids_monitor_thread_statuses(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.snortIDSStatuses == []

    def test_stopSnortIdsesMonitorThreads(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                          get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopSnortIdsesMonitorThreads grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "stop_snort_idses_monitor_threads", side_effect=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_snort_idses_monitor_threads(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_snort_idses_monitor_threads(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopSnortIds_(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopSnortIds grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "stop_snort_ids", side_effect=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_snort_ids(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                           container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_snort_ids(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                           container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopSnortIdsMonitorThread(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                       get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopSnortIdsMonitorThread grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "stop_snort_idses_monitor_thread", side_effect=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_snort_ids_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                          container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_snort_ids_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                          container_ip="123.456.78.99")
        assert not response.outcome

    def test_startSnortIds_(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startSnortIds grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "start_snort_ids", side_effect=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_snort_ids(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                            container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_snort_ids(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                            container_ip="123.456.78.99")
        assert not response.outcome

    def test_startSnortIdsMonitorThread_(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                         get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startSnortIdsMonitorThread grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "start_snort_idses_monitor_thread", side_effect=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_snort_ids_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                           container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_snort_ids_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                           container_ip="123.456.78.99")
        assert not response.outcome

    def test_startSnortIdsMonitorThreads(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                         get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startSnortIdsMonitorThreads grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "start_snort_idses_monitor_threads", side_effect=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_snort_ids_monitor_threads(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_snort_ids_monitor_threads(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startSnortIdsManagers(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                   get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startSnortIdsManagers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "start_snort_managers", side_effect=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_snort_ids_managers(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            start_snort_ids_managers(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopSnortIdsManagers(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                  get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopSnortIdsManagers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "stop_snort_managers", side_effect=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_snort_ids_managers(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            stop_snort_ids_managers(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startSnortIdsManager_(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                   get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startSnortIdsManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "start_snort_manager", side_effect=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_snort_ids_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                    container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            start_snort_ids_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                    container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopSnortIdsManager_(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                  get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopSnortIdsManager grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "stop_snort_manager", side_effect=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_snort_ids_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                   container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            stop_snort_ids_manager(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                   container_ip="123.456.78.99")
        assert not response.outcome

    def test_stopSnortIdsMonitorThreads(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                        get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopSnortIdsMonitorThreads grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "stop_snort_idses_monitor_threads", side_effect=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_snort_ids_monitor_threads(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response = query_cluster_manager. \
            stop_snort_ids_monitor_threads(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_getSnortIdsManagersInfo(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                                     active_ips: List[str]) -> None:
        """
        Tests the getSnortIdsManagersInfo grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param active_ips: fixture that creates a list of active IPs
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "get_snort_managers_info", return_value=TestClusterManagerSuite.snort_mng_info())
        mocker.patch("csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_active_ips",
                     side_effect=active_ips)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: SnortIdsManagersInfoDTO = query_cluster_manager. \
            get_snort_ids_managers_info(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ips == ["123.456.78.99"]
        assert response.ports == [1]
        assert response.emulationName == "JDoeEmulation"
        assert response.executionId == 1
        assert response.snortIdsManagersRunning
        assert response.snortIdsManagersStatuses[0].monitor_running
        assert response.snortIdsManagersStatuses[0].snort_ids_running
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: SnortIdsManagersInfoDTO = query_cluster_manager. \
            get_snort_ids_managers_info(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.ips == []
        assert response.ports == []
        assert response.emulationName == ""
        assert response.executionId == -1
        assert not response.snortIdsManagersRunning
        assert response.snortIdsManagersStatuses == []

    def test_getExecutionInfo(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution,
                              active_ips: List[str]) -> None:
        """
        Tests the getExecutionInfo grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :param active_ips: fixture that creates a list of active IPs
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "get_execution_info", return_value=TestClusterManagerSuite.em_exec_info())
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: ExecutionInfoDTO = query_cluster_manager.get_execution_info(stub=grpc_stub, emulation="JDoeEmulation",
                                                                              ip_first_octet=1)
        assert response.emulationName == "JDoeEmulation"
        assert response.executionId == 1
        assert response.snortIdsManagersInfo.ips == ["123.456.78.99"]
        assert response.snortIdsManagersInfo.ports == [1]
        assert response.snortIdsManagersInfo.emulationName == "JDoeEmulation"
        assert response.snortIdsManagersInfo.executionId == 1
        assert response.snortIdsManagersInfo.snortIdsManagersRunning
        assert response.snortIdsManagersInfo.snortIdsManagersStatuses[0].monitor_running
        assert response.snortIdsManagersInfo.snortIdsManagersStatuses[0].snort_ids_running
        assert response.ossecIdsManagersInfo.ips == ["123.456.78.99"]
        assert response.ossecIdsManagersInfo.ports == [1]
        assert response.ossecIdsManagersInfo.emulationName == "JDoeEmulation"
        assert response.ossecIdsManagersInfo.executionId == 1
        assert response.ossecIdsManagersInfo.ossecIdsManagersRunning
        assert response.ossecIdsManagersInfo.ossecIdsManagersStatuses[0].monitor_running
        assert response.ossecIdsManagersInfo.ossecIdsManagersStatuses[0].ossec_ids_running
        assert response.kafkaManagersInfo.ips == ["123.456.78.99"]
        assert response.kafkaManagersInfo.ports == [1]
        assert response.kafkaManagersInfo.emulationName == "JDoeEmulation"
        assert response.kafkaManagersInfo.executionId == 1
        assert response.kafkaManagersInfo.kafkaManagersRunning
        assert response.kafkaManagersInfo.kafkaManagersStatuses[0].running
        assert response.kafkaManagersInfo.kafkaManagersStatuses[0].topics == ["null"]
        assert response.hostManagersInfo.ips == ["123.456.78.99"]
        assert response.hostManagersInfo.ports == [1]
        assert response.hostManagersInfo.emulationName == "JDoeEmulation"
        assert response.hostManagersInfo.executionId == 1
        assert response.hostManagersInfo.hostManagersRunning
        assert response.hostManagersInfo.hostManagersStatuses[0].monitor_running
        assert response.hostManagersInfo.hostManagersStatuses[0].filebeat_running
        assert response.hostManagersInfo.hostManagersStatuses[0].packetbeat_running
        assert response.hostManagersInfo.hostManagersStatuses[0].metricbeat_running
        assert response.hostManagersInfo.hostManagersStatuses[0].heartbeat_running
        assert response.hostManagersInfo.hostManagersStatuses[0].ip == "123.456.78.99"
        assert response.clientManagersInfo.ips == ["123.456.78.99"]
        assert response.clientManagersInfo.ports == [1]
        assert response.clientManagersInfo.emulationName == "JohnDoeEmulation"
        assert response.clientManagersInfo.executionId == 1
        assert response.clientManagersInfo.clientManagersRunning
        assert response.clientManagersInfo.clientManagersStatuses[0].num_clients == 4
        assert response.clientManagersInfo.clientManagersStatuses[0].client_process_active
        assert response.clientManagersInfo.clientManagersStatuses[0].producer_active
        assert response.clientManagersInfo.clientManagersStatuses[0].clients_time_step_len_seconds == 4
        assert response.clientManagersInfo.clientManagersStatuses[0].producer_time_step_len_seconds == 5
        assert response.dockerStatsManagersInfo.ips == ["123.456.78.99"]
        assert response.dockerStatsManagersInfo.ports == [1]
        assert response.dockerStatsManagersInfo.emulationName == "JDoeEmulation"
        assert response.dockerStatsManagersInfo.executionId == 1
        assert response.dockerStatsManagersInfo.dockerStatsManagersRunning
        assert response.dockerStatsManagersInfo.dockerStatsManagersStatuses[0].num_monitors == 4
        assert response.dockerStatsManagersInfo.dockerStatsManagersStatuses[0].emulations == ["JDoeEmulation"]
        assert response.dockerStatsManagersInfo.dockerStatsManagersStatuses[0].emulation_executions == [4]
        assert response.runningContainers.runningContainers[0].name == "Container1"
        assert response.runningContainers.runningContainers[0].image == "Container1null-levelnull--1"
        assert response.runningContainers.runningContainers[0].ip == "123.456.78.99"
        assert response.stoppedContainers.stoppedContainers[0].name == "Container1"
        assert response.stoppedContainers.stoppedContainers[0].image == "Container1null-levelnull--1"
        assert response.stoppedContainers.stoppedContainers[0].ip == "123.456.78.99"
        assert response.trafficManagersInfoDTO.ips == ["123.456.78.99"]
        assert response.trafficManagersInfoDTO.ports == [1]
        assert response.trafficManagersInfoDTO.emulationName == "JohnDoeEmulation"
        assert response.trafficManagersInfoDTO.executionId == 1
        assert response.trafficManagersInfoDTO.trafficManagersRunning
        assert response.trafficManagersInfoDTO.trafficManagersStatuses[0].running
        assert response.trafficManagersInfoDTO.trafficManagersStatuses[0].script == "null"
        assert response.activeNetworks.networks == ["Network1"]
        assert response.activeNetworks.network_ids == [-1]
        assert response.elkManagersInfoDTO.ips == ["123.456.78.99"]
        assert response.elkManagersInfoDTO.ports == [1]
        assert response.elkManagersInfoDTO.emulationName == "JohnDoeEmulation"
        assert response.elkManagersInfoDTO.executionId == 1
        assert response.elkManagersInfoDTO.elkManagersRunning
        assert response.elkManagersInfoDTO.elkManagersStatuses[0].elasticRunning
        assert response.elkManagersInfoDTO.elkManagersStatuses[0].kibanaRunning
        assert response.elkManagersInfoDTO.elkManagersStatuses[0].logstashRunning
        assert response.elkManagersInfoDTO.localKibanaPort == -1
        assert response.elkManagersInfoDTO.physicalServerIp == "123.456.78.99"
        assert response.ryuManagersInfoDTO.ips == ["123.456.78.99"]
        assert response.ryuManagersInfoDTO.ports == [1]
        assert response.ryuManagersInfoDTO.emulationName == "JDoeEmulation"
        assert response.ryuManagersInfoDTO.executionId == 1
        assert response.ryuManagersInfoDTO.ryuManagersRunning
        assert response.ryuManagersInfoDTO.ryuManagersStatuses[0].ryu_running
        assert response.ryuManagersInfoDTO.ryuManagersStatuses[0].monitor_running
        assert response.ryuManagersInfoDTO.ryuManagersStatuses[0].port == 4
        assert response.ryuManagersInfoDTO.ryuManagersStatuses[0].web_port == 4
        assert response.ryuManagersInfoDTO.ryuManagersStatuses[0].controller == "null"
        assert response.ryuManagersInfoDTO.ryuManagersStatuses[0].kafka_ip == "123.456.78.99"
        assert response.ryuManagersInfoDTO.ryuManagersStatuses[0].kafka_port == 7
        assert response.ryuManagersInfoDTO.ryuManagersStatuses[0].time_step_len == 4
        assert response.ryuManagersInfoDTO.localControllerWebPort == 10
        assert response.ryuManagersInfoDTO.physicalServerIp == "123.456.78.99"

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: ExecutionInfoDTO = query_cluster_manager. \
            get_execution_info(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.emulationName == ""
        assert response.executionId == -1

    def test_listKibanaTunnels(self, grpc_stub, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the listKibanaTunnels grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        response: KibanaTunnelsDTO = query_cluster_manager.list_kibana_tunnels(stub=grpc_stub)
        assert response.tunnels == []

    def test_listRyuTunnels(self, grpc_stub, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the listRyuTunnels grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        response: RyuTunnelsDTO = query_cluster_manager.list_ryu_tunnels(stub=grpc_stub)
        assert response.tunnels == []

    def test_createKibanaTunnel(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                get_ex_exec: EmulationExecution) -> None:
        """
        Tests the createKibanaTunnel grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController.create_ssh_tunnel",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            create_kibana_tunnel(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            create_kibana_tunnel(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_createRyuTunnel(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the createRyuTunnel grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController.create_ssh_tunnel",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            create_ryu_tunnel(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            create_ryu_tunnel(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_removeRyuTunnel(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the removeRyuTunnel grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_ryu_tunnel(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_ryu_tunnel(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_removeKibanaTunnel(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                get_ex_exec: EmulationExecution) -> None:
        """
        Tests the removeKibanaTunnel grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_kibana_tunnel(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            remove_kibana_tunnel(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopHostMonitorThreads(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                    get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopHostMonitorThreads grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.stop_host_monitor_threads",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_host_monitor_threads(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_host_monitor_threads(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopHostMonitorThread_(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                    get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopHostMonitorThread grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.host_controller.HostController.stop_host_monitor_thread",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_host_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                     container_ip="123.456.78.99")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_host_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                     container_ip="123.456.78.99")
        assert not response.outcome
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_host_monitor_thread(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                     container_ip="123.456.78.99")
        assert not response.outcome

    def test_startRyuMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startRyuMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager."
                     "start_ryu_monitor", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ryu_monitor(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            start_ryu_monitor(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopRyuMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopRyuMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager."
                     "stop_ryu_monitor", return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ryu_monitor(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager. \
            stop_ryu_monitor(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_getRyuManagerLogs(self, grpc_stub, mocker: pytest_mock.MockFixture,
                               get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getRyuManagerLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager. \
            get_ryu_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager. \
            get_ryu_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.logs == ["abcdef"]

    def test_getRyuControllerLogs(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                  get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getRyuControllerLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager. \
            get_ryu_controller_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager. \
            get_ryu_controller_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.logs == ["abcdef"]

    def test_getElkLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getElkLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager. \
            get_elk_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager. \
            get_elk_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.logs == ["abcdef"]

    def test_getElkManagerLogs(self, grpc_stub, mocker: pytest_mock.MockFixture,
                               get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getElkManagerLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager. \
            get_elk_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager. \
            get_elk_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1)
        assert response.logs == ["abcdef"]

    def test_getTrafficManagerLogs(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                   get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getTrafficManagerLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager. \
            get_traffic_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                     container_ip="123.456.78.99")
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager. \
            get_traffic_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                     container_ip="123.456.78.99")
        assert response.logs == ["abcdef"]

    def test_getHostManagerLogs(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getHostManagerLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager. \
            get_host_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                  container_ip="123.456.78.99")
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager. \
            get_host_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                  container_ip="123.456.78.99")
        assert response.logs == ["abcdef"]

    def test_getOSSECIdsLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getOSSECIdsLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager. \
            get_ossec_ids_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                               container_ip="123.456.78.99")
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager. \
            get_ossec_ids_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                               container_ip="123.456.78.99")
        assert response.logs == ["abcdef"]

    def test_getOSSECIdsManagerLogsMsg(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                       get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getOSSECIdsManagerLogsMsg grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager. \
            get_ossec_ids_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                       container_ip="123.456.78.99")
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager. \
            get_ossec_ids_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                       container_ip="123.456.78.99")
        assert response.logs == ["abcdef"]
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: LogsDTO = query_cluster_manager. \
            get_ossec_ids_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                       container_ip="123.456.78.99")
        assert response.logs == []

    def test_getSnortIdsLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getSnortIdsLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager. \
            get_snort_ids_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                               container_ip="123.456.78.99")
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager. \
            get_snort_ids_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                               container_ip="123.456.78.99")
        assert response.logs == ["abcdef"]
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: LogsDTO = query_cluster_manager. \
            get_snort_ids_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                               container_ip="123.456.78.99")
        assert response.logs == []

    def test_getSnortIdsManagerLogsMsg(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                       get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getSnortIdsManagerLogsMsg grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager. \
            get_snort_ids_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                       container_ip="123.456.78.99")
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager. \
            get_snort_ids_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                       container_ip="123.456.78.99")
        assert response.logs == ["abcdef"]
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="99.87.654.321")
        response: LogsDTO = query_cluster_manager. \
            get_snort_ids_manager_logs(stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1,
                                       container_ip="123.456.78.99")
        assert response.logs == []

    def test_getKafkaLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getKafkaLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip", return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager.get_kafka_logs(stub=grpc_stub, emulation="JDoeEmulation",
                                                                 ip_first_octet=1)
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager.get_kafka_logs(stub=grpc_stub, emulation="JDoeEmulation",
                                                                 ip_first_octet=1)
        assert response.logs == ["abcdef"]
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip", return_value="99.87.654.321")
        response: LogsDTO = query_cluster_manager.get_kafka_logs(stub=grpc_stub, emulation="JDoeEmulation",
                                                                 ip_first_octet=1)
        assert response.logs == []

    def test_getKafkaManagerLogs(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                 get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getKafkaManagerLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip", return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager.get_kafka_manager_logs(stub=grpc_stub, emulation="JDoeEmulation",
                                                                         ip_first_octet=1)
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager.get_kafka_manager_logs(stub=grpc_stub, emulation="JDoeEmulation",
                                                                         ip_first_octet=1)
        assert response.logs == ["abcdef"]
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip", return_value="99.87.654.321")
        response: LogsDTO = query_cluster_manager.get_kafka_manager_logs(stub=grpc_stub, emulation="JDoeEmulation",
                                                                         ip_first_octet=1)
        assert response.logs == []

    def test_getClientManagerLogsMsg(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                     get_ex_exec: EmulationExecution) -> None:
        """
        Tests the getClientManagerLogsMsg grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip", return_value="123.456.78.99")
        response: LogsDTO = query_cluster_manager.get_client_manager_logs(stub=grpc_stub, emulation="JDoeEmulation",
                                                                          ip_first_octet=1)
        assert response.logs == []
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.get_logs',
                     return_value=LogsDTO(logs=["abcdef"]))
        response: LogsDTO = query_cluster_manager.get_client_manager_logs(stub=grpc_stub, emulation="JDoeEmulation",
                                                                          ip_first_octet=1)
        assert response.logs == ["abcdef"]
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip", return_value="99.87.654.321")
        response: LogsDTO = query_cluster_manager.get_client_manager_logs(stub=grpc_stub,
                                                                          emulation="JDoeEmulation", ip_first_octet=1)
        assert response.logs == []

    def test_getClusterManagerLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the getClusterManagerLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example configuration
        :return: None
        """
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config', return_value=example_config)
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail',
                     return_value="abcdef")
        response: LogsDTO = query_cluster_manager. \
            get_cluster_manager_logs(stub=grpc_stub)
        assert response.logs == ["abcdef"]
        mocker.patch("os.path.exists", return_value=False)
        response: LogsDTO = query_cluster_manager. \
            get_cluster_manager_logs(stub=grpc_stub)
        assert response.logs == []

    def test_getExecutionTimeSeriesData(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                        get_ex_exec: EmulationExecution, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the getExecutionTimeSeriesData grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture which creates an example emulation execution
        :param get_ex_em_env: fixture which creates an example emulation configuration
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.util.read_emulation_statistics_util.ReadEmulationStatisticsUtil"
                     ".read_all", return_value=TestClusterManagerSuite.emulation_mts(get_ex_em_env))
        response: EmulationMetricsTimeSeriesDTO = query_cluster_manager.get_execution_time_series_data(
            stub=grpc_stub, emulation="JDoeEmulation", ip_first_octet=1, minutes=1)
        assert response.client_metrics[0].ip == "123.456.78.99"
        assert response.client_metrics[0].ts == 100
        assert response.client_metrics[0].num_clients == 10
        assert response.client_metrics[0].rate == 2
        assert response.client_metrics[0].service_time == 4.5
        assert response.aggregated_docker_stats[0].pids == 10
        assert response.aggregated_docker_stats[0].timestamp == "null"
        assert response.aggregated_docker_stats[0].cpu_percent == 5.5
        assert round(response.aggregated_docker_stats[0].mem_current, 2) == 4.3
        assert round(response.aggregated_docker_stats[0].mem_total, 2) == 2.8
        assert round(response.aggregated_docker_stats[0].mem_percent, 2) == 1.7
        assert round(response.aggregated_docker_stats[0].blk_read, 2) == 2.3
        assert round(response.aggregated_docker_stats[0].blk_write, 2) == 1.2
        assert round(response.aggregated_docker_stats[0].net_rx, 2) == 2.4
        assert round(response.aggregated_docker_stats[0].net_tx, 2) == 5.3
        assert response.aggregated_docker_stats[0].container_name == "JDoeContainer"
        assert response.aggregated_docker_stats[0].ip == "123.456.78.99"
        assert round(response.aggregated_docker_stats[0].ts, 2) == 1.2
        assert response.docker_host_stats[0].key == "docker_stats"
        assert response.docker_host_stats[0].dtos[0].pids == 10
        assert response.docker_host_stats[0].dtos[0].timestamp == "null"
        assert round(response.docker_host_stats[0].dtos[0].cpu_percent, 2) == 5.5
        assert round(response.docker_host_stats[0].dtos[0].mem_current, 2) == 4.3
        assert round(response.docker_host_stats[0].dtos[0].mem_total, 2) == 2.8
        assert round(response.docker_host_stats[0].dtos[0].mem_percent, 2) == 1.7
        assert round(response.docker_host_stats[0].dtos[0].blk_read, 2) == 2.3
        assert round(response.docker_host_stats[0].dtos[0].blk_write, 2) == 1.2
        assert round(response.docker_host_stats[0].dtos[0].net_rx, 2) == 2.4
        assert round(response.docker_host_stats[0].dtos[0].net_tx, 2) == 5.3
        assert response.docker_host_stats[0].dtos[0].container_name == "JDoeContainer"
        assert response.docker_host_stats[0].dtos[0].ip == "123.456.78.99"
        assert round(response.docker_host_stats[0].dtos[0].ts, 2) == 1.2
        assert response.host_metrics[0].key == "host_metrics"
        assert response.host_metrics[0].dtos[0].num_logged_in_users == 10
        assert response.host_metrics[0].dtos[0].num_failed_login_attempts == 2
        assert response.host_metrics[0].dtos[0].num_open_connections == 4
        assert response.host_metrics[0].dtos[0].num_login_events == 22
        assert response.host_metrics[0].dtos[0].num_processes == 14
        assert response.host_metrics[0].dtos[0].num_users == 100
        assert response.host_metrics[0].dtos[0].ip == "123.456.78.99"
        assert round(response.host_metrics[0].dtos[0].ts, 2) == 15.4
        assert response.aggregated_host_metrics[0].num_logged_in_users == 10
        assert response.aggregated_host_metrics[0].num_failed_login_attempts == 2
        assert response.aggregated_host_metrics[0].num_open_connections == 4
        assert response.aggregated_host_metrics[0].num_login_events == 22
        assert response.aggregated_host_metrics[0].num_processes == 14
        assert response.aggregated_host_metrics[0].num_users == 100
        assert response.aggregated_host_metrics[0].ip == "123.456.78.99"
        assert round(response.aggregated_host_metrics[0].ts, 2) == 15.4
        assert response.defender_actions[0].name == "JohnDoe"
        assert response.defender_actions[0].cmds == ["JDoeCommands"]
        assert response.defender_actions[0].descr == "null"
        assert response.defender_actions[0].ips == ["123.456.78.99"]
        assert response.defender_actions[0].index == 1
        assert response.defender_actions[0].alt_cmds == ["JDoeCommands"]
        assert round(response.defender_actions[0].execution_time, 2) == 5.6
        assert round(response.defender_actions[0].ts, 2) == 10.2
        assert response.attacker_actions[0].name == "JohnDoe"
        assert response.attacker_actions[0].cmds == ["JDoeCommands"]
        assert response.attacker_actions[0].descr == "null"
        assert response.attacker_actions[0].ips == ["123.456.78.99"]
        assert response.attacker_actions[0].index == 1
        assert response.attacker_actions[0].alt_cmds == ["JDoeCommands"]
        assert round(response.attacker_actions[0].execution_time, 2) == 3.3
        assert round(response.attacker_actions[0].ts, 3) == 41.1
        assert response.attacker_actions[0].vulnerability == "null"
        assert response.agg_snort_ids_metrics[0].priority_alerts == [0, 0, 0, 0]
        assert response.agg_snort_ids_metrics[0].class_alerts == [0] * 34
        assert response.emulation_id == -1
        assert response.ossec_host_alert_counters[0].key == "ossec_host"
        assert response.ossec_host_alert_counters[0].dtos[0].level_alerts == [0] * 16
        assert response.ossec_host_alert_counters[0].dtos[0].group_alerts == [0] * 12
        assert response.aggregated_ossec_host_alert_counters[0].level_alerts == [0] * 16
        assert response.aggregated_ossec_host_alert_counters[0].group_alerts == [0] * 12
        assert round(response.openflow_flow_stats[0].timestamp, 3) == 10.5
        assert response.openflow_flow_stats[0].datapath_id == "null"
        assert response.openflow_flow_stats[0].in_port == "null"
        assert response.openflow_flow_stats[0].out_port == "null"
        assert response.openflow_flow_stats[0].dst_mac_address == "null"
        assert response.openflow_flow_stats[0].num_bytes == 4
        assert response.openflow_flow_stats[0].num_packets == 10
        assert response.openflow_flow_stats[0].duration_nanoseconds == 3
        assert response.openflow_flow_stats[0].duration_seconds == 4
        assert response.openflow_flow_stats[0].hard_timeout == 100
        assert response.openflow_flow_stats[0].idle_timeout == 12
        assert response.openflow_flow_stats[0].priority == 1
        assert response.openflow_flow_stats[0].cookie == 3
        assert round(response.openflow_port_stats[0].timestamp, 3) == 12.5
        assert response.openflow_port_stats[0].datapath_id == "null"
        assert response.openflow_port_stats[0].port == 1
        assert response.openflow_port_stats[0].num_received_packets == 12
        assert response.openflow_port_stats[0].num_received_errors == 21
        assert response.openflow_port_stats[0].num_received_bytes == 34
        assert response.openflow_port_stats[0].num_transmitted_packets == 13
        assert response.openflow_port_stats[0].num_transmitted_bytes == 22
        assert response.openflow_port_stats[0].num_transmitted_errors == 16
        assert response.openflow_port_stats[0].num_received_dropped == 41
        assert response.openflow_port_stats[0].num_transmitted_dropped == 55
        assert response.openflow_port_stats[0].num_received_frame_errors == 66
        assert response.openflow_port_stats[0].num_received_overrun_errors == 2
        assert response.openflow_port_stats[0].num_received_crc_errors == 1
        assert response.openflow_port_stats[0].num_collisions == 5
        assert response.openflow_port_stats[0].duration_nanoseconds == 8
        assert response.openflow_port_stats[0].duration_seconds == 5
        assert response.avg_openflow_flow_stats[0].timestamp == 1
        assert response.avg_openflow_flow_stats[0].datapath_id == "null"
        assert response.avg_openflow_flow_stats[0].total_num_packets == 10
        assert response.avg_openflow_flow_stats[0].total_num_bytes == 10
        assert response.avg_openflow_flow_stats[0].avg_duration_nanoseconds == 10
        assert response.avg_openflow_flow_stats[0].avg_duration_seconds == 10
        assert response.avg_openflow_flow_stats[0].avg_hard_timeout == 10
        assert response.avg_openflow_flow_stats[0].avg_idle_timeout == 10
        assert response.avg_openflow_flow_stats[0].avg_priority == 10
        assert response.avg_openflow_flow_stats[0].avg_cookie == 10
        assert response.avg_openflow_port_stats[0].timestamp == 1
        assert response.avg_openflow_port_stats[0].datapath_id == "null"
        assert response.avg_openflow_port_stats[0].total_num_received_packets == 10
        assert response.avg_openflow_port_stats[0].total_num_received_bytes == 10
        assert response.avg_openflow_port_stats[0].total_num_received_errors == 10
        assert response.avg_openflow_port_stats[0].total_num_transmitted_packets == 10
        assert response.avg_openflow_port_stats[0].total_num_transmitted_bytes == 10
        assert response.avg_openflow_port_stats[0].total_num_transmitted_errors == 10
        assert response.avg_openflow_port_stats[0].total_num_received_dropped == 10
        assert response.avg_openflow_port_stats[0].total_num_transmitted_dropped == 10
        assert response.avg_openflow_port_stats[0].total_num_received_frame_errors == 10
        assert response.avg_openflow_port_stats[0].total_num_received_overrun_errors == 10
        assert response.avg_openflow_port_stats[0].total_num_received_crc_errors == 10
        assert response.avg_openflow_port_stats[0].total_num_collisions == 10
        assert response.avg_openflow_port_stats[0].avg_duration_nanoseconds == 5
        assert response.avg_openflow_port_stats[0].avg_duration_seconds == 5
        assert response.openflow_flow_metrics_per_switch[0].key == "openflow_metrics"
        assert round(response.openflow_flow_metrics_per_switch[0].dtos[0].timestamp, 3) == 10.5
        assert response.openflow_flow_metrics_per_switch[0].dtos[0].datapath_id == "null"
        assert response.openflow_flow_metrics_per_switch[0].dtos[0].in_port == "null"
        assert response.openflow_flow_metrics_per_switch[0].dtos[0].out_port == "null"
        assert response.openflow_flow_metrics_per_switch[0].dtos[0].dst_mac_address == "null"
        assert response.openflow_flow_metrics_per_switch[0].dtos[0].num_packets == 10
        assert response.openflow_flow_metrics_per_switch[0].dtos[0].num_bytes == 4
        assert response.openflow_flow_metrics_per_switch[0].dtos[0].duration_nanoseconds == 3
        assert response.openflow_flow_metrics_per_switch[0].dtos[0].duration_seconds == 4
        assert response.openflow_flow_metrics_per_switch[0].dtos[0].hard_timeout == 100
        assert response.openflow_flow_metrics_per_switch[0].dtos[0].idle_timeout == 12
        assert response.openflow_flow_metrics_per_switch[0].dtos[0].priority == 1
        assert response.openflow_flow_metrics_per_switch[0].dtos[0].cookie == 3
        assert response.openflow_port_metrics_per_switch[0].key == "openflow_flow_metrics"
        assert round(response.openflow_port_metrics_per_switch[0].dtos[0].timestamp, 3) == 12.5
        assert response.openflow_port_metrics_per_switch[0].dtos[0].datapath_id == "null"
        assert response.openflow_port_metrics_per_switch[0].dtos[0].port == 1
        assert response.openflow_port_metrics_per_switch[0].dtos[0].num_received_packets == 12
        assert response.openflow_port_metrics_per_switch[0].dtos[0].num_received_bytes == 34
        assert response.openflow_port_metrics_per_switch[0].dtos[0].num_received_errors == 21
        assert response.openflow_port_metrics_per_switch[0].dtos[0].num_transmitted_packets == 13
        assert response.openflow_port_metrics_per_switch[0].dtos[0].num_transmitted_bytes == 22
        assert response.openflow_port_metrics_per_switch[0].dtos[0].num_transmitted_errors == 16
        assert response.openflow_port_metrics_per_switch[0].dtos[0].num_received_dropped == 41
        assert response.openflow_port_metrics_per_switch[0].dtos[0].num_received_frame_errors == 66
        assert response.openflow_port_metrics_per_switch[0].dtos[0].num_received_overrun_errors == 2
        assert response.openflow_port_metrics_per_switch[0].dtos[0].num_received_crc_errors == 1
        assert response.openflow_port_metrics_per_switch[0].dtos[0].num_collisions == 5
        assert response.openflow_port_metrics_per_switch[0].dtos[0].duration_nanoseconds == 8
        assert response.openflow_port_metrics_per_switch[0].dtos[0].duration_seconds == 5
        assert response.openflow_flow_avg_metrics_per_switch[0].key == "openflow_avg_metrics"
        assert response.openflow_flow_avg_metrics_per_switch[0].dtos[0].timestamp == 1
        assert response.openflow_flow_avg_metrics_per_switch[0].dtos[0].datapath_id == "null"
        assert response.openflow_flow_avg_metrics_per_switch[0].dtos[0].total_num_packets == 10
        assert response.openflow_flow_avg_metrics_per_switch[0].dtos[0].total_num_bytes == 10
        assert response.openflow_flow_avg_metrics_per_switch[0].dtos[0].avg_duration_nanoseconds == 10
        assert response.openflow_flow_avg_metrics_per_switch[0].dtos[0].avg_duration_seconds == 10
        assert response.openflow_flow_avg_metrics_per_switch[0].dtos[0].avg_hard_timeout == 10
        assert response.openflow_flow_avg_metrics_per_switch[0].dtos[0].avg_idle_timeout == 10
        assert response.openflow_flow_avg_metrics_per_switch[0].dtos[0].avg_priority == 10
        assert response.openflow_flow_avg_metrics_per_switch[0].dtos[0].avg_cookie == 10
        assert response.openflow_port_avg_metrics_per_switch[0].key == "openflow_port_avg_metrics"
        assert response.openflow_port_avg_metrics_per_switch[0].dtos[0].timestamp == 1
        assert response.openflow_port_avg_metrics_per_switch[0].dtos[0].datapath_id == "null"
        assert response.openflow_port_avg_metrics_per_switch[0].dtos[0].total_num_received_packets == 10
        assert response.openflow_port_avg_metrics_per_switch[0].dtos[0].total_num_received_overrun_errors == 10
        assert response.openflow_port_avg_metrics_per_switch[0].dtos[0].total_num_collisions == 10
        assert response.openflow_port_avg_metrics_per_switch[0].dtos[0].total_num_received_bytes == 10
        assert response.openflow_port_avg_metrics_per_switch[0].dtos[0].total_num_received_crc_errors == 10
        assert response.openflow_port_avg_metrics_per_switch[0].dtos[0].total_num_transmitted_dropped == 10
        assert response.openflow_port_avg_metrics_per_switch[0].dtos[0].total_num_transmitted_errors == 10
        assert response.openflow_port_avg_metrics_per_switch[0].dtos[0].total_num_received_frame_errors == 10
        assert response.openflow_port_avg_metrics_per_switch[0].dtos[0].total_num_received_dropped == 10
        assert response.openflow_port_avg_metrics_per_switch[0].dtos[0].total_num_transmitted_bytes == 10
        assert response.agg_openflow_flow_metrics_per_switch[0].key == "agg_openflow_flow_metrics"
        assert round(response.agg_openflow_flow_metrics_per_switch[0].dtos[0].timestamp, 2) == 4.3
        assert response.agg_openflow_flow_metrics_per_switch[0].dtos[0].datapath_id == "null"
        assert response.agg_openflow_flow_metrics_per_switch[0].dtos[0].total_num_packets == 2
        assert response.agg_openflow_flow_metrics_per_switch[0].dtos[0].total_num_bytes == 10
        assert response.agg_openflow_flow_metrics_per_switch[0].dtos[0].total_num_flows == 10
        assert round(response.agg_openflow_flow_stats[0].timestamp, 2) == 4.3
        assert response.agg_openflow_flow_stats[0].datapath_id == "null"
        assert response.agg_openflow_flow_stats[0].total_num_packets == 2
        assert response.agg_openflow_flow_stats[0].total_num_bytes == 10
        assert response.agg_openflow_flow_stats[0].total_num_flows == 10
        assert response.snort_ids_ip_metrics[0].key == "snort_ids_ip"
        assert response.snort_ids_ip_metrics[0].dtos[0].priority_alerts == [0] * 4
        assert response.snort_ids_ip_metrics[0].dtos[0].class_alerts == [0] * 34
        assert response.snort_alert_metrics_per_ids[0].key == "snort_alert_metrics"
        assert response.snort_alert_metrics_per_ids[0].dtos[0].priority_alerts == [0] * 4
        assert response.snort_alert_metrics_per_ids[0].dtos[0].class_alerts == [0] * 34

    def test_startSparkServer(self, grpc_stub, mocker: pytest_mock.MockFixture,
                              get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startSparkServer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_common.controllers.host_controller.HostController.start_spark', return_value=None)
        container_ip = get_ex_exec.emulation_env_config.containers_config.containers[0].get_ips()[0]
        physical_host_ip = get_ex_exec.emulation_env_config.containers_config.containers[0].physical_host_ip
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_host_ip', return_value=physical_host_ip)
        response: OperationOutcomeDTO = query_cluster_manager.start_spark_server(
            stub=grpc_stub, emulation=get_ex_exec.emulation_name, ip_first_octet=get_ex_exec.ip_first_octet,
            container_ip=container_ip)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_spark_server(
            stub=grpc_stub, emulation=get_ex_exec.emulation_name, ip_first_octet=get_ex_exec.ip_first_octet,
            container_ip=container_ip)
        assert not response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_host_ip', return_value="121.125.125.12")
        response: OperationOutcomeDTO = query_cluster_manager.start_spark_server(
            stub=grpc_stub, emulation=get_ex_exec.emulation_name, ip_first_octet=get_ex_exec.ip_first_octet,
            container_ip=container_ip)
        assert not response.outcome

    def test_stopSparkServer(self, grpc_stub, mocker: pytest_mock.MockFixture,
                             get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopSparkServer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_common.controllers.host_controller.HostController.stop_spark', return_value=None)
        container_ip = get_ex_exec.emulation_env_config.containers_config.containers[0].get_ips()[0]
        physical_host_ip = get_ex_exec.emulation_env_config.containers_config.containers[0].physical_host_ip
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_host_ip', return_value=physical_host_ip)
        response: OperationOutcomeDTO = query_cluster_manager.stop_spark_server(
            stub=grpc_stub, emulation=get_ex_exec.emulation_name, ip_first_octet=get_ex_exec.ip_first_octet,
            container_ip=container_ip)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_spark_server(
            stub=grpc_stub, emulation=get_ex_exec.emulation_name, ip_first_octet=get_ex_exec.ip_first_octet,
            container_ip=container_ip)
        assert not response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_host_ip', return_value="121.125.125.12")
        response: OperationOutcomeDTO = query_cluster_manager.stop_spark_server(
            stub=grpc_stub, emulation=get_ex_exec.emulation_name, ip_first_octet=get_ex_exec.ip_first_octet,
            container_ip=container_ip)
        assert not response.outcome

    def test_startSparkServers(self, grpc_stub, mocker: pytest_mock.MockFixture,
                               get_ex_exec: EmulationExecution) -> None:
        """
        Tests the startSparkServers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_common.controllers.host_controller.HostController.start_sparks', return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_spark_servers(
            stub=grpc_stub, emulation=get_ex_exec.emulation_name, ip_first_octet=get_ex_exec.ip_first_octet)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.start_spark_servers(
            stub=grpc_stub, emulation=get_ex_exec.emulation_name, ip_first_octet=get_ex_exec.ip_first_octet)
        assert not response.outcome

    def test_stopSparkServers(self, grpc_stub, mocker: pytest_mock.MockFixture,
                              get_ex_exec: EmulationExecution) -> None:
        """
        Tests the stopSparkServers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param get_ex_exec: fixture that creates an example emulation execution DTO
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch('csle_common.controllers.host_controller.HostController.stop_sparks', return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_spark_servers(
            stub=grpc_stub, emulation=get_ex_exec.emulation_name, ip_first_octet=get_ex_exec.ip_first_octet)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_spark_servers(
            stub=grpc_stub, emulation=get_ex_exec.emulation_name, ip_first_octet=get_ex_exec.ip_first_octet)
        assert not response.outcome

    def test_checkPid(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the checkPid grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_pid_running', return_value=True)
        response: OperationOutcomeDTO = query_cluster_manager.check_pid(stub=grpc_stub, pid=8888)
        assert response.outcome
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_pid_running', return_value=False)
        response: OperationOutcomeDTO = query_cluster_manager.check_pid(stub=grpc_stub, pid=8888)
        assert not response.outcome

    def test_stopPid(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopPid grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_pid', return_value=None)
        response: OperationOutcomeDTO = query_cluster_manager.stop_pid(stub=grpc_stub, pid=8888)
        assert response.outcome
