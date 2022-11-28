from typing import List, Dict, Any
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.credential import Credential


class NetworkService:
    """
    DTO Class representing a serice in the network
    """

    def __init__(self, protocol: TransportProtocol, port: int, name: str, credentials: List[Credential] = None):
        """
        Initializes the DTO

        :param protocol: the protocol of the service
        :param port: the port of the service
        :param name: the name of the service
        :param credentials: the list of credentials of the service
        """
        self.protocol = protocol
        self.port = port
        self.name = name
        self.credentials = credentials

    def __str__(self) -> str:
        """
        :return: a string representation of the service
        """
        cr = []
        if self.credentials is not None:
            cr = list(map(lambda x: str(x), self.credentials))
        return "protocol:{}, port:{}, name:{}, credentials: {}".format(self.protocol, self.port, self.name,
                                                                       cr)

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["protocol"] = self.protocol
        d["port"] = self.port
        d["name"] = self.name
        d["credentials"] = list(map(lambda x: x.to_dict(), self.credentials))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NetworkService":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = NetworkService(name=d["name"], port=d["port"], protocol=d["protocol"],
                             credentials=list(map(lambda x: Credential.from_dict(x), d["credentials"])))
        return dto

    def copy(self) -> "NetworkService":
        """
        :return: a copy of the DTO
        """
        return NetworkService(
            protocol=self.protocol, port=self.port, name=self.name, credentials=self.credentials
        )

    @staticmethod
    def pw_vuln_services():
        """
        :return: a list of all vulnerabilities that involve weak passwords
        """
        ssh_vuln_service = (NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh", credentials=[]),
                            constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS)
        ftp_vuln_service = (NetworkService(protocol=TransportProtocol.TCP, port=21, name="ftp", credentials=[]),
                            constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS)
        telnet_vuln_service = (NetworkService(protocol=TransportProtocol.TCP, port=23, name="telnet", credentials=[]),
                               constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS)
        return [ssh_vuln_service, ftp_vuln_service, telnet_vuln_service], [ssh_vuln_service, telnet_vuln_service]

    def __eq__(self, other) -> bool:
        """
        Tests equality with another service

        :param other: the service to compare with
        :return: True if equal otherwise False
        """
        if not isinstance(other, NetworkService):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.name == other.name and self.protocol == other.protocol and self.port == other.port

    @staticmethod
    def from_credential(credential: Credential) -> "NetworkService":
        """
        Converts the object into a network service representation

        :return: the network service representation
        """
        service = NetworkService(protocol=credential.protocol, port=credential.port,
                                 name=credential.service,
                                 credentials=[credential])
        return service

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
