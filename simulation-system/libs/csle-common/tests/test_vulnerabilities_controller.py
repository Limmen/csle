from unittest.mock import patch, MagicMock
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.vulnerability_type import VulnType
from csle_common.controllers.vulnerabilities_controller import VulnerabilitiesController


class TestVulnControllerSuite:
    """
    Test VulnerabilitiesController
    """

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    def test_create_vulns(self, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test method that creates vulnerabilities in an emulation environment

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :return: None
        """
        logger = MagicMock()
        credential = MagicMock(username="testuser")
        vuln = MagicMock(
            physical_host_ip="192.168.1.1", docker_gw_bridge_ip="192.168.1.2", vuln_type=VulnType.PRIVILEGE_ESCALATION,
            cve=constants.EXPLOIT_VULNERABILITES.CVE_2010_0426, credentials=[credential])
        emulation_env_config = MagicMock()
        emulation_env_config.vuln_config.node_vulnerability_configs = [vuln]
        emulation_env_config.connections = {"192.168.1.2": MagicMock()}
        physical_server_ip = "192.168.1.1"
        mock_execute_ssh_cmd.side_effect = [
            ("", "", 0),  # output of cp /etc/sudoers.bak /etc/sudoers
            ("", "", 0),  # output of adding CVE entry to sudoers
            ("", "", 0),  # output of chmod 440 /etc/sudoers
        ]
        VulnerabilitiesController.create_vulns(emulation_env_config, physical_server_ip, logger)
        mock_connect_admin.assert_any_call(emulation_env_config=emulation_env_config, ip="192.168.1.2")
        mock_execute_ssh_cmd.assert_called()
