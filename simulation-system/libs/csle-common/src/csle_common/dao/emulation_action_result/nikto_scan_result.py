from typing import List, Dict, Any
from csle_common.dao.emulation_action_result.nikto_vuln import NiktoVuln
from csle_base.json_serializable import JSONSerializable


class NiktoScanResult(JSONSerializable):
    """
    DTO representing the result of a NiktoScan
    """

    def __init__(self, vulnerabilities: List[NiktoVuln], port: int, ip: str, sitename: str):
        """
        Initializes the DTO

        :param vulnerabilities: the list of found vulnerabilities from the scan
        :param port: the port of the scan
        :param ip: the ip of the scan
        :param sitename: the sitename of the scan
        """
        self.vulnerabilities = vulnerabilities
        self.port = port
        self.ip = ip
        self.sitename = sitename

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, port:{self.port}, sitename:{self.sitename}, " \
               f"vulnerabilities:{' '.join(list(map(lambda x: str(x), self.vulnerabilities)))}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["port"] = self.port
        d["ip"] = self.ip
        d["sitename"] = self.sitename
        d["vulnerabilities"] = list(map(lambda x: x.to_dict(), self.vulnerabilities))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NiktoScanResult":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NiktoScanResult(
            vulnerabilities=list(map(lambda x: NiktoVuln.from_dict(x), d["vulnerabilities"])),
            port=d["port"], ip=d["ip"], sitename=d["sitename"]
        )
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "NiktoScanResult":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NiktoScanResult.from_dict(json.loads(json_str))
