from typing import List
from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.dao.observation.vulnerability_observation_state import VulnerabilityObservationState
from gym_pycr_pwcrack.dao.network.credential import Credential

class NmapVuln:


    def __init__(self, name : str, port: int, protocol: TransportProtocol, cvss: float, service: str,
                 credentials : List[Credential] = None):
        self.name = name
        self.port = port
        self.protocol = protocol
        self.cvss = cvss
        self.service = service
        self.credentials = credentials

    def to_obs(self) -> VulnerabilityObservationState:
        vuln = VulnerabilityObservationState(name=self.name, port=self.port, protocol=self.protocol, cvss=self.cvss,
                                             credentials=self.credentials)
        return vuln

    def __hash__(self):
        return hash(self.name) + 31 * hash(self.port)

    def __eq__(self, other):
        return (self.name == other.name and
                self.port == other.port)

    def __str__(self):
        return "name:{}, port:{}, protocol:{}, cvss:{}, service:{}, credentials:{}".format(
            self.name, self.port, self.protocol, self.cvss, self.service,
            list(map(lambda x: str(x), self.credentials)))