from unittest.mock import patch, MagicMock
import csle_common.constants.constants as constants
from csle_common.controllers.topology_controller import TopologyController


class TestTopologyControllerSuite:
    """
    Test suite for topology controller
    """

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("csle_common.util.emulation_util.EmulationUtil.disconnect_admin")
    def test_create_topology(self, mock_disconnect_admin, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test the utility function for connecting to a running emulation and creating the configuration

        :param mock_disconnect_admin: mock_disconnect_admin
        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :return: None
        """
        logger = MagicMock()
        # configure mock route and firewall
        mock_route = ("192.168.0.0/24", "192.168.1.1")
        mock_fw_config = MagicMock()
        mock_fw_config.physical_host_ip = "192.168.1.100"
        mock_fw_config.docker_gw_bridge_ip = "10.0.0.1"
        mock_fw_config.routes = [mock_route]
        mock_fw_config.ips_gw_default_policy_networks = []
        mock_fw_config.output_accept = []
        mock_fw_config.input_accept = []
        mock_fw_config.forward_accept = []
        mock_fw_config.output_drop = []
        mock_fw_config.input_drop = []
        mock_fw_config.forward_drop = []
        node_configs = [mock_fw_config]
        # configure mock topology and kafka
        topology_config = MagicMock()
        topology_config.node_configs = node_configs
        kafka_config = MagicMock()
        kafka_config.firewall_config = mock_fw_config
        # configure mock emulation environment
        emulation_env_config = MagicMock()
        emulation_env_config.topology_config = topology_config
        emulation_env_config.kafka_config = kafka_config
        emulation_env_config.sdn_controller_config = None
        emulation_env_config.get_connection.return_value = MagicMock()
        emulation_env_config.execution_id = "test_execution_id"
        emulation_env_config.level = "test_level"
        # set return values of execute_ssh_cmd
        mock_execute_ssh_cmd.return_value = (b"", b"", 0)
        TopologyController.create_topology(
            emulation_env_config=emulation_env_config, physical_server_ip="192.168.1.100", logger=logger)
        mock_connect_admin.assert_called()
        expected_cmd = f"{constants.COMMANDS.SUDO_ADD_ROUTE} 192.168.0.0/24 gw 192.168.1.1"
        mock_execute_ssh_cmd.assert_any_call(
            cmd=expected_cmd, conn=emulation_env_config.get_connection.return_value, wait_for_completion=True)
        mock_disconnect_admin.assert_called()
        logger.info.assert_any_call("Creating topology")
        logger.info.assert_any_call("Connecting to node:10.0.0.1")
        logger.info.assert_any_call(f"Adding route: {expected_cmd} to routing table of node: 10.0.0.1")
