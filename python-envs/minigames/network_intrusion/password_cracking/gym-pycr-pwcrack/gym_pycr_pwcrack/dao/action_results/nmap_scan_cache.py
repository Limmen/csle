from gym_pycr_pwcrack.dao.action_results.nmap_scan_result import NmapScanResult

class NMAPScanCache:

    def __init__(self):
        self.cache = {}

    def add(self, id, result : NmapScanResult):
        if id not in self.cache:
            self.cache[id]= result

    def get(self, id) -> NmapScanResult:
        if id in self.cache:
            return self.cache[id]
        return None
