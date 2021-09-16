from typing import List
from pycr_common.dao.action_results.nmap_hop import NmapHop


class NmapTrace:
    """
    DTO Representing an NMAP Trace
    """

    def __init__(self, hops : List[NmapHop]):
        """
        Initializes the DTO

        :param hops: the list of hops in the trace
        """
        self.hops = hops

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "hops:{}".format(list(map(lambda x: str(x), self.hops)))