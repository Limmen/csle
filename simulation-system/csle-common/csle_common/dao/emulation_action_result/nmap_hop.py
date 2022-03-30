
class NmapHop:
    """
    DTO representing a Nmap Hop
    """

    def __init__(self, ttl : int, ipaddr: str, rtt: float, host: str):
        """
        Initializes the object

        :param ttl: the TTL of the hop
        :param ipaddr: the ip address of the hop
        :param rtt: the RTT of the hop
        :param host: the host of the hop
        """
        self.ttl = ttl
        self.ipaddr = ipaddr
        self.rtt = rtt
        self.host =host

    def from_dict(self, d: dict) -> "NmapHop":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NmapHop(
            ttl = d["ttl"], ipaddr=d["ipaddr"], rtt = d["rtt"], host=d["host"]
        )
        return obj

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ttl"] = self.ttl
        d["ipaddr"] = self.ipaddr
        d["rtt"] = self.rtt
        d["host"] = self.host
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ttl:{}, ipaddr:{}, rtt:{}, host:{}".format(self.ttl, self.ipaddr, self.rtt, self.host)