import csle_common.constants.constants as constants
import logging
from unittest.mock import MagicMock
from unittest.mock import patch
from csle_common.controllers.management_system_controller import (
    ManagementSystemController,
)
import subprocess


class TestManagementControllerSuite:
    """
    Test suite for management system controller
    """

    @patch("builtins.open")
    @patch("os.path.exists", return_value=True)
    def test_read_pid_file(self, mock_exists, mock_open) -> None:
        """
        Tests read_pid_file

        :param mock_exists: mock exists
        :param mock_open: mock open
        :return: None
        """
        path = "/path/to/pidfile"
        mock_file = mock_open.return_value
        mock_file.read.return_value = "1234"
        pid = ManagementSystemController.read_pid_file(path)
        assert pid == 1234
        mock_exists.assert_called_once_with(path)
        mock_open.assert_called_once_with(path, "r")

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.read_pid_file")
    def test_is_prometheus_running(self, mock_read_pid_file) -> None:
        """
        Tests the method that checks if prometheus is running on the host

        :param mock_read_pid_file: mock read_pid_file
        :return: None
        """
        mock_read_pid_file.return_value = -1
        assert not ManagementSystemController.is_prometheus_running()

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.read_pid_file")
    def test_is_node_exporter_running(self, mock_read_pid_file) -> None:
        """
        Tests the method that checks if node_exporter is running on the host

        :param mock_read_pid_file: mock read_pid_file
        :return: None
        """
        mock_read_pid_file.return_value = -1
        assert not ManagementSystemController.is_node_exporter_running()

    @patch("subprocess.run")
    def test_is_nginx_running(self, mock_run) -> None:
        """
        Tests the method that checks if Nginx is running on the host

        :param mock_run: mock run
        :return: None
        """
        constants.COMMANDS.NGINX_STATUS = "nginx status"
        mock_run.return_value = MagicMock(stdout="Active: active (running)")
        assert ManagementSystemController.is_nginx_running()
        mock_run.assert_called_once_with(["nginx", "status"], capture_output=True, text=True)

    @patch("subprocess.run")
    def test_is_postgresql_running(self, mock_run) -> None:
        """
        Tests the method that checks if postgresql is running on the host

        :param mock_run: mock run
        :return: None
        """
        constants.COMMANDS.POSTGRESQL_STATUS = "postgresql status"
        mock_run.return_value = MagicMock(stdout="Active: active (running)")
        assert ManagementSystemController.is_postgresql_running()
        mock_run.assert_called_once_with(["postgresql", "status"], capture_output=True, text=True)

    @patch("subprocess.run")
    def test_is_docker_engine_running(self, mock_run) -> None:
        """
        Tests the method that checks if Docker engine is running on the host

        :param mock_run: mock run
        :return: None
        """
        constants.COMMANDS.DOCKER_ENGINE_STATUS = "docker engine status"
        mock_run.return_value = MagicMock(stdout="Active: active (running)")
        assert ManagementSystemController.is_docker_engine_running()
        mock_run.assert_called_once_with(["docker", "engine", "status"], capture_output=True, text=True)

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.read_pid_file")
    def test_is_flask_running(self, mock_read_pid_file) -> None:
        """
        Tests the method that checks if flask web server is running on the host

        :param mock_run: mock run
        :return: None
        """
        mock_read_pid_file.return_value = -1
        assert not ManagementSystemController.is_flask_running()

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_node_exporter_running")
    @patch("subprocess.Popen")
    def test_start_node_exporter(self, mock_popen, mock_is_running) -> None:
        """
        Tests the method thats starts the node exporter

        :param mock_popen: mock popen
        :param mock_is_running: mock is_node_exporter_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = True
        result = ManagementSystemController.start_node_exporter(logger)
        assert not result
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("Node exporter is already running")
        mock_popen.assert_not_called()

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_flask_running")
    @patch("subprocess.Popen")
    def test_start_flask(self, mock_popen, mock_is_running) -> None:
        """
        Tests the method that starts Flask REST API Server

        :param mock_popen: mock popen
        :param mock_is_running: mock is_node_exporter_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = True
        result = ManagementSystemController.start_flask(logger)
        assert not result
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("Flask is already running")
        mock_popen.assert_not_called()

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_node_exporter_running")
    @patch("subprocess.Popen")
    def test_stop_node_exporter(self, mock_popen, mock_is_running) -> None:
        """
        Tests the method that stops the node exporter

        :param mock_popen: mock popen
        :param mock_is_running: mock is_node_exporter_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = False
        result = ManagementSystemController.stop_node_exporter(logger)
        assert not result
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("Node exporter is not running")
        mock_popen.assert_not_called()

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_flask_running")
    @patch("subprocess.Popen")
    def test_stop_flask(self, mock_popen, mock_is_running) -> None:
        """
        Tests the method that stops the flask REST API

        :param mock_popen: mock popen
        :param mock_is_running: mock is_flask_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = False
        result = ManagementSystemController.stop_flask(logger)
        assert not result
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("Flask is not running")
        mock_popen.assert_not_called()

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_prometheus_running")
    @patch("subprocess.Popen")
    def test_start_prometheus(self, mock_popen, mock_is_running) -> None:
        """
        Tests the method that starts Prometheus

        :param mock_popen: mock popen
        :param mock_is_running: mock is_prometheus_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = True
        result = ManagementSystemController.start_prometheus(logger)
        assert not result
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("Prometheus is already running")
        mock_popen.assert_not_called()

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_prometheus_running")
    @patch("subprocess.Popen")
    def test_stop_prometheus(self, mock_popen, mock_is_running) -> None:
        """
        Tests the method that stops Prometheus

        :param mock_popen: mock popen
        :param mock_is_running: mock is_prometheus_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = False
        result = ManagementSystemController.stop_prometheus(logger)
        assert not result
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("Prometheus is not running")
        mock_popen.assert_not_called()

    @patch("docker.from_env")
    def test_is_cadvisor_running(self, mock_from_env) -> None:
        """
        Tests if cadvisor is running

        :param mock_from_env: mock from_env
        :return: None
        """
        constants.CONTAINER_IMAGES = MagicMock()  # type: ignore
        constants.CONTAINER_IMAGES.CADVISOR = "name"
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.name = "name"
        mock_client.containers.list.return_value = [mock_container]
        assert ManagementSystemController.is_cadvisor_running()
        mock_from_env.assert_called_once()
        mock_client.containers.list.assert_called_once()

    @patch("docker.from_env")
    def test_is_pgadmin_running(self, mock_from_env) -> None:
        """
        Tests if Prometheus is running

        :param mock_from_env: mock from_env
        :return: None
        """
        constants.CONTAINER_IMAGES = MagicMock()  # type: ignore
        constants.CONTAINER_IMAGES.PGADMIN = "name"
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.name = "name"
        mock_client.containers.list.return_value = [mock_container]
        assert ManagementSystemController.is_pgadmin_running()
        mock_from_env.assert_called_once()
        mock_client.containers.list.assert_called_once()

    @patch("docker.from_env")
    def test_stop_cadvisor(self, mock_from_env) -> None:
        """
        Tests if cadvisor is stopped

        :param mock_from_env: mock from_env
        :return: None
        """
        constants.CONTAINER_IMAGES.CADVISOR = "name"
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.name = "name"
        mock_client.containers.list.return_value = [mock_container]
        assert ManagementSystemController.stop_cadvisor()
        mock_from_env.assert_called_once()
        mock_client.containers.list.assert_called_once()
        mock_container.stop.assert_called_once()

    @patch("docker.from_env")
    def test_stop_pgadmin(self, mock_from_env) -> None:
        """
        Tests if pgadmin is stopped

        :param mock_from_env: mock from_env
        :return: None
        """
        constants.CONTAINER_IMAGES.PGADMIN = "name"
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.name = "name"
        mock_client.containers.list.return_value = [mock_container]
        assert ManagementSystemController.stop_pgadmin()
        mock_from_env.assert_called_once()
        mock_client.containers.list.assert_called_once()
        mock_container.stop.assert_called_once()

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_cadvisor_running")
    def test_start_cadvisor(self, mock_is_running) -> None:
        """
        Tests if cadvisor starts

        :param mock_is_running: mock is_cadvisor_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = True
        result = ManagementSystemController.start_cadvisor(logger)
        assert not result
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("cAdvisor is already running")

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_postgresql_running")
    def test_start_postgresql(self, mock_is_running) -> None:
        """
        Tests if postgresql starts

        :param mock_is_running: mock is_postgresql_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = True
        result = ManagementSystemController.start_postgresql(logger)
        assert result == (False, None, None)
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("PostgreSQL is already running")

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_postgresql_running")
    def test_stop_postgresql(self, mock_is_running) -> None:
        """
        Tests if postgresql stopped

        :param mock_is_running: mock is_postgresql_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = False
        result = ManagementSystemController.stop_postgresql(logger)
        assert result == (False, None, None)
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("PostgreSQL is not running")

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_nginx_running")
    def test_start_nginx(self, mock_is_running) -> None:
        """
        Tests if Nginx starts

        :param mock_is_running: mock is_nginx_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = True
        result = ManagementSystemController.start_nginx(logger)
        assert result == (False, None, None)
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("Nginx is already running")

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_nginx_running")
    def test_stop_nginx(self, mock_is_running) -> None:
        """
        Tests if Nginx stops

        :param mock_is_running: mock is_nginx_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = False
        result = ManagementSystemController.stop_nginx(logger)
        assert result == (False, None, None)
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("Nginx is not running")

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_docker_engine_running")
    def test_start_docker_engine(self, mock_is_running) -> None:
        """
        Tests if Docker engine starts

        :param mock_is_running: mock is_docker_engine_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = True
        result = ManagementSystemController.start_docker_engine(logger)
        assert result == (False, None, None)
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("The Docker engine is already running")

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_docker_engine_running")
    def test_stop_docker_engine(self, mock_is_running) -> None:
        """
        Tests if Docker engine stops

        :param mock_is_running: mock is_docker_engine_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = False
        result = ManagementSystemController.stop_docker_engine(logger)
        assert result == (False, None, None)
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("The Docker engine is not running")

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_pgadmin_running")
    def test_start_pgadmin(self, mock_is_running) -> None:
        """
        Tests if pgadmin starts

        :param mock_is_running: mock is_pgadmin_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = True
        result = ManagementSystemController.start_pgadmin(logger)
        assert not result
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("pgAdmin is already running")

    @patch("docker.from_env")
    def test_stop_grafana(self, mock_from_env) -> None:
        """
        Tests if grafana stops

        :param mock_from_env: mock from_env
        :return: None
        """
        constants.CONTAINER_IMAGES.GRAFANA = "name"
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.name = "name"
        mock_client.containers.list.return_value = [mock_container]
        assert ManagementSystemController.stop_grafana()
        mock_from_env.assert_called_once()
        mock_client.containers.list.assert_called_once()
        mock_container.stop.assert_called_once()

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_grafana_running")
    def test_start_grafana(self, mock_is_running) -> None:
        """
        Tests if grafana starts

        :param mock_is_running: mock is_grafana_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = True
        result = ManagementSystemController.start_grafana(logger)
        assert not result
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("Grafana is already running")

    @patch("docker.from_env")
    def test_is_grafana_running(self, mock_from_env) -> None:
        """
        Tests if grafana is running

        :param mock_from_env: mock from_env
        :return: None
        """
        constants.CONTAINER_IMAGES.GRAFANA = "name"
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_container = MagicMock()
        mock_container.name = "name"
        mock_client.containers.list.return_value = [mock_container]
        assert ManagementSystemController.is_grafana_running()
        mock_from_env.assert_called_once()
        mock_client.containers.list.assert_called_once()

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.read_pid_file")
    def test_is_statsmanager_running(self, mock_read_pid_file) -> None:
        """
        Tests the method that checks if statsmanager is running on the host

        :param mock_read_pid_file: mock read_pid_file
        :return: None
        """
        mock_read_pid_file.return_value = -1
        assert not ManagementSystemController.is_statsmanager_running()

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_statsmanager_running")
    def test_start_docker_statsmanager(self, mock_is_running) -> None:
        """
        Tests the method that checks if docker statsmanager is running on the host

        :param mock_is_running: mock is_statsmanager_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = True
        result = ManagementSystemController.start_docker_statsmanager(
            logger=logger,
            log_file="docker_stats_manager.log",
            log_dir="/var/log/csle",
            max_workers=10,
            port=50046,
        )
        assert not result
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("The docker statsmanager is already running")

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_statsmanager_running")
    def test_stop_docker_statsmanager(self, mock_is_running) -> None:
        """
        Tests the method that stops docker statsmanager

        :param mock_is_running: mock is_statsmanager_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = False
        result = ManagementSystemController.stop_docker_statsmanager(logger=logger)
        assert not result
        mock_is_running.assert_called_once()
        logger.info.assert_called_with("The statsmanager is not running")

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.read_pid_file")
    @patch("subprocess.Popen")
    def test_stop_cluster_manager(self, mock_popen, mock_read_pid_file) -> None:
        """
        Tests the method that stops the local cluster manager

        :param mock_read_pid_file: mock read_pid_file
        :return: None
        """
        mock_read_pid_file.return_value = 1234
        mock_popen.return_value.communicate.return_value = (None, None)
        result = ManagementSystemController.stop_cluster_manager()
        assert result
        mock_read_pid_file.assert_called_once_with(constants.COMMANDS.CLUSTER_MANAGER_PIDFILE)
        mock_popen.assert_called_once_with(constants.COMMANDS.KILL_PROCESS.format(1234), stdout=subprocess.DEVNULL,
                                           shell=True)
        mock_popen.return_value.communicate.assert_called_once()

    @patch("psutil.pid_exists")
    def test_is_pid_running(self, mock_pid_exists) -> None:
        """
        Tests the method that checks if the given pid is running on the host

        :param mock_pid_exists: mock pid_exists

        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_pid_exists.return_value = True
        pid = 1234
        result = ManagementSystemController.is_pid_running(pid, logger)
        assert result
        logger.info.assert_called_once_with(f"Checking if PID: {pid} is running")
        mock_pid_exists.assert_called_once_with(pid)

    @patch("csle_common.controllers.management_system_controller.ManagementSystemController.is_pid_running")
    def test_stop_pid(self, mock_is_running) -> None:
        """
        Tests the method that stops a process with a given pid

        :param mock_is_running: mock is_pid_running
        :return: None
        """
        logger = MagicMock(spec=logging.Logger)
        mock_is_running.return_value = False
        pid = 1234
        result = ManagementSystemController.stop_pid(pid, logger)
        assert not result
        logger.info.assert_not_called()
