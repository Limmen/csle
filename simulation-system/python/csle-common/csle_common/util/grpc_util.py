import grpc


class GrpcUtil:
    """
    Class with utility functions for GRPC functionality in CSLE
    """

    @staticmethod
    def grpc_server_on(channel) -> bool:
        """
        Utility function to test if a given gRPC channel is working or not

        :param channel: the channel to test
        :return: True if working, False if timeout
        """
        try:
            grpc.channel_ready_future(channel).result(timeout=15)
            return True
        except grpc.FutureTimeoutError:
            return False
