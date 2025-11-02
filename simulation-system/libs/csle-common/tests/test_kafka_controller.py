import logging
from unittest.mock import patch, MagicMock
import csle_common.constants.constants as constants
from csle_common.controllers.kafka_controller import KafkaController
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
import csle_collector.kafka_manager.kafka_manager_pb2_grpc
import csle_collector.kafka_manager.kafka_manager_pb2
import csle_collector.kafka_manager.query_kafka_server
import csle_collector.kafka_manager.kafka_manager_util


class TestKafkaControllerSuite:
    """
    Test suite for kafka controller
    """

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_start_stop_kafka_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test case for starting or stopping the kafka manager

        :param mock_disconnect_admin: Mocked disconnect_admin method
        :param mock_execute_ssh_cmd: Mocked execute_ssh_cmd method
        :param mock_connect_admin: Mocked connect_admin
        :param mock_sleep: Mocked sleep method
        :return: None
        """
        mock_connect_admin.return_value = None
        mock_execute_ssh_cmd.return_value = ("output", "error", 0)
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        kafka_config = MagicMock()
        emulation_env_config.kafka_config = kafka_config
        emulation_env_config.kafka_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.kafka_config.get_connection.return_value = MagicMock()
        KafkaController.start_kafka_manager(emulation_env_config)
        mock_connect_admin.assert_called_once_with(emulation_env_config=emulation_env_config, ip="172.17.0.1",
                                                   create_producer=False)
        mock_execute_ssh_cmd.assert_called()
        KafkaController.stop_kafka_manager(emulation_env_config)
        assert 2 == mock_connect_admin.call_count
        assert 4 == mock_execute_ssh_cmd.call_count

    @patch("csle_collector.kafka_manager.query_kafka_server.create_topic")
    @patch("csle_collector.kafka_manager.query_kafka_server.start_kafka")
    @patch("csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub")
    @patch("csle_common.controllers.kafka_controller.KafkaController.start_kafka_manager")
    @patch("csle_common.controllers.kafka_controller.KafkaController.get_kafka_status_by_port_and_ip")
    @patch("time.sleep", return_value=None)
    def test_create_topics(self, mock_time_sleep, mock_get_kafka_status_by_port_and_ip, mock_start_kafka_manager,
                           mock_KafkaManagerStub, mock_start_kafka, mock_create_topic) -> None:
        """
        Tests the method that sends a request to the KafkaManager to create topics according to the given configuration

        :param mock_time_sleep: mock time_sleep method
        :param mock_get_kafka_status_by_port_and_ip: mock get_kafka_status_by_port_and_ip method
        :param mock_start_kafka_manager: mock start_kafka_manager method
        :param mock_KafkaManagerStub: mock KafkaManagerStub
        :param mock_start_kafka: mock start_kafka
        :param mock_create_topic: mock create_topic
        :return: None
        """
        mock_stub = MagicMock()
        mock_KafkaManagerStub.return_value = mock_stub
        mock_logger = MagicMock(spec=logging.Logger)
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        kafka_config = MagicMock()
        kafka_container_mock = MagicMock()
        kafka_container_mock.docker_gw_bridge_ip = "127.0.0.1"
        kafka_container_mock.get_ips.return_value = ["127.0.0.1"]
        kafka_container_mock.get_full_name.return_value = "container_name"
        kafka_config.container = kafka_container_mock
        kafka_config.kafka_manager_port = 9092
        emulation_env_config.kafka_config = kafka_config
        topic1 = MagicMock()
        topic1.name = "topic1"
        topic1.num_partitions = 1
        topic1.num_replicas = 1
        topic1.retention_time_hours = 24
        topic2 = MagicMock()
        topic2.name = "topic2"
        topic2.num_partitions = 2
        topic2.num_replicas = 2
        topic2.retention_time_hours = 48
        emulation_env_config.kafka_config.topics = [topic1, topic2]
        mock_get_kafka_status_by_port_and_ip.return_value.running = False
        KafkaController.create_topics(emulation_env_config=emulation_env_config, logger=mock_logger)
        mock_logger.info.assert_any_call(f"Creating kafka topics on container: "
                                         f"{emulation_env_config.kafka_config.container.docker_gw_bridge_ip} "
                                         f"({kafka_container_mock.get_ips()[0]}, "
                                         f"{kafka_container_mock.get_full_name()})")
        mock_logger.info.assert_any_call("Kafka server is not running, starting it.")
        mock_logger.info.assert_any_call("Creating topic: topic1")
        mock_logger.info.assert_any_call("Creating topic: topic2")
        mock_start_kafka_manager.assert_called_once_with(emulation_env_config=emulation_env_config)
        mock_get_kafka_status_by_port_and_ip.assert_called_once_with(ip="127.0.0.1", port=9092)
        mock_start_kafka.assert_called_once_with(mock_stub)
        mock_create_topic.assert_any_call(mock_stub, name="topic1", partitions=1, replicas=1, retention_time_hours=24)
        mock_create_topic.assert_any_call(mock_stub, name="topic2", partitions=2, replicas=2, retention_time_hours=48)
        mock_time_sleep.assert_called_once_with(20)

    @patch("csle_common.controllers.kafka_controller.KafkaController.start_kafka_manager")
    @patch("csle_common.controllers.kafka_controller.KafkaController.get_kafka_status_by_port_and_ip")
    def test_get_kafka_status(self, mock_get_kafka_status_by_port_and_ip, mock_start_kafka_manager) -> None:
        """
        Test case for querying the KafkaManager about the status of the Kafka server

        :param mock_get_kafka_status_by_port_and_ip: mocked get_kafka_status_by_port_and_ip method
        :param mock_start_kafka_manager: mocked start_kafka_manager method
        :return: None
        """
        mock_start_kafka_manager.return_value = None
        expected_kafka_dto = MagicMock(spec=csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO)
        mock_get_kafka_status_by_port_and_ip.return_value = expected_kafka_dto
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        kafka_config = MagicMock()
        emulation_env_config.kafka_config = kafka_config
        emulation_env_config.kafka_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.kafka_config.kafka_manager_port = 5601
        result = KafkaController.get_kafka_status(emulation_env_config)
        mock_start_kafka_manager.assert_called_once_with(emulation_env_config=emulation_env_config)
        mock_get_kafka_status_by_port_and_ip.assert_called_once_with(ip="172.17.0.1", port=5601)
        assert result == expected_kafka_dto

    @patch("csle_collector.kafka_manager.query_kafka_server.get_kafka_status")
    @patch("csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub")
    @patch("grpc.insecure_channel")
    def test_get_kafka_status_by_port_and_ip(self, mock_insecure_channel, mock_KafkaManagerStub,
                                             mock_get_kafka_status) -> None:
        """
        Test case for querying the KafkaManager about the status of the kafka stack

        :param mock_insecure_channel: mocked insecure_channel method
        :param mock_KafkaManagerStub: mocked KafkaManagerStub method
        :param mock_get_kafka_status: mocked get_kafka_status method
        :return: None
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_KafkaManagerStub.return_value = mock_stub
        expected_kafka_dto = MagicMock(spec=csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO)
        mock_get_kafka_status.return_value = expected_kafka_dto
        ip = "172.17.0.1"
        port = 5601
        result = KafkaController.get_kafka_status_by_port_and_ip(ip, port)
        mock_insecure_channel.assert_called_once_with(f"{ip}:{port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_KafkaManagerStub.assert_called_once_with(mock_channel)
        mock_get_kafka_status.assert_called_once_with(mock_stub)
        assert result == expected_kafka_dto

    @patch("csle_common.controllers.kafka_controller.KafkaController.start_kafka_manager")
    @patch("csle_collector.kafka_manager.query_kafka_server.stop_kafka")
    @patch("csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub")
    @patch("grpc.insecure_channel")
    def test_stop_kafka_server(self, mock_insecure_channel, mock_KafkaManagerStub, mock_stop_kafka,
                               mock_start_kafka_manager) -> None:
        """
        Test the method for requesting the KafkaManager to stop the Kafka server

        :param mock_insecure_channel: mock insecure_channel
        :param mock_KafkaManagerStub: mock KafkaManagerStub
        :param mock_stop_kafka: mock stop_kafka
        :param mock_start_kafka_manager: mock start_kafka_manager
        :return: None
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_KafkaManagerStub.return_value = mock_stub
        expected_kafka_dto = MagicMock(spec=csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO)
        mock_stop_kafka.return_value = expected_kafka_dto
        mock_logger = MagicMock(spec=logging.Logger)
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        kafka_config = MagicMock()
        kafka_container_mock = MagicMock()
        kafka_container_mock.docker_gw_bridge_ip = "127.0.0.1"
        kafka_container_mock.get_ips.return_value = ["127.0.0.1"]
        kafka_container_mock.get_full_name.return_value = "container_name"
        kafka_config.container = kafka_container_mock
        kafka_config.kafka_manager_port = 9092
        emulation_env_config.kafka_config = kafka_config
        result = KafkaController.stop_kafka_server(emulation_env_config=emulation_env_config, logger=mock_logger)
        mock_logger.info.assert_any_call(f"Stopping Kafka server on container: "
                                         f"{kafka_container_mock.docker_gw_bridge_ip} "
                                         f"({kafka_container_mock.get_ips()[0]}, "
                                         f"{kafka_container_mock.get_full_name()})")
        mock_start_kafka_manager.assert_called_once_with(emulation_env_config=emulation_env_config)
        mock_insecure_channel.assert_called_once_with(
            f"{emulation_env_config.kafka_config.container.docker_gw_bridge_ip}:"
            f"{emulation_env_config.kafka_config.kafka_manager_port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_KafkaManagerStub.assert_called_once_with(mock_channel)
        mock_stop_kafka.assert_called_once_with(mock_stub)
        assert result == expected_kafka_dto

    @patch("csle_common.controllers.kafka_controller.KafkaController.start_kafka_manager")
    @patch("csle_collector.kafka_manager.query_kafka_server.start_kafka")
    @patch("csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub")
    @patch("grpc.insecure_channel")
    def test_start_kafka_server(self, mock_insecure_channel, mock_KafkaManagerStub, mock_start_kafka,
                                mock_start_kafka_manager) -> None:
        """
        Test the method for requesting the KafkaManager to start the Kafka server

        :param mock_insecure_channel: mock insecure_channel
        :param mock_KafkaManagerStub: mock KafkaManagerStub
        :param mock_start_kafka: mock start_kafka
        :param mock_start_kafka_manager: mock start_kafka_manager
        :return: None
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_KafkaManagerStub.return_value = mock_stub
        expected_kafka_dto = MagicMock(spec=csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO)
        mock_start_kafka.return_value = expected_kafka_dto
        mock_logger = MagicMock(spec=logging.Logger)
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        kafka_config = MagicMock()
        kafka_container_mock = MagicMock()
        kafka_container_mock.docker_gw_bridge_ip = "127.0.0.1"
        kafka_container_mock.get_ips.return_value = ["127.0.0.1"]
        kafka_container_mock.get_full_name.return_value = "container_name"
        kafka_config.container = kafka_container_mock
        kafka_config.kafka_manager_port = 9092
        emulation_env_config.kafka_config = kafka_config
        result = KafkaController.start_kafka_server(emulation_env_config=emulation_env_config, logger=mock_logger)
        mock_logger.info.assert_any_call(f"Starting Kafka server on container: "
                                         f"{kafka_config.container.docker_gw_bridge_ip} ("
                                         f"{kafka_container_mock.get_ips()[0]}, "
                                         f"{kafka_container_mock.get_full_name()})")
        mock_start_kafka_manager.assert_called_once_with(emulation_env_config=emulation_env_config)
        mock_insecure_channel.assert_called_once_with(
            f"{emulation_env_config.kafka_config.container.docker_gw_bridge_ip}:"
            f"{emulation_env_config.kafka_config.kafka_manager_port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_KafkaManagerStub.assert_called_once_with(mock_channel)
        mock_start_kafka.assert_called_once_with(mock_stub)
        assert result == expected_kafka_dto

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_collector.constants.constants.KAFKA.KAFKA_CONFIG_FILE")
    def test_configure_broker_ips(self, mock_kafka_config_file, mock_connect_admin) -> None:
        """
        Test the method for configuring the broker IPs on the Kafka container

        :param mock_kafka_config_file: mock kafka_config_file
        :param mock_connect_admin: mock_connect_admin
        :return: None
        """
        mock_logger = MagicMock(spec=logging.Logger)
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        kafka_config = MagicMock()
        kafka_container_mock = MagicMock()
        kafka_container_mock.docker_gw_bridge_ip = "127.0.0.1"
        kafka_container_mock.get_ips.return_value = ["127.0.0.1"]
        kafka_container_mock.get_full_name.return_value = "container_name"
        kafka_config.container = kafka_container_mock
        kafka_config.kafka_manager_port = 9092
        emulation_env_config.kafka_config = kafka_config
        mock_sftp_client = MagicMock()
        mock_file = MagicMock()
        emulation_env_config.get_connection.return_value.open_sftp.return_value = (mock_sftp_client)
        mock_file.read.return_value = b"internal_ip_placeholder external_ip_placeholder"
        mock_sftp_client.open.side_effect = [mock_file, mock_file]  # for read and write
        KafkaController.configure_broker_ips(emulation_env_config=emulation_env_config, logger=mock_logger)
        mock_logger.info.assert_any_call(f"Configuring broker IPs on container: "
                                         f"{kafka_container_mock.docker_gw_bridge_ip} "
                                         f"({kafka_container_mock.get_ips()[0]}, "
                                         f"{kafka_container_mock.get_full_name()})")
        mock_connect_admin.assert_called_once_with(emulation_env_config=emulation_env_config,
                                                   ip=kafka_container_mock.docker_gw_bridge_ip)
        emulation_env_config.get_connection.assert_called_once_with(ip=kafka_container_mock.docker_gw_bridge_ip)
        mock_sftp_client.open.assert_any_call(mock_kafka_config_file, mode="r")
        mock_sftp_client.open.assert_any_call(mock_kafka_config_file, mode="w")
        mock_file.flush.assert_called_once()
        mock_file.close.assert_called()

    def test_get_kafka_managers_ips(self) -> None:
        """
        Test case for extracting the IPS of the kafka managers in a given emulation

        :return: None
        """
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        kafka_config = MagicMock()
        emulation_env_config.kafka_config = kafka_config
        emulation_env_config.kafka_config.container.docker_gw_bridge_ip = "172.17.0.1"
        result = KafkaController.get_kafka_managers_ips(emulation_env_config)
        assert result == ["172.17.0.1"]

    def test_get_kafka_managers_ports(self) -> None:
        """
        Test case for extracting the ports of the kafka managers in a given emulation

        :return: None
        """
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        kafka_config = MagicMock()
        emulation_env_config.kafka_config = kafka_config
        emulation_env_config.kafka_config.kafka_manager_port = 5601
        result = KafkaController.get_kafka_managers_ports(emulation_env_config)
        assert result == [5601]

    @patch("csle_common.controllers.kafka_controller.KafkaController.get_kafka_managers_ips")
    @patch("csle_common.controllers.kafka_controller.KafkaController.get_kafka_managers_ports")
    @patch("csle_common.controllers.kafka_controller.KafkaController.get_kafka_status_by_port_and_ip")
    @patch("csle_collector.kafka_manager.kafka_manager_util.KafkaManagerUtil.kafka_dto_empty")
    def test_get_kafka_managers_infos(self, mock_kafka_dto_empty, mock_get_kafka_status_by_port_and_ip,
                                      mock_get_kafka_managers_ports, mock_get_kafka_managers_ips) -> None:
        """
        Test case for extracting the infomation of the kafka managers for a given emulation

        :param mock_kafka_dto_empty: mocked kafka_dto_empty method
        :param mock_get_kafka_status_by_port_and_ip: mocked get_kafka_status_by_port_and_ip method
        :param mock_get_kafka_managers_ports: mocked get_kafka_managers_ports
        :param mock_get_kafka_managers_ips: mocked get_kafka_managers_ips
        :return: None
        """
        mock_get_kafka_managers_ips.return_value = ["172.17.0.1"]
        mock_get_kafka_managers_ports.return_value = [5601]
        mock_kafka_status = MagicMock()
        mock_get_kafka_status_by_port_and_ip.return_value = mock_kafka_status
        mock_kafka_dto_empty.return_value = MagicMock()
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        kafka_config = MagicMock()
        emulation_env_config.kafka_config = kafka_config
        emulation_env_config.kafka_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.kafka_config.kafka_manager_port = 5601
        emulation_env_config.execution_id = 10
        emulation_env_config.name = "test_emulation"
        logger = MagicMock(spec=logging.Logger)
        active_ips = ["172.17.0.1"]
        physical_host_ip = "192.168.0.1"
        result = KafkaController.get_kafka_managers_info(emulation_env_config, active_ips, logger, physical_host_ip)
        mock_get_kafka_managers_ips.assert_called_once_with(emulation_env_config=emulation_env_config)
        mock_get_kafka_managers_ports.assert_called_once_with(emulation_env_config=emulation_env_config)
        assert result.ips == ["172.17.0.1"]
        assert result.ports == [5601]
        assert result.execution_id == 10
        assert result.emulation_name == "test_emulation"
