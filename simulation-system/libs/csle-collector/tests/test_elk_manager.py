from typing import Any
import pytest
import pytest_mock
import csle_collector.elk_manager.query_elk_manager
from csle_collector.elk_manager.elk_manager_pb2 import ElkDTO
from csle_collector.elk_manager.elk_manager import ElkManagerServicer


class TestElkManagerSuite:
    """
    Test suite for the ELK manager
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_collector.elk_manager.elk_manager_pb2_grpc import add_ElkManagerServicer_to_server
        return add_ElkManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> ElkManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the host manager servicer
        """
        return ElkManagerServicer()

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_collector.elk_manager.elk_manager_pb2_grpc import ElkManagerStub
        return ElkManagerStub

    def test_getElkStatus(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopElk grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.elk_manager.elk_manager.ElkManagerServicer._get_elk_status',
                     return_value=(False, False, False))
        response: ElkDTO = csle_collector.elk_manager.query_elk_manager.get_elk_status(stub=grpc_stub)
        assert not response.elasticRunning
        assert not response.kibanaRunning
        assert not response.logstashRunning
        mocker.patch('csle_collector.elk_manager.elk_manager.ElkManagerServicer._get_elk_status',
                     return_value=(True, False, False))
        response = csle_collector.elk_manager.query_elk_manager.get_elk_status(stub=grpc_stub)
        assert response.elasticRunning
        assert not response.kibanaRunning
        assert not response.logstashRunning

        mocker.patch('csle_collector.elk_manager.elk_manager.ElkManagerServicer._get_elk_status',
                     return_value=(True, False, True))
        response = csle_collector.elk_manager.query_elk_manager.get_elk_status(stub=grpc_stub)
        assert response.elasticRunning
        assert not response.kibanaRunning
        assert response.logstashRunning

        mocker.patch('csle_collector.elk_manager.elk_manager.ElkManagerServicer._get_elk_status',
                     return_value=(True, True, True))
        response = csle_collector.elk_manager.query_elk_manager.get_elk_status(stub=grpc_stub)
        assert response.elasticRunning
        assert response.kibanaRunning
        assert response.logstashRunning

    def test_stopElk(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopElk grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.system', return_value=True)
        response: ElkDTO = csle_collector.elk_manager.query_elk_manager.stop_elk(stub=grpc_stub)
        assert not response.elasticRunning
        assert not response.kibanaRunning
        assert not response.logstashRunning

    def test_startElk(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopElk grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.system', return_value=True)
        response: ElkDTO = csle_collector.elk_manager.query_elk_manager.start_elk(stub=grpc_stub)
        assert response.elasticRunning
        assert response.kibanaRunning
        assert response.logstashRunning

    def test_startElastic(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startElastic grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.system', return_value=True)
        mocker.patch('csle_collector.elk_manager.elk_manager.ElkManagerServicer._get_elk_status',
                     return_value=(False, False, False))
        response: ElkDTO = csle_collector.elk_manager.query_elk_manager.start_elastic(stub=grpc_stub)
        assert response.elasticRunning
        assert not response.kibanaRunning
        assert not response.logstashRunning

    def test_stopElastic(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopElastic grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.system', return_value=True)
        mocker.patch('csle_collector.elk_manager.elk_manager.ElkManagerServicer._get_elk_status',
                     return_value=(True, True, True))
        response: ElkDTO = csle_collector.elk_manager.query_elk_manager.stop_elastic(stub=grpc_stub)
        assert not response.elasticRunning
        assert response.kibanaRunning
        assert response.logstashRunning

    def test_startKibana(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startKibana grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.system', return_value=True)
        mocker.patch('csle_collector.elk_manager.elk_manager.ElkManagerServicer._get_elk_status',
                     return_value=(False, False, False))
        response: ElkDTO = csle_collector.elk_manager.query_elk_manager.start_kibana(stub=grpc_stub)
        assert not response.elasticRunning
        assert response.kibanaRunning
        assert not response.logstashRunning

    def test_stopKibana(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopKibana grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.system', return_value=True)
        mocker.patch('csle_collector.elk_manager.elk_manager.ElkManagerServicer._get_elk_status',
                     return_value=(True, True, True))
        response: ElkDTO = csle_collector.elk_manager.query_elk_manager.stop_kibana(stub=grpc_stub)
        assert response.elasticRunning
        assert not response.kibanaRunning
        assert response.logstashRunning

    def test_startLogstash(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startLogstash grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.system', return_value=True)
        mocker.patch('csle_collector.elk_manager.elk_manager.ElkManagerServicer._get_elk_status',
                     return_value=(False, False, False))
        response: ElkDTO = csle_collector.elk_manager.query_elk_manager.start_logstash(stub=grpc_stub)
        assert not response.elasticRunning
        assert not response.kibanaRunning
        assert response.logstashRunning

    def test_stopLogstash(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopLogstash grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.system', return_value=True)
        mocker.patch('csle_collector.elk_manager.elk_manager.ElkManagerServicer._get_elk_status',
                     return_value=(True, True, True))
        response: ElkDTO = csle_collector.elk_manager.query_elk_manager.stop_logstash(stub=grpc_stub)
        assert response.elasticRunning
        assert response.kibanaRunning
        assert not response.logstashRunning
