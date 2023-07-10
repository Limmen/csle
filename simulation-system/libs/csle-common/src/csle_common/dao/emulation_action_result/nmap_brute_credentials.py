from typing import Dict, Any
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.credential import Credential
from csle_base.json_serializable import JSONSerializable


class NmapBruteCredentials(JSONSerializable):
    """
    A DTO representing credentials found with NMAP Brute-Force Scans
    """

    def __init__(self, username: str, pw: str, state: str, port: int, protocol: TransportProtocol, service: str):
        """
        Initializes the DTO

        :param username: the username of the credential
        :param pw: the pw of the credential
        :param state: the state of the credential
        :param port: the port of the scan
        :param protocol: the protocol of the scan
        :param service: the service of the credential
        """
        self.username = username
        self.pw = pw
        self.state = state
        self.port = port
        self.protocol = protocol
        self.service = service

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "username:{},pw:{},state:{},port:{},protocol:{},service:{}".format(
            self.username, self.pw, self.state, self.port, self.protocol, self.service)

    def __hash__(self) -> int:
        """
        :return: a hash of the object
        """
        return hash(self.username) + 31 * hash(self.pw)

    def __eq__(self, other) -> bool:
        """
        Checks equality with another object

        :param other: the object to compare with
        :return: True if equal otherwise False
        """
        return (self.username == other.username and
                self.pw == other.pw)

    def to_obs(self) -> Credential:
        """
        Converts the Object into a Credential Object

        :return: the created Credential Object
        """
        return Credential(username=self.username, pw=self.pw, port=int(self.port), service=self.service,
                          protocol=self.protocol)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d = {}
        d["username"] = self.username
        d["pw"] = self.pw
        d["state"] = self.state
        d["port"] = self.port
        d["protocol"] = self.protocol
        d["service"] = self.service
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NmapBruteCredentials":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NmapBruteCredentials(username=d["username"], pw=d["pw"], state=d["state"], port=d["port"],
                                   protocol=d["protocol"], service=d["service"])
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "NmapBruteCredentials":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NmapBruteCredentials.from_dict(json.loads(json_str))
