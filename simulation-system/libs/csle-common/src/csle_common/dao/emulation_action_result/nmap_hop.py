from typing import Dict, Any
from csle_base.json_serializable import JSONSerializable


class NmapHop(JSONSerializable):
    """
    DTO representing a Nmap Hop
    """

    def __init__(self, ttl: int, ipaddr: str, rtt: float, host: str):
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
        self.host = host

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NmapHop":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NmapHop(ttl=d["ttl"], ipaddr=d["ipaddr"], rtt=d["rtt"], host=d["host"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
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

    @staticmethod
    def from_json_file(json_file_path: str) -> "NmapHop":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NmapHop.from_dict(json.loads(json_str))

    @staticmethod
    def schema() -> "NmapHop":
        """
        :return: get the schema of the DTO
        """
        return NmapHop(ttl=1, ipaddr="", rtt=0.5, host="")
