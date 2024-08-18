from csle_common.util.ssh_util import SSHUtil
from unittest.mock import patch, MagicMock
import pytest


class TestSSHUtilSuite:
    """
    Test suite for ssh_util
    """

    @pytest.fixture(autouse=True)
    def mock_sleep(self):
        """
        Mock time.sleep to avoid delays
        """
        with patch("time.sleep", return_value=None):
            yield

    @patch("csle_common.util.ssh_util.SSHUtil.execute_ssh_cmd")
    def test_execute_ssh_cmds(self, mock_execute_ssh_cmd) -> None:
        """
        Test the method that executes a list of commands over an ssh connection to the emulation

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :return: None
        """
        mock_execute_ssh_cmd.return_value = (b"output", b"error", 1.0)
        cmds = ["ls", "pwd", "whoami"]
        conn = MagicMock()
        results = SSHUtil.execute_ssh_cmds(cmds, conn)
        mock_execute_ssh_cmd.assert_called()
        assert results == [(b"output", b"error", 1.0)] * len(cmds)

    def test_execute_ssh_cmd(self) -> None:
        """
        Test the method that executes an action on the emulation over a ssh connection

        :return: None
        """
        conn = MagicMock()
        mock_transport = MagicMock()
        mock_session = MagicMock()
        mock_session.exit_status_ready.return_value = True
        mock_session.recv_ready.return_value = True
        mock_session.recv_stderr_ready.return_value = True
        mock_session.recv.side_effect = [b"output", b""]
        mock_session.recv_stderr.side_effect = [b"error", b""]
        conn.get_transport.return_value = mock_transport
        mock_transport.open_session.return_value = mock_session

        with pytest.raises(ConnectionError, match="Connection failed"):
            SSHUtil.execute_ssh_cmd("ls", conn)
