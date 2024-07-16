import grpc
import pytest
from unittest.mock import patch, MagicMock
from csle_common.util.grpc_util import GrpcUtil

class TestGrpcUtilSuite:
    """
    Test suite for grpc util
    """
    @patch("grpc.channel_ready_future")
    def test_grpc_server_on(self, mock_channel_ready_future):
        """
        Test 

        :param mock_channel_ready_future: _description_
        :type mock_channel_ready_future: _type_
        """
        mock_future = MagicMock()
        mock_channel_ready_future.return_value = mock_future
        result = GrpcUtil.grpc_server_on(mock_channel_ready_future)
        mock_future.result.assert_called()
        assert result
        
    @patch("grpc.channel_ready_future")
    def test_grpc_server_on_timeout(self, mock_channel_ready_future):
        """
        Test 

        :param mock_channel_ready_future: _description_
        :type mock_channel_ready_future: _type_
        """
        mock_future = MagicMock()
        mock_future.result.side_effect = grpc.FutureTimeoutError()
        mock_channel_ready_future.return_value = mock_future
        result = GrpcUtil.grpc_server_on(mock_channel_ready_future)
        mock_future.result.assert_called()
        assert not result
    