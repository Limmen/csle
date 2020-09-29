from typing import List
from gym_pycr_pwcrack.dao.action_results.nmap_host_status import NmapHostStatus
from gym_pycr_pwcrack.dao.action_results.nmap_port import NmapPort

class NmapHostResult:

    def __init__(self, status : NmapHostStatus = NmapHostStatus.DOWN, ip_addr : str = None,
                 mac_addr : str = None, hostnames : List[str] = None,
                 ports : List[NmapPort] = None):
        self.status = status
        self.ip_addr = ip_addr
        self.mac_addr = mac_addr
        self.hostnames = hostnames
        self.ports = ports

