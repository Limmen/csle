from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.dao.observation.vulnerability_observation_state import VulnerabilityObservationState

class NmapVuln:


    def __init__(self, name : str, port: int, protocol: TransportProtocol, cvss: float, service: str):
        self.name = name
        self.port = port
        self.protocol = protocol
        self.cvss = cvss
        self.service = service

    def to_obs(self) -> VulnerabilityObservationState:
        vuln = VulnerabilityObservationState(name=self.name, port=self.port, protocol=self.protocol, cvss=self.cvss)
        return vuln

    def __str__(self):
        return "name:{}, port:{}, protocol:{}, cvss:{}, service:{}".format(
            self.name, self.port, self.protocol, self.cvss, self.service)