
class NmapHop:

    def __init__(self, ttl : int, ipaddr: str, rtt: float, host: str):
        self.ttl = ttl
        self.ipaddr = ipaddr
        self.rtt = rtt
        self.host =host


    def __str__(self):
        return "ttl:{}, ipaddr:{}, rtt:{}, host:{}".format(self.ttl, self.ipaddr, self.rtt, self.host)