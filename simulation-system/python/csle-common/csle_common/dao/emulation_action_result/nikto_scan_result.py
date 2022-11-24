from typing import List
from csle_common.dao.emulation_action_result.nikto_vuln import NiktoVuln


class NiktoScanResult:
    """
    DTO representing the result of a NiktoScan
    """

    def __init__(self, vulnerabilities: List[NiktoVuln], port: int, ip: str, sitename: str):
        """
        Initializes the DTO

        :param vulnerabilities: the list of found vulnerabilities from the scan
        :param port: the port of the scan
        :param ip: the ip of the scan
        :param sitename: the sitename of the scan
        """
        self.vulnerabilities = vulnerabilities
        self.port = port
        self.ip = ip
        self.sitename = sitename

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, port:{self.port}, sitename:{self.sitename}, " \
               f"vulnerabilities:{' '.join(list(map(lambda x: str(x), self.vulnerabilities)))}"
