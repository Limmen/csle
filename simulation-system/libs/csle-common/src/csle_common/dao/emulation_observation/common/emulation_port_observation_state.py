from typing import Dict, Any, Union
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.network_service import NetworkService


class EmulationPortObservationState:
    """
    DTO Representation a port observation in the emulation
    """

    def __init__(self, port: int, open: bool, service: int, protocol: TransportProtocol, http_enum: str = "",
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
        :return: a dict representation of the object
        """
        d = {}
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
    def from_dict(d: Union[Dict[str, Any], None]) -> "EmulationPortObservationState":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created object instance
        """
        if d is None:
            return None
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
    def from_network_service(network_service: NetworkService, service_lookup: dict) -> "EmulationPortObservationState":
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
        return EmulationPortObservationState(port=-1, open=True, service=-1, protocol=TransportProtocol.TCP,
                                             http_enum="", http_grep="", vulscan="", version="", fingerprint="")
