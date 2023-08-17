from typing import Any
import pytest
import pytest_mock
from subprocess import CompletedProcess
from csle_collector.ossec_ids_manager.ossec_ids_manager_pb2 import OSSECIdsMonitorDTO, OSSECIdsLogDTO
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.ossec_ids_manager.ossec_ids_manager import OSSECIdsManagerServicer
import csle_collector.ossec_ids_manager.query_ossec_ids_manager


class TestOSSECIDSManagerSuite:
    """
    Test suite for the OSSEC IDS manager
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc import add_OSSECIdsManagerServicer_to_server
        return add_OSSECIdsManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> OSSECIdsManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the ossec manager servicer
        """
        return OSSECIdsManagerServicer()

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_collector.ossec_ids_manager.ossec_ids_manager_pb2_grpc import OSSECIdsManagerStub
        return OSSECIdsManagerStub

    def test_getOSSECIdsAlerts(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getOSSECIdsAlerts grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """

        def read_ossec_ids_data(timestamp: float):
            if timestamp == 0:
                return OSSECIdsAlertCounters()
            else:
                alerts = OSSECIdsAlertCounters()
                alerts.severe_alerts = 100
                alerts.warning_alerts = 200
                alerts.total_alerts = 300
                alerts.alerts_weighted_by_level = 400
                alerts.ip = "test"
                alerts.ts = 0.0
                return alerts

        read_data_mock = mocker.MagicMock(side_effect=read_ossec_ids_data)
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSecManagerUtil.read_ossec_ids_data',
                     side_effect=read_data_mock)
        response: OSSECIdsLogDTO = csle_collector.ossec_ids_manager.query_ossec_ids_manager.get_ossec_ids_alerts(
            stub=grpc_stub, timestamp=0, log_file_path="")
        assert response.attempted_admin_alerts == 0
        assert response.total_alerts == 0
        assert response.warning_alerts == 0
        assert response.severe_alerts == 0
        assert response.alerts_weighted_by_level == 0
        assert response.level_0_alerts == 0
        assert response.level_1_alerts == 0
        assert response.level_2_alerts == 0
        assert response.level_3_alerts == 0
        assert response.level_4_alerts == 0
        assert response.level_5_alerts == 0
        assert response.level_6_alerts == 0
        assert response.level_7_alerts == 0
        assert response.level_8_alerts == 0
        assert response.level_9_alerts == 0
        assert response.level_10_alerts == 0
        assert response.level_11_alerts == 0
        assert response.level_12_alerts == 0
        assert response.level_13_alerts == 0
        assert response.level_14_alerts == 0
        assert response.level_15_alerts == 0
        assert response.invalid_login_alerts == 0
        assert response.authentication_success_alerts == 0
        assert response.authentication_failed_alerts == 0
        assert response.connection_attempt_alerts == 0
        assert response.attacks_alerts == 0
        assert response.adduser_alerts == 0
        assert response.sshd_alerts == 0
        assert response.ids_alerts == 0
        assert response.firewall_alerts == 0
        assert response.squid_alerts == 0
        assert response.apache_alerts == 0
        assert response.syslog_alerts == 0
        response = csle_collector.ossec_ids_manager.query_ossec_ids_manager.get_ossec_ids_alerts(
            stub=grpc_stub, timestamp=1, log_file_path="")
        assert response.total_alerts == 300
        assert response.warning_alerts == 200
        assert response.severe_alerts == 100
        assert response.alerts_weighted_by_level == 400

    def test_startOSSECIdsMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startOSSECIdsMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.ossec_ids_manager.threads.ossec_ids_monitor_thread.OSSecIdsMonitorThread.run',
                     return_value=True)
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_ossec_running',
                     return_value=True)
        kafka_ip = "test_kafka_ip"
        kafka_port = 9292
        log_file_path = "test_log_file_path"
        time_step_len_seconds = 30
        response: OSSECIdsMonitorDTO = csle_collector.ossec_ids_manager.query_ossec_ids_manager.start_ossec_ids_monitor(
            stub=grpc_stub, kafka_ip=kafka_ip, kafka_port=kafka_port, log_file_path=log_file_path,
            time_step_len_seconds=time_step_len_seconds)
        assert response.monitor_running
        assert response.ossec_ids_running
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_ossec_running',
                     return_value=False)
        response = csle_collector.ossec_ids_manager.query_ossec_ids_manager.start_ossec_ids_monitor(
            stub=grpc_stub, kafka_ip=kafka_ip, kafka_port=kafka_port, log_file_path=log_file_path,
            time_step_len_seconds=time_step_len_seconds)
        assert response.monitor_running
        assert not response.ossec_ids_running

    def test_stopOSSECIdsMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopOSSECIdsMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_ossec_running',
                     return_value=True)
        response: OSSECIdsMonitorDTO = csle_collector.ossec_ids_manager.query_ossec_ids_manager.stop_ossec_ids_monitor(
            stub=grpc_stub)
        assert not response.monitor_running
        assert response.ossec_ids_running
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_ossec_running',
                     return_value=False)
        response = csle_collector.ossec_ids_manager.query_ossec_ids_manager.stop_ossec_ids_monitor(
            stub=grpc_stub)
        assert not response.monitor_running
        assert not response.ossec_ids_running

    def test_stopOSSECIds(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopOSSECIdsMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('subprocess.run', return_value=CompletedProcess(args="", returncode=0, stdout="testout",
                                                                     stderr="testerr"))
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_monitor_running',
                     return_value=False)
        response: OSSECIdsMonitorDTO = csle_collector.ossec_ids_manager.query_ossec_ids_manager.stop_ossec_ids(
            stub=grpc_stub)
        assert not response.monitor_running
        assert not response.ossec_ids_running
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_monitor_running',
                     return_value=True)
        response = csle_collector.ossec_ids_manager.query_ossec_ids_manager.stop_ossec_ids(
            stub=grpc_stub)
        assert response.monitor_running
        assert not response.ossec_ids_running

    def test_startOSSECIds(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startOSSECIdsMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('subprocess.run', return_value=CompletedProcess(args="", returncode=0, stdout="testout",
                                                                     stderr="testerr"))
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_monitor_running',
                     return_value=False)
        response: OSSECIdsMonitorDTO = csle_collector.ossec_ids_manager.query_ossec_ids_manager.start_ossec_ids(
            stub=grpc_stub)
        assert not response.monitor_running
        assert response.ossec_ids_running
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_monitor_running',
                     return_value=True)
        response = csle_collector.ossec_ids_manager.query_ossec_ids_manager.start_ossec_ids(
            stub=grpc_stub)
        assert response.monitor_running
        assert response.ossec_ids_running

    def test_getOSSECIdsMonitorStatus(self, grpc_stub, mocker) -> None:
        """
        Tests the getOSSECIdsMonitorStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_ossec_running',
                     return_value=False)
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_monitor_running',
                     return_value=False)
        response: OSSECIdsMonitorDTO = \
            csle_collector.ossec_ids_manager.query_ossec_ids_manager.get_ossec_ids_monitor_status(stub=grpc_stub)
        assert not response.monitor_running
        assert not response.ossec_ids_running

        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_ossec_running',
                     return_value=True)
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_monitor_running',
                     return_value=False)
        response = \
            csle_collector.ossec_ids_manager.query_ossec_ids_manager.get_ossec_ids_monitor_status(stub=grpc_stub)
        assert not response.monitor_running
        assert response.ossec_ids_running

        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_ossec_running',
                     return_value=False)
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_monitor_running',
                     return_value=True)
        response = \
            csle_collector.ossec_ids_manager.query_ossec_ids_manager.get_ossec_ids_monitor_status(stub=grpc_stub)
        assert response.monitor_running
        assert not response.ossec_ids_running

        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_ossec_running',
                     return_value=True)
        mocker.patch('csle_collector.ossec_ids_manager.ossec_ids_manager.OSSECIdsManagerServicer._is_monitor_running',
                     return_value=True)
        response = \
            csle_collector.ossec_ids_manager.query_ossec_ids_manager.get_ossec_ids_monitor_status(stub=grpc_stub)
        assert response.monitor_running
        assert response.ossec_ids_running
