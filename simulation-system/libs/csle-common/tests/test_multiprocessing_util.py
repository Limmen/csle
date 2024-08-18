from unittest.mock import patch
from csle_common.util.multiprocessing_util import NoDaemonProcess
from csle_common.util.multiprocessing_util import NoDaemonContext
from csle_common.util.multiprocessing_util import NestablePool


class TestMultiprocessingUtilSuite:
    """
    Test suite for multiprocessing util
    """

    def test_daemon(self) -> None:
        """
        Test the process with daemon property set to false

        :return: None
        """
        result = NoDaemonProcess(target=lambda: None).daemon
        assert not result

    def test_no_daemon_context(self) -> None:
        """
        Test the NoDaemonContext method

        :return: None
        """
        context = NoDaemonContext()
        process = context.Process(target=lambda: None)
        assert isinstance(process, NoDaemonProcess)
        assert not process.daemon

    @patch("multiprocessing.get_context")
    def test_nestable_pool_initialization(self, mock_get_context) -> None:
        """
        Test the method that initializes the pool

        :param mock_get_context: mock_get_context
        :return: None
        """
        mock_get_context.return_value = NoDaemonContext()
        pool = NestablePool()
        assert pool
