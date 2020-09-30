from typing import List
from gym_pycr_pwcrack.dao.action_results.nmap_host_status import NmapHostStatus
from gym_pycr_pwcrack.dao.action_results.nmap_port import NmapPort
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_pwcrack.dao.action_results.nmap_os import NmapOs

class NmapHostResult:

    def __init__(self, status : NmapHostStatus = NmapHostStatus.DOWN, ip_addr : str = None,
                 mac_addr : str = None, hostnames : List[str] = None,
                 ports : List[NmapPort] = None, os: NmapOs = None, os_matches: List[NmapOs] = None):
        self.status = status
        self.ip_addr = ip_addr
        self.mac_addr = mac_addr
        self.hostnames = hostnames
        self.ports = ports
        self.os = os
        self.os_matches = os_matches


    def __str__(self):
        return "status:{}, ip_addr:{}, mac_addr:{}, hostnames:{}, ports:{}, os:{}, os_matches:{}".format(
            self.status, self.ip_addr,self.mac_addr," ".join(self.hostnames),
            " ".join(list(map(lambda x: str(x), self.ports))), self.os,
            " ".join(list(map(lambda x: str(x), self.os_matches))))

    def to_obs(self) -> MachineObservationState:
        m_obs = MachineObservationState(ip=self.ip_addr)
        ports = list(map(lambda x: x.to_obs(), self.ports))
        m_obs.ports = ports
        if self.os is not None:
            m_obs.os = self.os.vendor.lower()
        return m_obs

