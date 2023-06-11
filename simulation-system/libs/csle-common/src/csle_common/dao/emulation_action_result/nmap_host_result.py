from typing import List, Dict, Any
import copy
from csle_common.dao.emulation_action_result.nmap_host_status import NmapHostStatus
from csle_common.dao.emulation_action_result.nmap_port import NmapPort
from csle_common.dao.emulation_action_result.nmap_os import NmapOs
from csle_common.dao.emulation_action_result.nmap_vuln import NmapVuln
from csle_common.dao.emulation_action_result.nmap_brute_credentials import NmapBruteCredentials
from csle_common.dao.emulation_action_result.nmap_trace import NmapTrace
from csle_base.json_serializable import JSONSerializable


class NmapHostResult(JSONSerializable):
    """
    A DTO representing a host found with an NMAP scan
    """

    def __init__(self, status: NmapHostStatus = NmapHostStatus.DOWN, ips: List[str] = None,
                 mac_addr: str = None, hostnames: List[str] = None,
                 ports: List[NmapPort] = None, os: NmapOs = None, os_matches: List[NmapOs] = None,
                 vulnerabilities: List[NmapVuln] = None, credentials: List[NmapBruteCredentials] = None,
                 trace: NmapTrace = None):
        """
        Initializes the DTO

        :param status: the status of the host
        :param ips: the ip address of the host
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
        self.ips = ips
        if self.ips is None:
            self.ips = []
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
        return f"status:{self.status}, ip_addr:{self.ips}, mac_addr:{self.mac_addr}, " \
               f"hostnames:{' '.join(self.hostnames)}, " \
               f"ports:{' '.join(list(map(lambda x: str(x), self.ports)))}, os:{self.os}, " \
               f"os_matches:{' '.join(list(map(lambda x: str(x), self.os_matches)))}, " \
               f"vulnerabilities:{' '.join(list(map(lambda x: str(x), self.vulnerabilities)))}, " \
               f"credentials:{' '.join(list(map(lambda x: str(x), self.credentials)))}, " \
               f"trace:{self.trace}"

    def copy(self) -> "NmapHostResult":
        """
        :return: a copy of the object
        """
        return copy.deepcopy(self)

    def ips_match(self, ips: List[str]) -> bool:
        """
        Checks if a list of ips overlap with the ips of this host

        :param ips: the list of ips to check
        :return:  True if they match, False otherwise
        """
        for ip in self.ips:
            if ip in ips:
                return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["status"] = self.status
        d["ips"] = self.ips
        d["mac_addr"] = self.mac_addr
        d["hostnames"] = self.hostnames
        d["ports"] = list(map(lambda x: x.to_dict(), self.ports))
        d["os"] = self.os.to_dict()
        d["os_matches"] = list(map(lambda x: x.to_dict(), self.os_matches))
        d["vulnerabilities"] = list(map(lambda x: x.to_dict(), self.vulnerabilities))
        d["credentials"] = list(map(lambda x: x.to_dict(), self.credentials))
        d["trace"] = self.trace.to_dict()
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NmapHostResult":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NmapHostResult(
            status=d["status"], ips=d["ips"], mac_addr=d["mac_addr"], hostnames=d["hostnames"],
            ports=list(map(lambda x: NmapPort.from_dict(x), d["ports"])),
            os=NmapOs.from_dict(d["os"]),
            os_matches=list(map(lambda x: NmapOs.from_dict(x), d["os_matches"])),
            vulnerabilities=list(map(lambda x: NmapVuln.from_dict(x), d["vulnerabilities"])),
            credentials=list(map(lambda x: NmapBruteCredentials.from_dict(x), d["credentials"])),
            trace=NmapTrace.from_dict(d["trace"])
        )
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "NmapHostResult":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NmapHostResult.from_dict(json.loads(json_str))
