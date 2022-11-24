from typing import List
from csle_common.dao.emulation_observation.common.emulation_vulnerability_observation_state import \
    EmulationVulnerabilityObservationState
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.credential import Credential


class NmapVuln:
    """
    DTO representing a vulnerability found with NMAP
    """

    def __init__(self, name: str, port: int, protocol: TransportProtocol, cvss: float, service: str,
                 credentials: List[Credential] = None):
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
        service = ""
        if len(self.credentials) > 0:
            service = self.credentials[0].service
        vuln = EmulationVulnerabilityObservationState(name=self.name, port=self.port, protocol=self.protocol,
                                                      cvss=self.cvss, credentials=self.credentials, service=service)
        return vuln

    def __hash__(self) -> int:
        """
        :return: a hash representation of the object
        """
        return hash(self.name) + 31 * hash(self.port)

    def __eq__(self, other):
        """
        Compares equality of the object with another object

        :param other: the object to compare with
        :return: True if equal otherwise False
        """
        return (self.name == other.name and
                self.port == other.kafka_port)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name:{self.name}, port:{self.port}, protocol:{self.protocol}, cvss:{self.cvss}, " \
               f"service:{self.service}, credentials:{list(map(lambda x: str(x), self.credentials))}"
