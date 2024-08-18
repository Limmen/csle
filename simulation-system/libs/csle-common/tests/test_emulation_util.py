from unittest.mock import patch, MagicMock
from csle_common.util.emulation_util import EmulationUtil
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state import (
    EmulationConnectionObservationState,
)
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType


class TestEmulationUtilSuite:
    """
    Test suite for emulation_util
    """

    @patch("csle_common.util.ssh_util.SSHUtil.execute_ssh_cmds")
    def test_execute_ssh_cmds(self, mock_execute_ssh_cmds) -> None:
        """
        Test the method that executes a list of commands over an ssh connection to the emulation

        :param mock_execute_ssh_cmds: mock_execute_ssh_cmds
        :return: None
        """
        cmds = ["ls", "pwd", "whoami"]
        mock_conn = MagicMock()
        wait_for_completion = True

        mock_return_value = [(b"file1\nfile2\n", b"", 0.1), (b"/home/user\n", b"", 0.05), (b"user\n", b"", 0.02)]
        mock_execute_ssh_cmds.return_value = mock_return_value
        result = EmulationUtil.execute_ssh_cmds(cmds=cmds, conn=mock_conn, wait_for_completion=wait_for_completion)
        mock_execute_ssh_cmds.assert_called()
        assert result == mock_return_value

    @patch("csle_common.util.ssh_util.SSHUtil.execute_ssh_cmd")
    def test_execute_ssh_cmd(self, mock_execute_ssh_cmd) -> None:
        """
        Test the method that executes an action on the emulation over a ssh connection

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :return: None
        """
        cmd = "ls -l"
        mock_conn = MagicMock()
        wait_for_completion = True
        mock_return_value = (b"file1\nfile2\n", b"", 0.1)
        mock_execute_ssh_cmd.return_value = mock_return_value
        result = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=mock_conn, wait_for_completion=wait_for_completion)
        mock_execute_ssh_cmd.assert_called()
        assert result == mock_return_value

    def test_log_measured_action_time(self) -> None:
        """
        Test the method that logs the measured time of an action to Kafka

        :return: None
        """
        total_time = 6
        action = MagicMock()
        emulation_env_config = MagicMock()
        create_producer = True
        action.to_kafka_record.return_value = "mock_record"
        EmulationUtil.log_measured_action_time(
            total_time=total_time,
            action=action,
            emulation_env_config=emulation_env_config,
            create_producer=create_producer,
        )
        action.to_kafka_record.assert_called()

    @patch("csle_common.util.ssh_util.SSHUtil.execute_ssh_cmd")
    def test_check_if_ssh_server_is_running_ssh(self, mock_execute_ssh_cmd) -> None:
        """
        Test the method that checks if an ssh server is running on the machine

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :return: None
        """
        mock_conn = MagicMock()
        mock_execute_ssh_cmd.return_value = (b"sshd is running", b"", 0.1)
        result = EmulationUtil._check_if_ssh_server_is_running(conn=mock_conn, telnet=False)
        mock_execute_ssh_cmd.assert_called()
        assert result

    @patch("csle_common.util.ssh_util.SSHUtil.execute_ssh_cmd")
    def test_list_all_users_ssh(self, mock_execute_ssh_cmd) -> None:
        """
        Test the method that list all users on a machine

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :return: None
        """
        mock_conn = MagicMock()
        emulation_env_config = MagicMock()
        c = EmulationConnectionObservationState(
            conn=mock_conn, credential=MagicMock(), root=False, service="ssh", port=22, ip="192.168.1.2"
        )
        mock_execute_ssh_cmd.return_value = (b"root\nuser1\nuser2\n", b"", 0.1)
        result = EmulationUtil._list_all_users(c=c, emulation_env_config=emulation_env_config, telnet=False)
        mock_execute_ssh_cmd.assert_called()
        assert result == ["root", "user1", "user2"]

    def test_is_connection_active(self) -> None:
        """
        Test the method that checks if a given connection is active or not

        :return: None
        """
        mock_conn = MagicMock()
        mock_transport = MagicMock()
        mock_transport.is_active.return_value = True
        mock_conn.get_transport.return_value = mock_transport

        result = EmulationUtil.is_connection_active(conn=mock_conn)
        assert result
        mock_conn.get_transport.assert_called()
        mock_transport.is_active.assert_called()

    @patch("paramiko.SSHClient")
    def test_setup_custom_connection(self, mock_SSHClient) -> None:
        """
        Test utility function for setting up a custom SSH connection given credentials and a proxy connection

        :param mock_SSHClient: mock_SSHClient
        :return: None
        """
        user = "user"
        pw = "password"
        source_ip = "192.168.1.1"
        port = 22
        target_ip = "192.168.1.2"
        root = True

        mock_proxy_conn = MagicMock()
        mock_transport = MagicMock()
        mock_proxy_conn.conn.get_transport.return_value = mock_transport

        mock_ssh_client = MagicMock()
        mock_SSHClient.return_value = mock_ssh_client
        mock_relay_channel = MagicMock()
        mock_transport.open_channel.return_value = mock_relay_channel
        mock_transport.is_active.return_value = True

        result = EmulationUtil.setup_custom_connection(
            user=user, pw=pw, source_ip=source_ip, port=port, target_ip=target_ip, proxy_conn=mock_proxy_conn, root=root
        )
        mock_SSHClient.assert_called()
        assert result

    def test_write_remote_file(self) -> None:
        """
        Test utility function for writing contents to a file

        :return: None
        """
        mock_conn = MagicMock()
        mock_sftp_client = MagicMock()
        mock_remote_file = MagicMock()

        mock_conn.open_sftp.return_value = mock_sftp_client
        mock_sftp_client.file.return_value = mock_remote_file

        file_name = "filename.txt"
        contents = "content"
        write_mode = "w"

        EmulationUtil.write_remote_file(conn=mock_conn, file_name=file_name, contents=contents, write_mode=write_mode)
        mock_conn.open_sftp.assert_called()
        mock_sftp_client.file.assert_called()
        mock_remote_file.write.assert_called()
        mock_remote_file.close.assert_called()

    def test_connect_admin(self) -> None:
        """
        Test the method that connects the admin agent

        :return: None
        """
        emulation_env_config = MagicMock()
        ip = "192.168.1.100"
        create_producer = True
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip, create_producer=create_producer)
        assert emulation_env_config.agent_ip == ip
        emulation_env_config.connect.assert_called()

    def test_disconnect_admin(self) -> None:
        """
        Test the method that disconnects the admin agent

        :return: None
        """
        emulation_env_config = MagicMock()
        EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)
        emulation_env_config.close_all_connections.assert_called()

    def test_execute_cmd_interactive_channel(self) -> None:
        """
        Test method that executes an action on the emulation using an interactive shell (non synchronous)

        :return: None
        """
        mock_channel = MagicMock()
        cmd = "ls -la"
        EmulationUtil.execute_cmd_interactive_channel(cmd=cmd, channel=mock_channel)
        mock_channel.send.assert_called()

    @patch("csle_common.util.emulation_util.EmulationUtil.read_result_interactive_channel")
    def test_read_result_interactive(self, mock_read_result_interactive_channel) -> None:
        """
        Test the method that reads the result of an action executed in interactive mode

        :param mock_read_result_interactive_channel: mock_read_result_interactive_channel
        :return: None
        """
        mock_read_result_interactive_channel.return_value = "result"
        emulation_env_config = MagicMock()
        mock_channel = MagicMock()
        result = EmulationUtil.read_result_interactive(emulation_env_config=emulation_env_config, channel=mock_channel)
        assert result == "result"

    def test_read_result_interactive_channel(self) -> None:
        """
        Test the method that reads the result of an action executed in interactive mode

        :return: None
        """
        emulation_env_config = MagicMock()
        mock_channel = MagicMock()
        mock_channel.recv_ready.side_effect = [False, True]
        mock_channel.recv.return_value = b"Mocked result"
        mock_shell_escape = MagicMock()
        mock_shell_escape.sub.return_value = "result"
        result = EmulationUtil.read_result_interactive_channel(emulation_env_config=emulation_env_config,
                                                               channel=mock_channel)
        mock_channel.recv_ready.assert_called()
        mock_channel.recv.assert_called()
        assert result

    def test_is_emulation_defense_action_legal(self) -> None:
        """
        Test the method that checks if a given defense action is legal in the current state of the environment

        :return: None
        """
        defense_action_id = 1
        emulation_env_config = MagicMock()
        emulation_env_state = MagicMock()
        result = EmulationUtil.is_emulation_defense_action_legal(
            defense_action_id=defense_action_id, env_config=emulation_env_config, env_state=emulation_env_state)
        assert result

    @patch("csle_common.util.env_dynamics_util.EnvDynamicsUtil.logged_in_ips_str")
    def test_is_emulation_attack_action_legal(self, mock_logged_in_ips_str) -> None:
        """
        Test the method that checks if a given attack action is legal in the current state of the environment

        :param mock_logged_in_ips_str: mock_logged_in_ips_str
        :return: None
        """
        mock_env_config = MagicMock()
        mock_env_state = MagicMock()

        mock_env_state.attacker_action_config.actions = [MagicMock(id=0), MagicMock(id=1)]
        mock_env_state.attacker_obs_state = MagicMock()
        mock_env_state.attacker_obs_state.get_action_ips.return_value = "192.168.1.1"
        mock_env_state.attacker_obs_state.actions_tried = set()
        mock_env_state.attacker_obs_state.machines = [
            MagicMock(
                ips="192.168.1.1",
                logged_in=True,
                root=False,
                filesystem_searched=False,
                tools_installed=False,
                backdoor_installed=False,
                untried_credentials=True,
            )
        ]

        action_id = 1
        mock_action = MagicMock()
        mock_action.id = action_id
        mock_action.index = 0
        mock_action.type = EmulationAttackerActionType.RECON
        mock_env_state.attacker_action_config.actions[action_id] = mock_action
        result = EmulationUtil.is_emulation_attack_action_legal(action_id, mock_env_config, mock_env_state)
        assert not result

    def test_check_pid(self) -> None:
        """
        Test the method that checks if a given pid is running on the host

        :return: None
        """
        result = EmulationUtil.check_pid(1)
        assert result

    def test_physical_ip_match(self) -> None:
        """
        Test utility method for checking if a container ip matches a physical ip

        :return: None
        """
        emulation_env_config = MagicMock()
        emulation_env_config.kafka_config.container.docker_gw_bridge_ip = "192.168.0.1"
        emulation_env_config.kafka_config.container.physical_host_ip = "10.0.0.1"
        emulation_env_config.elk_config.container.docker_gw_bridge_ip = "192.168.0.2"
        emulation_env_config.elk_config.container.physical_host_ip = "10.0.0.2"
        emulation_env_config.sdn_controller_config = None

        mock_container = MagicMock()
        mock_container.physical_host_ip = "10.0.0.3"
        emulation_env_config.containers_config.get_container_from_ip.return_value = mock_container

        ip = "192.168.0.1"
        physical_host_ip = "10.0.0.1"

        result = EmulationUtil.physical_ip_match(
            emulation_env_config=emulation_env_config, ip=ip, physical_host_ip=physical_host_ip)
        assert result
