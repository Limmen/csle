from typing import Any
import pytest
import pytest_mock
import csle_collector.traffic_manager.query_traffic_manager
from csle_collector.traffic_manager.traffic_manager_pb2 import TrafficDTO
from csle_collector.traffic_manager.traffic_manager import TrafficManagerServicer


class TestTrafficManagerSuite:
    """
    Test suite for the Traffic manager
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_collector.traffic_manager.traffic_manager_pb2_grpc import add_TrafficManagerServicer_to_server
        return add_TrafficManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> TrafficManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the host manager servicer
        """
        return TrafficManagerServicer()

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_collector.traffic_manager.traffic_manager_pb2_grpc import TrafficManagerStub
        return TrafficManagerStub

    def test_getTrafficStatus(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getTrafficStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.traffic_manager.traffic_manager.'
                     'TrafficManagerServicer._read_traffic_script', return_value="script_file")
        mocker.patch('csle_collector.traffic_manager.traffic_manager.'
                     'TrafficManagerServicer._create_traffic_script', return_value=None)
        mocker.patch('csle_collector.traffic_manager.traffic_manager.TrafficManagerServicer._get_traffic_status',
                     return_value=False)
        response: TrafficDTO = csle_collector.traffic_manager.query_traffic_manager.get_traffic_status(stub=grpc_stub)
        assert response is not None
        assert not response.running
        assert response.script == "script_file"

        mocker.patch('csle_collector.traffic_manager.traffic_manager.TrafficManagerServicer._get_traffic_status',
                     return_value=True)
        response = csle_collector.traffic_manager.query_traffic_manager.get_traffic_status(stub=grpc_stub)
        assert response is not None
        assert response.running
        assert response.script == "script_file"

    def test_stopTraffic(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopTraffic grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.traffic_manager.traffic_manager.'
                     'TrafficManagerServicer._read_traffic_script', return_value="script_file")
        mocker.patch('csle_collector.traffic_manager.traffic_manager.'
                     'TrafficManagerServicer._create_traffic_script', return_value=None)
        mocker.patch('os.system', return_value=True)
        mocker.patch('csle_collector.traffic_manager.traffic_manager.TrafficManagerServicer._get_traffic_status',
                     return_value=False)
        response: TrafficDTO = csle_collector.traffic_manager.query_traffic_manager.stop_traffic(stub=grpc_stub)
        assert response is not None
        assert not response.running
        assert response.script == "script_file"

    def test_startTraffic(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startTraffic grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.traffic_manager.traffic_manager.'
                     'TrafficManagerServicer._read_traffic_script', return_value="script_file")
        mocker.patch('csle_collector.traffic_manager.traffic_manager.'
                     'TrafficManagerServicer._create_traffic_script', return_value=None)
        mocker.patch('os.system', return_value=True)
        mocker.patch('csle_collector.traffic_manager.traffic_manager.TrafficManagerServicer._get_traffic_status',
                     return_value=False)
        commands = ["ping localhost"]
        sleep_time = 30
        response: TrafficDTO = csle_collector.traffic_manager.query_traffic_manager.start_traffic(
            stub=grpc_stub, commands=commands, sleep_time=sleep_time)
        assert response is not None
        assert response.running
        assert response.script == "script_file"
