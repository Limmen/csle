from csle_common.dao.network.transport_protocol import TransportProtocol

class Credential:
    """
    A DTO Class to represent a credential to a service of some component in the infrastructure
    """

    def __init__(self, username: str, pw: str, port: int = None, protocol: TransportProtocol = None,
                 service: str = None, root: bool = False):
        """
        Initializes the DTO

        :param username: the username of the credential
        :param pw: the password of the credential
        :param port: the port of the service of the credential
        :param protocol: the protocol of the service of the credential
        :param service: the service of the credential
        :param root: whether it is a root credential or not
        """
        self.username = username
        self.pw = pw
        self.port = port
        self.protocol = protocol
        self.service = service
        self.root = root


    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["username"] = self.username
        d["pw"] = self.pw
        d["port"] = self.port
        d["protocol"] = self.protocol.name
        d["service"] = self.service
        d["root"] = self.root
        return d


    @staticmethod
    def from_dict(d) -> "Credential":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = Credential(username = d["username"], port = d["port"],
                         protocol=TransportProtocol._from_str(d["protocol"]), pw=d["pw"], service=d["service"],
                         root = d["root"])
        return dto


    def __str__(self) -> str:
        """
        :return: a string representation of the credential
        """
        return "username:{},pw:{},port:{},protocol:{},service:{},root:{}".format(self.username, self.pw, self.port,
                                                                         self.protocol, self.service, self.root)

    def __eq__(self, other) -> bool:
        """
        Tests equality

        :param other: the credential to test equality with
        :return: true if equal otherwise false
        """
        if not isinstance(other, Credential):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.username == other.username and self.pw == other.pw and self.service == other.service

    def __hash__(self) -> int:
        """
        :return: a hash representation of the object
        """
        return hash(self.username) + 31 * hash(self.pw)+ + 31 * hash(self.service)
