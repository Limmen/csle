from typing import Dict, Any


class NmapHop:
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

    def from_dict(self, d: Dict[str, Any]) -> "NmapHop":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NmapHop(ttl=d["ttl"], ipaddr=d["ipaddr"], rtt=d["rtt"], host=d["host"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
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

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    @staticmethod
    def schema() -> "NmapHop":
        """
        :return: get the schema of the DTO
        """
        return NmapHop(ttl=1, ipaddr="", rtt=0.5, host="")
