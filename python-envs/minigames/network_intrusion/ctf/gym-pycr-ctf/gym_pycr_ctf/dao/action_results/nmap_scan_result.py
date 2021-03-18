from typing import List
from gym_pycr_ctf.dao.action_results.nmap_host import NmapHostResult

class NmapScanResult:

    def __init__(self, hosts: List[NmapHostResult], ip: str):
        self.hosts = hosts
        self.ip = ip
        self.reachable = []
        for h in self.hosts:
            self.reachable.append(h.ip_addr)

    def __str__(self):
        return "hosts:{}".format(" ".join(list(map(lambda x: str(x), self.hosts))))

    def copy(self):
        hosts = []
        for host in self.hosts:
            hosts.append(host.copy())
        return NmapScanResult(hosts = hosts, ip = self.ip)