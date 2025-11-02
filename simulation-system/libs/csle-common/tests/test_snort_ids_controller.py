from unittest.mock import patch, MagicMock
import csle_common.constants.constants as constants
import pytest
from csle_common.controllers.snort_ids_controller import SnortIDSController


class TestSnortIdsControllerSuite:
    """
    Test snort_ids_controller
    """

    @pytest.fixture(autouse=True)
    def emulation_env_config_setup(self) -> None:
        """
        Set up emulation environment configuration

        :return: None
        """
        logger = MagicMock()
        constants.CONTAINER_IMAGES.SNORT_IDS_IMAGES = ["container1", "container2"]
        container1 = MagicMock()
        container1.name = "container1"
        container1.physical_host_ip = "192.168.1.1"
        container1.docker_gw_bridge_ip = "10.0.0.1"
        container1.get_ips.return_value = ["10.0.1.1"]
        container1.get_full_name.return_value = "container-1"
        container2 = MagicMock()
        container2.name = "container2"
        container2.physical_host_ip = "192.168.1.2"
        container2.docker_gw_bridge_ip = "10.0.0.2"
        container2.get_ips.return_value = ["10.0.1.2"]
        container2.get_full_name.return_value = "container-2"
        containers = [container1, container2]
        emulation_env_config = MagicMock()
        emulation_env_config.containers_config.containers = containers
        emulation_env_config.snort_ids_manager_config.snort_ids_manager_port = 50051
        emulation_env_config.execution_id = "12345"
        emulation_env_config.level = "1"
        self.emulation_env_config = emulation_env_config
        self.logger = logger

    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.start_snort_ids")
    def test_start_snort_idses(self, mock_start_snort_ids) -> None:
        """
        Test utility function for starting the Snort IDSes

        :param mock_start_snort_ides: mock_start_snort_ides
        :return: None
        """
        SnortIDSController.start_snort_idses(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=self.emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        self.logger.info.assert_called_once_with(
            f"Starting the Snort IDS on IP: "
            f"{self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip} ("
            f"{self.emulation_env_config.containers_config.containers[0].get_ips()[0]}, "
            f"{self.emulation_env_config.containers_config.containers[0].get_full_name()})")
        mock_start_snort_ids.assert_called_once_with(
            emulation_env_config=self.emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)

    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.stop_snort_ids")
    def test_stop_snort_ides(self, mock_stop_snort_ids) -> None:
        """
        Test utility function for stopping the Snort IDSes

        :param mock_start_snort_ides: mock_start_snort_ides
        :return: None
        """
        SnortIDSController.stop_snort_idses(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=self.emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_stop_snort_ids.assert_called_once_with(
            emulation_env_config=self.emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)

    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.start_snort_manager")
    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
           "get_snort_idses_monitor_threads_statuses_by_ip_and_port")
    @patch("csle_collector.snort_ids_manager.query_snort_ids_manager.start_snort_ids")
    @patch("grpc.insecure_channel")
    def test_start_snort_ids(self, mock_insecure_channel, mock_start_snort_ids, mock_get_statuses, mock_start_manager) \
            -> None:
        """
        Test utility function for starting the Snort IDS on a specific IP

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_start_snort_ids: mock_start_snort_ids
        :param mock_get_statuses: mock_get_statuses
        :param mock_start_manager: mock_start_manager
        :return: None
        """
        mock_get_statuses.return_value.snort_ids_running = False
        constants.CSLE.CSLE_LEVEL_SUBNETMASK_SUFFIX = ".0/24"
        constants.NETWORKING.ETH2 = "eth2"
        constants.NETWORKING.ETH0 = "eth0"
        constants.GRPC_SERVERS.GRPC_OPTIONS = []
        mock_channel = MagicMock()
        mock_insecure_channel.return_value = mock_channel
        mock_stub = MagicMock()
        mock_channel.__enter__.return_value = mock_stub
        SnortIDSController.start_snort_ids(
            emulation_env_config=self.emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)
        mock_start_manager.assert_called_once_with(
            emulation_env_config=self.emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)
        self.logger.info.assert_any_call(
            f"Snort IDS is not running on "
            f"{self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip}, starting it.")
        mock_insecure_channel.assert_called()
        mock_start_snort_ids.assert_called()

    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.start_snort_manager")
    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
           "get_snort_idses_monitor_threads_statuses_by_ip_and_port")
    @patch("csle_collector.snort_ids_manager.query_snort_ids_manager.stop_snort_ids")
    @patch("grpc.insecure_channel")
    def test_stop_snort_ids(self, mock_insecure_channel, mock_stop_snort_ids, mock_get_statuses,
                            mock_start_manager) -> None:
        """
        Test utility function for stopping the Snort IDS on a specific IP


        :param mock_insecure_channel: mock_insecure_channel
        :param mock_start_snort_ids: mock_start_snort_ids
        :param mock_get_statuses: mock_get_statuse
        :param mock_start_manager: mock_start_manager
        :return: None
        """
        mock_get_statuses.return_value.snort_ids_running = True
        mock_channel = MagicMock()
        mock_insecure_channel.return_value = mock_channel
        mock_stub = MagicMock()
        mock_channel.__enter__.return_value = mock_stub
        SnortIDSController.stop_snort_ids(
            emulation_env_config=self.emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        mock_start_manager.assert_called_once_with(
            emulation_env_config=self.emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        self.logger.info.assert_any_call(
            f"Snort IDS is running on {self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip}, "
            f"stopping it.")
        mock_insecure_channel.assert_called()
        mock_stop_snort_ids.assert_called()

    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.start_snort_manager")
    @patch("time.sleep", return_value=None)
    def test_start_snort_managers(self, mock_sleep, mock_start_manager) -> None:
        """
        Test utility function for starting snort IDS managers

        :param mock_start_manager: mock_start_manager
        :param mock_sleep: mock_sleep
        :return: None
        """
        SnortIDSController.start_snort_managers(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=self.emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_start_manager.assert_called()

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_start_snort_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test utility function for starting the snort IDS manager on a specific IP

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :param mock_sleep: mock_sleep
        :return: None
        """
        emulation_env_config = self.emulation_env_config
        emulation_env_config.snort_ids_manager_config.snort_ids_manager_port = 50051
        emulation_env_config.snort_ids_manager_config.snort_ids_manager_log_dir = "/var/log/snort"
        emulation_env_config.snort_ids_manager_config.snort_ids_manager_log_file = "snort.log"
        emulation_env_config.snort_ids_manager_config.snort_ids_manager_max_workers = 4

        mock_connection = MagicMock()
        emulation_env_config.get_connection.return_value = mock_connection
        mock_execute_ssh_cmd.side_effect = [
            (b"", b"", 0),  # Output for checking if ids_manager is running (not running)
            (b"", b"", 0),  # Output for stopping old background job
            (b"", b"", 0),  # Output for starting the ids_manager
        ]
        SnortIDSController.start_snort_manager(
            emulation_env_config=emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        mock_connect_admin.assert_called_once_with(
            emulation_env_config=emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip)
        mock_execute_ssh_cmd.assert_called()
        self.logger.info.assert_any_call(
            f"Starting Snort IDS manager on node "
            f"{self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip}")

    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.stop_snort_manager")
    @patch("time.sleep", return_value=None)
    def test_stop_snort_managers(self, mock_sleep, mock_stop_manager) -> None:
        """
        Test Utility function for stopping snort IDS managers

        :param mock_start_manager: mock_start_manager
        :param mock_sleep: mock_sleep
        :return: None
        """
        SnortIDSController.stop_snort_managers(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=self.emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_stop_manager.assert_called()

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_stop_snort_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test utility function for stopping the snort IDS manager on a specific IP

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :param mock_sleep: mock_sleep
        :return: None
        """
        emulation_env_config = self.emulation_env_config
        mock_connection = MagicMock()
        emulation_env_config.get_connection.return_value = mock_connection
        mock_execute_ssh_cmd.return_value = (b"", b"", 0)
        SnortIDSController.stop_snort_manager(
            emulation_env_config=emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        mock_connect_admin.assert_called_once_with(
            emulation_env_config=emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip)
        mock_execute_ssh_cmd.assert_called()
        self.logger.info.assert_any_call(
            f"Stopping Snort IDS manager on node "
            f"{self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip}")

    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.start_snort_idses_monitor_thread")
    def test_start_snort_idses_monitor_threads(self, mock_start_monitor_thread) -> None:
        """
        Test a method that sends a request to the SnortIDSManager on every container that runs
        an IDS to start the IDS manager and the monitor thread

        :param mock_start_monitor_thread: mock_start_monitor_thread
        :return: None
        """
        SnortIDSController.start_snort_idses_monitor_threads(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=self.emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_start_monitor_thread.assert_called_once_with(
            emulation_env_config=self.emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        self.logger.info.assert_called_once_with(
            f"Starting Snort IDS monitor thread on IP: "
            f"{self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip} "
            f"({self.emulation_env_config.containers_config.containers[0].get_ips()[0]}, "
            f"{self.emulation_env_config.containers_config.containers[0].get_full_name()})")

    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.start_snort_manager")
    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
           "get_snort_idses_monitor_threads_statuses_by_ip_and_port")
    @patch("csle_collector.snort_ids_manager.query_snort_ids_manager.start_snort_ids_monitor")
    @patch("grpc.insecure_channel")
    def test_start_snort_idses_monitor_thread(self, mock_insecure_channel, mock_start_monitor, mock_get_statuses,
                                              mock_start_manager) -> None:
        """
        Test a method that sends a request to the SnortIDSManager on a specific container that runs
        an IDS to start the IDS manager and the monitor thread

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_start_monitor: mock_start_monitor
        :param mock_get_statuses: mock_get_statuses
        :param mock_start_manager: mock_start_manager
        :return: None
        """
        emulation_env_config = self.emulation_env_config
        emulation_env_config.snort_ids_manager_config.snort_ids_manager_port = 50051
        emulation_env_config.kafka_config.container.get_ips.return_value = ["127.0.0.1"]
        emulation_env_config.kafka_config.kafka_port = 9092
        emulation_env_config.snort_ids_manager_config.time_step_len_seconds = 60
        mock_get_statuses.return_value.monitor_running = False
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        SnortIDSController.start_snort_idses_monitor_thread(
            emulation_env_config=emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        mock_start_manager.assert_called_once_with(
            emulation_env_config=emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        mock_get_statuses.assert_called_once_with(
            port=50051, ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip)
        self.logger.info.assert_called_once_with(
            f"Snort IDS monitor thread is not running on "
            f"{self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip}, starting it.")
        mock_insecure_channel.assert_called_once_with(
            f"{self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip}:50051",
            options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_start_monitor.assert_called()

    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.stop_snort_idses_monitor_thread")
    def test_stop_snort_idses_monitor_threadas(self, mock_stop_monitor_thread) -> None:
        """
        Test a method that sends a request to the SnortIDSManager on every container that runs
        an IDS to stop the monitor threads

        :param mock_stop_monitor_thread: mock_stop_monitor_thread
        :return: None
        """
        SnortIDSController.stop_snort_idses_monitor_threads(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=self.emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_stop_monitor_thread.assert_called_once_with(
            emulation_env_config=self.emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)

    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.start_snort_manager")
    @patch("csle_collector.snort_ids_manager.query_snort_ids_manager.stop_snort_ids_monitor")
    @patch("grpc.insecure_channel")
    def test_stop_snort_idses_monitor_thread(self, mock_insecure_channel, mock_stop_monitor, mock_start_manager):
        """
        Test a method that sends a request to the SnortIDSManager on a specific container that runs
        an IDS to stop the monitor threads

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_stop_monitor: mock_stop_monitor
        :param mock_start_manager: mock_start_manager
        :return: None
        """
        emulation_env_config = self.emulation_env_config
        emulation_env_config.snort_ids_manager_config.snort_ids_manager_port = 50051
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        SnortIDSController.stop_snort_idses_monitor_thread(
            emulation_env_config=emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        mock_start_manager.assert_called_once_with(
            emulation_env_config=emulation_env_config,
            ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        self.logger.info.assert_called_once_with(
            "Stopping the Snort IDS monitor thread on "
            f"{self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip}.")
        mock_insecure_channel.assert_called_once_with(
            f"{self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip}:50051",
            options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_stop_monitor.assert_called()

    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.start_snort_managers")
    @patch(
        "csle_common.controllers.snort_ids_controller.SnortIDSController."
        "get_snort_idses_monitor_threads_statuses_by_ip_and_port"
    )
    def test_get_snort_idses_monitor_threads_statuses(self, mock_get_statuses, mock_start_managers) -> None:
        """
        Test a method that sends a request to the SnortIDSManager on every container to get the status of the
        IDS monitor thread

        :param mock_get_statuses: mock_get_statuses
        :param mock_start_managers: mock_start_managers
        :return: None
        """
        emulation_env_config = self.emulation_env_config
        emulation_env_config.snort_ids_manager_config.snort_ids_manager_port = 50051
        mock_status = MagicMock()
        mock_get_statuses.return_value = mock_status
        statuses = SnortIDSController.get_snort_idses_monitor_threads_statuses(
            emulation_env_config=emulation_env_config,
            physical_server_ip=self.emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger, start_if_stopped=True)
        mock_start_managers.assert_called_once_with(
            emulation_env_config=emulation_env_config,
            physical_server_ip=self.emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_get_statuses.assert_called_once_with(
            port=50051, ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip)
        assert statuses == [mock_status]

    @patch("grpc.insecure_channel")
    @patch("csle_collector.snort_ids_manager.query_snort_ids_manager.get_snort_ids_monitor_status")
    def test_get_snort_idses_monitor_threads_statuses_by_ip_and_port(self, mock_get_status, mock_insecure_channel) \
            -> None:
        """
        Test a method that sends a request to the SnortIDSManager with a specific port and ip
        to get the status of the IDS monitor thread

        :param mock_get_status: mock_get_status
        :param mock_insecure_channel: mock_insecure_channel
        :return: None
        """
        mock_status = MagicMock()
        mock_get_status.return_value = mock_status
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        port = 50051
        ip = self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip
        status = SnortIDSController.get_snort_idses_monitor_threads_statuses_by_ip_and_port(port=port, ip=ip)
        mock_insecure_channel.assert_called_once_with(f"{ip}:{port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        assert status == mock_status

    def test_get_snort_ids_managers_ips(self) -> None:
        """
        Test a method that extracts the IPs of the snort IDS managers in a given emulation
        """
        ips = SnortIDSController.get_snort_ids_managers_ips(emulation_env_config=self.emulation_env_config)
        expected_ips = [self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
                        self.emulation_env_config.containers_config.containers[1].docker_gw_bridge_ip]
        assert ips == expected_ips

    def test_get_snort_idses_managers_ports(self) -> None:
        """
        Test a method that extracts the ports of the snort IDS managers in a given emulation
        """
        ports = SnortIDSController.get_snort_idses_managers_ports(emulation_env_config=self.emulation_env_config)
        expected_ports = [50051, 50051]
        assert ports == expected_ports

    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.get_snort_ids_managers_ips")
    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController.get_snort_idses_managers_ports")
    @patch("csle_common.controllers.snort_ids_controller.SnortIDSController."
           "get_snort_idses_monitor_threads_statuses_by_ip_and_port")
    @patch("csle_common.util.emulation_util.EmulationUtil.physical_ip_match")
    @patch("csle_collector.snort_ids_manager.snort_ids_manager_util.SnortIdsManagerUtil.snort_ids_monitor_dto_empty")
    def test_get_snort_managers_info(
            self, mock_snort_ids_monitor_dto_empty, mock_physical_ip_match, mock_get_statuses, mock_get_ports,
            mock_get_ips) -> None:
        """
        Test the method that extracts the information of the Snort managers for a given emulation

        :param mock_snort_ids_monitor_dto_empty: mock_snort_ids_monitor_dto_empty
        :param mock_physical_ip_match: mock_physical_ip_match
        :param mock_get_statuses: mock_get_statuses
        :param mock_get_ports:mock_get_ports
        :param mock_get_ips: mock_get_ips
        :return: None
        """
        mock_get_ips.return_value = [self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
                                     self.emulation_env_config.containers_config.containers[1].docker_gw_bridge_ip]
        mock_get_ports.return_value = [50051, 50052]
        mock_status = MagicMock()
        mock_get_statuses.side_effect = [mock_status, Exception("Test exception")]
        mock_physical_ip_match.side_effect = [True, False]
        mock_empty_dto = MagicMock()
        mock_snort_ids_monitor_dto_empty.return_value = mock_empty_dto
        emulation_env_config = self.emulation_env_config
        emulation_env_config.snort_ids_manager_config.snort_ids_manager_port = 50051
        emulation_env_config.execution_id = "test_execution_id"
        emulation_env_config.name = "test_emulation_name"
        active_ips = [self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip]
        physical_server_ip = self.emulation_env_config.containers_config.containers[0].physical_server_ip
        SnortIDSController.get_snort_managers_info(emulation_env_config=emulation_env_config, active_ips=active_ips,
                                                   logger=self.logger, physical_server_ip=physical_server_ip)
        mock_get_ips.assert_called_once_with(emulation_env_config=emulation_env_config)
        mock_get_ports.assert_called_once_with(emulation_env_config=emulation_env_config)
        mock_get_statuses.assert_any_call(
            port=50051, ip=self.emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip)
