from typing import Dict, Any
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.network_service import NetworkService
from csle_base.json_serializable import JSONSerializable


class EmulationPortObservationState(JSONSerializable):
    """
    DTO Representation a port observation in the emulation
    """

    def __init__(self, port: int, open: bool, service: str, protocol: TransportProtocol, http_enum: str = "",
                 http_grep: str = "", vulscan: str = "", version: str = "", fingerprint: str = ""):
        """
        Initializes the DTO

        :param port: the port
        :param open: whether the port is open or not (boolean)
        :param service: the service of the port
        :param protocol: the protocol of the port
        :param http_enum: the HTTP enum result on the port
        :param http_grep: the HTTP grep result on the port
        :param vulscan: the vulscan result of the port
        :param version: the version of the port
        :param fingerprint: the fingerprint output of the port
        """
        self.port = port
        self.open = open
        self.service = service
        self.protocol = protocol
        self.http_enum = http_enum
        self.http_grep = http_grep
        self.vulscan = vulscan
        self.version = version
        self.fingerprint = fingerprint

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["port"] = self.port
        d["open"] = self.open
        d["service"] = self.service
        d["protocol"] = self.protocol
        d["http_enum"] = self.http_enum
        d["http_grep"] = self.http_grep
        d["vulscan"] = self.vulscan
        d["version"] = self.version
        d["fingerprint"] = self.fingerprint
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationPortObservationState":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created object instance
        """
        obj = EmulationPortObservationState(
            port=d["port"],
            open=d["open"],
            service=d["service"],
            protocol=d["protocol"],
            http_enum=d["http_enum"],
            http_grep=d["http_grep"],
            vulscan=d["vulscan"],
            version=d["version"],
            fingerprint=d["fingerprint"]
        )
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"port:{self.port}, open:{self.open}, service:{self.service}, protocol:{self.protocol}, " \
               f"http_enum:{self.http_enum}, http_grep:{self.http_grep}, vulscan:{self.vulscan}, " \
               f"version:{self.version}, fingerprint:{self.fingerprint}"

    def to_network_service(self) -> NetworkService:
        """
        Converts the object into a network service representation

        :return: the network service representation
        """
        service = NetworkService(protocol=self.protocol, port=self.port, name=self.service, credentials=[])
        return service

    @staticmethod
    def from_network_service(network_service: NetworkService,
                             service_lookup: Dict[str, str]) -> "EmulationPortObservationState":
        """
        Converts a network service into a port observation state

        :param network_service: the network service to convert
        :param service_lookup: a lookup table for converting between service names and service ids
        :return:
        """
        if network_service.name in service_lookup:
            s = service_lookup[network_service.name]
        else:
            s = service_lookup["unknown"]
        port = EmulationPortObservationState(port=network_service.port, open=True,
                                             service=s,
                                             protocol=network_service.protocol)
        return port

    def copy(self) -> "EmulationPortObservationState":
        """
        :return: a copy of the object
        """
        c = EmulationPortObservationState(
            port=self.port, open=self.open, service=self.service, protocol=self.protocol, http_enum=self.http_enum,
            http_grep=self.http_grep, vulscan=self.vulscan, version=self.version, fingerprint=self.fingerprint
        )
        return c

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationPortObservationState":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationPortObservationState.from_dict(json.loads(json_str))

    def num_attributes(self) -> int:
        """
        :return: The number of attribute of the DTO
        """
        return 9

    @staticmethod
    def schema() -> "EmulationPortObservationState":
        """
        :return: get the schema of the DTO
        """
        return EmulationPortObservationState(port=-1, open=True, service="", protocol=TransportProtocol.TCP,
                                             http_enum="", http_grep="", vulscan="", version="", fingerprint="")
