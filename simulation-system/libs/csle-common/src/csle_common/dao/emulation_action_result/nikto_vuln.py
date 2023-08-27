from typing import Dict, Any
from csle_common.dao.emulation_observation.common.emulation_vulnerability_observation_state \
    import EmulationVulnerabilityObservationState
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_base.json_serializable import JSONSerializable


class NiktoVuln(JSONSerializable):
    """
    DTO representing a vulnerability found with a Nikto scan
    """

    def __init__(self, id: str, osvdb_id: int, method: str, iplink: str,
                 namelink: str, uri: str, description: str):
        """
        Initializes the object

        :param id: the id of the vuln
        :param osvdb_id: the osvdb_id of the vuln
        :param method: the method of the vuln
        :param iplink: the iplink of the vuln
        :param namelink: the namelink of the vuln
        :param uri: the uri of the vuln
        :param description: the description of the vuln
        """
        self.id = id
        self.osvdb_id = osvdb_id
        self.method = method
        self.iplink = iplink
        self.namelink = namelink
        self.uri = uri
        self.description = description

    def to_obs(self) -> EmulationVulnerabilityObservationState:
        """
        Converts the object into a VulnerabilityObservationState

        :return: the created VulnerabilityObservationState object
        """
        vuln = EmulationVulnerabilityObservationState(name="nikto_" + str(self.osvdb_id), port=-1,
                                                      protocol=TransportProtocol.TCP,
                                                      cvss=0, osvdbid=self.osvdb_id, description=self.description,
                                                      service="http", credentials=[])
        return vuln

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"id:{self.id}, osvdb_id:{self.osvdb_id}, method:{self.method}, iplink:{self.iplink}, " \
               f"namelink:{self.namelink}, uri:{self.uri}, descr:{self.description}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["id"] = self.id
        d["osvdb_id"] = self.osvdb_id
        d["method"] = self.method
        d["iplink"] = self.iplink
        d["namelink"] = self.namelink
        d["uri"] = self.uri
        d["description"] = self.description
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NiktoVuln":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NiktoVuln(id=d["id"], osvdb_id=d["osvdb_id"], method=d["method"], iplink=d["iplink"],
                        namelink=d["namelink"], uri=d["uri"], description=d["description"])
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "NiktoVuln":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NiktoVuln.from_dict(json.loads(json_str))
