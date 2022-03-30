from typing import List
from csle_common.dao.emulation_action_result.nmap_hop import NmapHop


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


    def from_dict(self, d: dict) -> "NmapTrace":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NmapTrace(
            hops=list(map(lambda x: NmapHop.from_dict(x), d["hops"]))
        )
        return obj


    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["hops"] = list(map(lambda x: x.to_dict(), self.hops))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "hops:{}".format(list(map(lambda x: str(x), self.hops)))