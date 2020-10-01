try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer

class ForwardSSHServer(SocketServer.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True