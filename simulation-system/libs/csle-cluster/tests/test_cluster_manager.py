from typing import Any
import pytest
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_collector.ryu_manager.ryu_manager_pb2 import RyuDTO
import pytest_mock
from csle_cluster.cluster_manager.cluster_manager_pb2 import OperationOutcomeDTO
import csle_common.constants.constants as constants
from csle_cluster.cluster_manager.cluster_manager import ClusterManagerServicer
from csle_cluster.cluster_manager.cluster_manager_pb2 import ServiceStatusDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import LogsDTO
from csle_common.dao.emulation_config.config import Config
import csle_cluster.cluster_manager.query_cluster_manager
from csle_cluster.cluster_manager.cluster_manager_pb2 import NodeStatusDTO
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
    def st_ryu(self, mocker):
        """
        Pytest fixture for mocking the start_ryu method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def start_ryu(emulation_env_config: EmulationEnvConfig,
                      physical_server_ip: str,
                      logger: logging.RootLogger):
            ryu = RyuDTO(ryu_running=True, monitor_running=True, port=4, web_port=4,
                         controller="null", kafka_ip="123.456.78.99", kafka_port = 7,
                         time_step_len=4)
            return ryu
        start_ryu_mocker = mocker.MagicMock(side_effect=start_ryu)
        return start_ryu_mocker

    @staticmethod
    def with_class():
        class A:
            def __init__(self):
                pass

            def __enter__(self):
                pass

            def __exit__(self, exc_type, exc_value, traceback):
                pass

        return A()

    def test_getNodeStatus(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config: Config) -> None:
        """
        Tests the getNodeStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
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
        response: NodeStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.get_node_status(stub=grpc_stub)
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
        response = csle_cluster.cluster_manager.query_cluster_manager.get_node_status(stub=grpc_stub)
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
        :return: None
        """
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_postgresql', return_value=(False, None, None))
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_postgresql_running', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_postgresql(stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_postgresql', return_value=(True, "PIPE", "PIPE"))
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_postgresql_running', return_value=False)
        response = csle_cluster.cluster_manager.query_cluster_manager.start_postgresql(stub=grpc_stub)
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_postgresql(stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_postgresql', return_value=(True, "PIPE", "PIPE"))
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_postgresql_running', return_value=False)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_postgresql(stub=grpc_stub)
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_docker_engine(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_docker_engine_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_docker_engine', return_value=(True, "PIPE", "PIPE"))
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_docker_engine(
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_docker_engine(
            stub=grpc_stub)
        assert not response.running

        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_docker_engine_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_docker_engine', return_value=(True, "PIPE", "PIPE"))
        response = csle_cluster.cluster_manager.query_cluster_manager.stop_docker_engine(stub=grpc_stub)
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_nginx(stub=grpc_stub)
        assert response.running

        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_nginx_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_nginx', return_value=(True, "PIPE", "PIPE"))
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_nginx(stub=grpc_stub)
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_nginx(stub=grpc_stub)
        assert not response.running

        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.is_nginx_running', return_value=False)
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_nginx', return_value=(True, "PIPE", "PIPE"))
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_nginx(stub=grpc_stub)
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_cadvisor(stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_cadvisor', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_cadvisor(stub=grpc_stub)
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_cadvisor(stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_cadvisor', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_cadvisor(stub=grpc_stub)
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_node_exporter(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_node_exporter', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_node_exporter(
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_node_exporter(
            stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_node_exporter', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_node_exporter(
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_grafana(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_grafana', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_grafana(
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_grafana(
            stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_grafana', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_grafana(
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_prometheus(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_prometheus', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_prometheus(
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_prometheus(
            stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_prometheus', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_prometheus(
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_pgadmin(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_pgadmin', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_pgadmin(
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_pgadmin(
            stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_pgadmin', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_pgadmin(
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_flask(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_flask', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_flask(
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_flask(
            stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_flask', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_flask(
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_docker_statsmanager(
            stub=grpc_stub)
        assert response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.start_docker_statsmanager', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_docker_statsmanager(
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
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_docker_statsmanager(
            stub=grpc_stub)
        assert not response.running
        mocker.patch('csle_common.controllers.management_system_controller.'
                     'ManagementSystemController.stop_docker_statsmanager', return_value=True)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_docker_statsmanager(
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
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_log_file(stub=grpc_stub,
                                                                                            log_file_name="abcdef")
        assert response.logs == ['abcdef']
        mocker.patch('builtins.open', return_value=None)
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_log_file(stub=grpc_stub,
                                                                                            log_file_name="abcdef")
        assert response.logs == []

    def test_getFlaskLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config) -> None:
        """
        Tests the getFlaskLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config', return_value=example_config)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail',
                     return_value="abcdef")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_flask_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']
        mocker.patch('builtins.open', return_value=None)
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_flask_logs(stub=grpc_stub)
        assert response.logs == []

    def test_getPostrgreSQLLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config) -> None:
        """
        Tests the getPostrgreSQLLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param examople_config: an example Config object, obtained from the conftest.py file
        :return: None
        """
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config', return_value=example_config)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail',
                     return_value="abcdef")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_postgresql_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']
        mocker.patch('builtins.open', return_value=None)
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_postgresql_logs(stub=grpc_stub)
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
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_docker_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']

        Popen_mock.configure_mock(**{"communicate.return_value": (b'', None)})
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_docker_logs(stub=grpc_stub)
        assert response.logs == ['']

    def test_getNginxLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config) -> None:
        """
        Tests the getNginxLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.listdir', return_value=[constants.FILE_PATTERNS.LOG_SUFFIX])
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config', return_value=example_config)
        mocker.patch('os.path.isfile', return_value=True)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail', return_value="abcdef")
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_nginx_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']
        mocker.patch('os.listdir', return_value="null")
        mocker.patch('os.path.isfile', return_value=False)
        response = csle_cluster.cluster_manager.query_cluster_manager.get_nginx_logs(stub=grpc_stub)
        assert response.logs == []

    def test_getGrafanaLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config) -> None:
        """
        Tests the getGrafanaLogs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        Popen_mock = mocker.MagicMock()
        mocker.patch('subprocess.Popen', return_value=Popen_mock)
        Popen_mock.configure_mock(**{"communicate.return_value": (b'abcdef', None)})
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_grafana_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']

    def test_getPgAdminLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config) -> None:
        """
        Tests the getPgAdminLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        Popen_mock = mocker.MagicMock()
        mocker.patch('subprocess.Popen', return_value=Popen_mock)
        Popen_mock.configure_mock(**{"communicate.return_value": (b'abcdef', None)})
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_pgadmin_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']

    def test_getCadvisorLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config) -> None:
        """
        Tests the getCadvisorLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        Popen_mock = mocker.MagicMock()
        mocker.patch('subprocess.Popen', return_value=Popen_mock)
        Popen_mock.configure_mock(**{"communicate.return_value": (b'abcdef', None)})
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_cadvisor_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']

    def test_getNodeExporterLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config) -> None:
        """
        Tests the getNodeExporterLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.listdir', return_value=[constants.FILE_PATTERNS.LOG_SUFFIX])
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config', return_value=example_config)
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail', return_value="abcdef")
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_node_exporter_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']
        mocker.patch('os.path.exists', return_value=False)
        response = csle_cluster.cluster_manager.query_cluster_manager.get_node_exporter_logs(stub=grpc_stub)
        assert response.logs == []

    def test_getPrometheusLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config) -> None:
        """
        Tests the getPrometheusLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.listdir', return_value=[constants.FILE_PATTERNS.LOG_SUFFIX])
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config', return_value=example_config)
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail', return_value="abcdef")
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_prometheus_logs(stub=grpc_stub)
        assert response.logs == ['abcdef']
        mocker.patch('os.path.exists', return_value=False)
        response = csle_cluster.cluster_manager.query_cluster_manager.get_prometheus_logs(stub=grpc_stub)
        assert response.logs == []

    def test_getDockerStatsManagerLogs(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config) -> None:
        """
        Tests the getDockerStatsManagerLogs grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.listdir', return_value=[constants.FILE_PATTERNS.LOG_SUFFIX])
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config',
                     return_value=example_config)
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerSuite.with_class())
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail', return_value="abcdef")
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_docker_statsmanager_logs(
            stub=grpc_stub)
        assert response.logs == ['abcdef']
        mocker.patch('os.path.exists', return_value=False)
        response = csle_cluster.cluster_manager.query_cluster_manager.get_docker_statsmanager_logs(
            stub=grpc_stub)
        assert response.logs == []

    def test_getCsleLogFiles(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config) -> None:
        """
        Tests the getCsleLogFiles grpc
        
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('os.listdir', return_value=['1', '2', '3', '4', '5', '6', '8', '9', '0', '8', '7',
                                                 '5', '4', '3', '2', '6', '8', '87', '6', '1', '2'])
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config',
                     return_value=example_config)
        mocker.patch('os.path.isfile', return_value=True)
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_csle_log_files(
            stub=grpc_stub)
        assert len(response.logs) == 20
        mocker.patch('os.listdir', return_value=['abcdef'])
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_csle_log_files(
            stub=grpc_stub)
        assert response.logs == [f"{example_config.default_log_dir}{constants.COMMANDS.SLASH_DELIM}abcdef"]
        mocker.patch('os.path.isfile', return_value=False)
        response: LogsDTO = csle_cluster.cluster_manager.query_cluster_manager.get_csle_log_files(
            stub=grpc_stub)
        assert response.logs == []

    def test_startContainersInExecution(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config,
                                        get_ex_exec) -> None:
        """
        Tests the startContainersInExecution grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController.run_containers",
                     return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.update_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager. \
            start_containers_in_execution(stub=grpc_stub,
                                          emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager. \
            start_containers_in_execution(stub=grpc_stub, emulation="JohnDoeEmulation",
                                          ip_first_octet=1)
        assert not response.outcome

    def test_attachContainersInExecutionToNetworks(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config,
                                                   get_ex_exec) -> None:
        """
        Tests the attachContainersInExecutionToNetworks grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.container_controller.ContainerController."
                     "connect_containers_to_networks", return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.update_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager. \
            attach_containers_in_execution_to_networks(stub=grpc_stub, emulation="JohnDoeEmulation",
                                                       ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager. \
            attach_containers_in_execution_to_networks(stub=grpc_stub,
                                                       emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_installLibraries(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the installLibraries grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "install_csle_collector_and_ryu_libraries", return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.install_libraries(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.install_libraries(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_applyKafkaConfig(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the applyKafkaConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip",
                     return_value="123.456.78.99")
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "apply_kafka_config", return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.apply_kafka_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.apply_kafka_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startSdnController(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec,
                                st_ryu) -> None:
        """
        Tests the startSdnController grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.start_ryu",
                     side_effect=st_ryu)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_sdn_controller(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_sdn_controller(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_applyResourceConstraints(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startSdnController grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.resource_constraints_controller.ResourceConstraintsController."
                     "apply_resource_constraints", return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.apply_resource_constraints(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.apply_resource_constraints(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_createOvsSwitches(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the createOvsSwitches grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.ovs_controller.OVSController."
                     "create_virtual_switches_on_container", return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.create_ovs_switches(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.create_ovs_switches(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_pingExecution(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the pingExecution grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController.ping_all",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.ping_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.ping_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_configureOvs(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the configureOvs grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.ovs_controller.OVSController.apply_ovs_config",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.configure_ovs(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.configure_ovs(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startSdnControllerMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startSdnControllerMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.start_ryu_monitor",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_sdn_controller_monitor(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_sdn_controller_monitor(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_createUsers(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the createUsers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.users_controller.UsersController.create_users",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.create_users(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.create_users(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_createVulnerabilities(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the createVulnerabilities grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.vulnerabilities_controller.VulnerabilitiesController.create_vulns",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.create_vulnerabilities(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.create_vulnerabilities(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_createFlags(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the createFlags grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.flags_controller.FlagsController.create_flags",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.create_flags(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.create_flags(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_createTopology(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the createTopology grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.topology_controller.TopologyController.create_topology",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.create_topology(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.create_topology(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startTrafficManagers(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startTrafficManagers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.start_traffic_managers",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_traffic_managers(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_traffic_managers(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startTrafficGenerators(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startTrafficGenerators grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.start_internal_traffic_generators",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_traffic_generators(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_traffic_generators(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startClientPopulation(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startClientPopulation grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.start_client_population",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_client_population(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_client_population(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startKafkaClientProducer(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startKafkaClientProducer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.start_client_producer",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_kafka_client_producer(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_kafka_client_producer(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopKafkaClientProducer(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the stopKafkaClientProducer grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.traffic_controller.TrafficController.stop_client_producer",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_kafka_client_producer(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_kafka_client_producer(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startSnortIdses(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startSnortIdses grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController.start_snort_idses",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_snort_idses(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_snort_idses(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startSnortIdsesMonitorThreads(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startSnortIdsesMonitorThreads grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
                     "start_snort_idses_monitor_threads", return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_snort_idses_monitor_threads(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_snort_idses_monitor_threads(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startOssecIdses(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startOssecIdses grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "start_ossec_idses", return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_ossec_idses(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_ossec_idses(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startOssecIdsesMonitorThreads(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startOssecIdsesMonitorThreads grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController."
                     "start_ossec_idses_monitor_threads", return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_ossec_idses_monitor_threads(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_ossec_idses_monitor_threads(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startElkStack(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startElkStack grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.elk_controller.ELKController.start_elk_stack",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_elk_stack(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_elk_stack(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startHostManagers(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startHostManagers grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.start_host_monitor_threads",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_host_managers(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_host_managers(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_applyFileBeatsConfig(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the applyFileBeatsConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.config_filebeats",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.apply_filebeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.apply_filebeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_applyPacketBeatsConfig(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the applyPacketBeatsConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.config_packetbeats",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.apply_packetbeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.apply_packetbeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_applyMetricBeatsConfig(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the applyMetricBeatsConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.config_metricbeats",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.apply_metricbeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.apply_metricbeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_applyHeartBeatsConfig(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the applyHeartBeatsConfig grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.config_heartbeats",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.apply_heartbeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.apply_heartbeats_config(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startFilebeats(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startFilebeats grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.start_filebeats",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_filebeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_filebeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startPacketbeats(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startPacketbeats grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.start_packetbeats",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_packetbeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_packetbeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startMetricbeats(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startMetricbeats grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.start_metricbeats",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_metricbeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_metricbeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startHeartbeats(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startHeartbeats grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.host_controller.HostController.start_heartbeats",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_heartbeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.start_heartbeats(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_startDockerStatsManagerThread(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the startDockerStatsManagerThread grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.container_controller.ContainerController.start_docker_stats_thread",
                     return_value=None)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_docker_statsmanager_thread(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.running
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: ServiceStatusDTO = csle_cluster.cluster_manager.query_cluster_manager.start_docker_statsmanager_thread(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.running

    def test_stopAllExecutionsOfEmulation(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_em_env) -> None:
        """
        Tests the stopAllExecutionsOfEmulation grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_by_name",
                     return_value=get_ex_em_env)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "stop_all_executions_of_emulation", return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_all_executions_of_emulation(
            stub=grpc_stub, emulation="JohnDoeEmulation")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_by_name",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_all_executions_of_emulation(
            stub=grpc_stub, emulation="JohnDoeEmulation")
        assert not response.outcome

    def test_stopExecution(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the stopExecution grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=get_ex_exec)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "stop_execution_of_emulation", return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome

    def test_stopAllExecutions(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec) -> None:
        """
        Tests the stopAllExecutions grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "stop_all_executions", return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.stop_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome

    def test_cleanAllExecutions(self, grpc_stub, mocker: pytest_mock.MockFixture, example_config) -> None:
        """
        Tests the cleanAllExecutions grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController."
                     "clean_all_executions", return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     return_value=example_config)
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.am_i_leader",
                     return_value=True)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.clean_all_executions(stub=grpc_stub)
        assert response.outcome
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.am_i_leader",
                     return_value=False)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.clean_all_executions(stub=grpc_stub)
        assert response.outcome

    def test_cleanAllExecutionsOfEmulation(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_em_env,
                                           example_config) -> None:
        """
        Tests the cleanAllExecutionsOfEmulation grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
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
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.clean_all_executions_of_emulation(
            stub=grpc_stub, emulation="JohnDoeEmulation")
        assert response.outcome
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.am_i_leader",
                     return_value=False)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.clean_all_executions_of_emulation(
            stub=grpc_stub, emulation="JohnDoeEmulation")
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_by_name",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.clean_all_executions_of_emulation(
                    stub=grpc_stub, emulation="JohnDoeEmulation")
        assert not response.outcome

    def test_cleanExecution(self, grpc_stub, mocker: pytest_mock.MockFixture, get_ex_exec, example_config) -> None:
        """
        Tests the cleanExecution grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
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
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.clean_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.util.cluster_util.ClusterUtil.am_i_leader",
                     return_value=False)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.clean_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert response.outcome
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     return_value=None)
        response: OperationOutcomeDTO = csle_cluster.cluster_manager.query_cluster_manager.clean_execution(
            stub=grpc_stub, emulation="JohnDoeEmulation", ip_first_octet=1)
        assert not response.outcome
