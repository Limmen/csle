
class ConnectionObservationState:

    def __init__(self, conn, username : str, root: bool, service: str, port: int, tunnel_thread = None,
                 tunnel_port : int = None, interactive_shell = None, proxy = None, ip = None):
        self.conn = conn
        self.username = username
        self.root = root
        self.port = port
        self.service = service
        self.tunnel_thread = tunnel_thread
        self.tunnel_port = tunnel_port
        self.interactive_shell = interactive_shell
        self.proxy = proxy
        self.ip = ip


    def __str__(self):
        return "username:{},root:{},service:{},port:{}".format(self.username, self.root, self.service, self.port)

    def __eq__(self, other):
        if not isinstance(other, ConnectionObservationState):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.username == other.username and self.root == other.root and self.service == other.service \
               and self.port == other.port and self.ip == other.ip

    def __hash__(self):
        return hash(self.username) + 31 * hash(self.root) + 31 * hash(self.service) + 31 * hash(self.port) \
               + 31 * hash(self.ip)

    def cleanup(self) -> None:
        """
        Utility function for cleaning up the connection.

        :return: None
        """
        if self.tunnel_thread is not None:
            self.tunnel_thread.shutdown()
        if self.interactive_shell is not None:
            self.interactive_shell.close()
        if self.conn is not None:
            self.conn.close()