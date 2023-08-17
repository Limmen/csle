from typing import Any
import pytest
import pytest_mock
from subprocess import CompletedProcess
from csle_collector.snort_ids_manager.snort_ids_manager_pb2 import SnortIdsLogDTO, SnortIdsMonitorDTO
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_collector.snort_ids_manager.dao.snort_ids_ip_alert_counters import SnortIdsIPAlertCounters
from csle_collector.snort_ids_manager.snort_ids_manager import SnortIdsManagerServicer
import csle_collector.snort_ids_manager.query_snort_ids_manager
import csle_collector.constants.constants as constants


class TestSnortIDSManagerSuite:
    """
    Test suite for the Snort IDS manager
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc import add_SnortIdsManagerServicer_to_server
        return add_SnortIdsManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> SnortIdsManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the snort manager servicer
        """
        return SnortIdsManagerServicer()

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc import SnortIdsManagerStub
        return SnortIdsManagerStub

    def test_getSnortIdsAlerts(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getSnortIdsAlerts grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """

        def read_snort_ids_data(timestamp: float):
            if timestamp == 0:
                return SnortIdsAlertCounters(), SnortIdsRuleCounters(), SnortIdsIPAlertCounters()
            else:
                alerts = SnortIdsAlertCounters()
                alerts.severe_alerts = 100
                alerts.warning_alerts = 200
                alerts.total_alerts = 300
                alerts.alerts_weighted_by_priority = 400
                alerts.ip = "test"
                alerts.ts = 0.0
                rule_alert_counters = SnortIdsRuleCounters()
                rule_alert_counters.rule_alerts["rule_1"] = 10
                ip_alert_counters = SnortIdsIPAlertCounters()
                ip_alert_counters.severe_alerts = 1000
                ip_alert_counters.warning_alerts = 2000
                ip_alert_counters.total_alerts = 3000
                ip_alert_counters.alerts_weighted_by_priority = 4000
                return alerts, rule_alert_counters, ip_alert_counters

        read_data_mock = mocker.MagicMock(side_effect=read_snort_ids_data)
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager_util.SnortIdsManagerUtil.read_snort_ids_data',
                     side_effect=read_data_mock)
        response: SnortIdsLogDTO = csle_collector.snort_ids_manager.query_snort_ids_manager.get_snort_ids_alerts(
            stub=grpc_stub, timestamp=0, log_file_path="")
        assert response.priority_1_alerts == 0
        assert response.priority_2_alerts == 0
        assert response.priority_3_alerts == 0
        assert response.priority_4_alerts == 0
        assert response.total_alerts == 0
        assert response.warning_alerts == 0
        assert response.severe_alerts == 0
        assert response.alerts_weighted_by_priority == 0
        response = csle_collector.snort_ids_manager.query_snort_ids_manager.get_snort_ids_alerts(
            stub=grpc_stub, timestamp=1, log_file_path="")
        assert response.priority_1_alerts == 0
        assert response.priority_2_alerts == 0
        assert response.priority_3_alerts == 0
        assert response.priority_4_alerts == 0
        assert response.total_alerts == 300
        assert response.warning_alerts == 200
        assert response.severe_alerts == 100
        assert response.alerts_weighted_by_priority == 400

    def test_startSnortIdsMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startSnortIdsMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.snort_ids_manager.threads.snort_ids_monitor_thread.SnortIDSMonitorThread.run',
                     return_value=True)
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_snort_running',
                     return_value=True)
        kafka_ip = "test_kafka_ip"
        kafka_port = 9292
        log_file_path = "test_log_file_path"
        time_step_len_seconds = 30
        response: SnortIdsMonitorDTO = csle_collector.snort_ids_manager.query_snort_ids_manager.start_snort_ids_monitor(
            stub=grpc_stub, kafka_ip=kafka_ip, kafka_port=kafka_port, log_file_path=log_file_path,
            time_step_len_seconds=time_step_len_seconds)
        assert response.monitor_running
        assert response.snort_ids_running
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_snort_running',
                     return_value=False)
        response = csle_collector.snort_ids_manager.query_snort_ids_manager.start_snort_ids_monitor(
            stub=grpc_stub, kafka_ip=kafka_ip, kafka_port=kafka_port, log_file_path=log_file_path,
            time_step_len_seconds=time_step_len_seconds)
        assert response.monitor_running
        assert not response.snort_ids_running

    def test_stopSnortIdsMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopSnortIdsMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_snort_running',
                     return_value=True)
        response: SnortIdsMonitorDTO = csle_collector.snort_ids_manager.query_snort_ids_manager.stop_snort_ids_monitor(
            stub=grpc_stub)
        assert not response.monitor_running
        assert response.snort_ids_running
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_snort_running',
                     return_value=False)
        response = csle_collector.snort_ids_manager.query_snort_ids_manager.stop_snort_ids_monitor(
            stub=grpc_stub)
        assert not response.monitor_running
        assert not response.snort_ids_running

    def test_stopSnortIds(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopSnortIdsMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('subprocess.run', return_value=CompletedProcess(args="", returncode=0, stdout="testout",
                                                                     stderr="testerr"))
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_monitor_running',
                     return_value=False)
        response: SnortIdsMonitorDTO = csle_collector.snort_ids_manager.query_snort_ids_manager.stop_snort_ids(
            stub=grpc_stub)
        assert not response.monitor_running
        assert not response.snort_ids_running
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_monitor_running',
                     return_value=True)
        response = csle_collector.snort_ids_manager.query_snort_ids_manager.stop_snort_ids(
            stub=grpc_stub)
        assert response.monitor_running
        assert not response.snort_ids_running

    def test_startSnortIds(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startSnortIdsMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        popen_res = mocker.MagicMock()
        popen_res.configure_mock(**{"stdout": "", "wait.return_value": None})
        mocker.patch('subprocess.Popen', return_value=popen_res)
        mocker.patch('subprocess.run', return_value=CompletedProcess(
            args="", returncode=0, stdout=constants.SNORT_IDS_ROUTER.SEARCH_SNORT_RUNNING, stderr="testerr"))
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_monitor_running',
                     return_value=False)
        response: SnortIdsMonitorDTO = csle_collector.snort_ids_manager.query_snort_ids_manager.start_snort_ids(
            stub=grpc_stub, ingress_interface="eth0", egress_interface="eth1", subnetmask="255.255.255.0")
        assert not response.monitor_running
        assert response.snort_ids_running
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_monitor_running',
                     return_value=True)
        response = csle_collector.snort_ids_manager.query_snort_ids_manager.start_snort_ids(
            stub=grpc_stub, ingress_interface="eth0", egress_interface="eth1", subnetmask="255.255.255.0")
        assert response.monitor_running
        assert response.snort_ids_running

    def test_getSnortIdsMonitorStatus(self, grpc_stub, mocker) -> None:
        """
        Tests the getSnortIdsMonitorStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_snort_running',
                     return_value=False)
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_monitor_running',
                     return_value=False)
        response: SnortIdsMonitorDTO = \
            csle_collector.snort_ids_manager.query_snort_ids_manager.get_snort_ids_monitor_status(stub=grpc_stub)
        assert not response.monitor_running
        assert not response.snort_ids_running

        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_snort_running',
                     return_value=True)
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_monitor_running',
                     return_value=False)
        response = \
            csle_collector.snort_ids_manager.query_snort_ids_manager.get_snort_ids_monitor_status(stub=grpc_stub)
        assert not response.monitor_running
        assert response.snort_ids_running

        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_snort_running',
                     return_value=False)
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_monitor_running',
                     return_value=True)
        response = \
            csle_collector.snort_ids_manager.query_snort_ids_manager.get_snort_ids_monitor_status(stub=grpc_stub)
        assert response.monitor_running
        assert not response.snort_ids_running

        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_snort_running',
                     return_value=True)
        mocker.patch('csle_collector.snort_ids_manager.snort_ids_manager.SnortIdsManagerServicer._is_monitor_running',
                     return_value=True)
        response = \
            csle_collector.snort_ids_manager.query_snort_ids_manager.get_snort_ids_monitor_status(stub=grpc_stub)
        assert response.monitor_running
        assert response.snort_ids_running
