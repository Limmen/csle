from typing import List
from csle_common.dao.emulation_action_result.nmap_host_result import NmapHostResult


class NmapScanResult:
    """
    DTO representing the result of a NMAP Scan
    """

    def __init__(self, hosts: List[NmapHostResult], ips: List[str]):
        """
        Initializes the DTO

        :param hosts: the list of NMAP hosts
        :param ips: the ips of the host
        """
        self.hosts = hosts
        self.ips = ips
        self.reachable = []
        for h in self.hosts:
            self.reachable = self.reachable + h.ips

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
        return NmapScanResult(hosts=hosts, ips=self.ips)
