from unittest.mock import patch, MagicMock
import csle_common.constants.constants as constants
from csle_common.controllers.traffic_controller import TrafficController
import pytest


class TestTrafficControllerSuite:
    """
    Test Trafic controller
    """

    @pytest.fixture(autouse=True)
    def emulation_env_config_setup(self) -> None:
        """
        Set up emulation environment configuration

        :return: None
        """
        logger = MagicMock()

        # Create mock node traffic configurations
        mock_traffic_config1 = MagicMock()
        mock_traffic_config1.physical_host_ip = "192.168.1.100"
        mock_traffic_config2 = MagicMock()
        mock_traffic_config2.physical_host_ip = "192.168.1.101"
        node_traffic_configs = [mock_traffic_config1, mock_traffic_config2]

        # Create mock traffic config
        traffic_config = MagicMock()
        traffic_config.node_traffic_configs = node_traffic_configs

        # Create mock emulation environment config
        emulation_env_config = MagicMock()
        emulation_env_config.traffic_config = traffic_config
        emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip = "192.168.0.1"
        emulation_env_config.traffic_config.client_population_config.ip = "192.168.8.1"
        emulation_env_config.traffic_config.client_population_config.physical_host_ip = "192.168.1.1"
        emulation_env_config.traffic_config.client_population_config.client_manager_port = 50051
        emulation_env_config.traffic_config.client_population_config.client_manager_log_dir = "/var/log"
        emulation_env_config.traffic_config.client_population_config.client_manager_log_file = "client_manager.log"
        emulation_env_config.traffic_config.client_population_config.client_manager_max_workers = 4
        emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds = 5
        emulation_env_config.traffic_config.client_population_config.clients = ["client1", "client2"]
        emulation_env_config.traffic_config.client_population_config.workflows_config.workflow_markov_chains = [
            "chain1", "chain2"]
        emulation_env_config.traffic_config.client_population_config.workflows_config.workflow_services = [
            "service1", "service2"]
        emulation_env_config.get_connection.return_value = "mock_connection"
        emulation_env_config.kafka_config.container.get_ips.return_value = ["192.168.0.2"]
        emulation_env_config.kafka_config.kafka_port = 9092
        emulation_env_config.kafka_config.time_step_len_seconds = 5
        self.emulation_env_config = emulation_env_config
        self.logger = logger

    @patch("csle_common.controllers.traffic_controller.TrafficController.start_traffic_manager")
    @patch("time.sleep", return_value=None)
    def test_start_traffic_managers(self, mock_sleep, mock_start_traffic_manager) -> None:
        """
        Test utility method for checking if the traffic manager is running and starting it if it is not running
        on every node

        :param mock_start_traffic_manager: mock_start_traffic_manager
        :param mock_sleep: mock_sleep
        :return: None
        """
        TrafficController.start_traffic_managers(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=self.emulation_env_config.traffic_config.node_traffic_configs[0].physical_host_ip,
            logger=self.logger)
        mock_start_traffic_manager.assert_called()

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_start_traffic_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test utility method for starting traffic manager on a specific container

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :param mock_sleep: mock_sleep
        :return: None
        """
        self.emulation_env_config.get_connection.return_value = MagicMock()
        node_traffic_config = MagicMock()
        node_traffic_config.docker_gw_bridge_ip = "10.0.0.1"
        node_traffic_config.ip = "10.0.5.1"
        node_traffic_config.traffic_manager_port = 50051
        node_traffic_config.traffic_manager_log_dir = "/var/log/traffic"
        node_traffic_config.traffic_manager_log_file = "traffic.log"
        node_traffic_config.traffic_manager_max_workers = 4
        mock_execute_ssh_cmd.side_effect = [
            (b"", b"", 0),  # Output for checking if traffic_manager is running
            (b"", b"", 0),  # Output for stopping old background job
            (b"", b"", 0),  # Output for starting the traffic_manager
        ]
        TrafficController.start_traffic_manager(
            emulation_env_config=self.emulation_env_config, node_traffic_config=node_traffic_config, logger=self.logger
        )
        mock_connect_admin.assert_called()
        check_cmd = (constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP + constants.COMMANDS.SPACE_DELIM
                     + constants.TRAFFIC_COMMANDS.TRAFFIC_MANAGER_FILE_NAME)
        mock_execute_ssh_cmd.assert_any_call(cmd=check_cmd, conn=self.emulation_env_config.get_connection.return_value)
        stop_cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL
                    + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.TRAFFIC_MANAGER_FILE_NAME)
        mock_execute_ssh_cmd.assert_any_call(cmd=stop_cmd, conn=self.emulation_env_config.get_connection.return_value)
        start_cmd = constants.COMMANDS.START_TRAFFIC_MANAGER.format(
            node_traffic_config.traffic_manager_port, node_traffic_config.traffic_manager_log_dir,
            node_traffic_config.traffic_manager_log_file, node_traffic_config.traffic_manager_max_workers)
        mock_execute_ssh_cmd.assert_any_call(cmd=start_cmd, conn=self.emulation_env_config.get_connection.return_value)
        self.logger.info.assert_called_with(f"Starting traffic manager on node "
                                            f"{node_traffic_config.docker_gw_bridge_ip} ({node_traffic_config.ip}), "
                                            f"with cmd:{start_cmd}")

    @patch("csle_common.controllers.traffic_controller.TrafficController.stop_traffic_manager")
    def test_stop_traffic_managers(self, mock_stop_traffic_manager) -> None:
        """
        Test utility method for stopping traffic managers on a given server

        :param mock_start_traffic_manager: mock_start_traffic_manager

        :return: None
        """
        TrafficController.stop_traffic_managers(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=self.emulation_env_config.traffic_config.node_traffic_configs[0].physical_host_ip,
            logger=self.logger)
        mock_stop_traffic_manager.assert_called()

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    def test_stop_traffic_manager(self, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test utility method for stopping a specific traffic manager

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :return: None
        """
        self.emulation_env_config.get_connection.return_value = MagicMock()
        node_traffic_config = MagicMock()
        node_traffic_config.docker_gw_bridge_ip = "10.0.0.1"
        node_traffic_config.ip = "10.0.5.1"
        mock_execute_ssh_cmd.return_value = ("output", "error", None)
        TrafficController.stop_traffic_manager(
            emulation_env_config=self.emulation_env_config, node_traffic_config=node_traffic_config, logger=self.logger)
        mock_connect_admin.assert_called_once_with(emulation_env_config=self.emulation_env_config,
                                                   ip=node_traffic_config.docker_gw_bridge_ip)
        self.logger.info.assert_any_call(f"Stopping traffic manager on node "
                                         f"{node_traffic_config.docker_gw_bridge_ip} ({node_traffic_config.ip})")
        self.emulation_env_config.get_connection.assert_called_once_with(ip=node_traffic_config.docker_gw_bridge_ip)
        mock_execute_ssh_cmd.assert_called()

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("csle_common.util.emulation_util.EmulationUtil.disconnect_admin")
    @patch("time.sleep", return_value=None)
    def test_start_client_manager(self, mock_sleep, mock_disconnect_admin, mock_execute_ssh_cmd,
                                  mock_connect_admin) -> None:
        """
        Test utility method starting the client manager

        :param mock_disconnect_admin: mock_disconnect_admin
        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :param mock_sleep: mock_sleep
        :return: None
        """
        mock_execute_ssh_cmd.side_effect = [
            ("", "", None),  # PS command, client manager not running
            ("", "", None),  # PKILL command
            ("", "", None),  # Start client manager command
        ]
        result = TrafficController.start_client_manager(
            emulation_env_config=self.emulation_env_config, logger=self.logger
        )
        mock_connect_admin.assert_called_once_with(
            emulation_env_config=self.emulation_env_config,
            ip=self.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip)
        mock_execute_ssh_cmd.assert_called()
        self.logger.info.assert_called()
        assert result

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("csle_common.util.emulation_util.EmulationUtil.disconnect_admin")
    def test_stop_client_manager(self, mock_disconnect_admin, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test utility method starting the client manager

        :param mock_disconnect_admin: mock_disconnect_admin
        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :return: None
        """
        mock_execute_ssh_cmd.return_value = ("output", "error", None)
        TrafficController.stop_client_manager(emulation_env_config=self.emulation_env_config, logger=self.logger)
        mock_connect_admin.assert_called_once_with(
            emulation_env_config=self.emulation_env_config,
            ip=self.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip)
        mock_execute_ssh_cmd.assert_called()
        self.logger.info.assert_called()

    @patch("csle_common.controllers.traffic_controller.TrafficController.start_client_manager")
    @patch("csle_common.controllers.traffic_controller.TrafficController.get_clients_dto_by_ip_and_port")
    @patch("grpc.insecure_channel")
    def test_stop_client_population(self, mock_insecure_channel, mock_get_clients_dto,
                                    mock_start_client_manager) -> None:
        """
        Test function for stopping the client arrival process of an emulation

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_get_clients_dto: mock_get_clients_dto
        :param mock_start_client_manager: mock_start_client_manager
        :return: None
        """
        mock_client_dto = MagicMock()
        mock_client_dto.client_process_active = True
        mock_get_clients_dto.return_value = mock_client_dto
        mock_channel = MagicMock()
        mock_stub = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_channel.return_value = mock_stub

        TrafficController.stop_client_population(emulation_env_config=self.emulation_env_config, logger=self.logger)
        self.logger.info.assert_any_call(
            f"Stopping client population on container: "
            f"{self.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip} "
            f"({self.emulation_env_config.traffic_config.client_population_config.ip})")
        mock_start_client_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config,
                                                          logger=self.logger)
        mock_get_clients_dto.assert_called()
        mock_insecure_channel.assert_called()

    @patch("csle_common.controllers.traffic_controller.TrafficController.start_client_manager")
    @patch("csle_common.controllers.traffic_controller.TrafficController.start_client_population")
    @patch("csle_common.controllers.traffic_controller.TrafficController.get_clients_dto_by_ip_and_port")
    @patch("grpc.insecure_channel")
    @patch("time.sleep", return_value=None)
    def test_start_client_producer(self, mock_sleep, mock_insecure_channel, mock_get_clients_dto,
                                   mock_start_client_population, mock_start_client_manager) -> None:
        """
        Test method that starts the Kafka producer for client metrics

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_get_clients_dto: mock_get_clients_dto
        :param mock_start_client_population: mock_start_client_population
        :param mock_start_client_manager: mock_start_client_manager
        :param mock_sleep: mock_sleep
        :return: None
        """
        mock_start_client_manager.return_value = True
        mock_client_dto = MagicMock()
        mock_client_dto.producer_active = False
        mock_get_clients_dto.return_value = mock_client_dto
        mock_channel = MagicMock()
        mock_stub = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_channel.return_value = mock_stub

        TrafficController.start_client_producer(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=self.emulation_env_config.traffic_config.client_population_config.physical_host_ip,
            logger=self.logger)
        self.logger.info.assert_any_call(
            f"Starting client producer on container:"
            f" {self.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip} "
            f"({self.emulation_env_config.traffic_config.client_population_config.ip})")
        mock_start_client_manager.assert_called_once_with(emulation_env_config=self.emulation_env_config,
                                                          logger=self.logger)
        mock_start_client_population.assert_called()
        mock_get_clients_dto.assert_called()
        mock_insecure_channel.assert_called()

    @patch("csle_common.controllers.traffic_controller.TrafficController.start_client_manager")
    @patch("csle_common.controllers.traffic_controller.TrafficController.get_clients_dto_by_ip_and_port")
    @patch("grpc.insecure_channel")
    def test_stop_client_producer(self, mock_insecure_channel, mock_get_clients_dto, mock_start_client_manager) -> None:
        """
        Test method that stops the Kafka producer for client metrics

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_get_clients_dto: mock_get_clients_dto
        :param mock_start_client_manager: mock_start_client_manager
        :return: None
        """
        mock_start_client_manager.return_value = True
        mock_client_dto = MagicMock()
        mock_client_dto.producer_active = True
        mock_get_clients_dto.return_value = mock_client_dto
        mock_channel = MagicMock()
        mock_stub = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_channel.return_value = mock_stub
        TrafficController.stop_client_producer(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=self.emulation_env_config.traffic_config.client_population_config.physical_host_ip,
            logger=self.logger)
        self.logger.info.assert_any_call(
            "Stopping client producer on container: "
            f"{self.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip} "
            f"({self.emulation_env_config.traffic_config.client_population_config.ip})")
        mock_start_client_manager.assert_called_once_with(
            emulation_env_config=self.emulation_env_config, logger=self.logger)
        mock_get_clients_dto.assert_called()
        mock_insecure_channel.assert_called()

    @patch("csle_common.controllers.traffic_controller.TrafficController.start_client_manager")
    @patch("csle_common.controllers.traffic_controller.TrafficController.get_clients_dto_by_ip_and_port")
    @patch("grpc.insecure_channel")
    @patch("csle_collector.client_manager.query_clients.stop_clients")
    @patch("csle_collector.client_manager.query_clients.start_clients")
    @patch("time.sleep", return_value=None)
    def test_start_client_population(self, mock_sleep, mock_start_clients, mock_stop_clients, mock_insecure_channel,
                                     mock_get_clients_dto, mock_start_client_manager) -> None:
        """
        Test method that starts the arrival process of clients

        :param mock_start_clients: mock_start_clients
        :param mock_stop_clients: mock_stop_clients
        :param mock_insecure_channel: mock_insecure_channel
        :param mock_get_clients_dto: mock_get_clients_dto
        :param mock_start_client_manager: mock_start_client_manager
        :param mock_sleep: mock_sleep
        :return: None
        """
        mock_start_client_manager.return_value = True
        mock_client_dto = MagicMock()
        mock_client_dto.producer_active = True
        mock_get_clients_dto.return_value = mock_client_dto
        mock_channel = MagicMock()
        mock_stub = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_channel.return_value = mock_stub

        TrafficController.start_client_population(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=self.emulation_env_config.traffic_config.client_population_config.physical_host_ip,
            logger=self.logger)
        self.logger.info.assert_any_call(
            f"Starting client population on container: "
            f"{self.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip} "
            f"({self.emulation_env_config.traffic_config.client_population_config.ip})")
        mock_start_client_manager.assert_called()
        mock_get_clients_dto.assert_called()
        mock_insecure_channel.assert_called()

    @patch("csle_common.controllers.traffic_controller.TrafficController.start_client_manager")
    @patch("csle_common.controllers.traffic_controller.TrafficController.get_clients_dto_by_ip_and_port")
    def test_get_num_active_clients(self, mock_get_clients_dto, mock_start_client_manager) -> None:
        """
        Test method that gets the number of active clients

        :param mock_get_clients_dto: mock_get_clients_dto
        :param mock_start_client_manager: mock_start_client_manager
        :return: None
        """
        mock_client_dto = MagicMock()
        mock_get_clients_dto.return_value = mock_client_dto
        result = TrafficController.get_num_active_clients(
            emulation_env_config=self.emulation_env_config, logger=self.logger)
        mock_start_client_manager.assert_called_once_with(
            emulation_env_config=self.emulation_env_config, logger=self.logger)
        mock_get_clients_dto.assert_called()
        assert result == mock_client_dto

    @patch("grpc.insecure_channel")
    @patch("csle_collector.client_manager.query_clients.get_clients")
    def test_get_clients_dto_by_ip_and_port(self, mock_get_clients, mock_insecure_channel) -> None:
        """
        Test method that sends a request to the ClientManager on a specific container
        to get its status

        :param mock_get_clients: mock_get_clients
        :param mock_insecure_channel: mock_insecure_channel
        :return: None
        """
        ip = "192.168.0.1"
        port = 50051
        mock_channel = MagicMock()
        mock_stub = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_channel.return_value = mock_stub
        mock_status = MagicMock()
        mock_get_clients.return_value = mock_status
        result = TrafficController.get_clients_dto_by_ip_and_port(ip=ip, port=port, logger=self.logger)
        self.logger.info.assert_any_call(
            f"Get client manager status from container with ip: {ip} and client manager port: {port}")
        mock_insecure_channel.assert_called()
        assert result == mock_status

    @patch("csle_common.controllers.traffic_controller.TrafficController.stop_internal_traffic_generator")
    def test_stop_internal_traffic_generators(self, mock_stop_internal_traffic_generator) -> None:
        """
        Test utility function for stopping internal traffic generators

        :param mock_stop_internal_traffic_generator: mock_stop_internal_traffic_generator
        :return: None
        """
        mock_node_traffic_config_1 = MagicMock()
        mock_node_traffic_config_1.physical_host_ip = "192.168.1.1"
        mock_node_traffic_config_2 = MagicMock()
        mock_node_traffic_config_2.physical_host_ip = "192.168.1.2"
        self.emulation_env_config.traffic_config.node_traffic_configs = [mock_node_traffic_config_1,
                                                                         mock_node_traffic_config_2]
        TrafficController.stop_internal_traffic_generators(
            emulation_env_config=self.emulation_env_config, logger=self.logger,
            physical_server_ip=mock_node_traffic_config_1.physical_host_ip)
        mock_stop_internal_traffic_generator.assert_called()

    @patch("csle_common.controllers.traffic_controller.TrafficController.start_traffic_manager")
    @patch("grpc.insecure_channel")
    @patch("csle_collector.traffic_manager.query_traffic_manager.stop_traffic")
    def test_stop_internal_traffic_generator(self, mock_stop_traffic, mock_insecure_channel,
                                             mock_start_traffic_manager) -> None:
        """
        Test utility function for stopping a specific internal traffic generator

        :param mock_stop_traffic: mock_stop_traffic
        :param mock_insecure_channel: mock_insecure_channel
        :param mock_start_traffic_manager: mock_start_traffic_manager
        :return: None
        """
        mock_node_traffic_config = MagicMock()
        mock_node_traffic_config.docker_gw_bridge_ip = "192.168.0.1"
        mock_node_traffic_config.ip = "192.168.5.1"
        mock_node_traffic_config.traffic_manager_port = 50051
        mock_channel = MagicMock()
        mock_stub = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_channel.return_value = mock_stub
        TrafficController.stop_internal_traffic_generator(
            emulation_env_config=self.emulation_env_config, node_traffic_config=mock_node_traffic_config,
            logger=self.logger)
        mock_start_traffic_manager.assert_called()
        self.logger.info.assert_any_call(f"Stopping traffic generator script, node ip:"
                                         f"{mock_node_traffic_config.docker_gw_bridge_ip} "
                                         f"({mock_node_traffic_config.ip})")
        mock_insecure_channel.assert_called()
        TrafficController.stop_internal_traffic_generator(
            emulation_env_config=self.emulation_env_config,
            node_traffic_config=mock_node_traffic_config, logger=self.logger)
        mock_start_traffic_manager.assert_called()
        self.logger.info.assert_any_call(f"Stopping traffic generator script, node ip:"
                                         f"{mock_node_traffic_config.docker_gw_bridge_ip} "
                                         f"({mock_node_traffic_config.ip})")
        mock_insecure_channel.assert_called()

    @patch("csle_common.controllers.traffic_controller.TrafficController.start_internal_traffic_generator")
    def test_start_internal_traffic_generators(self, mock_start_internal_traffic_generator) -> None:
        """
        Test utility function for starting internal traffic generators

        :param mock_start_internal_traffic_generator: mock_start_internal_traffic_generator
        :return: None
        """
        mock_node_traffic_config_1 = MagicMock()
        mock_node_traffic_config_1.physical_host_ip = "192.168.1.1"
        mock_node_traffic_config_1.ip = "10.0.0.1"
        mock_node_traffic_config_2 = MagicMock()
        mock_node_traffic_config_2.physical_host_ip = "192.168.1.2"
        self.emulation_env_config.traffic_config.node_traffic_configs = [mock_node_traffic_config_1,
                                                                         mock_node_traffic_config_2]
        # Create mock containers
        mock_container_1 = MagicMock()
        mock_container_1.get_ips.return_value = ["10.0.0.1"]
        mock_container_2 = MagicMock()
        mock_container_2.get_ips.return_value = ["10.0.0.2"]
        self.emulation_env_config.containers_config.containers = [mock_container_1, mock_container_2]
        TrafficController.start_internal_traffic_generators(
            emulation_env_config=self.emulation_env_config,
            physical_server_ip=mock_node_traffic_config_1.physical_host_ip, logger=self.logger)
        mock_start_internal_traffic_generator.assert_called()

    @patch("csle_common.controllers.traffic_controller.TrafficController.start_traffic_manager")
    @patch("grpc.insecure_channel")
    @patch("csle_collector.traffic_manager.query_traffic_manager.start_traffic")
    def test_start_internal_traffic_generator(self, mock_start_traffic, mock_insecure_channel,
                                              mock_start_traffic_manager) -> None:
        """
        Test utility function for starting internal traffic generators

        :param mock_start_traffic: mock_start_traffic
        :param mock_insecure_channel: mock_insecure_channel
        :param mock_start_traffic_manager: mock_start_traffic_manager
        :return: None
        """
        mock_node_traffic_config = MagicMock()
        mock_node_traffic_config.docker_gw_bridge_ip = "192.168.0.1"
        mock_node_traffic_config.traffic_manager_port = 50051

        mock_container = MagicMock()
        mock_container.ips_and_networks = [("10.0.0.1", MagicMock(subnet_mask="255.255.255.0"))]
        mock_container.get_ips.return_value = ["10.0.0.1"]

        mock_container_1 = MagicMock()
        mock_container_1.ips_and_networks = [("10.0.0.2", MagicMock(subnet_mask="255.255.255.0"))]
        mock_container_1.get_ips.return_value = ["10.0.0.2"]

        mock_container_2 = MagicMock()
        mock_container_2.ips_and_networks = [("10.0.0.3", MagicMock(subnet_mask="255.255.255.0"))]
        mock_container_2.get_ips.return_value = ["10.0.0.3"]

        self.emulation_env_config.containers_config.containers = [mock_container_1, mock_container_2]

        mock_node_traffic_config_1 = MagicMock()
        mock_node_traffic_config_1.ip = "10.0.0.2"
        mock_node_traffic_config_1.commands = ["cmd1"]

        mock_node_traffic_config_2 = MagicMock()
        mock_node_traffic_config_2.ip = "10.0.0.3"
        mock_node_traffic_config_2.commands = ["cmd2"]

        self.emulation_env_config.traffic_config.node_traffic_configs = [
            mock_node_traffic_config_1, mock_node_traffic_config_2]
        self.emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds = 5

        mock_channel = MagicMock()
        mock_stub = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_channel.return_value = mock_stub

        TrafficController.start_internal_traffic_generator(
            emulation_env_config=self.emulation_env_config,
            node_traffic_config=mock_node_traffic_config, container=mock_container, logger=self.logger)
        mock_start_traffic_manager.assert_called()
        self.logger.info.assert_any_call(f"Starting traffic generator script, node ip:"
                                         f"{mock_node_traffic_config.docker_gw_bridge_ip} "
                                         f"({mock_node_traffic_config.ip})")
        mock_insecure_channel.assert_called()

    def test_get_client_managers_ips(self) -> None:
        """
        Test method that extracts the IPS of the Client managers in a given emulation

        :return: None
        """
        result = TrafficController.get_client_managers_ips(emulation_env_config=self.emulation_env_config)
        assert result == [self.emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip]

    def test_get_client_managers_ports(self) -> None:
        """
        Test method that extracts the ports of the Client managers in a given emulation

        :return: None
        """
        result = TrafficController.get_client_managers_ports(emulation_env_config=self.emulation_env_config)
        assert result == [50051]

    @patch("csle_common.controllers.traffic_controller.TrafficController.get_client_managers_ips")
    @patch("csle_common.controllers.traffic_controller.TrafficController.get_client_managers_ports")
    @patch("csle_common.controllers.traffic_controller.TrafficController.get_clients_dto_by_ip_and_port")
    @patch("csle_collector.client_manager.client_manager_util.ClientManagerUtil.clients_dto_empty")
    def test_get_client_managers_info(self, mock_clients_dto_empty, mock_get_clients_dto_by_ip_and_port,
                                      mock_get_client_managers_ports, mock_get_client_managers_ips) -> None:
        """
        Test method that extracts the information of the Client managers for a given emulation

        :param mock_clients_dto_empty: mock_clients_dto_empty
        :param mock_get_clients_dto_by_ip_and_port: mock_get_clients_dto_by_ip_and_port
        :param mock_get_client_managers_ports: mock_get_client_managers_ports
        :param mock_get_client_managers_ips: mock_get_client_managers_ips
        :return: None
        """
        self.emulation_env_config.execution_id = "test_execution_id"
        self.emulation_env_config.name = "test_emulation"
        self.emulation_env_config.traffic_config.client_population_config.client_manager_port = 50051

        active_ips = ["192.168.0.1", "192.168.0.2"]
        ports = [50051, 50051]
        mock_get_client_managers_ips.return_value = active_ips
        mock_get_client_managers_ports.return_value = ports

        mock_status = MagicMock()
        mock_get_clients_dto_by_ip_and_port.side_effect = [mock_status, Exception("Test Exception")]
        mock_clients_dto_empty.return_value = "empty_dto"

        result = TrafficController.get_client_managers_info(
            emulation_env_config=self.emulation_env_config, active_ips=active_ips, logger=self.logger)

        mock_get_client_managers_ips.assert_called_once_with(emulation_env_config=self.emulation_env_config)
        mock_get_client_managers_ports.assert_called_once_with(emulation_env_config=self.emulation_env_config)
        mock_get_clients_dto_by_ip_and_port.assert_any_call(ip=active_ips[0], port=ports[0], logger=self.logger)
        mock_get_clients_dto_by_ip_and_port.assert_any_call(ip=active_ips[1], port=ports[1], logger=self.logger)
        assert result

    @patch("grpc.insecure_channel")
    @patch("csle_collector.traffic_manager.query_traffic_manager.get_traffic_status")
    def test_get_traffic_manager_status_by_port_and_ip(self, mock_get_traffic_status, mock_insecure_channel) -> None:
        """
        Test method that sends a request to the TrafficManager on a specific container
        to get its status

        :param mock_get_traffic_status: mock_get_traffic_status
        :param mock_insecure_channel: mock_insecure_channel
        :return: None
        """
        ip = "192.168.0.1"
        port = 50051
        mock_channel = MagicMock()
        mock_stub = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_channel.return_value = mock_stub
        mock_status = MagicMock()
        mock_get_traffic_status.return_value = mock_status
        result = TrafficController.get_traffic_manager_status_by_port_and_ip(ip=ip, port=port)
        mock_insecure_channel.assert_called()
        assert result == mock_status

    def test_get_traffic_managers_ips(self) -> None:
        """
        Test method that extracts the ips of the traffic managers in a given emulation

        :return: None
        """
        mock_node_traffic_config_1 = MagicMock()
        mock_node_traffic_config_1.docker_gw_bridge_ip = "192.168.0.1"
        mock_node_traffic_config_2 = MagicMock()
        mock_node_traffic_config_2.docker_gw_bridge_ip = "192.168.0.2"
        self.emulation_env_config.traffic_config.node_traffic_configs = [
            mock_node_traffic_config_1, mock_node_traffic_config_2]
        result = TrafficController.get_traffic_managers_ips(emulation_env_config=self.emulation_env_config)
        assert result == [mock_node_traffic_config_1.docker_gw_bridge_ip,
                          mock_node_traffic_config_2.docker_gw_bridge_ip]

    def test_get_traffic_managers_ports(self) -> None:
        """
        Test method that extracts the ports of the Traffic managers in a given emulation

        :return: None
        """
        mock_node_traffic_config_1 = MagicMock()
        mock_node_traffic_config_1.traffic_manager_port = 50051
        mock_node_traffic_config_2 = MagicMock()
        mock_node_traffic_config_2.traffic_manager_port = 50052
        self.emulation_env_config.traffic_config.node_traffic_configs = [
            mock_node_traffic_config_1, mock_node_traffic_config_2]
        result = TrafficController.get_traffic_managers_ports(emulation_env_config=self.emulation_env_config)
        assert result == [mock_node_traffic_config_1.traffic_manager_port,
                          mock_node_traffic_config_2.traffic_manager_port]

    @patch("csle_common.controllers.traffic_controller.TrafficController.get_traffic_managers_ips")
    @patch("csle_common.controllers.traffic_controller.TrafficController.get_traffic_managers_ports")
    @patch("csle_common.controllers.traffic_controller.TrafficController.get_traffic_manager_status_by_port_and_ip")
    @patch("csle_collector.traffic_manager.traffic_manager_util.TrafficManagerUtil.traffic_dto_empty")
    @patch("csle_common.util.emulation_util.EmulationUtil.physical_ip_match")
    @patch("time.sleep", return_value=None)
    def test_get_traffic_managers_info(
            self, mock_sleep, mock_physical_ip_match, mock_traffic_dto_empty,
            mock_get_traffic_manager_status_by_port_and_ip, mock_get_traffic_managers_ports,
            mock_get_traffic_managers_ips) -> None:
        """
        Test method that extracts the information of the traffic managers for a given emulation

        :param mock_physical_ip_match: mock_physical_ip_match
        :param mock_traffic_dto_empty: mock_traffic_dto_empty
        :param mock_get_traffic_manager_status_by_port_and_ip: mock_get_traffic_manager_status_by_port_and_ip
        :param mock_get_traffic_managers_ports: mock_get_traffic_managers_ports
        :param mock_get_traffic_managers_ips: mock_get_traffic_managers_ips
        :param mock_sleep: mock_sleep
        :return: None
        """
        self.emulation_env_config.execution_id = "test_execution_id"
        self.emulation_env_config.name = "test_emulation"

        mock_node_traffic_config_1 = MagicMock()
        mock_node_traffic_config_1.docker_gw_bridge_ip = "192.168.0.1"
        mock_node_traffic_config_1.traffic_manager_port = 50051
        mock_node_traffic_config_1.ip = "10.0.0.1"

        mock_node_traffic_config_2 = MagicMock()
        mock_node_traffic_config_2.docker_gw_bridge_ip = "192.168.0.2"
        mock_node_traffic_config_2.traffic_manager_port = 50052
        mock_node_traffic_config_2.ip = "10.0.0.2"

        self.emulation_env_config.traffic_config.node_traffic_configs = [
            mock_node_traffic_config_1, mock_node_traffic_config_2]

        mock_get_traffic_managers_ips.return_value = [mock_node_traffic_config_1.docker_gw_bridge_ip,
                                                      mock_node_traffic_config_2.docker_gw_bridge_ip]
        mock_get_traffic_managers_ports.return_value = [mock_node_traffic_config_1.traffic_manager_port,
                                                        mock_node_traffic_config_2.traffic_manager_port]

        mock_status = MagicMock()
        mock_get_traffic_manager_status_by_port_and_ip.side_effect = [mock_status, Exception("Test Exception")]
        mock_traffic_dto_empty.return_value = "empty_dto"
        mock_physical_ip_match.return_value = True

        active_ips = [mock_node_traffic_config_1.docker_gw_bridge_ip, mock_node_traffic_config_2.docker_gw_bridge_ip]
        physical_host_ip = mock_node_traffic_config_1.ip

        result = TrafficController.get_traffic_managers_info(
            emulation_env_config=self.emulation_env_config,
            active_ips=active_ips, physical_host_ip=physical_host_ip, logger=self.logger)
        mock_get_traffic_managers_ips.assert_called_once_with(emulation_env_config=self.emulation_env_config)
        mock_get_traffic_managers_ports.assert_called_once_with(emulation_env_config=self.emulation_env_config)
        mock_get_traffic_manager_status_by_port_and_ip.assert_any_call(
            port=mock_node_traffic_config_1.traffic_manager_port,
            ip=mock_node_traffic_config_1.docker_gw_bridge_ip)
        mock_get_traffic_manager_status_by_port_and_ip.assert_any_call(
            port=mock_node_traffic_config_2.traffic_manager_port, ip=mock_node_traffic_config_2.docker_gw_bridge_ip)
        assert result
