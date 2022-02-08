from csle_common.dao.action_results.nmap_scan_result import NmapScanResult


class NMAPScanCache:
    """
    Class representing the NMAP Scan Cache
    """

    def __init__(self):
        """
        Initializes teh cache
        """
        self.cache = {}

    def add(self, id, result : NmapScanResult) -> None:
        """
        Adds an entry to the cache

        :param id: the cache entry id
        :param result: the result to add
        :return: None
        """
        hash = id
        if hash not in self.cache:
            self.cache[hash]= result


    def get(self, id) -> NmapScanResult:
        """
        Gets an entry from the cache

        :param id: the id of the cache entry
        :return: the result of the cache entry
        """
        hash = id
        if hash in self.cache:
            return self.cache[hash]
        return None
