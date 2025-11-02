from unittest.mock import patch, MagicMock
import csle_common.constants.constants as constants
from csle_common.controllers.sdn_controller_manager import SDNControllerManager
import csle_collector.ryu_manager.ryu_manager_pb2 as ryu_manager_pb2
import csle_collector.ryu_manager.ryu_manager_pb2_grpc as ryu_manager_pb2_grpc


class TestSDNControllerSuite:
    """
    Test SDNControllerManager
    """

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_start_ryu_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test method for starting the Ryu manager

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :param mock_sleep: mock_sleep
        :return: None
        """
        logger = MagicMock()
        sdn_controller_config = MagicMock(
            container=MagicMock(docker_gw_bridge_ip="192.168.1.2"), manager_port=6633, manager_log_dir="/var/log/ryu",
            manager_log_file="ryu.log", manager_max_workers=4)
        emulation_env_config = MagicMock(sdn_controller_config=sdn_controller_config, name="Test Emulation")
        mock_execute_ssh_cmd.side_effect = [
            (b"", b"", 0),  # output of cp /etc/sudoers.bak /etc/sudoers
            (b"", b"", 0),  # output of adding CVE entry to sudoers
            (b"", b"", 0),  # output of chmod 440 /etc/sudoers
        ]
        SDNControllerManager.start_ryu_manager(emulation_env_config, logger)
        mock_connect_admin.assert_any_call(emulation_env_config=emulation_env_config, ip="192.168.1.2",
                                           create_producer=False)
        mock_execute_ssh_cmd.assert_called()

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_stop_ryu_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test method for stopping the Ryu manager

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :param mock_sleep: mock_sleep
        :return: None
        """
        logger = MagicMock()
        sdn_controller_config = MagicMock(container=MagicMock(docker_gw_bridge_ip="192.168.1.2"))
        emulation_env_config = MagicMock(sdn_controller_config=sdn_controller_config, name="Test Emulation")
        mock_execute_ssh_cmd.side_effect = [(b"", b"", 0)]  # output of pkill ryu_manager
        SDNControllerManager.stop_ryu_manager(emulation_env_config, logger)
        mock_connect_admin.assert_any_call(emulation_env_config=emulation_env_config, ip="192.168.1.2",
                                           create_producer=False)
        mock_execute_ssh_cmd.assert_called()

    @patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.start_ryu_manager")
    @patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.get_ryu_status_by_port_and_ip")
    def test_get_ryu_status(self, mock_get_ryu_status_by_port_and_ip, mock_get_ryu_manager) -> None:
        """
        Test method for querying the RyuManager about the status of the Ryu SDN controller

        :param mock_get_ryu_status_by_port_and_ip: mock_get_ryu_status_by_port_and_ip
        :param mock_get_ryu_manager: mock_get_ryu_manager
        :return: None
        """
        logger = MagicMock()
        ryu_dto_mock = MagicMock(spec=ryu_manager_pb2.RyuDTO)
        mock_get_ryu_status_by_port_and_ip.return_value = ryu_dto_mock
        sdn_controller_config = MagicMock(container=MagicMock(docker_gw_bridge_ip="192.168.1.2"), manager_port=6633)
        emulation_env_config = MagicMock(sdn_controller_config=sdn_controller_config, name="Test Emulation")
        result = SDNControllerManager.get_ryu_status(emulation_env_config=emulation_env_config, logger=logger)
        assert result == ryu_dto_mock
        mock_get_ryu_manager.assert_called()
        mock_get_ryu_status_by_port_and_ip.assert_called()

    @patch("grpc.insecure_channel")
    @patch("csle_collector.ryu_manager.query_ryu_manager.get_ryu_status")
    def test_get_ryu_status_by_port_and_ip(self, mock_get_ryu_status, mock_insecure_channel) -> None:
        """
        Test method for querying the RyuManager about the status of the Ryu SDN controller

        :param mock_get_ryu_status: mock_get_ryu_status
        :param mock_insecure_channel: mock_insecure_channel
        :return: None
        """
        ryu_dto_mock = MagicMock(spec=ryu_manager_pb2.RyuDTO)
        mock_get_ryu_status.return_value = ryu_dto_mock
        channel_mock = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = channel_mock
        ip = "192.168.1.2"
        port = 6633
        result = SDNControllerManager.get_ryu_status_by_port_and_ip(ip, port)
        mock_insecure_channel.assert_called_once_with(f"{ip}:{port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_get_ryu_status.assert_called_once()
        assert isinstance(mock_get_ryu_status.call_args[0][0], ryu_manager_pb2_grpc.RyuManagerStub)
        assert result == ryu_dto_mock

    @patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.start_ryu_manager")
    @patch("grpc.insecure_channel")
    @patch("csle_collector.ryu_manager.query_ryu_manager.stop_ryu")
    @patch("time.sleep", return_value=None)
    def test_stop_ryu(self, mock_sleep, mock_stop_ryu, mock_insecure_channel, mock_start_manager) -> None:
        """
        Test method for requesting the RyuManager to stop the RYU SDN controller

        :param mock_stop_ryu: mock_stop_ryu
        :param mock_insecure_channel: mock_insecure_channel
        :param mock_start_manager: mock_start_manager
        :param mock_sleep: mock_sleep
        :return: None
        """
        logger = MagicMock()
        ryu_dto_mock = MagicMock(spec=ryu_manager_pb2.RyuDTO)
        mock_stop_ryu.return_value = ryu_dto_mock
        channel_mock = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = channel_mock
        sdn_controller_config = MagicMock(container=MagicMock(docker_gw_bridge_ip="192.168.1.2"), manager_port=6633)
        emulation_env_config = MagicMock(sdn_controller_config=sdn_controller_config, name="Test Emulation")
        ip = "192.168.1.2"
        port = 6633
        result = SDNControllerManager.stop_ryu(emulation_env_config=emulation_env_config, logger=logger)
        mock_insecure_channel.assert_called_once_with(f"{ip}:{port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_stop_ryu.assert_called_once()
        assert isinstance(mock_stop_ryu.call_args[0][0], ryu_manager_pb2_grpc.RyuManagerStub)
        assert result == ryu_dto_mock

    @patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.start_ryu_manager")
    @patch("grpc.insecure_channel")
    @patch("csle_collector.ryu_manager.query_ryu_manager.start_ryu")
    @patch("time.sleep", return_value=None)
    def test_start_ryu(self, mock_sleep, mock_start_ryu, mock_insecure_channel, mock_start_manager) -> None:
        """
        Test method for requesting the RyuManager to start the RYU SDN controller

        :param mock_start_ryu: mock_start_ryu
        :param mock_insecure_channel: mock_insecure_channel
        :param mock_start_manager: mock_start_manager
        :param mock_sleep: mock_sleep
        :return: None
        """
        logger = MagicMock()
        ryu_dto_mock = MagicMock(spec=ryu_manager_pb2.RyuDTO)
        mock_start_ryu.return_value = ryu_dto_mock
        channel_mock = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = channel_mock
        sdn_controller_config = MagicMock(
            container=MagicMock(docker_gw_bridge_ip="192.168.1.2", physical_host_ip="192.168.1.1"),
            manager_port=6633,
            controller_port=6653,
            controller_web_api_port=8080,
            controller_module_name="controller_module",
        )
        emulation_env_config = MagicMock(sdn_controller_config=sdn_controller_config, name="Test Emulation")
        ip = "192.168.1.1"

        result = SDNControllerManager.start_ryu(emulation_env_config=emulation_env_config, physical_server_ip=ip,
                                                logger=logger)
        mock_insecure_channel.assert_called_once_with("192.168.1.2:6633", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_start_ryu.assert_called_once()
        assert isinstance(mock_start_ryu.call_args[0][0], ryu_manager_pb2_grpc.RyuManagerStub)
        assert result == ryu_dto_mock

    @patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.start_ryu_manager")
    @patch("grpc.insecure_channel")
    @patch("csle_collector.ryu_manager.query_ryu_manager.start_ryu_monitor")
    def test_start_ryu_monitor(self, mock_start_ryu_monitor, mock_insecure_channel, mock_start_manager) -> None:
        """
        Test method for requesting the RyuManager to start the Ryu monitor

        :param mock_start_ryu_monitor: mock_start_ryu_monitor
        :param mock_insecure_channel: mock_insecure_channel
        :param mock_start_manager: mock_start_manager
        :return: None
        """
        logger = MagicMock()
        ryu_dto_mock = MagicMock(spec=ryu_manager_pb2.RyuDTO)
        mock_start_ryu_monitor.return_value = ryu_dto_mock
        channel_mock = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = channel_mock
        sdn_controller_config = MagicMock(
            container=MagicMock(docker_gw_bridge_ip="192.168.1.2", physical_host_ip="192.168.1.1"),
            manager_port=6633, time_step_len_seconds=10)
        kafka_config = MagicMock(container=MagicMock(get_ips=MagicMock(return_value=["192.168.1.3"])), kafka_port=9092)
        emulation_env_config = MagicMock(sdn_controller_config=sdn_controller_config, kafka_config=kafka_config,
                                         name="Test Emulation")
        ip = "192.168.1.1"
        result = SDNControllerManager.start_ryu_monitor(emulation_env_config=emulation_env_config,
                                                        physical_server_ip=ip, logger=logger)
        mock_insecure_channel.assert_called_once_with("192.168.1.2:6633", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_start_ryu_monitor.assert_called_once()
        assert isinstance(mock_start_ryu_monitor.call_args[0][0], ryu_manager_pb2_grpc.RyuManagerStub)
        assert result == ryu_dto_mock

    @patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.start_ryu_manager")
    @patch("grpc.insecure_channel")
    @patch("csle_collector.ryu_manager.query_ryu_manager.stop_ryu_monitor")
    def test_stop_ryu_monitor(self, mock_stop_ryu_monitor, mock_insecure_channel, mock_start_manager) -> None:
        """
        Test method for requesting the RyuManager to stop the Ryu monitor

        :param mock_stop_ryu_monitor: mock_stop_ryu_monitor
        :param mock_insecure_channel: mock_insecure_channel
        :param mock_start_manager: mock_start_manager
        :return: None
        """
        logger = MagicMock()
        ryu_dto_mock = MagicMock(spec=ryu_manager_pb2.RyuDTO)
        mock_stop_ryu_monitor.return_value = ryu_dto_mock
        channel_mock = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = channel_mock
        sdn_controller_config = MagicMock(
            container=MagicMock(docker_gw_bridge_ip="192.168.1.2", physical_host_ip="192.168.1.1"), manager_port=6633)
        emulation_env_config = MagicMock(sdn_controller_config=sdn_controller_config, name="Test Emulation")
        result = SDNControllerManager.stop_ryu_monitor(emulation_env_config=emulation_env_config, logger=logger)
        mock_insecure_channel.assert_called_once_with("192.168.1.2:6633", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_stop_ryu_monitor.assert_called_once()
        assert isinstance(mock_stop_ryu_monitor.call_args[0][0], ryu_manager_pb2_grpc.RyuManagerStub)
        assert result == ryu_dto_mock

    def test_get_ryu_managers_ips(self) -> None:
        """
        Test method that extracts the IPS of the Ryu managers in a given emulation

        :return: None
        """
        sdn_controller_config = MagicMock(container=MagicMock(docker_gw_bridge_ip="192.168.1.2"))
        emulation_env_config = MagicMock(sdn_controller_config=sdn_controller_config, name="Test Emulation")
        result = SDNControllerManager.get_ryu_managers_ips(emulation_env_config)
        assert result == ["192.168.1.2"]

    def test_get_ryu_managers_ports(self) -> None:
        """
        Test method that extracts the ports of the Ryu managers in a given emulation

        :return: None
        """
        sdn_controller_config = MagicMock(manager_port=6633)
        emulation_env_config = MagicMock(sdn_controller_config=sdn_controller_config, name="Test Emulation")
        result = SDNControllerManager.get_ryu_managers_ports(emulation_env_config)
        assert result == [6633]

    @patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.get_ryu_managers_ips")
    @patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.get_ryu_managers_ports")
    @patch("csle_common.controllers.sdn_controller_manager.SDNControllerManager.get_ryu_status_by_port_and_ip")
    @patch("csle_common.util.emulation_util.EmulationUtil.physical_ip_match")
    @patch("csle_collector.ryu_manager.ryu_manager_util.RyuManagerUtil.ryu_dto_empty", return_value=MagicMock())
    def test_get_ryu_managers_info(self, mock_ryu_dto_empty, mock_physical_ip_match, mock_get_ryu_status_by_port_and_ip,
                                   mock_get_ryu_managers_ports, mock_get_ryu_managers_ips) -> None:
        """
        Test method that extracts the information of the Ryu managers for a given emulation

        :param mock_ryu_dto_empty: mock_ryu_dto_empty
        :param mock_physical_ip_match: mock_physical_ip_match
        :param mock_get_ryu_status_by_port_and_ip: mock_get_ryu_status_by_port_and_ip
        :param mock_get_ryu_managers_ports: mock_get_ryu_managers_ports
        :param mock_get_ryu_managers_ips: mock_get_ryu_managers_ips
        :return: None
        """
        logger = MagicMock()
        sdn_controller_config = MagicMock(
            container=MagicMock(docker_gw_bridge_ip="192.168.1.2", physical_host_ip="192.168.1.1"), manager_port=6633)
        emulation_env_config = MagicMock(sdn_controller_config=sdn_controller_config, execution_id="123",
                                         name="Test Emulation")
        mock_get_ryu_managers_ips.return_value = ["192.168.1.2"]
        mock_get_ryu_managers_ports.return_value = [6633]
        mock_physical_ip_match.return_value = True
        mock_get_ryu_status_by_port_and_ip.return_value = MagicMock()

        active_ips = ["192.168.1.2"]
        physical_server_ip = "192.168.1.1"

        result = SDNControllerManager.get_ryu_managers_info(emulation_env_config, active_ips, logger,
                                                            physical_server_ip)
        mock_get_ryu_managers_ips.assert_called_once_with(emulation_env_config=emulation_env_config)
        mock_get_ryu_managers_ports.assert_called_once_with(emulation_env_config=emulation_env_config)
        mock_physical_ip_match.assert_called_once_with(emulation_env_config=emulation_env_config,
                                                       ip="192.168.1.2", physical_host_ip="192.168.1.1")
        mock_get_ryu_status_by_port_and_ip.assert_called_once_with(port=6633, ip="192.168.1.2")
        assert result
