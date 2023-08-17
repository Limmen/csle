from typing import Any
import pytest
import pytest_mock
import csle_collector.host_manager.query_host_manager
from csle_collector.host_manager.host_manager_pb2 import HostStatusDTO, HostMetricsDTO
from csle_collector.host_manager.host_manager import HostManagerServicer
from csle_collector.host_manager.dao.host_metrics import HostMetrics


class TestHostManagerSuite:
    """
    Test suite for the Host manager
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_collector.host_manager.host_manager_pb2_grpc import add_HostManagerServicer_to_server
        return add_HostManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> HostManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the host manager servicer
        """
        return HostManagerServicer()

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_collector.host_manager.host_manager_pb2_grpc import HostManagerStub
        return HostManagerStub

    def test_startHostMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startHostMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.threads.host_monitor_thread.HostMonitorThread.run',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.threads.host_monitor_thread.HostMonitorThread.__init__',
                     return_value=None)
        mocker.patch('csle_collector.host_manager.threads.host_monitor_thread.HostMonitorThread.start',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        kafka_ip = "test_kafka_ip"
        kafka_port = 9292
        time_step_len_seconds = 30
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.start_host_monitor(
            stub=grpc_stub, kafka_ip=kafka_ip, kafka_port=kafka_port, time_step_len_seconds=time_step_len_seconds)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=False)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=False)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=False)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=False)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=False)
        response = csle_collector.host_manager.query_host_manager.start_host_monitor(
            stub=grpc_stub, kafka_ip=kafka_ip, kafka_port=kafka_port, time_step_len_seconds=time_step_len_seconds)
        assert response.monitor_running
        assert not response.filebeat_running
        assert not response.packetbeat_running
        assert not response.metricbeat_running
        assert not response.heartbeat_running

    def test_stopHostMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopHostMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.threads.host_monitor_thread.HostMonitorThread.run',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.threads.host_monitor_thread.HostMonitorThread.__init__',
                     return_value=None)
        mocker.patch('csle_collector.host_manager.threads.host_monitor_thread.HostMonitorThread.start',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.stop_host_monitor(stub=grpc_stub)
        assert not response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=False)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=False)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=False)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=False)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=False)
        response = csle_collector.host_manager.query_host_manager.stop_host_monitor(stub=grpc_stub)
        assert not response.monitor_running
        assert not response.filebeat_running
        assert not response.packetbeat_running
        assert not response.metricbeat_running
        assert not response.heartbeat_running

    def test_startFilebeat(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startFilebeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._start_filebeat',
                     return_value=True)
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.start_filebeat(stub=grpc_stub)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_stopFilebeat(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopFilebeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._stop_filebeat',
                     return_value=True)
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.stop_filebeat(stub=grpc_stub)
        assert response.monitor_running
        assert not response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_configFilebeat(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the configFilebeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._set_filebeat_config',
                     return_value=True)
        log_files_paths = ["test_path"]
        kibana_ip = "test_kibana_ip"
        kibana_port = 999
        elastic_ip = "test_elastic_ip"
        elastic_port = 333
        num_elastic_shards = 415
        kafka_topics = ["topic1"]
        kafka_ip = "test_kafka_ip"
        kafka_port = 5125
        filebeat_modules = ["mod1", "mod2"]
        reload_enabled = False
        kafka = True
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.config_filebeat(
            stub=grpc_stub, log_files_paths=log_files_paths, kibana_ip=kibana_ip, kibana_port=kibana_port,
            elastic_ip=elastic_ip, elastic_port=elastic_port, num_elastic_shards=num_elastic_shards,
            kafka_topics=kafka_topics, kafka_port=kafka_port, filebeat_modules=filebeat_modules,
            reload_enabled=reload_enabled, kafka=kafka, kafka_ip=kafka_ip)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_startMetricbeat(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startMetricbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._start_metricbeat',
                     return_value=True)
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.start_metricbeat(stub=grpc_stub)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_stopMetricbeat(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopMetricbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._stop_metricbeat',
                     return_value=True)
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.stop_metricbeat(stub=grpc_stub)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert not response.metricbeat_running
        assert response.heartbeat_running

    def test_configMetricbeat(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the configMetricbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._set_metricbeat_config',
                     return_value=True)
        kibana_ip = "test_kibana_ip"
        kibana_port = 999
        elastic_ip = "test_elastic_ip"
        elastic_port = 333
        num_elastic_shards = 415
        kafka_ip = "test_kafka_ip"
        kafka_port = 5125
        metricbeat_modules = ["mod1", "mod2"]
        reload_enabled = False
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.config_metricbeat(
            stub=grpc_stub, kibana_ip=kibana_ip, kibana_port=kibana_port,
            elastic_ip=elastic_ip, elastic_port=elastic_port, num_elastic_shards=num_elastic_shards,
            kafka_port=kafka_port, metricbeat_modules=metricbeat_modules,
            reload_enabled=reload_enabled, kafka_ip=kafka_ip)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_startPacketbeat(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startPacketbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._start_packetbeat',
                     return_value=True)
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.start_packetbeat(stub=grpc_stub)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_stopPacketbeat(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopPacketbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._stop_packetbeat',
                     return_value=True)
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.stop_packetbeat(stub=grpc_stub)
        assert response.monitor_running
        assert response.filebeat_running
        assert not response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_configPacketbeat(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the configPacketbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._set_packetbeat_config',
                     return_value=True)
        kibana_ip = "test_kibana_ip"
        kibana_port = 999
        elastic_ip = "test_elastic_ip"
        elastic_port = 333
        num_elastic_shards = 415
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.config_packetbeat(
            stub=grpc_stub, kibana_ip=kibana_ip, kibana_port=kibana_port,
            elastic_ip=elastic_ip, elastic_port=elastic_port, num_elastic_shards=num_elastic_shards)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_startHeartbeat(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startHeartbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._start_heartbeat',
                     return_value=True)
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.start_heartbeat(stub=grpc_stub)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_stopHeartbeat(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopPacketbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._stop_heartbeat',
                     return_value=True)
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.stop_heartbeat(stub=grpc_stub)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert not response.heartbeat_running

    def test_configHeartbeat(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the configHeartbeat grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._set_heartbeat_config',
                     return_value=True)
        kibana_ip = "test_kibana_ip"
        kibana_port = 999
        elastic_ip = "test_elastic_ip"
        elastic_port = 333
        num_elastic_shards = 415
        hosts_to_monitor = ["host1", "host2"]
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.config_heartbeat(
            stub=grpc_stub, kibana_ip=kibana_ip, kibana_port=kibana_port,
            elastic_ip=elastic_ip, elastic_port=elastic_port, num_elastic_shards=num_elastic_shards,
            hosts_to_monitor=hosts_to_monitor)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_startSpark(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startSpark grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._start_spark',
                     return_value=True)
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.start_spark(stub=grpc_stub)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_stopSpark(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopSpark grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._stop_spark',
                     return_value=True)
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.stop_spark(stub=grpc_stub)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_getHostStatus(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getHostStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_filebeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_packetbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_metricbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._get_heartbeat_status',
                     return_value=True)
        mocker.patch('csle_collector.host_manager.host_manager.HostManagerServicer._is_monitor_running',
                     return_value=True)
        response: HostStatusDTO = csle_collector.host_manager.query_host_manager.get_host_status(stub=grpc_stub)
        assert response.monitor_running
        assert response.filebeat_running
        assert response.packetbeat_running
        assert response.metricbeat_running
        assert response.heartbeat_running

    def test_getHostMetrics(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getHostMetrics grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        num_logged_in_users = 23
        num_failed_login_attempts = 99
        num_open_connections = 3
        num_login_events = 71
        num_processes = 31
        num_users = 6
        ip = "test_ip"
        ts = 0.0
        host_metrics = HostMetrics(
            num_logged_in_users=num_logged_in_users, num_failed_login_attempts=num_failed_login_attempts,
            num_open_connections=num_open_connections, num_login_events=num_login_events,
            num_processes=num_processes, num_users=num_users, ip=ip, ts=ts)
        mocker.patch('csle_collector.host_manager.host_manager_util.HostManagerUtil.read_host_metrics',
                     return_value=host_metrics)
        response: HostMetricsDTO = csle_collector.host_manager.query_host_manager.get_host_metrics(
            stub=grpc_stub, login_last_ts=0.0, failed_auth_last_ts=0.0)
        assert response.num_logged_in_users == num_logged_in_users
        assert response.num_failed_login_attempts == num_failed_login_attempts
        assert response.num_open_connections == num_open_connections
        assert response.num_login_events == num_login_events
        assert response.num_processes == num_processes
        assert response.num_users == num_users
