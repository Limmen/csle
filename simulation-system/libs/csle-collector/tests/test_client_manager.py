from typing import Any
import pytest
import pytest_mock
import csle_collector.client_manager.query_clients
from csle_collector.client_manager.client_manager_pb2 import ClientsDTO
from csle_collector.client_manager.client_manager import ClientManagerServicer
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.client import Client
from csle_collector.client_manager.dao.sine_arrival_config import SineArrivalConfig
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.eptmp_arrival_config import EPTMPArrivalConfig
from csle_collector.client_manager.dao.spiking_arrival_config import SpikingArrivalConfig
from csle_collector.client_manager.dao.piece_wise_constant_arrival_config import PieceWiseConstantArrivalConfig


class TestClientManagerSuite:
    """
    Test suite for the Client manager
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_collector.client_manager.client_manager_pb2_grpc import add_ClientManagerServicer_to_server
        return add_ClientManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> ClientManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the client manager servicer
        """
        return ClientManagerServicer()

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_collector.client_manager.client_manager_pb2_grpc import ClientManagerStub
        return ClientManagerStub

    def test_getClients(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getClients grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        arrival_thread = mocker.MagicMock()
        arrival_thread.client_threads = ["client1", "client2"]
        arrival_thread.time_step_len_seconds = 30
        producer_thread = mocker.MagicMock()
        producer_thread.time_step_len_seconds = 30
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_producer_thread',
                     return_value=producer_thread)
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_arrival_thread',
                     return_value=arrival_thread)
        response: ClientsDTO = csle_collector.client_manager.query_clients.get_clients(stub=grpc_stub)
        assert response is not None
        assert response.num_clients == len(arrival_thread.client_threads)
        assert response.client_process_active
        assert response.producer_active
        assert response.clients_time_step_len_seconds == 30
        assert response.producer_time_step_len_seconds == 30
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_producer_thread',
                     return_value=None)
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_arrival_thread',
                     return_value=None)
        response = csle_collector.client_manager.query_clients.get_clients(stub=grpc_stub)
        assert response is not None
        assert response.num_clients == 0
        assert not response.client_process_active
        assert not response.producer_active
        assert response.clients_time_step_len_seconds == 0.0
        assert response.producer_time_step_len_seconds == 0.0

    def test_stopClients(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopClients grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        arrival_thread = mocker.MagicMock()
        arrival_thread.client_threads = ["client1", "client2"]
        arrival_thread.time_step_len_seconds = 30
        producer_thread = mocker.MagicMock()
        producer_thread.time_step_len_seconds = 30
        mocker.patch('time.sleep', return_value=None)
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_producer_thread',
                     return_value=producer_thread)
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_arrival_thread',
                     return_value=arrival_thread)
        response: ClientsDTO = csle_collector.client_manager.query_clients.stop_clients(stub=grpc_stub)
        assert response is not None
        assert response.num_clients == 0
        assert not response.client_process_active
        assert response.producer_active
        assert response.clients_time_step_len_seconds == 30
        assert response.producer_time_step_len_seconds == 30

        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_producer_thread',
                     return_value=None)
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_arrival_thread',
                     return_value=None)
        response = csle_collector.client_manager.query_clients.stop_clients(stub=grpc_stub)
        assert response is not None
        assert response.num_clients == 0
        assert not response.client_process_active
        assert not response.producer_active
        assert response.clients_time_step_len_seconds == 0.0
        assert response.producer_time_step_len_seconds == 0.0

    def test_startClients(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startClients grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        arrival_thread = mocker.MagicMock()
        arrival_thread.client_threads = ["client1", "client2"]
        arrival_thread.time_step_len_seconds = 30
        producer_thread = mocker.MagicMock()
        producer_thread.time_step_len_seconds = 30
        mocker.patch('time.sleep', return_value=None)
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_producer_thread',
                     return_value=producer_thread)
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_arrival_thread',
                     return_value=arrival_thread)
        mocker.patch('csle_collector.client_manager.threads.arrival_thread.ArrivalThread.__init__',
                     return_value=None)
        mocker.patch('csle_collector.client_manager.threads.arrival_thread.ArrivalThread.run',
                     return_value=True)
        mocker.patch('csle_collector.client_manager.threads.arrival_thread.ArrivalThread.start',
                     return_value=True)
        time_step_len_seconds = 30
        workflows_config = WorkflowsConfig(
            workflow_markov_chains=[
                WorkflowMarkovChain(transition_matrix=[[0.2, 0.8], [0.8, 0.2]], initial_state=0, id=0)],
            workflow_services=[WorkflowService(ips_and_commands=[("192.168.1.1", ["ping localhost"])], id=0)])
        response: ClientsDTO = csle_collector.client_manager.query_clients.start_clients(
            stub=grpc_stub, time_step_len_seconds=time_step_len_seconds, workflows_config=workflows_config,
            clients=[Client(id=0, workflow_distribution=[0.9, 0.1],
                            arrival_config=SineArrivalConfig(
                                lamb=9.0, time_scaling_factor=2.0, period_scaling_factor=5.0),
                            mu=4, exponential_service_time=False)])
        assert response is not None
        assert response.num_clients == 0
        assert response.client_process_active
        assert response.producer_active
        assert response.clients_time_step_len_seconds == time_step_len_seconds
        assert response.producer_time_step_len_seconds == 30

        workflows_config = WorkflowsConfig(
            workflow_markov_chains=[
                WorkflowMarkovChain(transition_matrix=[[0.2, 0.8], [0.8, 0.2]], initial_state=0, id=0)],
            workflow_services=[WorkflowService(ips_and_commands=[("192.168.1.1", ["ping localhost"])], id=0)])
        response = csle_collector.client_manager.query_clients.start_clients(
            stub=grpc_stub, time_step_len_seconds=time_step_len_seconds, workflows_config=workflows_config,
            clients=[Client(id=0, workflow_distribution=[0.9, 0.1],
                            arrival_config=SpikingArrivalConfig(exponents=[0.2, 0.5], factors=[0.9, 0.1]),
                            mu=4, exponential_service_time=False)])
        assert response is not None
        assert response.num_clients == 0
        assert response.client_process_active
        assert response.producer_active
        assert response.clients_time_step_len_seconds == time_step_len_seconds
        assert response.producer_time_step_len_seconds == 30

        workflows_config = WorkflowsConfig(
            workflow_markov_chains=[
                WorkflowMarkovChain(transition_matrix=[[0.2, 0.8], [0.8, 0.2]], initial_state=0, id=0)],
            workflow_services=[WorkflowService(ips_and_commands=[("192.168.1.1", ["ping localhost"])], id=0)])
        response = csle_collector.client_manager.query_clients.start_clients(
            stub=grpc_stub, time_step_len_seconds=time_step_len_seconds, workflows_config=workflows_config,
            clients=[Client(id=0, workflow_distribution=[0.9, 0.1],
                            arrival_config=ConstantArrivalConfig(lamb=9.0),
                            mu=4, exponential_service_time=False)])
        assert response is not None
        assert response.num_clients == 0
        assert response.client_process_active
        assert response.producer_active
        assert response.clients_time_step_len_seconds == time_step_len_seconds
        assert response.producer_time_step_len_seconds == 30

        workflows_config = WorkflowsConfig(
            workflow_markov_chains=[
                WorkflowMarkovChain(transition_matrix=[[0.2, 0.8], [0.8, 0.2]], initial_state=0, id=0)],
            workflow_services=[WorkflowService(ips_and_commands=[("192.168.1.1", ["ping localhost"])], id=0)])
        response = csle_collector.client_manager.query_clients.start_clients(
            stub=grpc_stub, time_step_len_seconds=time_step_len_seconds, workflows_config=workflows_config,
            clients=[Client(id=0, workflow_distribution=[0.9, 0.1],
                            arrival_config=EPTMPArrivalConfig(
                                thetas=[0.15, 0.6, 0.215], gammas=[0.1, 0.6, 0.8], phis=[0.16, 0.52, 0.1],
                                omegas=[0.1, 0.6, 0.9]),
                            mu=4, exponential_service_time=False)])
        assert response is not None
        assert response.num_clients == 0
        assert response.client_process_active
        assert response.producer_active
        assert response.clients_time_step_len_seconds == time_step_len_seconds
        assert response.producer_time_step_len_seconds == 30

        workflows_config = WorkflowsConfig(
            workflow_markov_chains=[
                WorkflowMarkovChain(transition_matrix=[[0.2, 0.8], [0.8, 0.2]], initial_state=0, id=0)],
            workflow_services=[WorkflowService(ips_and_commands=[("192.168.1.1", ["ping localhost"])], id=0)])
        response = csle_collector.client_manager.query_clients.start_clients(
            stub=grpc_stub, time_step_len_seconds=time_step_len_seconds, workflows_config=workflows_config,
            clients=[Client(id=0, workflow_distribution=[0.9, 0.1],
                            arrival_config=PieceWiseConstantArrivalConfig(
                                breakvalues=[0.65, 0.12, 0.9], breakpoints=[1, 5, 10]),
                            mu=4, exponential_service_time=False)])
        assert response is not None
        assert response.num_clients == 0
        assert response.client_process_active
        assert response.producer_active
        assert response.clients_time_step_len_seconds == time_step_len_seconds
        assert response.producer_time_step_len_seconds == 30

    def test_startProducer(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startProducer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        arrival_thread = mocker.MagicMock()
        arrival_thread.client_threads = ["client1", "client2"]
        arrival_thread.time_step_len_seconds = 30
        producer_thread = mocker.MagicMock()
        producer_thread.time_step_len_seconds = 30
        mocker.patch('time.sleep', return_value=None)
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_producer_thread',
                     return_value=producer_thread)
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_arrival_thread',
                     return_value=arrival_thread)
        mocker.patch('csle_collector.client_manager.threads.producer_thread.ProducerThread.__init__',
                     return_value=None)
        mocker.patch('csle_collector.client_manager.threads.producer_thread.ProducerThread.run',
                     return_value=True)
        mocker.patch('csle_collector.client_manager.threads.producer_thread.ProducerThread.start',
                     return_value=True)
        time_step_len_seconds = 30
        ip = "192.168.12.5"
        port = 3333
        response: ClientsDTO = csle_collector.client_manager.query_clients.start_producer(
            stub=grpc_stub, time_step_len_seconds=time_step_len_seconds, ip=ip, port=port)
        assert response is not None
        assert response.num_clients == len(arrival_thread.client_threads)
        assert response.client_process_active
        assert response.producer_active
        assert response.clients_time_step_len_seconds == 30
        assert response.producer_time_step_len_seconds == time_step_len_seconds

    def test_stopProducer(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopProducer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        arrival_thread = mocker.MagicMock()
        arrival_thread.client_threads = ["client1", "client2"]
        arrival_thread.time_step_len_seconds = 30
        producer_thread = mocker.MagicMock()
        producer_thread.time_step_len_seconds = 30
        mocker.patch('time.sleep', return_value=None)
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_producer_thread',
                     return_value=producer_thread)
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_arrival_thread',
                     return_value=arrival_thread)
        response: ClientsDTO = csle_collector.client_manager.query_clients.stop_producer(stub=grpc_stub)
        assert response is not None
        assert response.num_clients == len(arrival_thread.client_threads)
        assert response.client_process_active
        assert not response.producer_active
        assert response.clients_time_step_len_seconds == arrival_thread.time_step_len_seconds
        assert response.producer_time_step_len_seconds == 0

        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_producer_thread',
                     return_value=None)
        mocker.patch('csle_collector.client_manager.client_manager.ClientManagerServicer.get_arrival_thread',
                     return_value=None)
        response = csle_collector.client_manager.query_clients.stop_clients(stub=grpc_stub)
        assert response is not None
        assert response.num_clients == 0
        assert not response.client_process_active
        assert not response.producer_active
        assert response.clients_time_step_len_seconds == 0.0
        assert response.producer_time_step_len_seconds == 0.0
