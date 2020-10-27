import hashlib
from gym_pycr_pwcrack.dao.action_results.nmap_scan_result import NmapScanResult

class NMAPScanCache:

    def __init__(self):
        self.cache = {}

    def add(self, id, result : NmapScanResult):
        hash = hashlib.sha1(id.encode())
        if hash not in self.cache:
            self.cache[hash]= result


    def get(self, id) -> NmapScanResult:
        hash = hashlib.sha1(id.encode())
        if hash in self.cache:
            return self.cache[hash]
        return None
