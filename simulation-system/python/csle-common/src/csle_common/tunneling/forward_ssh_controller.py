import select
try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer
import csle_common.constants.constants as constants
from csle_common.logging.log import Logger


class ForwardSSHHandler(SocketServer.BaseRequestHandler):
    """
    SSH Server for forwarding local port over a SSH tunnel
    """
    def handle(self):
        try:
            chan = self.server.ssh_transport.open_channel(
                constants.SSH.DIRECT_CHANNEL,
                (self.server.chain_host, self.server.chain_port),
                self.request.getpeername(),
            )
            while True:
                r, w, x = select.select([self.request, chan], [], [])
                if self.request in r:
                    try:
                        data = self.request.recv(1024)
                    except Exception as e:
                        if "Connection reset by peer" not in str(e):
                            Logger.__call__().get_logger().warning(f"forward SSH exception: {str(e)}, {repr(e)}")
                        data = []
                    if len(data) == 0:
                        break
                    chan.send(data)
                if chan in r:
                    data = chan.recv(1024)
                    if len(data) == 0:
                        break
                    self.request.send(data)

            chan.close()
            self.request.close()
        except Exception as e:
            if "Transport endpoint" not in str(e):
                Logger.__call__().get_logger().warning(f"forward SSH exception2, {str(e)}, {repr(e)}")
