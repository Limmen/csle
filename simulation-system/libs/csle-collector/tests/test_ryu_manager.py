from typing import Any
import pytest
import pytest_mock
from subprocess import CompletedProcess
import csle_collector.ryu_manager.query_ryu_manager
from csle_collector.ryu_manager.ryu_manager_pb2 import RyuDTO
from csle_collector.ryu_manager.ryu_manager import RyuManagerServicer


class TestRyuManagerSuite:
    """
    Test suite for the Ryu manager
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_collector.ryu_manager.ryu_manager_pb2_grpc import add_RyuManagerServicer_to_server
        return add_RyuManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> RyuManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the host manager servicer
        """
        return RyuManagerServicer()

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_collector.ryu_manager.ryu_manager_pb2_grpc import RyuManagerStub
        return RyuManagerStub

    def test_getRyuStatus(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getRyuStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_ryu_status',
                     return_value=False)
        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_monitor_status',
                     return_value=False)
        response: RyuDTO = csle_collector.ryu_manager.query_ryu_manager.get_ryu_status(stub=grpc_stub)
        assert response is not None
        assert not response.monitor_running
        assert not response.ryu_running

        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_ryu_status',
                     return_value=True)
        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_monitor_status',
                     return_value=False)
        response = csle_collector.ryu_manager.query_ryu_manager.get_ryu_status(stub=grpc_stub)
        assert response is not None
        assert not response.monitor_running
        assert response.ryu_running

        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_ryu_status',
                     return_value=False)
        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_monitor_status',
                     return_value=True)
        response = csle_collector.ryu_manager.query_ryu_manager.get_ryu_status(stub=grpc_stub)
        assert response is not None
        assert not response.monitor_running
        assert not response.ryu_running

        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_ryu_status',
                     return_value=True)
        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_monitor_status',
                     return_value=True)
        response = csle_collector.ryu_manager.query_ryu_manager.get_ryu_status(stub=grpc_stub)
        assert response is not None
        assert response.monitor_running
        assert response.ryu_running

    def test_stopRyu(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopRyu grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_ryu_status',
                     return_value=True)
        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_monitor_status',
                     return_value=True)
        mocker.patch('subprocess.run', return_value=CompletedProcess(args="", returncode=0, stdout="testout",
                                                                     stderr="testerr"))
        response: RyuDTO = csle_collector.ryu_manager.query_ryu_manager.stop_ryu(stub=grpc_stub)
        assert response is not None
        assert not response.monitor_running
        assert not response.ryu_running

    def test_startRyu(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startRyu grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_ryu_status',
                     return_value=False)
        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_monitor_status',
                     return_value=False)
        mocker.patch('subprocess.run', return_value=CompletedProcess(args="", returncode=0, stdout="testout",
                                                                     stderr="testerr"))
        mocker.patch('subprocess.Popen', return_value=None)
        mocker.patch('csle_collector.ryu_manager.threads.failure_detector.FailureDetector.run',
                     return_value=True)
        mocker.patch('csle_collector.ryu_manager.threads.failure_detector.FailureDetector.__init__',
                     return_value=None)
        mocker.patch('csle_collector.ryu_manager.threads.failure_detector.FailureDetector.start',
                     return_value=True)
        port = 6060
        web_port = 8080
        controller = "controller"
        response: RyuDTO = csle_collector.ryu_manager.query_ryu_manager.start_ryu(stub=grpc_stub, port=port,
                                                                                  web_port=web_port,
                                                                                  controller=controller)
        assert response is not None
        assert not response.monitor_running
        assert response.ryu_running
        assert response.web_port == web_port
        assert response.port == port
        assert response.controller == controller

    def test_stopRyuMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopRyuMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_ryu_status',
                     return_value=True)
        mocker.patch('requests.post', return_value=True)
        response: RyuDTO = csle_collector.ryu_manager.query_ryu_manager.stop_ryu_monitor(stub=grpc_stub)
        assert response is not None
        assert not response.monitor_running
        assert response.ryu_running

    def test_startRyuMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startRyuMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        http_response_mock = mocker.MagicMock()
        http_response_mock.status_code = 200
        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_ryu_status',
                     return_value=False)
        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_monitor_status',
                     return_value=False)
        mocker.patch('requests.put', return_value=http_response_mock)
        kafka_ip = "192.168.5.5"
        kafka_port = 3333
        time_step_len = 30
        response: RyuDTO = csle_collector.ryu_manager.query_ryu_manager.start_ryu_monitor(
            stub=grpc_stub, kafka_ip=kafka_ip, kafka_port=kafka_port, time_step_len=time_step_len)
        assert response is not None
        assert not response.monitor_running
        assert not response.ryu_running
        assert response.kafka_ip == kafka_ip
        assert response.kafka_port == kafka_port
        assert response.time_step_len == time_step_len

        mocker.patch('csle_collector.ryu_manager.ryu_manager.RyuManagerServicer._get_ryu_status',
                     return_value=True)
        response = csle_collector.ryu_manager.query_ryu_manager.start_ryu_monitor(
            stub=grpc_stub, kafka_ip=kafka_ip, kafka_port=kafka_port, time_step_len=time_step_len)
        assert response is not None
        assert response.monitor_running
        assert response.ryu_running
        assert response.kafka_ip == kafka_ip
        assert response.kafka_port == kafka_port
        assert response.time_step_len == time_step_len

        http_response_mock = mocker.MagicMock()
        http_response_mock.status_code = 500
        mocker.patch('requests.put', return_value=http_response_mock)
        response = csle_collector.ryu_manager.query_ryu_manager.start_ryu_monitor(
            stub=grpc_stub, kafka_ip=kafka_ip, kafka_port=kafka_port, time_step_len=time_step_len)
        assert response is not None
        assert not response.monitor_running
        assert response.ryu_running
        assert response.kafka_ip == kafka_ip
        assert response.kafka_port == kafka_port
        assert response.time_step_len == time_step_len
