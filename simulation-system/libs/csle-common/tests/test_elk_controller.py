import logging
from unittest.mock import MagicMock, patch
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.controllers.elk_controller import ELKController
import csle_common.constants.constants as constants
import csle_collector.elk_manager.elk_manager_pb2_grpc
import csle_collector.elk_manager.elk_manager_pb2
import csle_collector.elk_manager.query_elk_manager
import csle_collector.elk_manager.elk_manager_util


class TestElkControllerSuite:
    """
    Test suite for elk controller
    """

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_start_stop_elk_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test case for starting or stopping the ELK manager

        :param mock_disconnect_admin: Mocked disconnect_admin method
        :param mock_execute_ssh_cmd: Mocked execute_ssh_cmd method
        :param mock_connect_admin: Mocked connect_admin
        :param mock_sleep: Mocked sleep method
        :return: None
        """
        mock_connect_admin.return_value = None
        mock_execute_ssh_cmd.return_value = ("output", "error", 0)
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.elk_config.get_connection.return_value = MagicMock()
        logger = MagicMock(spec=logging.Logger)
        ELKController.start_elk_manager(emulation_env_config, logger)
        mock_connect_admin.assert_called_once_with(emulation_env_config=emulation_env_config, ip="172.17.0.1",
                                                   create_producer=False)
        mock_execute_ssh_cmd.assert_called()
        ELKController.stop_elk_manager(emulation_env_config, logger)
        assert 2 == mock_connect_admin.call_count
        assert 4 == mock_execute_ssh_cmd.call_count

    @patch("csle_common.controllers.elk_controller.ELKController.start_elk_manager")
    @patch("csle_common.controllers.elk_controller.ELKController.get_elk_status_by_port_and_ip")
    def test_get_elk_status(self, mock_get_elk_status_by_port_and_ip, mock_start_elk_manager) -> None:
        """
        Test case for querying the ELKManager about the status of the ELK stack

        :param mock_get_elk_status_by_port_and_ip: mocked get_elk_status_by_port_and_ip method
        :param mock_start_elk_manager: mocked start_elk_manager method
        """
        mock_start_elk_manager.return_value = None
        expected_elk_dto = MagicMock(spec=csle_collector.elk_manager.elk_manager_pb2.ElkDTO)
        mock_get_elk_status_by_port_and_ip.return_value = expected_elk_dto
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.elk_config.elk_manager_port = 5601
        logger = MagicMock(spec=logging.Logger)
        result = ELKController.get_elk_status(emulation_env_config, logger)
        mock_start_elk_manager.assert_called_once_with(emulation_env_config=emulation_env_config, logger=logger)
        mock_get_elk_status_by_port_and_ip.assert_called_once_with(ip="172.17.0.1", port=5601)
        assert result == expected_elk_dto

    @patch("csle_collector.elk_manager.query_elk_manager.get_elk_status")
    @patch("csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub")
    @patch("grpc.insecure_channel")
    def test_get_elk_status_by_port_and_ip(self, mock_insecure_channel, mock_ElkManagerStub, mock_get_elk_status) \
            -> None:
        """
        Test case for querying the ElkManager about the status of the ELK stack

        :param mock_insecure_channel: mocked insecure_channel method
        :param mock_ElkManagerStub: mocked ElkManagerStub method
        :param mock_get_elk_status: mocked get_elk_status method
        """
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_ElkManagerStub.return_value = mock_stub
        expected_elk_dto = MagicMock(spec=csle_collector.elk_manager.elk_manager_pb2.ElkDTO)
        mock_get_elk_status.return_value = expected_elk_dto
        ip = "172.17.0.1"
        port = 5601
        result = ELKController.get_elk_status_by_port_and_ip(ip, port)
        mock_insecure_channel.assert_called_once_with(f"{ip}:{port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_ElkManagerStub.assert_called_once_with(mock_channel)
        mock_get_elk_status.assert_called_once_with(mock_stub)
        assert result == expected_elk_dto

    @patch("csle_collector.elk_manager.query_elk_manager.stop_elk")
    @patch("csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub")
    @patch("grpc.insecure_channel")
    @patch("csle_common.controllers.elk_controller.ELKController.start_elk_manager")
    def test_stop_elk_stack(self, mock_start_elk_manager, mock_insecure_channel, mock_ElkManagerStub, mock_stop_elk) \
            -> None:
        """
        Test case for requesting the ELKManager to stop the ELK server

        :param mock_start_elk_manager: mocked start_elk_manager method
        :param mock_insecure_channel: mocked insecure_channel method
        :param mock_ElkManagerStub: mocked ElkManagerStub
        :param mock_stop_elk: mocked stop_elk method
        """
        mock_start_elk_manager.return_value = None
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_ElkManagerStub.return_value = mock_stub
        expected_elk_dto = MagicMock(spec=csle_collector.elk_manager.elk_manager_pb2.ElkDTO)
        mock_stop_elk.return_value = expected_elk_dto
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.elk_config.elk_manager_port = 5601
        logger = MagicMock(spec=logging.Logger)
        result = ELKController.stop_elk_stack(emulation_env_config, logger)
        mock_insecure_channel.assert_called_once_with("172.17.0.1:5601", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_ElkManagerStub.assert_called_once_with(mock_channel)
        mock_stop_elk.assert_called_once_with(mock_stub)
        assert result == expected_elk_dto

    @patch("csle_collector.elk_manager.query_elk_manager.start_elk")
    @patch("csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub")
    @patch("grpc.insecure_channel")
    @patch("csle_common.controllers.elk_controller.ELKController.start_elk_manager")
    def test_start_elk_stack(self, mock_start_elk_manager, mock_insecure_channel, mock_ElkManagerStub,
                             mock_start_elk) -> None:
        """
        Test case for requesting the ELKManager to start the ELK server

        :param mock_start_elk_manager: mocked start_elk_manager method
        :param mock_insecure_channel: mocked insecure_channel method
        :param mock_ElkManagerStub: mocked ElkManagerStub
        :param mock_start_elk: mocked start_elk method
        """
        mock_start_elk_manager.return_value = None
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_ElkManagerStub.return_value = mock_stub
        expected_elk_dto = MagicMock(spec=csle_collector.elk_manager.elk_manager_pb2.ElkDTO)
        mock_start_elk.return_value = expected_elk_dto
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.elk_config.container.physical_host_ip = "192.168.0.1"
        emulation_env_config.elk_config.elk_manager_port = 5601
        logger = MagicMock(spec=logging.Logger)
        physical_server_ip = "192.168.0.1"
        result = ELKController.start_elk_stack(emulation_env_config, physical_server_ip, logger)
        mock_insecure_channel.assert_called_once_with("172.17.0.1:5601", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_ElkManagerStub.assert_called_once_with(mock_channel)
        mock_start_elk.assert_called_once_with(mock_stub)
        assert result == expected_elk_dto

    @patch("csle_collector.elk_manager.query_elk_manager.start_elastic")
    @patch("csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub")
    @patch("grpc.insecure_channel")
    @patch("csle_common.controllers.elk_controller.ELKController.start_elk_manager")
    def test_start_elastic(self, mock_start_elk_manager, mock_insecure_channel, mock_ElkManagerStub,
                           mock_start_elastic) -> None:
        """
        Test case for requesting the ELKManager to start elasticsearch

        :param mock_start_elk_manager: mocked start_elk_manager method
        :param mock_insecure_channel: mocked insecure_channel method
        :param mock_ElkManagerStub: mocked ElkManagerStub
        :param mock_start_elastic: mocked start_elastic method
        """
        mock_start_elk_manager.return_value = None
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_ElkManagerStub.return_value = mock_stub
        expected_elk_dto = MagicMock(spec=csle_collector.elk_manager.elk_manager_pb2.ElkDTO)
        mock_start_elastic.return_value = expected_elk_dto
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.elk_config.elk_manager_port = 5601
        logger = MagicMock(spec=logging.Logger)
        result = ELKController.start_elastic(emulation_env_config, logger)
        mock_insecure_channel.assert_called_once_with("172.17.0.1:5601", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_ElkManagerStub.assert_called_once_with(mock_channel)
        mock_start_elastic.assert_called_once_with(mock_stub)
        assert result == expected_elk_dto

    @patch("csle_collector.elk_manager.query_elk_manager.start_kibana")
    @patch("csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub")
    @patch("grpc.insecure_channel")
    @patch("csle_common.controllers.elk_controller.ELKController.start_elk_manager")
    def test_start_kibana(self, mock_start_elk_manager, mock_insecure_channel, mock_ElkManagerStub,
                          mock_start_kibana) -> None:
        """
        Test case for requesting the ELKManager to start kibana

        :param mock_start_elk_manager: mocked start_elk_manager method
        :param mock_insecure_channel: mocked insecure_channel method
        :param mock_ElkManagerStub: mocked ElkManagerStub
        :param mock_start_kibana: mocked start_kibana method
        """
        mock_start_elk_manager.return_value = None
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_ElkManagerStub.return_value = mock_stub
        expected_elk_dto = MagicMock(spec=csle_collector.elk_manager.elk_manager_pb2.ElkDTO)
        mock_start_kibana.return_value = expected_elk_dto
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.elk_config.elk_manager_port = 5601
        logger = MagicMock(spec=logging.Logger)
        result = ELKController.start_kibana(emulation_env_config, logger)
        mock_insecure_channel.assert_called_once_with("172.17.0.1:5601", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_ElkManagerStub.assert_called_once_with(mock_channel)
        mock_start_kibana.assert_called_once_with(mock_stub)
        assert result == expected_elk_dto

    @patch("csle_collector.elk_manager.query_elk_manager.start_logstash")
    @patch("csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub")
    @patch("grpc.insecure_channel")
    @patch("csle_common.controllers.elk_controller.ELKController.start_elk_manager")
    def test_start_logstash(self, mock_start_elk_manager, mock_insecure_channel, mock_ElkManagerStub,
                            mock_start_logstash) -> None:
        """
        Test case for requesting the ELKManager to start logstash

        :param mock_start_elk_manager: mocked start_elk_manager method
        :param mock_insecure_channel: mocked insecure_channel method
        :param mock_ElkManagerStub: mocked ElkManagerStub
        :param mock_start_logstash: mocked start_logstash method
        """
        mock_start_elk_manager.return_value = None
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_ElkManagerStub.return_value = mock_stub
        expected_elk_dto = MagicMock(spec=csle_collector.elk_manager.elk_manager_pb2.ElkDTO)
        mock_start_logstash.return_value = expected_elk_dto
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.elk_config.elk_manager_port = 5601
        logger = MagicMock(spec=logging.Logger)
        result = ELKController.start_logstash(emulation_env_config, logger)
        mock_insecure_channel.assert_called_once_with("172.17.0.1:5601", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_ElkManagerStub.assert_called_once_with(mock_channel)
        mock_start_logstash.assert_called_once_with(mock_stub)
        assert result == expected_elk_dto

    @patch("csle_collector.elk_manager.query_elk_manager.stop_elastic")
    @patch("csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub")
    @patch("grpc.insecure_channel")
    @patch("csle_common.controllers.elk_controller.ELKController.start_elk_manager")
    def test_stop_elastic(self, mock_start_elk_manager, mock_insecure_channel, mock_ElkManagerStub,
                          mock_stop_elastic) -> None:
        """
        Test case for requesting the ELKManager to stop elasticsearch

        :param mock_start_elk_manager: mocked start_elk_manager method
        :param mock_insecure_channel: mocked insecure_channel method
        :param mock_ElkManagerStub: mocked ElkManagerStub
        :param mock_stop_elastic: mocked stop_elastic method
        """
        mock_start_elk_manager.return_value = None
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_ElkManagerStub.return_value = mock_stub
        expected_elk_dto = MagicMock(spec=csle_collector.elk_manager.elk_manager_pb2.ElkDTO)
        mock_stop_elastic.return_value = expected_elk_dto
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.elk_config.elk_manager_port = 5601
        logger = MagicMock(spec=logging.Logger)
        result = ELKController.stop_elastic(emulation_env_config, logger)
        mock_insecure_channel.assert_called_once_with("172.17.0.1:5601", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_ElkManagerStub.assert_called_once_with(mock_channel)
        mock_stop_elastic.assert_called_once_with(mock_stub)
        assert result == expected_elk_dto

    @patch("csle_collector.elk_manager.query_elk_manager.stop_kibana")
    @patch("csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub")
    @patch("grpc.insecure_channel")
    @patch("csle_common.controllers.elk_controller.ELKController.start_elk_manager")
    def test_stop_kibana(self, mock_start_elk_manager, mock_insecure_channel, mock_ElkManagerStub,
                         mock_stop_kibana) -> None:
        """
        Test case for requesting the ELKManager to stop kibana

        :param mock_start_elk_manager: mocked start_elk_manager method
        :param mock_insecure_channel: mocked insecure_channel method
        :param mock_ElkManagerStub: mocked ElkManagerStub
        :param mock_stop_kibana: mocked stop_kibana method
        """
        mock_start_elk_manager.return_value = None
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_ElkManagerStub.return_value = mock_stub
        expected_elk_dto = MagicMock(spec=csle_collector.elk_manager.elk_manager_pb2.ElkDTO)
        mock_stop_kibana.return_value = expected_elk_dto
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.elk_config.elk_manager_port = 5601
        logger = MagicMock(spec=logging.Logger)
        result = ELKController.stop_kibana(emulation_env_config, logger)
        mock_insecure_channel.assert_called_once_with("172.17.0.1:5601", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_ElkManagerStub.assert_called_once_with(mock_channel)
        mock_stop_kibana.assert_called_once_with(mock_stub)
        assert result == expected_elk_dto

    @patch("csle_collector.elk_manager.query_elk_manager.stop_logstash")
    @patch("csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerStub")
    @patch("grpc.insecure_channel")
    @patch("csle_common.controllers.elk_controller.ELKController.start_elk_manager")
    def test_stop_logstash(self, mock_start_elk_manager, mock_insecure_channel, mock_ElkManagerStub,
                           mock_stop_logstash) -> None:
        """
        Test case for requesting the ELKManager to stop logstash

        :param mock_start_elk_manager: mocked start_elk_manager method
        :param mock_insecure_channel: mocked insecure_channel method
        :param mock_ElkManagerStub: mocked ElkManagerStub
        :param mock_stop_logstash: mocked stop_logstash method
        """
        mock_start_elk_manager.return_value = None
        mock_channel = MagicMock()
        mock_insecure_channel.return_value.__enter__.return_value = mock_channel
        mock_stub = MagicMock()
        mock_ElkManagerStub.return_value = mock_stub
        expected_elk_dto = MagicMock(spec=csle_collector.elk_manager.elk_manager_pb2.ElkDTO)
        mock_stop_logstash.return_value = expected_elk_dto
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.elk_config.elk_manager_port = 5601
        logger = MagicMock(spec=logging.Logger)
        result = ELKController.stop_logstash(emulation_env_config, logger)
        mock_insecure_channel.assert_called_once_with("172.17.0.1:5601", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        mock_ElkManagerStub.assert_called_once_with(mock_channel)
        mock_stop_logstash.assert_called_once_with(mock_stub)
        assert result == expected_elk_dto

    def test_get_elk_managers_ips(self) -> None:
        """
        Test case for extracting the IPS of the ELK managers in a given emulation
        """
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "172.17.0.1"
        result = ELKController.get_elk_managers_ips(emulation_env_config)
        assert result == ["172.17.0.1"]

    def test_get_elk_managers_ports(self) -> None:
        """
        Test case for extracting the ports of the ELK managers in a given emulation
        """
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.elk_manager_port = 5601
        result = ELKController.get_elk_managers_ports(emulation_env_config)
        assert result == [5601]

    @patch("csle_common.controllers.elk_controller.ELKController.get_elk_managers_ips")
    @patch("csle_common.controllers.elk_controller.ELKController.get_elk_managers_ports")
    @patch("csle_common.controllers.elk_controller.ELKController.get_elk_status_by_port_and_ip")
    @patch("csle_collector.elk_manager.elk_manager_util.ElkManagerUtil.elk_dto_empty")
    def test_get_elk_managers_infos(self, mock_elk_dto_empty, mock_get_elk_status_by_port_and_ip,
                                    mock_get_elk_managers_ports, mock_get_elk_managers_ips) -> None:
        """
        Test case for extracting the infomation of the ELK managers for a given emulation

        :param mock_elk_dto_empty: mocked elk_dto_empty method
        :param mock_get_elk_status_by_port_and_ip: mocked get_elk_status_by_port_and_ip method
        :param mock_get_elk_managers_ports: mocked get_elk_managers_ports
        :param mock_get_elk_managers_ips: mocked get_elk_managers_ips
        """
        mock_get_elk_managers_ips.return_value = ["172.17.0.1"]
        mock_get_elk_managers_ports.return_value = [5601]
        mock_elk_status = MagicMock()
        mock_get_elk_status_by_port_and_ip.return_value = mock_elk_status
        mock_elk_dto_empty.return_value = MagicMock()
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        elk_config = MagicMock()
        emulation_env_config.elk_config = elk_config
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "172.17.0.1"
        emulation_env_config.elk_config.elk_manager_port = 5601
        emulation_env_config.execution_id = 1
        emulation_env_config.name = "test_emulation"
        logger = MagicMock(spec=logging.Logger)
        active_ips = ["172.17.0.1"]
        physical_host_ip = "192.168.0.1"
        result = ELKController.get_elk_managers_info(emulation_env_config, active_ips, logger, physical_host_ip)
        mock_get_elk_managers_ips.assert_called_once_with(emulation_env_config=emulation_env_config)
        mock_get_elk_managers_ports.assert_called_once_with(emulation_env_config=emulation_env_config)
        assert result.ips == ["172.17.0.1"]
        assert result.ports == [5601]
        assert result.execution_id == 1
        assert result.emulation_name == "test_emulation"
