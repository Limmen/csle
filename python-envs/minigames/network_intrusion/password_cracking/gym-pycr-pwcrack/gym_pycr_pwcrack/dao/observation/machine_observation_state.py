from typing import List
from gym_pycr_pwcrack.dao.observation.port_observation_state import PortObservationState
from gym_pycr_pwcrack.dao.observation.vulnerability_observation_state import VulnerabilityObservationState

class MachineObservationState:

    def __init__(self, ip : str):
        self.ip = ip
        self.os="unknown"
        self.ports : List[PortObservationState] = []
        self.vuln : List[VulnerabilityObservationState] = []

    def __str__(self):
        return "ip:{},os:{},num_ports:{},num_vuln:{}".format(self.ip, self.os, len(self.ports), len(self.vuln))

    def sort_ports(self):
        self.ports = sorted(self.ports, key=lambda x: x.port, reverse=False)

    def sort_vuln(self, vuln_lookup):
        self.vuln = sorted(self.vuln, key=lambda x: vuln_lookup[x.name], reverse=False)