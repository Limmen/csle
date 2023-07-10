from typing import List, Dict, Any
from csle_common.dao.emulation_action_result.nmap_hop import NmapHop
from csle_base.json_serializable import JSONSerializable


class NmapTrace(JSONSerializable):
    """
    DTO Representing an NMAP Trace
    """

    def __init__(self, hops: List[NmapHop]):
        """
        Initializes the DTO

        :param hops: the list of hops in the trace
        """
        self.hops = hops

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NmapTrace":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NmapTrace(
            hops=list(map(lambda x: NmapHop.from_dict(x), d["hops"]))
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

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

    @staticmethod
    def from_json_file(json_file_path: str) -> "NmapTrace":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NmapTrace.from_dict(json.loads(json_str))

    @staticmethod
    def schema() -> "NmapTrace":
        """
        :return: get the schema of the DTO
        """
        return NmapTrace(hops=[NmapHop.schema()])
