import pytest
import logging
import csle_common.constants.constants as constants
from unittest.mock import patch, MagicMock
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.controllers.ossec_ids_controller import OSSECIDSController


class TestOssecIdsSuite:
    """
    Test suite for ossec_ids_controller
    """

    @pytest.fixture(autouse=True)
    def emulation_env_config_setup(self) -> None:
        """
        Set up emulation environment configuration

        :return: None
        """
        # setup container configurations
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        container1 = MagicMock()
        container1.physical_host_ip = "192.168.1.10"
        container1.docker_gw_bridge_ip = "172.17.0.1"
        container1.get_ips.return_value = ["172.18.0.1"]
        container1.get_full_name.return_value = "container-1"
        container1.name = "container-1"
        container2 = MagicMock()
        container2.physical_host_ip = "192.168.1.10"
        container2.docker_gw_bridge_ip = "172.17.0.2"
        container2.name = "container-2"
        container1.get_ips.return_value = ["172.18.0.2"]
        container1.get_full_name.return_value = "container-2"
        container3 = MagicMock()
        container3.physical_host_ip = "192.168.1.11"
        container3.docker_gw_bridge_ip = "172.17.0.3"
        container3.name = "container-3"
        containers_config = MagicMock()
        emulation_env_config.containers_config = containers_config
        emulation_env_config.containers_config.containers = [container1, container2, container3]
        ossec_ids_manager_config = MagicMock()
        emulation_env_config.ossec_ids_manager_config = ossec_ids_manager_config
        emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port = 1515
        self.emulation_env_config = emulation_env_config
        self.logger = MagicMock(spec=logging.Logger)

    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.stop_ossec_ids")
    def test_stop_ossec_idses(self, mock_stop_ossec_ids) -> None:
        """
        Test the method for stopping the OSSEC IDSes

        :param mock_stop_ossec_ids: mock stop_ossec_ids
        :return: None
        """
        constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES = [
            self.emulation_env_config.containers_config.containers[0].name,
            self.emulation_env_config.containers_config.containers[1].name
        ]
        physical_host_ip = self.emulation_env_config.containers_config.containers[0].physical_host_ip
        OSSECIDSController.stop_ossec_idses(emulation_env_config=self.emulation_env_config,
                                            physical_host_ip=physical_host_ip)
        assert mock_stop_ossec_ids.call_count == 2

    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.start_ossec_ids")
    def test_start_ossec_idses(self, mock_start_ossec_ids) -> None:
        """
        Test the method for starting the OSSEC IDSes

        :param mock_start_ossec_ids: mock start_ossec_ids
        :return: None
        """
        constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES = [
            self.emulation_env_config.containers_config.containers[0].name,
            self.emulation_env_config.containers_config.containers[1].name
        ]
        physical_server_ip = self.emulation_env_config.containers_config.containers[0].physical_host_ip
        OSSECIDSController.start_ossec_idses(
            emulation_env_config=self.emulation_env_config, physical_server_ip=physical_server_ip, logger=self.logger)
        for i in [0, 1]:
            self.logger.info.assert_any_call(
                f"Starting the OSSEC IDS on ip: "
                f"{self.emulation_env_config.containers_config.containers[i].docker_gw_bridge_ip} "
                f"({self.emulation_env_config.containers_config.containers[i].get_ips()[0]}, "
                f"{self.emulation_env_config.containers_config.containers[i].get_full_name()})")
        assert mock_start_ossec_ids.call_count == 2

    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.start_ossec_ids_manager")
    @patch(
        "csle_common.controllers.ossec_ids_controller.OSSECIDSController"
        ".get_ossec_ids_monitor_thread_status_by_ip_and_port"
    )
    @patch("grpc.insecure_channel")
    @patch("csle_common.controllers.ossec_ids_controller.Logger")
    def test_start_ossec_ids(
            self, mock_logger, mock_insecure_channel, mock_get_monitor_status, mock_start_manager) -> None:
        """
        Test the method for starting a OSSEC IDS with a specific IP

        :param mock_logger: mock logger
        :param mock_insecure_channel: mock insecure_channel
        :param mock_get_monitor_status: mock get_monitor_status
        :param mock_start_manager: mock start_manager
        :return: None
        """
        mock_get_monitor_status.return_value.ossec_ids_running = False
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        ip = "192.168.1.10"
        OSSECIDSController.start_ossec_ids(emulation_env_config=self.emulation_env_config, ip=ip)
        mock_start_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ip)
        mock_get_monitor_status.assert_called_once_with(port=1515, ip=ip)
        mock_insecure_channel.assert_called_once_with(f"{ip}:1515", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_logger.__call__().get_logger().info.assert_called_once_with(f"Starting OSSEC IDS on {ip}.")

    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.start_ossec_ids_manager")
    @patch(
        "csle_common.controllers.ossec_ids_controller.OSSECIDSController"
        ".get_ossec_ids_monitor_thread_status_by_ip_and_port"
    )
    @patch("grpc.insecure_channel")
    def test_stop_ossec_ids(self, mock_insecure_channel, mock_get_monitor_status, mock_start_manager) -> None:
        """
        Test the method for stopping a OSSEC IDS with a specific IP

        :param mock_insecure_channel: mock insecure_channel
        :param mock_get_monitor_status: mock get_monitor_status
        :param mock_start_manager: mock start_manager
        :return: None
        """
        mock_get_monitor_status.return_value.ossec_ids_running = True
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        ip = "192.168.1.10"
        OSSECIDSController.start_ossec_ids(emulation_env_config=self.emulation_env_config, ip=ip)
        mock_start_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ip)
        mock_get_monitor_status.assert_called_once_with(port=1515, ip=ip)

    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.start_ossec_ids_manager")
    def test_start_ossec_idses_managers(self, mock_start_manager) -> None:
        """
        Test the method for starting OSSEC IDS managers

        :param mock_start_manager: mock start_manager
        :return: None
        """
        constants.CONTAINER_IMAGES = MagicMock()  # type: ignore
        constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES = [
            self.emulation_env_config.containers_config.containers[0].name,
            self.emulation_env_config.containers_config.containers[1].name
        ]
        physical_server_ip = self.emulation_env_config.containers_config.containers[0].physical_host_ip
        OSSECIDSController.start_ossec_idses_managers(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip)
        assert mock_start_manager.call_count == 2

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_start_ossec_ids_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test method for starting the OSSEC IDS manager on a specific container

        :param mock_execute_ssh_cmd: mock execute_ssh_cmd
        :param mock_connect_admin: mock connect_admin
        :param mock_sleep: mock sleep
        :return: None
        """
        ip = "192.168.1.10"
        mock_execute_ssh_cmd.return_value = ("ossec_ids_manager running", "", 0)
        constants.COMMANDS.SEARCH_OSSEC_IDS_MANAGER = "ossec_ids_manager running"
        OSSECIDSController.start_ossec_ids_manager(emulation_env_config=self.emulation_env_config, ip=ip)
        mock_execute_ssh_cmd.assert_called()
        mock_connect_admin.assert_called()

    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.stop_ossec_ids_manager")
    @patch("time.sleep", return_value=None)
    def test_stop_ossec_idses_managers(self, mock_sleep, mock_stop_manager) -> None:
        """
        Test method for stopping ossec ids managers

        :param mock_stop_manager: mock stop_manager
        :param mock_sleep: mock sleep
        :return: None
        """
        constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES = [
            self.emulation_env_config.containers_config.containers[0].name,
            self.emulation_env_config.containers_config.containers[1].name
        ]
        physical_server_ip = self.emulation_env_config.containers_config.containers[0].physical_host_ip
        OSSECIDSController.stop_ossec_idses_managers(emulation_env_config=self.emulation_env_config,
                                                     physical_server_ip=physical_server_ip)
        assert mock_stop_manager.call_count == 2

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_stop_ossec_ids_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test method for stopping the OSSEC IDS manager on a specific container

        :param mock_execute_ssh_cmd: mock execute_ssh_cmd
        :param mock_connect_admin: mock connect_admin
        :param mock_sleep: mock sleep
        :return: None
        """
        ip = "192.168.1.10"
        mock_execute_ssh_cmd.return_value = ("ossec_ids_manager running", "", 0)
        OSSECIDSController.stop_ossec_ids_manager(emulation_env_config=self.emulation_env_config, ip=ip)
        mock_execute_ssh_cmd.assert_called()
        mock_connect_admin.assert_called()

    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.start_ossec_idses_managers")
    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.start_ossec_ids_monitor_thread")
    def test_start_ossec_idses_monitor_threads(self, mock_start_monitor, mock_start_managers) -> None:
        """
        Unit test for the start_ossec_ids_monnitor_threads method of the OSSEC IDS controller

        :param mock_start_monitor: mock of the start_monitor method
        :param mock_start_managers: mock of the start_managers method
        :return: None
        """
        constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES = ["container-1", "container-2"]
        physical_server_ip = "192.168.1.10"
        OSSECIDSController.start_ossec_idses_monitor_threads(emulation_env_config=self.emulation_env_config,
                                                             physical_server_ip=physical_server_ip,
                                                             logger=self.logger)
        mock_start_managers.assert_called_once_with(emulation_env_config=self.emulation_env_config,
                                                    physical_server_ip=physical_server_ip)
        assert mock_start_monitor.call_count == 2

    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.start_ossec_ids_manager")
    @patch(
        "csle_common.controllers.ossec_ids_controller.OSSECIDSController"
        ".get_ossec_ids_monitor_thread_status_by_ip_and_port"
    )
    @patch("grpc.insecure_channel")
    def test_start_ossec_ids_monitor_thread(self, mock_insecure_channel, mock_get_monitor_status, mock_start_manager) \
            -> None:
        """
        A method that sends a request to the OSSECIDSManager on a specific IP to start
        the IDS manager and the monitor thread

        :param mock_insecure_channel: mock insecure_channel
        :param mock_get_monitor_status: mock get_monitor_status
        :param mock_start_manager:  mock start_manager
        :return: None
        """
        mock_get_monitor_status.return_value.ossec_ids_running = False
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        ip = "192.168.1.10"
        OSSECIDSController.start_ossec_ids_monitor_thread(emulation_env_config=self.emulation_env_config, ip=ip)
        mock_start_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ip)
        mock_get_monitor_status.assert_called_once_with(port=1515, ip=ip)

    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.stop_ossec_ids_monitor_thread")
    def test_stop_ossec_ids_monitor_threads(self, mock_stop_monitor) -> None:
        """
        Test a method that sends a request to the OSSECIDSManager on every container that runs
        an IDS to stop the monitor threads

        :param mock_stop_monitor: _description_
        :return: None
        """
        constants.CONTAINER_IMAGES = MagicMock()  # type: ignore
        constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES = ["container-1", "container-2"]
        physical_server_ip = "192.168.1.10"
        OSSECIDSController.stop_ossec_idses_monitor_threads(
            emulation_env_config=self.emulation_env_config, physical_server_ip=physical_server_ip)
        assert mock_stop_monitor.call_count == 2

    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.start_ossec_ids_manager")
    @patch("grpc.insecure_channel")
    def test_stop_ossec_ids_monitor_thread(self, mock_insecure_channel, mock_start_manager) -> None:
        """
        Test a method that sends a request to the OSSECIDSManager for a specific IP to stop the monitor thread

        :param mock_start_manager: mock start_manager
        :param mock_insecure_channel: mock of the channel
        :return: None
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        ip = "192.168.1.10"
        OSSECIDSController.stop_ossec_ids_monitor_thread(emulation_env_config=self.emulation_env_config, ip=ip)
        mock_start_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ip)

    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.start_ossec_idses_managers")
    @patch("grpc.insecure_channel")
    def test_get_ossec_idses_monitor_threads_statuses(self, mock_insecure_channel, mock_start_managers) -> None:
        """
        Test a method that sends a request to the OSSECIDSManager on every container to get the status of the
        IDS monitor thread

        :param mock_start_manager: mock start_manager
        :param mock_insecure_channel: mock of the channel
        :return: None
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        physical_server_ip = "192.168.1.10"
        constants.CONTAINER_IMAGES = MagicMock()  # type: ignore
        constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES = ["container-1", "container-2"]
        OSSECIDSController.get_ossec_idses_monitor_threads_statuses(
            emulation_env_config=self.emulation_env_config, physical_server_ip=physical_server_ip)
        mock_start_managers.assert_called_once_with(
            emulation_env_config=self.emulation_env_config, physical_server_ip=physical_server_ip)

    def test_get_ossec_idses_managers_ips(self) -> None:
        """
        Tests a method that extracts the IPS of the OSSEC IDS managers in a given emulation

        :return: None
        """
        constants.CONTAINER_IMAGES = MagicMock()  # type: ignore
        constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES = ["container-1", "container-2"]
        ips = OSSECIDSController.get_ossec_idses_managers_ips(emulation_env_config=self.emulation_env_config)
        assert ips == ["172.17.0.1", "172.17.0.2"]

    def test_get_ossec_idses_managers_ports(self) -> None:
        """
        Tests a method that extracts the ports of the OSSEC IDS managers in a given emulation

        :return: None
        """
        constants.CONTAINER_IMAGES = MagicMock()  # type: ignore
        constants.CONTAINER_IMAGES.OSSEC_IDS_IMAGES = ["container-1", "container-2"]
        ports = OSSECIDSController.get_ossec_idses_managers_ports(emulation_env_config=self.emulation_env_config)
        assert ports == [1515, 1515]

    @patch("grpc.insecure_channel")
    def test_get_ossec_ids_monitor_thread_status_by_ip_and_port(self, mock_insecure_channel) -> None:
        """
        Tests a method that sends a request to the OSSECIDSManager with a specific port and ip
        to get the status of the IDS monitor thread

        :param mock_insecure_channel: mock insecure_channel
        :return: None
        """
        port = 1515
        ip = "192.168.1.100"
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        OSSECIDSController.get_ossec_ids_monitor_thread_status_by_ip_and_port(port=port, ip=ip)
        mock_insecure_channel.assert_called_once_with(f"{ip}:{port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS)

    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.get_ossec_idses_managers_ips")
    @patch("csle_common.controllers.ossec_ids_controller.OSSECIDSController.get_ossec_idses_managers_ports")
    @patch(
        "csle_common.controllers.ossec_ids_controller.OSSECIDSController"
        ".get_ossec_ids_monitor_thread_status_by_ip_and_port"
    )
    @patch("csle_common.util.emulation_util.EmulationUtil.physical_ip_match")
    @patch("csle_collector.ossec_ids_manager.ossec_ids_manager_util.OSSecManagerUtil.ossec_ids_monitor_dto_empty")
    def test_get_ossec_managers_info(
            self, mock_ossec_dto_empty, mock_physical_ip_match, mock_get_status, mock_get_ports, mock_get_ips) -> None:
        """
        Tests the method that extracts the information of the OSSEC IDS managers for a given emulation

        :param mock_ossec_dto_empty: mock ossec_dto_empty
        :param mock_physical_ip_match: mock physical_ip_match
        :param mock_get_status: mock get_status
        :param mock_get_ports: mock get_ports
        :param mock_get_ips: mock get_ips
        :retun: None
        """
        emulation_env_config = self.emulation_env_config
        emulation_env_config.execution_id = "test_execution_id"
        emulation_env_config.name = "test_emulation_name"
        emulation_env_config.ossec_ids_manager_config.ossec_ids_manager_port = 1515
        active_ips = ["192.168.1.10", "192.168.1.11"]
        physical_host_ip = "192.168.1.1"
        logger = self.logger
        mock_get_ips.return_value = ["192.168.1.10", "192.168.1.12"]
        mock_get_ports.return_value = [1515, 1515]
        mock_status_1 = MagicMock()
        mock_get_status.side_effect = [mock_status_1, Exception("Test Exception")]
        mock_physical_ip_match.side_effect = [True, True]
        mock_ossec_dto_empty.return_value = MagicMock()
        OSSECIDSController.get_ossec_managers_info(emulation_env_config, active_ips, logger, physical_host_ip)
        mock_get_ips.assert_called_once_with(emulation_env_config=emulation_env_config)
        mock_get_ports.assert_called_once_with(emulation_env_config=emulation_env_config)
        assert mock_get_status.call_count == 1
