from unittest.mock import patch, MagicMock
from csle_common.util.emulation_util import EmulationUtil
import csle_common.constants.constants as constants
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state import (
    EmulationConnectionObservationState,
)


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
