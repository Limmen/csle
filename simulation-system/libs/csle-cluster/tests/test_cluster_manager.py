from typing import Any
import pytest
import pytest_mock
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
    