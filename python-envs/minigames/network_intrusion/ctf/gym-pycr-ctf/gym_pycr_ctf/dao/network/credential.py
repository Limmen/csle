from gym_pycr_ctf.dao.network.transport_protocol import TransportProtocol


class Credential:
    """
    A DTO Class to represent a credential to a service of some component in the infrastructure
    """

    def __init__(self, username: str, pw: str, port: int = None, protocol: TransportProtocol = None,
                 service: str = None):
        """
        Initializes the DTO

        :param username: the username of the credential
        :param pw: the password of the credential
        :param port: the port of the service of the credential
        :param protocol: the protocol of the service of the credential
        :param service: the service of the credential
        """
        self.username = username
        self.pw = pw
        self.port = port
        self.protocol = protocol
        self.service = service


    def __str__(self) -> str:
        """
        :return: a string representation of the credential
        """
        return "username:{},pw:{},port:{},protocol:{},service:{}".format(self.username, self.pw, self.port,
                                                                         self.protocol, self.service)

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