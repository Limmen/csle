from typing import Any
import pytest
import pytest_mock
import csle_collector.docker_stats_manager.query_docker_stats_manager
from csle_collector.docker_stats_manager.docker_stats_manager_pb2 import DockerStatsMonitorDTO, ContainerIp
from csle_collector.docker_stats_manager.docker_stats_manager import DockerStatsManagerServicer


class TestDockerStatsManagerSuite:
    """
    Test suite for the Docker stats manager
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc \
            import add_DockerStatsManagerServicer_to_server
        return add_DockerStatsManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> DockerStatsManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the docker stats manager servicer
        """
        return DockerStatsManagerServicer()

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc import DockerStatsManagerStub
        return DockerStatsManagerStub

    def test_getDockerStatsMonitorStatus(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getDockerStatsMonitorStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        dsmt_1 = mocker.MagicMock()
        dsmt_1.stopped = True
        dsmt_1.emulation = "em1"
        dsmt_1.execution_first_ip_octet = 5
        dsmt_1.configure_mock(**{"is_alive.return_value": False})
        dsmt_2 = mocker.MagicMock()
        dsmt_2.stopped = False
        dsmt_2.emulation = "em2"
        dsmt_2.execution_first_ip_octet = 8
        dsmt_2.configure_mock(**{"is_alive.return_value": True})
        mocker.patch('csle_collector.docker_stats_manager.docker_stats_manager.DockerStatsManagerServicer.'
                     'get_docker_stats_monitor_threads', return_value=[dsmt_1, dsmt_2])
        response: DockerStatsMonitorDTO = (
            csle_collector.docker_stats_manager.query_docker_stats_manager.get_docker_stats_manager_status(
                stub=grpc_stub))
        assert response is not None
        assert response.num_monitors == 1
        assert len(response.emulations) == 1
        assert list(response.emulations) == ["em2"]
        assert len(list(response.emulation_executions)) == 1
        assert list(response.emulation_executions) == [8]

    def test_stopDockerStatsMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopDockerStatsMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        dsmt_1 = mocker.MagicMock()
        dsmt_1.stopped = False
        dsmt_1.emulation = "em1"
        dsmt_1.execution_first_ip_octet = 5
        dsmt_1.configure_mock(**{"is_alive.return_value": True})
        dsmt_2 = mocker.MagicMock()
        dsmt_2.stopped = False
        dsmt_2.emulation = "em2"
        dsmt_2.execution_first_ip_octet = 8
        dsmt_2.configure_mock(**{"is_alive.return_value": True})
        mocker.patch('csle_collector.docker_stats_manager.docker_stats_manager.DockerStatsManagerServicer.'
                     'get_docker_stats_monitor_threads', return_value=[dsmt_1, dsmt_2])
        response: DockerStatsMonitorDTO = (
            csle_collector.docker_stats_manager.query_docker_stats_manager.stop_docker_stats_monitor(
                stub=grpc_stub, emulation="em1", execution_first_ip_octet=5))
        assert response is not None
        assert response.num_monitors == 1
        assert len(response.emulations) == 1
        assert list(response.emulations) == ["em2"]
        assert len(list(response.emulation_executions)) == 1
        assert list(response.emulation_executions) == [8]

    def test_startDockerStatsMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startDockerStatsMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        dsmt_1 = mocker.MagicMock()
        dsmt_1.stopped = False
        dsmt_1.emulation = "em1"
        dsmt_1.execution_first_ip_octet = 5
        dsmt_1.configure_mock(**{"is_alive.return_value": True})
        dsmt_2 = mocker.MagicMock()
        dsmt_2.stopped = False
        dsmt_2.emulation = "em2"
        dsmt_2.execution_first_ip_octet = 8
        dsmt_2.configure_mock(**{"is_alive.return_value": True})
        mocker.patch('csle_collector.docker_stats_manager.docker_stats_manager.DockerStatsManagerServicer.'
                     'get_docker_stats_monitor_threads', return_value=[dsmt_1, dsmt_2])
        mocker.patch('csle_collector.docker_stats_manager.threads.docker_stats_thread.DockerStatsThread.__init__',
                     return_value=None)
        mocker.patch('csle_collector.docker_stats_manager.threads.docker_stats_thread.DockerStatsThread.run',
                     return_value=True)
        mocker.patch('csle_collector.docker_stats_manager.threads.docker_stats_thread.DockerStatsThread.start',
                     return_value=True)
        kafka_ip = "192.168.25.1"
        stats_queue_maxsize = 5
        time_step_len_seconds = 19
        kafka_port = 34
        containers = [ContainerIp(ip="7.7.7.7", container="container1")]
        response: DockerStatsMonitorDTO = (
            csle_collector.docker_stats_manager.query_docker_stats_manager.start_docker_stats_monitor(
                stub=grpc_stub, emulation="em3", execution_first_ip_octet=9, kafka_ip=kafka_ip,
                stats_queue_maxsize=stats_queue_maxsize, time_step_len_seconds=time_step_len_seconds,
                kafka_port=kafka_port, containers=containers))
        assert response is not None
        import logging
        logging.getLogger().info(response.emulations)
        assert response.num_monitors == 3
        assert len(response.emulations) == 3
        assert "em1" in list(response.emulations)
        assert "em2" in list(response.emulations)
        assert "em3" in list(response.emulations)
        assert len(list(response.emulation_executions)) == 3
        assert 5 in list(response.emulation_executions)
        assert 8 in list(response.emulation_executions)
        assert 9 in list(response.emulation_executions)
