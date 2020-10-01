
class ConnectionObservationState:

    def __init__(self, conn, username : str, root: bool, service: str):
        self.conn = conn
        self.username = username
        self.root = root
        self.service = service


    def __str__(self):
        return "username:{},root:{},service:{}".format(self.username, self.root, self.service)