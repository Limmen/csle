from typing import List
from gym_pycr_pwcrack.dao.action_results.nmap_host_status import NmapHostStatus
from gym_pycr_pwcrack.dao.action_results.nmap_port import NmapPort
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_pwcrack.dao.action_results.nmap_os import NmapOs
from gym_pycr_pwcrack.dao.action_results.nmap_vuln import NmapVuln
from gym_pycr_pwcrack.dao.action_results.nmap_brute_credentials import NmapBruteCredentials
from gym_pycr_pwcrack.dao.action_results.nmap_trace import NmapTrace


class NmapHostResult:

    def __init__(self, status: NmapHostStatus = NmapHostStatus.DOWN, ip_addr: str = None,
                 mac_addr: str = None, hostnames: List[str] = None,
                 ports: List[NmapPort] = None, os: NmapOs = None, os_matches: List[NmapOs] = None,
                 vulnerabilities: List[NmapVuln] = None, credentials: List[NmapBruteCredentials] = None,
                 trace: NmapTrace = None):
        self.status = status
        self.ip_addr = ip_addr
        self.mac_addr = mac_addr
        self.hostnames = hostnames
        self.ports = ports
        self.os = os
        self.os_matches = os_matches
        self.vulnerabilities = vulnerabilities
        self.credentials = credentials
        self.trace = trace

    def __str__(self):
        return "status:{}, ip_addr:{}, mac_addr:{}, hostnames:{}, ports:{}, os:{}, os_matches:{}, " \
               "vulnerabilities:{}, credentials:{}, trace:{}".format(
            self.status, self.ip_addr, self.mac_addr, " ".join(self.hostnames),
            " ".join(list(map(lambda x: str(x), self.ports))), self.os,
            " ".join(list(map(lambda x: str(x), self.os_matches))),
            " ".join(list(map(lambda x: str(x), self.vulnerabilities))),
            " ".join(list(map(lambda x: str(x), self.credentials))),
            self.trace
        )

    def to_obs(self) -> MachineObservationState:
        m_obs = MachineObservationState(ip=self.ip_addr)
        ports = list(map(lambda x: x.to_obs(), self.ports))
        m_obs.ports = ports
        if self.os is not None:
            m_obs.os = self.os.vendor.lower()
        vulnerabilities = list(map(lambda x: x.to_obs(), self.vulnerabilities))
        m_obs.cve_vulns = vulnerabilities
        credentials = list(map(lambda x: x.to_obs(), self.credentials))
        m_obs.shell_access_credentials = credentials
        if len(credentials) > 0:
            m_obs.shell_access = True
        m_obs.hostnames = self.hostnames
        m_obs.trace = self.trace
        return m_obs
