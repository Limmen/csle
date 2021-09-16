from typing import List
import copy
from gym_pycr_ctf.dao.observation.attacker.attacker_machine_observation_state import AttackerMachineObservationState
from pycr_common.dao.action_results.nmap_host_status import NmapHostStatus
from pycr_common.dao.action_results.nmap_port import NmapPort
from pycr_common.dao.action_results.nmap_os import NmapOs
from pycr_common.dao.action_results.nmap_vuln import NmapVuln
from pycr_common.dao.action_results.nmap_brute_credentials import NmapBruteCredentials
from pycr_common.dao.action_results.nmap_trace import NmapTrace


class NmapHostResult:
    """
    A DTO representing a host found with an NMAP scan
    """

    def __init__(self, status: NmapHostStatus = NmapHostStatus.DOWN, ip_addr: str = None,
                 mac_addr: str = None, hostnames: List[str] = None,
                 ports: List[NmapPort] = None, os: NmapOs = None, os_matches: List[NmapOs] = None,
                 vulnerabilities: List[NmapVuln] = None, credentials: List[NmapBruteCredentials] = None,
                 trace: NmapTrace = None):
        """
        Initializes the DTO

        :param status: the status of the host
        :param ip_addr: the ip address of the host
        :param mac_addr: the mac address of the host
        :param hostnames: the hostnames of the host
        :param ports: the ports of the host
        :param os: the operating system of the host
        :param os_matches: the matched operating system of the host
        :param vulnerabilities: the vulnerabilities of the host
        :param credentials: the credentials of the host
        :param trace: the trace of the host
        """
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

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "status:{}, ip_addr:{}, mac_addr:{}, hostnames:{}, ports:{}, os:{}, os_matches:{}, " \
               "vulnerabilities:{}, credentials:{}, trace:{}".format(
            self.status, self.ip_addr, self.mac_addr, " ".join(self.hostnames),
            " ".join(list(map(lambda x: str(x), self.ports))), self.os,
            " ".join(list(map(lambda x: str(x), self.os_matches))),
            " ".join(list(map(lambda x: str(x), self.vulnerabilities))),
            " ".join(list(map(lambda x: str(x), self.credentials))),
            self.trace
        )

    def to_obs(self) -> AttackerMachineObservationState:
        """
        Converts the DTO intoa a AttackerMachineObservationState

        :return: the created AttackerMachineObservationState
        """
        m_obs = AttackerMachineObservationState(ip=self.ip_addr)
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
            m_obs.untried_credentials = True
        m_obs.hostnames = self.hostnames
        m_obs.trace = self.trace
        return m_obs

    def copy(self) -> "NmapHostResult":
        """
        :return: a copy of the object
        """
        return copy.deepcopy(self)
