from typing import Optional, Dict, Any
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_base.json_serializable import JSONSerializable


class Credential(JSONSerializable):
    """
    A DTO Class to represent a credential to a service of some component in the infrastructure
    """

    def __init__(self, username: str, pw: str, port: int = -1, protocol: Optional[TransportProtocol] = None,
                 service: Optional[str] = None, root: bool = False):
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

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["username"] = self.username
        d["pw"] = self.pw
        d["port"] = self.port
        if self.protocol is not None:
            d["protocol"] = self.protocol.name
        else:
            d["protocol"] = None
        d["service"] = self.service
        d["root"] = self.root
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Credential":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        protocol = None
        if d["protocol"] is not None:
            protocol = TransportProtocol._from_str(d["protocol"])
        dto = Credential(username=d["username"], port=d["port"], protocol=protocol,
                         pw=d["pw"], service=d["service"], root=d["root"])
        return dto

    def __str__(self) -> str:
        """
        :return: a string representation of the credential
        """
        return f"username:{self.username}, pw:{self.pw}, port:{self.port}, protocol:{self.protocol}, " \
               f"service:{self.service}, root:{self.root}"

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
        return hash(self.username) + 31 * hash(self.pw) + 31 * hash(self.service)

    @staticmethod
    def from_json_file(json_file_path: str) -> "Credential":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return Credential.from_dict(json.loads(json_str))

    def copy(self) -> "Credential":
        """
        :return: a copy of the DTO
        """
        return Credential.from_dict(self.to_dict())

    def num_attributes(self) -> int:
        """
        :return: The number of attribute of the DTO
        """
        return 6

    @staticmethod
    def schema() -> "Credential":
        """
        :return: get the schema of the DTO
        """
        return Credential(username="", pw="", port=-1, protocol=TransportProtocol.TCP, service="", root=False)
