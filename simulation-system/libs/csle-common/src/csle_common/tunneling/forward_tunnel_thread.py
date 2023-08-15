import threading
import time
from csle_common.tunneling.forward_ssh_server import ForwardSSHServer
from csle_common.tunneling.forward_ssh_controller import ForwardSSHHandler
from typing import Dict, Any


class ForwardTunnelThread(threading.Thread):
    """
    Thread that starts up a SSH tunnel that forwards a local port to a remote machine
    """

    def __init__(self, local_port: int, remote_host: str, remote_port: int,
                 transport, tunnels_dict: Dict[str, Any] = {}) -> None:
        """
        Initializes the thread

        :param local_port: the local port for port-forwarding
        :param remote_host: the remote host
        :param remote_port: the remote port
        :param transport: the transport protocol
        :param tunnels_dict: the tunnels dict for garbage collection
        """
        super().__init__()
        self.local_port = local_port
        self.remote_host = remote_host
        self.transport = transport
        self.remote_port = remote_port
        self.forward_server = ForwardSSHServer(("", local_port), ForwardSSHHandler)
        self.forward_server.ssh_transport = self.transport
        self.forward_server.chain_host = self.remote_host
        self.forward_server.chain_port = self.remote_port
        self.forward_server.tunnels_dict = tunnels_dict
        self.daemon = True

    def run(self) -> None:
        """
        Starts the server

        :return:
        """
        self.forward_server.serve_forever()

    def shutdown(self) -> None:
        """
        Shutsdown the server

        :return: None
        """
        self.forward_server.shutdown()
        time.sleep(0.5)  # wait for server to shutdown
