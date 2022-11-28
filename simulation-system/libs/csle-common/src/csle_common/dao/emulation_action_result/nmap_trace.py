from typing import List, Dict, Any
from csle_common.dao.emulation_action_result.nmap_hop import NmapHop


class NmapTrace:
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
    def schema() -> "NmapTrace":
        """
        :return: get the schema of the DTO
        """
        return NmapTrace(hops=[NmapHop.schema()])
