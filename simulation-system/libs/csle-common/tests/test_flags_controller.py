import logging
from unittest.mock import MagicMock, patch
from csle_common.controllers.flags_controller import FlagsController
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.node_flags_config import NodeFlagsConfig
from csle_common.dao.emulation_config.flag import Flag


class TestFlagsControllerSuite:
    """
    Test suite for flags controller
    """

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("csle_common.util.emulation_util.EmulationUtil.disconnect_admin")
    def test_create_flags(self, mock_disconnect_admin, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test case for creating flags using the FlagsController

        :param mock_disconnect_admin: Mocked disconnect_admin method
        :param mock_execute_ssh_cmd: Mocked execute_ssh_cmd method
        :param mock_connect_admin: Mocked connect_admin
        :return: None
        """
        emulation_env_config = MagicMock(spec=EmulationEnvConfig)
        flags_config = MagicMock()
        emulation_env_config.flags_config = flags_config
        flags_config.node_flag_configs = [
            NodeFlagsConfig(
                ip="10.0.0.1",
                docker_gw_bridge_ip="172.17.0.1",
                physical_host_ip="192.168.0.1",
                flags=[
                    Flag(name="flag1", dir="/dir1", id=1, path="/path/to/flag1"),
                    Flag(name="flag2", dir="/dir2", id=2, path="/path/to/flag2"),
                ]
            )
        ]
        logger = MagicMock(spec=logging.Logger)
        physical_server_ip = "192.168.0.1"
        FlagsController.create_flags(emulation_env_config, physical_server_ip, logger)
        mock_connect_admin.assert_called_once_with(emulation_env_config=emulation_env_config, ip="172.17.0.1")
        mock_disconnect_admin.assert_called_once_with(emulation_env_config=emulation_env_config)
        mock_execute_ssh_cmd.assert_called()
