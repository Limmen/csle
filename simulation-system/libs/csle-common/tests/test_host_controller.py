import logging
import pytest
import csle_common.constants.constants as constants
from unittest.mock import MagicMock, patch
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.controllers.host_controller import HostController


class TestHostControllerSuite:
    """
    Test suite for host controller
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
        container1.name = "spark-container-1"
        container1.get_ips.return_value = ["192.168.1.2"]
        container1.get_full_name.return_value = "container_name"

        container2 = MagicMock()
        container2.physical_host_ip = "192.168.1.11"
        container2.docker_gw_bridge_ip = "172.17.0.2"
        container2.name = "spark-container-2"
        containers_config = MagicMock()
        emulation_env_config.containers_config = containers_config
        emulation_env_config.containers_config.containers = [container1, container2]
        # setup kafka container
        kafka_container = MagicMock()
        kafka_container.physical_host_ip = "192.168.1.10"
        kafka_container.docker_gw_bridge_ip = "172.17.0.3"
        kafka_config = MagicMock()
        emulation_env_config.kafka_config = kafka_config
        emulation_env_config.kafka_config.container = kafka_container
        emulation_env_config.kafka_config.container.get_ips.return_value = ["192.168.1.2"]
        emulation_env_config.kafka_config.kafka_port = 9092
        emulation_env_config.kafka_config.time_step_len_seconds = 10
        emulation_env_config.kafka_config.topics = [MagicMock(name="topic1"), MagicMock(name="topic2")]
        # setup ELK configuration
        elk_container = MagicMock()
        elk_container.physical_host_ip = "192.168.1.10"
        elk_container.docker_gw_bridge_ip = "172.17.0.4"
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container = elk_container
        emulation_env_config.elk_config.container.get_ips.return_value = ["192.168.1.3"]
        emulation_env_config.elk_config.kibana_port = 5601
        emulation_env_config.elk_config.elastic_port = 9200
        # setup SDN controller configuration
        sdn_container = MagicMock()
        sdn_container.physical_host_ip = "192.168.1.11"
        sdn_container.docker_gw_bridge_ip = "172.17.0.5"
        sdn_controller_config = MagicMock()
        emulation_env_config.sdn_controller_config = sdn_controller_config
        emulation_env_config.sdn_controller_config.container = sdn_container
        # setup host_manager configuration
        host_manager_config = MagicMock()
        emulation_env_config.host_manager_config = host_manager_config
        emulation_env_config.host_manager_config.host_manager_port = 12345
        # setup base_config
        beats_config = MagicMock()
        emulation_env_config.beats_config = beats_config
        emulation_env_config.beats_config.num_elastic_shards = 5
        emulation_env_config.beats_config.reload_enabled = True
        # setup node_beats_config
        node_beats_config = MagicMock()
        node_beats_config.log_files_paths = ["/var/log/syslog"]
        node_beats_config.filebeat_modules = ["system"]
        node_beats_config.kafka_input = True
        emulation_env_config.beats_config.get_node_beats_config_by_ips.return_value = (node_beats_config)
        emulation_env_config.execution_id = "execution_id"
        emulation_env_config.name = "emulation_name"
        self.emulation_env_config = emulation_env_config
        self.logger = MagicMock(spec=logging.Logger)

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    def test_start_host_managers(self, mock_start_host_manager) -> None:
        """
        Test start_host_managers

        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        HostController.start_host_managers(self.emulation_env_config, self.logger)
        mock_start_host_manager.assert_called()
        assert mock_start_host_manager.call_count == 5

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_start_host_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test start_host_manager

        :param mock_sleep: mock sleep
        :param mock_execute_ssh_cmd: mock execute_ssh_cmd
        :param mock_connect_admin: mock connect_admin
        :return: None
        """
        mock_connect_admin.return_value = None
        mock_execute_ssh_cmd.return_value = ("output", "error", 0)
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        emulation_env_config.get_connection.return_value = MagicMock()
        host_manager_config = MagicMock()
        emulation_env_config.host_manager_config = host_manager_config
        emulation_env_config.host_manager_config.host_manager_port = 8080
        emulation_env_config.host_manager_config.host_manager_log_dir = ("/var/log/host_manager")
        emulation_env_config.host_manager_config.host_manager_log_file = ("host_manager.log")
        emulation_env_config.host_manager_config.host_manager_max_workers = 4
        logger = MagicMock(spec=logging.Logger)
        ip = "172.17.0.1"
        HostController.start_host_manager(emulation_env_config, ip, logger)
        mock_connect_admin.assert_called_once_with(emulation_env_config=emulation_env_config, ip=ip)
        mock_sleep.assert_called_once_with(5)

    @patch("csle_common.controllers.host_controller.HostController.stop_host_manager")
    def test_stop_host_managers(self, mock_stop_host_manager) -> None:
        """
        Test stop_host_managers

        :param mock_stop_host_manager: mock stop_host_manager
        :return: None
        """
        physical_host_ip = "192.168.1.10"
        HostController.stop_host_managers(self.emulation_env_config, physical_host_ip)
        mock_stop_host_manager.assert_called()
        assert mock_stop_host_manager.call_count == 3
        mock_stop_host_manager.reset_mock()
        physical_host_ip = "192.168.1.11"
        HostController.stop_host_managers(self.emulation_env_config, physical_host_ip)
        assert mock_stop_host_manager.call_count == 2

    @patch("csle_common.controllers.host_controller.EmulationUtil.connect_admin")
    @patch("csle_common.controllers.host_controller.Logger.__call__")
    @patch("csle_common.controllers.host_controller.EmulationUtil.execute_ssh_cmd")
    def test_stop_host_manager(self, mock_execute_ssh_cmd, mock_logger, mock_connect_admin) -> None:
        """
        Test stop_host_manager method

        :param mock_execute_ssh_cmd: mock execute_ssh_cmd
        :param mock_logger: mock logger
        :param mock_connect_admin: mock connect_admin
        :return: None
        """
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        mock_get_logger = mock_logger_instance.get_logger()
        mock_execute_ssh_cmd.return_value = ("output", "error", 0)
        ip = "172.17.0.2"
        HostController.stop_host_manager(emulation_env_config=self.emulation_env_config, ip=ip)
        mock_connect_admin.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ip)
        mock_get_logger.info.assert_called_once_with(f"Stopping host manager on node {ip}")
        expected_cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
                        constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.HOST_MANAGER_FILE_NAME)
        mock_execute_ssh_cmd.assert_called_once_with(cmd=expected_cmd,
                                                     conn=self.emulation_env_config.get_connection(ip))

    @patch("csle_common.controllers.host_controller.HostController.start_host_monitor_thread")
    def test_start_host_monitor_threads(self, mock_start_host_monitor_thread) -> None:
        """
        Test start_host_monitor_threads method

        :param mock_start_host_monitor_threads: mock start_host_monitor_threads
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.start_host_monitor_threads(
            emulation_env_config=self.emulation_env_config, physical_server_ip=physical_server_ip, logger=self.logger)
        assert mock_start_host_monitor_thread.call_count == 3
        mock_start_host_monitor_thread.reset_mock()
        physical_server_ip = "192.168.1.11"
        HostController.start_host_monitor_threads(emulation_env_config=self.emulation_env_config,
                                                  physical_server_ip=physical_server_ip, logger=self.logger)
        assert mock_start_host_monitor_thread.call_count == 2

    @patch("csle_common.controllers.host_controller.HostController.start_filebeat")
    def test_start_filebeats(self, mock_start_filebeat) -> None:
        """
        Test start_filebeats method

        :param mock_start_filebeat: mock start_filebeat
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.start_filebeats(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip,
            logger=self.logger,
            initial_start=True,
        )
        assert mock_start_filebeat.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.start_packetbeat")
    def test_start_packetbeats(self, mock_start_packetbeat) -> None:
        """
        Test start_packetbeats method

        :param mock_start_packetbeat: mock start_packetbeat
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.start_packetbeats(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip,
            logger=self.logger,
            initial_start=True,
        )
        assert mock_start_packetbeat.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.start_metricbeat")
    def test_start_metricbeats(self, mock_start_metricbeat) -> None:
        """
        Test start_metricbeats method

        :param mock_start_metricbeat: mock start_metricbeat
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.start_metricbeats(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip,
            logger=self.logger,
            initial_start=True,
        )
        assert mock_start_metricbeat.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.start_heartbeat")
    def test_start_heartbeats(self, mock_start_heartbeat) -> None:
        """
        Test start_heartbeats method

        :param mock_start_heartbeat: mock start_heartbeat
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.start_heartbeats(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip,
            logger=self.logger,
            initial_start=True,
        )
        assert mock_start_heartbeat.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.stop_filebeat")
    def test_stop_filebeats(self, mock_stop_filebeat) -> None:
        """
        Test stop_filebeats method

        :param mock_stop_filebeat: mock stop_filebeat
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.stop_filebeats(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip,
            logger=self.logger,
        )
        assert mock_stop_filebeat.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.stop_packetbeat")
    def test_stop_packetbeats(self, mock_stop_packetbeat) -> None:
        """
        Test stop_packetbeats method

        :param mock_stop_packetbeat: mock stop_packetbeat
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.stop_packetbeats(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip,
            logger=self.logger,
        )
        assert mock_stop_packetbeat.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.stop_metricbeat")
    def test_stop_metricbeats(self, mock_stop_metricbeat) -> None:
        """
        Test stop_metricbeats method

        :param mock_stop_metricbeat: mock stop_metricbeat
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.stop_metricbeats(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip,
            logger=self.logger,
        )
        assert mock_stop_metricbeat.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.stop_heartbeat")
    def test_stop_heartbeats(self, mock_stop_heartbeat) -> None:
        """
        Test stop_heartbeats method

        :param mock_stop_heartbeat: mock stop_heartbeat
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.stop_heartbeats(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip,
            logger=self.logger,
        )
        assert mock_stop_heartbeat.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.config_filebeat")
    def test_config_filebeats(self, mock_config_filebeat) -> None:
        """
        Test config_filebeats method

        :param mock_config_filebeat: mock config_filebeat
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.config_filebeats(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip,
            logger=self.logger,
        )
        assert mock_config_filebeat.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.config_packetbeat")
    def test_config_packetbeats(self, mock_config_packetbeat) -> None:
        """
        Test config_packetbeats method
        :param mock_config_packetbeat: mock config_packetbeat
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.config_packetbeats(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip,
            logger=self.logger,
        )
        assert mock_config_packetbeat.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.config_metricbeat")
    def test_config_metricbeats(self, mock_config_metricbeat) -> None:
        """
        Test config_metricbeats method

        :param mock_config_metricbeat: mock config_metricbeat
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.config_metricbeats(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip,
            logger=self.logger,
        )
        assert mock_config_metricbeat.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.config_heartbeat")
    def test_config_heartbeats(self, mock_config_heartbeat) -> None:
        """
        Test config_heartbeats method

        :param mock_config_heartbeat: mock config_heartbeat
        :return: None
        """
        physical_server_ip = "192.168.1.10"
        HostController.config_heartbeats(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=physical_server_ip,
            logger=self.logger,
        )
        assert mock_config_heartbeat.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.HostController.get_host_monitor_thread_status_by_port_and_ip")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.start_host_monitor")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_start_host_monitor_thread(
            self, mock_HostManagerStub, mock_start_host_monitor, mock_insecure_channel,
            mock_get_host_monitor_thread_status, mock_start_host_manager) -> None:
        """
        Test start_host_monitor_thread method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_start_host_monitor_thread: mock start_host_monitor_thread
        :param mock_insecure_channel: mock insecure_channel
        :param mock_get_host_monitor_thread_status: mock get_host_monitor_thread_status
        :param mock_start_host_manager: mock start_host_manager

        :return: None
        """
        # Mock the host_monitor_dto to return monitor_running as False
        host_monitor_dto = MagicMock()
        host_monitor_dto.monitor_running = False
        mock_get_host_monitor_thread_status.return_value = host_monitor_dto
        # Mock the gRPC channel and stub
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ip = "172.17.0.2"
        HostController.start_host_monitor_thread(emulation_env_config=self.emulation_env_config, ip=ip,
                                                 logger=self.logger)
        mock_start_host_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ip,
                                                        logger=self.logger)
        mock_get_host_monitor_thread_status.assert_called_once_with(ip=ip, port=12345)
        self.logger.info.assert_called_once_with(f"Host monitor thread is not running on {ip}, starting it.")
        mock_insecure_channel.assert_called_once_with(f"{ip}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_start_host_monitor.assert_called_once_with(
            stub=mock_stub,
            kafka_ip="192.168.1.2",
            kafka_port=9092,
            time_step_len_seconds=10,
        )

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.HostController.get_host_monitor_thread_status_by_port_and_ip")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.start_filebeat")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_start_filebeat(
            self, mock_HostManagerStub, mock_start_filebeat, mock_insecure_channel, mock_get_host_monitor_thread_status,
            mock_start_host_manager) -> None:
        """
        Test start_filebeat method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_start_filebeat: mock start_filebeat
        :param mock_insecure_channel: mock insecure_channel
        :param mock_get_host_monitor_thread_status: mock get_host_monitor_thread_status
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        beats_config = MagicMock()
        self.emulation_env_config.beats_config = beats_config
        self.emulation_env_config.beats_config.get_node_beats_config_by_ips.return_value = MagicMock(
            start_filebeat_automatically=True)
        host_monitor_dto = MagicMock()
        host_monitor_dto.filebeat_running = False
        mock_get_host_monitor_thread_status.return_value = host_monitor_dto
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ips = ["172.17.0.2", "192.168.1.2"]
        HostController.start_filebeat(emulation_env_config=self.emulation_env_config, ips=ips, logger=self.logger,
                                      initial_start=True)
        mock_start_host_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ips[0],
                                                        logger=self.logger)
        self.emulation_env_config.beats_config.get_node_beats_config_by_ips.assert_called_once_with(ips=ips)
        mock_get_host_monitor_thread_status.assert_called_once_with(ip=ips[0], port=12345)
        self.logger.info.assert_called_once_with(f"Filebeat is not running on {ips[0]}, starting it.")
        mock_insecure_channel.assert_called_once_with(f"{ips[0]}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_start_filebeat.assert_called_once_with(stub=mock_stub)

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.HostController.get_host_monitor_thread_status_by_port_and_ip")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.start_packetbeat")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_start_packetbeat(
            self, mock_HostManagerStub, mock_start_packetbeat, mock_insecure_channel,
            mock_get_host_monitor_thread_status,
            mock_start_host_manager) -> None:
        """
        Test start_packetbeat method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_start_packetbeat: mock start_packetbeat
        :param mock_insecure_channel: mock insecure_channel
        :param mock_get_host_monitor_thread_status: mock get_host_monitor_thread_status
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        beats_config = MagicMock()
        self.emulation_env_config.beats_config = beats_config
        self.emulation_env_config.beats_config.get_node_beats_config_by_ips.return_value = MagicMock(
            start_packetbeat_automatically=True)
        host_monitor_dto = MagicMock()
        host_monitor_dto.packetbeat_running = False
        mock_get_host_monitor_thread_status.return_value = host_monitor_dto
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ips = ["172.17.0.2", "192.168.1.2"]
        HostController.start_packetbeat(emulation_env_config=self.emulation_env_config, ips=ips, logger=self.logger,
                                        initial_start=True)
        mock_start_host_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ips[0],
                                                        logger=self.logger)
        self.emulation_env_config.beats_config.get_node_beats_config_by_ips.assert_called_once_with(ips=ips)
        mock_get_host_monitor_thread_status.assert_called_once_with(ip=ips[0], port=12345)
        self.logger.info.assert_called_once_with(f"Packetbeat is not running on {ips[0]}, starting it.")
        mock_insecure_channel.assert_called_once_with(f"{ips[0]}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_start_packetbeat.assert_called_once_with(stub=mock_stub)

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.HostController.get_host_monitor_thread_status_by_port_and_ip")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.start_metricbeat")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_start_metricbeat(
            self, mock_HostManagerStub, mock_start_metricbeat, mock_insecure_channel,
            mock_get_host_monitor_thread_status,
            mock_start_host_manager) -> None:
        """
        Test start_metricbeat method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_start_metricbeat: mock start_metricbeat
        :param mock_insecure_channel: mock insecure_channel
        :param mock_get_host_monitor_thread_status: mock get_host_monitor_thread_status
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        beats_config = MagicMock()
        self.emulation_env_config.beats_config = beats_config
        self.emulation_env_config.beats_config.get_node_beats_config_by_ips.return_value = MagicMock(
            start_metricbeat_automatically=True)
        host_monitor_dto = MagicMock()
        host_monitor_dto.metricbeat_running = False
        mock_get_host_monitor_thread_status.return_value = host_monitor_dto
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ips = ["172.17.0.2", "192.168.1.2"]
        HostController.start_metricbeat(emulation_env_config=self.emulation_env_config, ips=ips, logger=self.logger,
                                        initial_start=True)
        mock_start_host_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ips[0],
                                                        logger=self.logger)
        self.emulation_env_config.beats_config.get_node_beats_config_by_ips.assert_called_once_with(ips=ips)
        mock_get_host_monitor_thread_status.assert_called_once_with(ip=ips[0], port=12345)
        self.logger.info.assert_called_once_with(f"Metricbeat is not running on {ips[0]}, starting it.")
        mock_insecure_channel.assert_called_once_with(f"{ips[0]}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_start_metricbeat.assert_called_once_with(stub=mock_stub)

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.HostController.get_host_monitor_thread_status_by_port_and_ip")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.start_heartbeat")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_start_heartbeat(self, mock_HostManagerStub, mock_start_heartbeat, mock_insecure_channel,
                             mock_get_host_monitor_thread_status, mock_start_host_manager) -> None:
        """
        Test start_heartbeat method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_start_heartbeat: mock start_heartbeat
        :param mock_insecure_channel: mock insecure_channel
        :param mock_get_host_monitor_thread_status: mock get_host_monitor_thread_status
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        beats_config = MagicMock()
        self.emulation_env_config.beats_config = beats_config
        self.emulation_env_config.beats_config.get_node_beats_config_by_ips.return_value = MagicMock(
            start_heartbeat_automatically=True)
        host_monitor_dto = MagicMock()
        host_monitor_dto.heartbeat_running = False
        mock_get_host_monitor_thread_status.return_value = host_monitor_dto
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ips = ["172.17.0.2", "192.168.1.2"]
        HostController.start_heartbeat(emulation_env_config=self.emulation_env_config, ips=ips, logger=self.logger,
                                       initial_start=True)
        mock_start_host_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ips[0],
                                                        logger=self.logger)
        self.emulation_env_config.beats_config.get_node_beats_config_by_ips.assert_called_once_with(ips=ips)
        mock_get_host_monitor_thread_status.assert_called_once_with(ip=ips[0], port=12345)
        self.logger.info.assert_called_once_with(f"Heartbeat is not running on {ips[0]}, starting it.")
        mock_insecure_channel.assert_called_once_with(f"{ips[0]}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_start_heartbeat.assert_called_once_with(stub=mock_stub)

    @patch("csle_common.controllers.host_controller.HostController.start_spark")
    def test_start_sparks(self, mock_start_spark) -> None:
        """
        Test start_sparks method

        :param mock_start_spark: mock start_spark
        :return: None
        """
        constants.CONTAINER_IMAGES.SPARK_IMAGES = ["spark-container-1"]
        container1 = self.emulation_env_config.containers_config.containers[0]
        physical_server_ip = "192.168.1.10"
        HostController.start_sparks(
            emulation_env_config=self.emulation_env_config, physical_server_ip=physical_server_ip, logger=self.logger)
        self.logger.info.assert_called_once_with(f"Starting Spark on IP: {container1.docker_gw_bridge_ip}")
        mock_start_spark.assert_called_once_with(
            emulation_env_config=self.emulation_env_config, ips=[container1.docker_gw_bridge_ip], logger=self.logger)
        # Reset mocks to clear previous call history
        self.logger.reset_mock()
        mock_start_spark.reset_mock()
        physical_server_ip = "192.168.1.11"
        HostController.start_sparks(
            emulation_env_config=self.emulation_env_config, physical_server_ip=physical_server_ip, logger=self.logger)
        self.logger.info.assert_not_called()
        mock_start_spark.assert_not_called()

    @patch("csle_common.controllers.host_controller.HostController.stop_spark")
    def test_stop_sparks(self, mock_stop_spark) -> None:
        """
        Test stop_sparks method

        :param mock_stop_spark: mock stop_sparks
        :return: None
        """
        constants.CONTAINER_IMAGES.SPARK_IMAGES = ["spark-container-1"]
        container1 = self.emulation_env_config.containers_config.containers[0]
        physical_server_ip = "192.168.1.10"
        HostController.stop_sparks(emulation_env_config=self.emulation_env_config,
                                   physical_server_ip=physical_server_ip,
                                   logger=self.logger)
        self.logger.info.assert_called_once_with(f"Stopping Spark on IP: {container1.docker_gw_bridge_ip}")
        mock_stop_spark.assert_called_once_with(
            emulation_env_config=self.emulation_env_config, ips=[container1.docker_gw_bridge_ip], logger=self.logger)
        # Reset mocks to clear previous call history
        self.logger.reset_mock()
        mock_stop_spark.reset_mock()
        physical_server_ip = "192.168.1.11"
        HostController.stop_sparks(
            emulation_env_config=self.emulation_env_config, physical_server_ip=physical_server_ip, logger=self.logger)
        self.logger.info.assert_not_called()
        mock_stop_spark.assert_not_called()

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.start_spark")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_start_spark(self, mock_HostManagerStub, mock_start_spark, mock_insecure_channel, mock_start_host_manager) \
            -> None:
        """
        Test start_spark method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_start_spark: mock start_spark
        :param mock_insecure_channel: mock insecure_channel
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ips = ["172.17.0.2", "192.168.1.2"]
        HostController.start_spark(emulation_env_config=self.emulation_env_config, ips=ips, logger=self.logger)
        mock_start_host_manager.assert_called_once_with(
            emulation_env_config=self.emulation_env_config, ip=ips[0], logger=self.logger)
        mock_insecure_channel.assert_called_once_with(f"{ips[0]}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_start_spark.assert_called_once_with(stub=mock_stub)

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.stop_spark")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_stop_spark(self, mock_HostManagerStub, mock_stop_spark, mock_insecure_channel, mock_start_host_manager) \
            -> None:
        """
        Test stop_spark method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_stop_spark: mock stop_spark
        :param mock_insecure_channel: mock insecure_channel
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ips = ["172.17.0.2", "192.168.1.2"]
        HostController.stop_spark(emulation_env_config=self.emulation_env_config, ips=ips, logger=self.logger)
        mock_start_host_manager.assert_called_once_with(
            emulation_env_config=self.emulation_env_config, ip=ips[0], logger=self.logger)
        mock_insecure_channel.assert_called_once_with(f"{ips[0]}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_stop_spark.assert_called_once_with(stub=mock_stub)

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.config_filebeat")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_config_filebeat(
            self, mock_HostManagerStub, mock_config_filebeat, mock_insecure_channel, mock_start_host_manager) -> None:
        """
        Test config_filebeat method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_config_filebeat: mock stop_config_filebeat
        :param mock_insecure_channel: mock insecure_channel
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        # Mock the gRPC channel and stub
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        # Call the function
        container = self.emulation_env_config.containers_config.containers[0]
        HostController.config_filebeat(self.emulation_env_config, container, self.logger)
        mock_start_host_manager.assert_called_once_with(
            emulation_env_config=self.emulation_env_config, ip=container.docker_gw_bridge_ip, logger=self.logger)
        self.emulation_env_config.beats_config.get_node_beats_config_by_ips.assert_called_once_with(
            ips=container.get_ips())
        self.logger.info.assert_called_once_with(
            f"Configuring filebeat on {container.docker_gw_bridge_ip}, "
            f"{container.get_full_name()}, ips: {container.get_ips()}"
        )
        mock_insecure_channel.assert_called_once_with(
            f"{container.docker_gw_bridge_ip}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_config_filebeat.assert_called()

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.config_packetbeat")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_config_packetbeat(
            self, mock_HostManagerStub, mock_config_packetbeat, mock_insecure_channel, mock_start_host_manager) -> None:
        """
        Test config_packetbeat method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_config_packetbeat: mock stop_config_packetbeat
        :param mock_insecure_channel: mock insecure_channel
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        # Mock the gRPC channel and stub
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        # Call the function
        container = self.emulation_env_config.containers_config.containers[0]
        HostController.config_packetbeat(self.emulation_env_config, container, self.logger)
        mock_start_host_manager.assert_called_once_with(
            emulation_env_config=self.emulation_env_config, ip=container.docker_gw_bridge_ip, logger=self.logger)
        self.logger.info.assert_called_once_with(
            f"Configuring packetbeat on {container.docker_gw_bridge_ip}, "
            f"{container.get_full_name()}, ips: {container.get_ips()}")
        mock_insecure_channel.assert_called_once_with(f"{container.docker_gw_bridge_ip}:12345",
                                                      options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_config_packetbeat.assert_called()

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.config_metricbeat")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_config_metricbeat(
            self, mock_HostManagerStub, mock_config_metricbeat, mock_insecure_channel, mock_start_host_manager) -> None:
        """
        Test config_metricbeat method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_config_metricbeat: mock stop_config_metricbeat
        :param mock_insecure_channel: mock insecure_channel
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        # Mock the gRPC channel and stub
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        # Call the function
        container = self.emulation_env_config.containers_config.containers[0]
        HostController.config_metricbeat(self.emulation_env_config, container, self.logger)
        mock_start_host_manager.assert_called_once_with(
            emulation_env_config=self.emulation_env_config, ip=container.docker_gw_bridge_ip, logger=self.logger)
        self.emulation_env_config.beats_config.get_node_beats_config_by_ips.assert_called_once_with(
            ips=container.get_ips())
        self.logger.info.assert_called_once_with(
            f"Configuring metricbeat on {container.docker_gw_bridge_ip}, "
            f"{container.get_full_name()}, ips: {container.get_ips()}")
        mock_insecure_channel.assert_called_once_with(
            f"{container.docker_gw_bridge_ip}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_config_metricbeat.assert_called()

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.config_heartbeat")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_config_heartbeat(self, mock_HostManagerStub, mock_config_heartbeat, mock_insecure_channel,
                              mock_start_host_manager) -> None:
        """
        Test config_heartbeat method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_config_heartbeat: mock stop_config_heartbeat
        :param mock_insecure_channel: mock insecure_channel
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        # Mock the gRPC channel and stub
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        # Call the function
        container = self.emulation_env_config.containers_config.containers[0]
        HostController.config_heartbeat(self.emulation_env_config, container, self.logger)
        mock_start_host_manager.assert_called_once_with(
            emulation_env_config=self.emulation_env_config,
            ip=container.docker_gw_bridge_ip,
            logger=self.logger,
        )
        self.emulation_env_config.beats_config.get_node_beats_config_by_ips.assert_called_once_with(
            ips=container.get_ips())
        self.logger.info.assert_called_once_with(
            f"Configuring heartbeat on {container.docker_gw_bridge_ip}, "
            f"{container.get_full_name()}, ips: {container.get_ips()}")
        mock_insecure_channel.assert_called_once_with(
            f"{container.docker_gw_bridge_ip}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_config_heartbeat.assert_called()

    @patch("csle_common.controllers.host_controller.HostController.stop_host_monitor_thread")
    def test_stop_host_monitor_threads(self, mock_stop_host_monitor_thread) -> None:
        """
        Test stop_host_monitor_threads method

        :param mock_stop_host_monitor_thread: mock stop_host_monitor_thread
        :return: None
        """
        physical_host_ip = "192.168.1.10"
        HostController.stop_host_monitor_threads(
            emulation_env_config=self.emulation_env_config, physical_host_ip=physical_host_ip, logger=self.logger)
        assert mock_stop_host_monitor_thread.call_count == 3

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.stop_host_monitor")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_stop_host_monitor_thread(self, mock_HostManagerStub, mock_stop_host_monitor_thread,
                                      mock_insecure_channel, mock_start_host_manager) -> None:
        """
        Test stop_host_monitor_thread method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_stop_host_monitor_thread: mock stop_host_monitor_thread
        :param mock_insecure_channel: mock insecure_channel
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ip = "172.17.0.2"
        HostController.stop_host_monitor_thread(emulation_env_config=self.emulation_env_config, ip=ip,
                                                logger=self.logger)
        mock_start_host_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ip,
                                                        logger=self.logger)
        mock_insecure_channel.assert_called_once_with(f"{ip}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_stop_host_monitor_thread.assert_called_once_with(stub=mock_stub)

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.stop_filebeat")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_stop_filebeat(self, mock_HostManagerStub, mock_stop_filebeat, mock_insecure_channel,
                           mock_start_host_manager) -> None:
        """
        Test stop_filebeat method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_stop_filebeat: mock stop_filebeat
        :param mock_insecure_channel: mock insecure_channel
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ip = "172.17.0.2"
        HostController.stop_filebeat(emulation_env_config=self.emulation_env_config, ip=ip, logger=self.logger)
        mock_start_host_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ip,
                                                        logger=self.logger)
        mock_insecure_channel.assert_called_once_with(f"{ip}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_stop_filebeat.assert_called_once_with(stub=mock_stub)

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.stop_packetbeat")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_stop_packetbeat(self, mock_HostManagerStub, mock_stop_packetbeat, mock_insecure_channel,
                             mock_start_host_manager) -> None:
        """
        Test stop_packetbeat method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_stop_packetbeat: mock stop_packetbeat
        :param mock_insecure_channel: mock insecure_channel
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ip = "172.17.0.2"
        HostController.stop_packetbeat(emulation_env_config=self.emulation_env_config, ip=ip, logger=self.logger)
        mock_start_host_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ip,
                                                        logger=self.logger)
        mock_insecure_channel.assert_called_once_with(f"{ip}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_stop_packetbeat.assert_called_once_with(stub=mock_stub)

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.stop_metricbeat")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_stop_metricbeat(self, mock_HostManagerStub, mock_stop_metricbeat, mock_insecure_channel,
                             mock_start_host_manager) -> None:
        """
        Test stop_metricbeat method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_stop_metricbeat: mock stop_metricbeat
        :param mock_insecure_channel: mock insecure_channel
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ip = "172.17.0.2"
        HostController.stop_metricbeat(emulation_env_config=self.emulation_env_config, ip=ip, logger=self.logger)
        mock_start_host_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ip,
                                                        logger=self.logger)
        mock_insecure_channel.assert_called_once_with(f"{ip}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_stop_metricbeat.assert_called_once_with(stub=mock_stub)

    @patch("csle_common.controllers.host_controller.HostController.start_host_manager")
    @patch("csle_common.controllers.host_controller.grpc.insecure_channel")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.query_host_manager.stop_heartbeat")
    @patch("csle_common.controllers.host_controller.csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    def test_stop_heartbeat(self, mock_HostManagerStub, mock_stop_heartbeat, mock_insecure_channel,
                            mock_start_host_manager) -> None:
        """
        Test stop_heartbeat method

        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_stop_heartbeat: mock stop_heartbeat
        :param mock_insecure_channel: mock insecure_channel
        :param mock_start_host_manager: mock start_host_manager
        :return: None
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ip = "172.17.0.2"
        HostController.stop_heartbeat(emulation_env_config=self.emulation_env_config, ip=ip, logger=self.logger)
        mock_start_host_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config, ip=ip,
                                                        logger=self.logger)
        mock_insecure_channel.assert_called_once_with(f"{ip}:12345", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_stop_heartbeat.assert_called_once_with(stub=mock_stub)

    @patch("csle_common.controllers.host_controller.HostController.start_host_managers")
    @patch("csle_common.controllers.host_controller.HostController.get_host_monitor_thread_status_by_port_and_ip")
    def test_get_host_monitor_threads_statuses(self, mock_get_status, mock_start_host_managers) -> None:
        """
        Test get_host_monitor_threads_statuses method

        :param mock_get_status: mock get_status method
        :param mock_start_host_managers: mock start_host_managers
        :return: None
        """
        status_mock = MagicMock()
        mock_get_status.return_value = status_mock
        physical_server_ip = "192.168.1.10"
        result = HostController.get_host_monitor_threads_statuses(
            emulation_env_config=self.emulation_env_config, physical_server_ip=physical_server_ip, logger=self.logger)
        mock_start_host_managers.assert_called_once_with(emulation_env_config=self.emulation_env_config,
                                                         logger=self.logger)
        assert mock_get_status.call_count == 3
        expected_result = [
            (status_mock, "172.17.0.1"),
            (status_mock, "172.17.0.3"),
            (status_mock, "172.17.0.4"),
        ]
        assert result == expected_result

    @patch("csle_collector.host_manager.query_host_manager.get_host_status")
    @patch("csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub")
    @patch("grpc.insecure_channel")
    def test_get_host_monitor_thread_status_by_port_and_ip(self, mock_insecure_channel, mock_HostManagerStub,
                                                           mock_get_host_status) -> None:
        """
        Test get_host_monitor_thread_status_by_port_and_ip method

        :param mock_insecure_channel: mock insecure_channel
        :param mock_HostManagerStub: mock HostManagerStub
        :param mock_get_host_status: mock get_host_status
        :return: None
        """
        # Create a mock status to return
        status_mock = MagicMock()
        mock_get_host_status.return_value = status_mock
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_HostManagerStub.return_value = mock_stub
        ip = "172.17.0.2"
        port = 12345
        result = HostController.get_host_monitor_thread_status_by_port_and_ip(ip, port)
        mock_insecure_channel.assert_called_once_with(f"{ip}:{port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_HostManagerStub.assert_called_once_with(mock_channel)
        mock_get_host_status.assert_called_once_with(stub=mock_stub)
        assert result == status_mock

    def test_get_host_managers_ips(self) -> None:
        """
        Test the method for extracting the ips of the Host managers in a given emulation

        :return: None
        """
        result = HostController.get_host_managers_ips(self.emulation_env_config)
        expected_result = ["172.17.0.1", "172.17.0.2", "172.17.0.3", "172.17.0.4", "172.17.0.5"]
        assert result == expected_result

    def test_get_host_managers_ports(self) -> None:
        """
        Test the method for extracting the ports of the Host managers in a given emulation

        :return: None
        """
        result = HostController.get_host_managers_ports(self.emulation_env_config)
        expected_result = [12345, 12345, 12345, 12345, 12345]
        assert result == expected_result

    def test_get_host_managers_info(self) -> None:
        """
        Test the method for extracting the information of the Host managers for a given emulation

        :retur: None
        """
        active_ips = ["172.17.0.2", "172.17.0.3"]
        physical_host_ip = "192.168.1.1"
        result = HostController.get_host_managers_info(self.emulation_env_config, active_ips, self.logger,
                                                       physical_host_ip)
        assert result
