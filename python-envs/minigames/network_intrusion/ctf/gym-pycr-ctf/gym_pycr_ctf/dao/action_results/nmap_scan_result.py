from typing import List
from gym_pycr_ctf.dao.action_results.nmap_host_result import NmapHostResult


class NmapScanResult:
    """
    DTO representing the result of a NMAP Scan
    """

    def __init__(self, hosts: List[NmapHostResult], ip: str):
        """
        Initializes the DTO

        :param hosts: the list of NMAP hosts
        :param ip: the ip of the host
        """
        self.hosts = hosts
        self.ip = ip
        self.reachable = []
        for h in self.hosts:
            self.reachable.append(h.ip_addr)

    def __str__(self) -> str:
        """
        :return:  a string representation of the objectp
        """
        return "hosts:{}".format(" ".join(list(map(lambda x: str(x), self.hosts))))

    def copy(self) -> "NmapScanResult":
        """
        :return: a copy of the object
        """
        hosts = []
        for host in self.hosts:
            hosts.append(host.copy())
        return NmapScanResult(hosts = hosts, ip = self.ip)