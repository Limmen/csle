from unittest.mock import patch, MagicMock
from csle_common.controllers.users_controller import UsersController


class TestUsersControllerSuite:
    """
    Test UsersController
    """

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.disconnect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    def test_create_users(self, mock_execute_ssh_cmd, mock_disconnect_admin, mock_connect_admin) -> None:
        """
        Test method that creates users in an emulation environment according to a specified users-configuration

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_disconnect_admin: mock_disconnect_admin
        :param mock_connect_admin: mock_connect_admin
        :return: None
        """
        logger = MagicMock()
        user1 = MagicMock(username="user1", pw="password1", root=False)
        user2 = MagicMock(username="user2", pw="password2", root=True)
        users_conf = MagicMock(
            physical_host_ip="192.168.1.1", docker_gw_bridge_ip="192.168.1.2", users=[user1, user2])
        cred1 = MagicMock(username="cred1", pw="password1", root=False)
        cred2 = MagicMock(username="cred2", pw="password2", root=True)
        vuln_conf = MagicMock(
            physical_host_ip="192.168.1.1", docker_gw_bridge_ip="192.168.1.3", credentials=[cred1, cred2])
        emulation_env_config = MagicMock()
        emulation_env_config.users_config.users_configs = [users_conf]
        emulation_env_config.vuln_config.node_vulnerability_configs = [vuln_conf]
        emulation_env_config.connections = {"192.168.1.2": MagicMock(), "192.168.1.3": MagicMock()}

        physical_server_ip = "192.168.1.1"
        mock_execute_ssh_cmd.side_effect = [
            (b"user1\nuser2\n", "", 0),  # output of ls /home
            ("", "", 0),  # output of deluser user1
            ("", "", 0),  # output of rm -rf /home/user1
            ("", "", 0),  # output of deluser user2
            ("", "", 0),  # output of rm -rf /home/user2
            ("", "", 0),  # output of useradd for user1
            ("", "", 0),  # output of useradd for user2
            ("", "", 0),  # output of useradd for cred1
            ("", "", 0),  # output of useradd for cred2
        ]

        UsersController.create_users(emulation_env_config, physical_server_ip, logger)
        mock_connect_admin.assert_any_call(emulation_env_config=emulation_env_config, ip="192.168.1.2")
        mock_connect_admin.assert_any_call(emulation_env_config=emulation_env_config, ip="192.168.1.3")
        mock_execute_ssh_cmd.assert_called()
        mock_disconnect_admin.assert_called()
