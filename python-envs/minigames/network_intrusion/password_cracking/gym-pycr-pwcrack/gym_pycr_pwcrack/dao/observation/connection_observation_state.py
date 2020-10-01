
class ConnectionObservationState:

    def __init__(self, conn, username : str, root: bool, service: str, port: int, tunnel_thread = None,
                 tunnel_port : int = None):
        self.conn = conn
        self.username = username
        self.root = root
        self.port = port
        self.service = service
        self.tunnel_thread = tunnel_thread
        self.tunnel_port = tunnel_port


    def __str__(self):
        return "username:{},root:{},service:{},port:{}".format(self.username, self.root, self.service, self.port)