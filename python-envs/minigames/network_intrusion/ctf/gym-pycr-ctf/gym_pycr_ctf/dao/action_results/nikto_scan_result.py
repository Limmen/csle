from typing import List
from gym_pycr_ctf.dao.action_results.nikto_vuln import NiktoVuln

class NiktoScanResult:

    def __init__(self, vulnerabilities: List[NiktoVuln], port: int, ip: str, sitename: str):
        self.vulnerabilities = vulnerabilities
        self.port = port
        self.ip = ip
        self.sitename = sitename


    def __str__(self):
        return "ip:{}, port:{}, sitename:{}, vulnerabilities:{}".format(
            self.ip, self.port, self.sitename,
            " ".join(list(map(lambda x: str(x), self.vulnerabilities))))