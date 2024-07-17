import grpc
from unittest.mock import patch, MagicMock
from csle_common.util.grpc_util import GrpcUtil


class TestGrpcUtilSuite:
    """
    Test suite for grpc_util
    """

    @patch("grpc.channel_ready_future")
    def test_grpc_server_on(self, mock_channel_ready_future) -> None:
        """
        Test utility function to test if a given gRPC channel is working or not

        :param mock_channel_ready_future: mock_channel_ready_future
        :return: None
        """
        mock_future = MagicMock()
        mock_channel_ready_future.return_value = mock_future
        result = GrpcUtil.grpc_server_on(mock_channel_ready_future)
        mock_future.result.assert_called()
        assert result

    @patch("grpc.channel_ready_future")
    def test_grpc_server_on_timeout(self, mock_channel_ready_future) -> None:
        """
        Test utility function to test if a given gRPC channel is not working

        :param mock_channel_ready_future: mock_channel_ready_future
        :return: None
        """
        mock_future = MagicMock()
        mock_future.result.side_effect = grpc.FutureTimeoutError()
        mock_channel_ready_future.return_value = mock_future
        result = GrpcUtil.grpc_server_on(mock_channel_ready_future)
        mock_future.result.assert_called()
        assert not result
