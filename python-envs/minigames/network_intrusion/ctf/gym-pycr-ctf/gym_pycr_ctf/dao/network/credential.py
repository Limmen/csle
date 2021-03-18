from gym_pycr_ctf.dao.network.transport_protocol import TransportProtocol

class Credential:

    def __init__(self, username: str, pw: str, port: int = None, protocol: TransportProtocol = None,
                 service: str = None):
        self.username = username
        self.pw = pw
        self.port = port
        self.protocol = protocol
        self.service = service


    def __str__(self):
        return "username:{},pw:{},port:{},protocol:{},service:{}".format(self.username, self.pw, self.port,
                                                                         self.protocol, self.service)

    def __eq__(self, other):
        if not isinstance(other, Credential):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.username == other.username and self.pw == other.pw and self.service == other.service

    def __hash__(self):
        return hash(self.username) + 31 * hash(self.pw)+ + 31 * hash(self.service)