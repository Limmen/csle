from unittest.mock import patch, MagicMock
from csle_common.util.connection_util import ConnectionUtil
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state import (
    EmulationConnectionObservationState,
)
import csle_common.constants.constants as constants


class TestConnectionUtilSuite:
    """
    Test suite for connection_util
    """

    @patch("paramiko.SSHClient")
    def test_ssh_setup_connection(self, mock_SSHClient) -> None:
        """
        Test the helper function for setting up a SSH connection

        :param mock_SSHClient: mock_SSHClient
        :return: None
        """
        mock_ssh_client = MagicMock()
        mock_SSHClient.return_value = mock_ssh_client
        mock_transport = MagicMock()
        mock_relay_channel = MagicMock()
        mock_ssh_client.get_transport.return_value = mock_transport
        mock_transport.open_channel.return_value = mock_relay_channel
        a = MagicMock()
        a.ips = ["192.168.1.2"]
        a.ips_match.side_effect = lambda ips: True
        credentials = [MagicMock()]
        credentials[0].service = constants.SSH.SERVICE_NAME
        credentials[0].username = "user"
        credentials[0].pw = "password"
        credentials[0].port = 22
        proxy_connections = [MagicMock()]
        proxy_connections[0].ip = "192.168.1.1"
        proxy_connections[0].conn.get_transport.return_value = mock_transport
        s = MagicMock()
        s.emulation_env_config.containers_config.agent_ip = "192.168.1.3"
        s.attacker_obs_state.agent_reachable = ["192.168.1.1"]
        result = ConnectionUtil._ssh_setup_connection(a=a, credentials=credentials,
                                                      proxy_connections=proxy_connections, s=s)
        mock_SSHClient.assert_not_called()
        assert result

    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_ssh_finalize_connection(self, mock_sleep, mock_execute_ssh_cmd) -> None:
        """
        Test the helper function for finalizing a SSH connection and setting up the DTO

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_sleep: mock_sleep
        :return: None
        """
        mock_execute_ssh_cmd.side_effect = [
            (b"output", b"error", 0.1),
            (b"output", b"error", 0.1),
            (b"output", b"error", 0.1),
            (b"output", b"error", 0.1),
            (b"(ALL) NOPASSWD: ALL", b"", 0.1),
        ]
        target_machine = MagicMock()
        connection_setup_dto = MagicMock()
        connection_setup_dto.target_connections = [MagicMock()]
        connection_setup_dto.credentials = [MagicMock()]
        connection_setup_dto.credentials[0].username = "user"
        connection_setup_dto.ports = [22]
        connection_setup_dto.proxies = [MagicMock()]
        connection_setup_dto.ip = "192.168.1.2"

        root, total_time = ConnectionUtil._ssh_finalize_connection(
            target_machine=target_machine, connection_setup_dto=connection_setup_dto, i=0
        )
        assert not root
        assert total_time
        mock_execute_ssh_cmd.assert_called()

    @patch("telnetlib.Telnet")
    @patch("time.sleep", return_value=None)
    def test_telnet_setup_connection(self, mock_sleep, mock_telnet) -> None:
        """
        Test the helper function for setting up a Telnet connection to a target machine

        :param mock_telnet: mock_telnet
        :param mock_sleep: mock_sleep
        :return: None
        """
        mock_telnet_conn = MagicMock()
        mock_telnet.return_value = mock_telnet_conn
        mock_telnet_conn.read_until.side_effect = [constants.TELNET.LOGIN_PROMPT, constants.TELNET.PASSWORD_PROMPT,
                                                   constants.TELNET.PROMPT]
        mock_telnet_conn.write.return_value = None
        mock_telnet_conn.read_until.return_value = b"$"
        a = MagicMock()
        a.ips = ["192.168.1.2"]
        a.ips_match.side_effect = lambda ips: True
        credentials = [MagicMock()]
        credentials[0].service = constants.TELNET.SERVICE_NAME
        credentials[0].username = "user"
        credentials[0].pw = "password"
        credentials[0].port = 23
        proxy_connections = [MagicMock()]
        proxy_connections[0].ip = "192.168.1.1"
        proxy_connections[0].conn.get_transport.return_value = MagicMock()
        s = MagicMock()
        s.emulation_env_config.containers_config.agent_ip = "192.168.1.3"
        s.attacker_obs_state.agent_reachable = ["192.168.1.1"]
        s.get_attacker_machine.return_value.reachable = ["192.168.1.2"]
        s.emulation_env_config.get_port_forward_port.return_value = 9999

        result = ConnectionUtil._telnet_setup_connection(
            a=a, credentials=credentials, proxy_connections=proxy_connections, s=s)
        mock_telnet.assert_called()
        assert result

    @patch("time.sleep", return_value=None)
    def test_telnet_finalize_connection(self, mock_sleep) -> None:
        """
        Test the helper function for finalizing a Telnet connection to a target machine and creating the DTO

        :param mock_sleep: mock_sleep
        :return: None
        """
        target_machine = MagicMock()
        connection_setup_dto = MagicMock()
        mock_telnet_conn = [MagicMock() for _ in range(constants.ENV_CONSTANTS.ATTACKER_RETRY_CHECK_ROOT)]
        connection_setup_dto.target_connections = mock_telnet_conn
        connection_setup_dto.credentials = [
            MagicMock() for _ in range(constants.ENV_CONSTANTS.ATTACKER_RETRY_CHECK_ROOT)]
        for credential in connection_setup_dto.credentials:
            credential.username = "user"
        connection_setup_dto.tunnel_threads = [
            MagicMock() for _ in range(constants.ENV_CONSTANTS.ATTACKER_RETRY_CHECK_ROOT)]
        connection_setup_dto.forward_ports = [9999 for _ in range(constants.ENV_CONSTANTS.ATTACKER_RETRY_CHECK_ROOT)]
        connection_setup_dto.ports = [23 for _ in range(constants.ENV_CONSTANTS.ATTACKER_RETRY_CHECK_ROOT)]
        connection_setup_dto.proxies = [MagicMock() for _ in range(constants.ENV_CONSTANTS.ATTACKER_RETRY_CHECK_ROOT)]
        connection_setup_dto.ip = "192.168.1.2"

        for i, conn in enumerate(mock_telnet_conn):
            conn.read_until.side_effect = [b"user may not run sudo" if i < 4 else b"(ALL) NOPASSWD: ALL"]

        root, total_time = ConnectionUtil._telnet_finalize_connection(
            target_machine=target_machine, i=0, connection_setup_dto=connection_setup_dto)
        assert not root
        assert total_time

    @patch("ftplib.FTP")
    def test_ftp_setup_connection(self, mock_ftp) -> None:
        """
        Test the helper function for setting up a FTP connection

        :param mock_ftp: mock_ftp
        :return: None
        """
        mock_ftp_conn = MagicMock()
        mock_ftp.return_value = mock_ftp_conn
        mock_ftp_conn.login.return_value = "230 Login successful."

        a = MagicMock()
        a.ips = ["192.168.1.2"]
        a.ips_match.side_effect = lambda ips: True

        credentials = [MagicMock()]
        credentials[0].service = constants.FTP.SERVICE_NAME
        credentials[0].username = "user"
        credentials[0].pw = "password"
        credentials[0].port = 21

        proxy_connections = [MagicMock()]
        proxy_connections[0].ip = "192.168.1.1"
        proxy_connections[0].conn.get_transport.return_value = MagicMock()
        proxy_connections[0].conn.invoke_shell.return_value = MagicMock()

        s = MagicMock()
        s.emulation_env_config.containers_config.agent_ip = "192.168.1.3"
        s.attacker_obs_state.agent_reachable = ["192.168.1.1"]
        s.get_attacker_machine.return_value.reachable = ["192.168.1.2"]
        s.emulation_env_config.get_port_forward_port.return_value = 9999

        result = ConnectionUtil._ftp_setup_connection(
            a=a, credentials=credentials, proxy_connections=proxy_connections, s=s)
        mock_ftp.assert_not_called()
        assert result

    def test_ftp_finalize_connection(self) -> None:
        """
        Test helper function for creating the connection DTO for FTP

        :return: None
        """
        target_machine = MagicMock()
        target_machine.ftp_connections = []

        connection_setup_dto = MagicMock()
        connection_setup_dto.target_connections = [MagicMock()]
        connection_setup_dto.credentials = [MagicMock()]
        connection_setup_dto.tunnel_threads = [MagicMock()]
        connection_setup_dto.forward_ports = [9999]
        connection_setup_dto.ports = [21]
        connection_setup_dto.interactive_shells = [MagicMock()]
        connection_setup_dto.proxies = [MagicMock()]
        connection_setup_dto.ip = "192.168.1.2"

        root, cost = ConnectionUtil._ftp_finalize_connection(
            target_machine=target_machine, i=0, connection_setup_dto=connection_setup_dto)
        assert not root
        assert cost == 0

    def test__find_jump_host_connection(self) -> None:
        """
        Test utility function for finding a jump-host from the set of compromised machines to reach a target IP

        :return: None
        """
        ip = "192.168.1.100"
        s = MagicMock()
        s.attacker_obs_state = MagicMock()
        s.attacker_obs_state.agent_reachable = ["192.168.1.100"]
        s.emulation_env_config.containers_config.agent_ip = "192.168.1.1"
        s.emulation_env_config.get_hacker_connection.return_value = MagicMock()

        result = ConnectionUtil.find_jump_host_connection(ip=ip, s=s)
        assert result.ip == "192.168.1.1"
        assert result.root

    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    def test_test_connection(self, mock_execute_ssh_cmd) -> None:
        """
        Test utility function for testing if a connection is alive or not

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :return: None
        """
        mock_conn = MagicMock()
        mock_execute_ssh_cmd.return_value = (b"user", b"", 0.1)
        c = EmulationConnectionObservationState(
            conn=mock_conn, credential=MagicMock(), root=False, service="ssh", port=22)
        result = ConnectionUtil.test_connection(c=c)
        assert result

    @patch("paramiko.SSHClient")
    def test_reconnect_ssh(self, mock_SSHClient) -> None:
        """
        Test the method that reconnects the given SSH connection if it has died for some reason

        :param mock_SSHClient: mock_SSHClient

        :return: None
        """
        mock_credential = MagicMock()
        mock_credential.username = "user"
        mock_credential.pw = "password"
        mock_credential.port = 22

        c = EmulationConnectionObservationState(
            conn=MagicMock(), credential=mock_credential, root=False, service="ssh", port=22, ip="192.168.1.2")
        mock_ssh_client = mock_SSHClient.return_value
        mock_transport = MagicMock()
        mock_ssh_client.get_transport.return_value = mock_transport

        result = ConnectionUtil.reconnect_ssh(c)
        assert result.conn == mock_ssh_client

    @patch("csle_common.util.connection_util.ConnectionUtil.reconnect_ssh")
    @patch("telnetlib.Telnet")
    def test_reconnect_telnet(self, mock_telnet, mock_reconnect_ssh) -> None:
        """
        Test the method that reconnects the given Telnet connection if it has died for some reason

        :param mock_telnet: mock_telnet
        :param mock_reconnect_ssh: mock_reconnect_ssh
        :return: None
        """
        mock_credential = MagicMock()
        mock_credential.username = "user"
        mock_credential.pw = "password"

        mock_proxy_conn = MagicMock()
        proxy = EmulationConnectionObservationState(
            conn=mock_proxy_conn, credential=mock_credential, root=False, service="ssh", port=22, ip="192.168.1.1")
        c = EmulationConnectionObservationState(
            conn=None, credential=mock_credential, root=False, service="telnet", port=23, ip="192.168.1.2", proxy=proxy)

        mock_telnet_conn = mock_telnet.return_value
        mock_telnet_conn.read_until.side_effect = [constants.TELNET.LOGIN_PROMPT, constants.TELNET.PASSWORD_PROMPT,
                                                   constants.TELNET.PROMPT]
        mock_reconnect_ssh.return_value = proxy
        result = ConnectionUtil.reconnect_telnet(c)
        assert result.conn == mock_telnet_conn
