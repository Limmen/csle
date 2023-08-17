from typing import Dict, Any, Union
from csle_base.json_serializable import JSONSerializable


class NmapOs(JSONSerializable):
    """
    DTO representing the operating system found with an NMAP scan
    """

    def __init__(self, name: str, vendor: str, osfamily: str, accuracy: int):
        """
        Initializes the DTO object

        :param name: the name of the operating system
        :param vendor: the vendor of the operating system
        :param osfamily: the family of the operating system
        :param accuracy: the accuracy of the OS guess
        """
        self.name = name
        self.vendor = vendor
        self.osfamily = osfamily
        self.accuracy = accuracy

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name:{self.name}, vendor:{self.vendor}, os_family:{self.osfamily}, accuracy:{self.accuracy}"

    @staticmethod
    def get_best_match(os_matches):
        """
        Returns the best matching os

        :param os_matches: list of os matches
        :return: best matching os
        """
        best_accuracy = 0
        best_os = None
        for os in os_matches:
            if os.accuracy > best_accuracy:
                best_os = os
        return best_os

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, int]] = {}
        d["name"] = self.name
        d["vendor"] = self.vendor
        d["osfamily"] = self.osfamily
        d["accuracy"] = self.accuracy
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NmapOs":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NmapOs(name=d["name"], vendor=d["vendor"], osfamily=d["osfamily"], accuracy=d["accuracy"])
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "NmapOs":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NmapOs.from_dict(json.loads(json_str))
