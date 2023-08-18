from typing import Optional, Dict, Any
import csle_common.constants.constants as constants
from csle_common.dao.emulation_observation.common.emulation_port_observation_state import EmulationPortObservationState
from csle_common.dao.emulation_action_result.nmap_port_status import NmapPortStatus
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_action_result.nmap_http_enum import NmapHttpEnum
from csle_common.dao.emulation_action_result.nmap_http_grep import NmapHttpGrep
from csle_common.dao.emulation_action_result.nmap_vulscan import NmapVulscan
from csle_base.json_serializable import JSONSerializable


class NmapPort(JSONSerializable):
    """
    DTO Representing a Port found with a NMAP scan
    """

    def __init__(self, port_id: int, protocol: TransportProtocol, status: NmapPortStatus = NmapPortStatus.DOWN,
                 service_name: str = "none", http_enum: Optional[NmapHttpEnum] = None,
                 http_grep: Optional[NmapHttpGrep] = None, vulscan: Optional[NmapVulscan] = None,
                 service_version: str = "",
                 service_fp: str = ""):
        """
        Initializes the DTO

        :param port_id: the id of the port found
        :param protocol: the protocol of the port
        :param status: the status of the port
        :param service_name: the service running on the port
        :param http_enum: the http enum output
        :param http_grep: the http grep output
        :param vulscan: the vulscan output
        :param service_version: the service version
        :param service_fp: the service fp
        """
        self.port_id = port_id
        self.protocol = protocol
        self.status = status
        self.service_name = service_name
        self.http_enum = http_enum
        self.http_grep = http_grep
        self.vulscan = vulscan
        self.service_version = service_version
        self.service_fp = service_fp

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"port_id:{self.port_id}, protocol:{self.protocol}, status:{self.status}, " \
               f"service_name:{self.service_name}, http_enum:{self.http_enum}, " \
               f"http_grep:{self.http_grep}, vulscan:{self.vulscan}, " \
               f"service_version:{self.service_version}, service_fp:{self.service_fp}"

    def __hash__(self) -> int:
        """
        :return: a hash of the object
        """
        return hash(self.port_id)

    def __eq__(self, other) -> bool:
        """
        Compares equality of the object with another object

        :param other: the object to compare with
        :return: True if equal otherwise False
        """
        return bool(self.port_id == other.port_id)

    def to_obs(self) -> EmulationPortObservationState:
        """
        Converts the object into a PortObservationState

        :return: the created PortObservationState
        """
        open = self.status == NmapPortStatus.UP
        if self.service_name not in constants.SERVICES.service_lookup:
            self.service_name = "unknown"
        hp_enum = ""
        if self.http_enum is not None:
            hp_enum = self.http_enum.output
        hp_grep = ""
        if self.http_grep is not None:
            hp_grep = self.http_grep.output
        vulscan = ""
        if self.vulscan is not None:
            vulscan = self.vulscan.output
        port_obs = EmulationPortObservationState(port=self.port_id, open=open, service=self.service_name,
                                                 protocol=self.protocol, http_enum=hp_enum,
                                                 http_grep=hp_grep, vulscan=vulscan, version=self.service_version,
                                                 fingerprint=self.service_fp)
        return port_obs

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["port_id"] = self.port_id
        d["protocol"] = self.protocol
        d["status"] = self.status
        d["service_name"] = self.service_name
        d["http_enum"] = self.http_enum.to_dict() if self.http_enum is not None else self.http_enum
        d["http_grep"] = self.http_grep.to_dict() if self.http_grep is not None else self.http_grep
        d["vulscan"] = self.vulscan.to_dict() if self.vulscan is not None else self.vulscan
        d["service_version"] = self.service_version
        d["service_fp"] = self.service_fp
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NmapPort":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NmapPort(port_id=d["port_id"], protocol=d["protocol"], status=d["status"],
                       service_name=d["service_name"], http_enum=NmapHttpEnum.from_dict(d["http_enum"]),
                       http_grep=NmapHttpGrep.from_dict(d["http_grep"]), vulscan=NmapVulscan.from_dict(d["vulscan"]),
                       service_version=d["service_version"], service_fp=d["service_fp"])
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "NmapPort":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NmapPort.from_dict(json.loads(json_str))
