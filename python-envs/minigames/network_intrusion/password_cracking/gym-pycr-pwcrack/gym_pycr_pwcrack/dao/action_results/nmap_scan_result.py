from typing import List
from gym_pycr_pwcrack.dao.action_results.nmap_host import NmapHostResult

class NmapScanResult:

    def __init__(self, hosts: List[NmapHostResult]):
        self.hosts = hosts

    def __str__(self):
        return "hosts:{}".format(" ".join(list(map(lambda x: str(x), self.hosts))))