try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer


class ForwardSSHServer(SocketServer.ThreadingTCPServer):
    """
    SSH Server for forwarding local port over a SSH tunnel
    """
    daemon_threads = True
    allow_reuse_address = True
