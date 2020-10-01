import select
try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer
import gym_pycr_pwcrack.constants.constants as constants

class ForwardSSHHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        chan = self.server.ssh_transport.open_channel(
            constants.SSH.DIRECT_CHANNEL,
            (self.server.chain_host, self.server.chain_port),
            self.request.getpeername(),
        )
        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
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