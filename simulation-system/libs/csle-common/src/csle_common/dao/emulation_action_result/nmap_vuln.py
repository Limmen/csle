from typing import Optional, List, Dict, Any
from csle_common.dao.emulation_observation.common.emulation_vulnerability_observation_state import \
    EmulationVulnerabilityObservationState
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.credential import Credential
from csle_base.json_serializable import JSONSerializable


class NmapVuln(JSONSerializable):
    """
    DTO representing a vulnerability found with NMAP
    """

    def __init__(self, name: str, port: int, protocol: TransportProtocol, cvss: float, service: str,
                 credentials: Optional[List[Credential]] = None):
        """
        Initializes the DTO

        :param name: the name of the vulnerability
        :param port: the port of the vulnerability
        :param protocol: the protocol of the vulnerability
        :param cvss: the cvss of the vulnerability
        :param service: the service of the vulnerability
        :param credentials: the credentials of the vulnerability
        """
        self.name = name
        self.port = port
        self.protocol = protocol
        self.cvss = cvss
        self.service = service
        self.credentials = credentials
        if self.credentials is None:
            self.credentials = []

    def to_obs(self) -> EmulationVulnerabilityObservationState:
        """
        Converts the object into a VulnerabilityObservationState

        :return: the created VulnerabilityObservationState
        """
        service: Optional[str] = ""
        if self.credentials is None:
            raise ValueError("self.credentials is None")
        if len(self.credentials) > 0:
            service = self.credentials[0].service
        vuln = EmulationVulnerabilityObservationState(name=self.name, port=self.port, protocol=self.protocol,
                                                      cvss=self.cvss, credentials=self.credentials, service=service)
        return vuln

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        if self.credentials is None:
            raise ValueError("Credential list is None")
        return f"name:{self.name}, port:{self.port}, protocol:{self.protocol}, cvss:{self.cvss}, " \
               f"service:{self.service}, credentials:{list(map(lambda x: str(x), self.credentials))}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["name"] = self.name
        d["port"] = self.port
        d["protocol"] = self.protocol
        d["cvss"] = self.cvss
        d["service"] = self.service
        d["credentials"] = list(map(lambda x: x.to_dict(), self.credentials)) if \
            self.credentials is not None else self.credentials
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NmapVuln":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NmapVuln(
            name=d["name"], port=d["port"], protocol=d["protocol"], cvss=d["cvss"], service=d["service"],
            credentials=list(map(lambda x: Credential.from_dict(x), d["credentials"]))
        )
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "NmapVuln":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NmapVuln.from_dict(json.loads(json_str))

    def __hash__(self) -> int:
        """
        :return: a hash representation of the object
        """
        return hash(self.name) + 31 * hash(self.port) + 31 * hash(self.protocol.value) + 28 * hash(self.service)
