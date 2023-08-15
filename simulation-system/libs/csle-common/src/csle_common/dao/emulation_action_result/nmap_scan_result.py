from typing import List, Dict, Any
from csle_common.dao.emulation_action_result.nmap_host_result import NmapHostResult
from csle_base.json_serializable import JSONSerializable


class NmapScanResult(JSONSerializable):
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
        self.reachable: List[str] = []
        for h in self.hosts:
            if h.ips is None:
                raise ValueError("No ips found")
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

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["hosts"] = list(map(lambda x: x.to_dict(), self.hosts))
        d["ips"] = self.ips
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NmapScanResult":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NmapScanResult(hosts=list(map(lambda x: NmapHostResult.from_dict(x), d["hosts"])), ips=d["ips"])
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "NmapScanResult":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NmapScanResult.from_dict(json.loads(json_str))
