from typing import Optional, List, Dict, Any
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState
from csle_common.dao.emulation_config.credential import Credential
from csle_common.tunneling.forward_tunnel_thread import ForwardTunnelThread
from csle_base.json_serializable import JSONSerializable


class ConnectionSetupDTO(JSONSerializable):
    """
    DTO class containing information for setting up connections in the emulation
    """

    def __init__(self, connected: bool = False, credentials: Optional[List[Credential]] = None,
                 target_connections: Optional[List[str]] = None,
                 tunnel_threads: Optional[List[ForwardTunnelThread]] = None, forward_ports: Optional[List[int]] = None,
                 ports: Optional[List[int]] = None, interactive_shells: Optional[List[str]] = None,
                 total_time: float = 0.0,
                 non_failed_credentials: Optional[List[Credential]] = None,
                 proxies: Optional[List[EmulationConnectionObservationState]] = None, ip: Optional[str] = None):
        """
        Initializes the DTO

        :param connected: whether the connection is connected or not
        :param credentials: the list of credentials
        :param target_connections: the list of target connections
        :param tunnel_threads: the list of tunnel threads
        :param forward_ports: the list of forward ports
        :param ports: the list of ports
        :param interactive_shells: the list of interactive shells
        :param total_time: the total time of connection
        :param non_failed_credentials: the non-failed-credentials
        :param proxies: the list of proxy connections
        :param ip: the ip address of the connectio
        """
        self.connected = connected
        self.total_time = total_time
        self.credentials = credentials
        self.target_connections = target_connections
        self.tunnel_threads = tunnel_threads
        self.forward_ports = forward_ports
        self.ports = ports
        self.interactive_shells = interactive_shells
        self.total_time = total_time
        self.non_failed_credentials = non_failed_credentials
        self.proxies = proxies
        self.ip = ip

        if self.target_connections is None:
            self.target_connections = []
        if self.tunnel_threads is None:
            self.tunnel_threads = []
        if self.credentials is None:
            self.credentials = []
        if self.forward_ports is None:
            self.forward_ports = []
        if self.ports is None:
            self.ports = []
        if self.interactive_shells is None:
            self.interactive_shells = []
        if self.non_failed_credentials is None:
            self.non_failed_credentials = []
        if self.proxies is None:
            self.proxies = []

    def __str__(self) -> str:
        """
        :return: a string represetation of the object
        """
        if self.credentials is None or self.target_connections is None or self.tunnel_threads is None or \
                self.forward_ports is None or self.ports is None or self.interactive_shells is None or \
                self.non_failed_credentials is None or self.proxies is None:
            raise ValueError("At leat one of the iterables is None")
        return f"connected:{self.connected}, total_time:{self.total_time}, " \
               f"credentials:{list(map(lambda x: str(x), self.credentials))}, " \
               f"target_connections:{list(map(lambda x: str(x), self.target_connections))}, " \
               f"tunnel_threads:{list(map(lambda x: str(x), self.tunnel_threads))}, " \
               f"forward_ports:{list(map(lambda x: str(x), self.forward_ports))}, " \
               f"ports:{list(map(lambda x: str(x), self.ports))}, " \
               f"interactive_shells:{list(map(lambda x: str(x), self.interactive_shells))}, " \
               f"non_failed_credentials:{list(map(lambda x: str(x), self.non_failed_credentials))}, " \
               f"proxies:{list(map(lambda x: str(x), self.proxies))}, ip:{self.ip}"

    def copy(self) -> "ConnectionSetupDTO":
        """
        :return: a copy of the object
        """
        return ConnectionSetupDTO(
            connected=self.connected, credentials=self.credentials, target_connections=self.target_connections,
            tunnel_threads=self.tunnel_threads, forward_ports=self.forward_ports, ports=self.ports,
            interactive_shells=self.interactive_shells, total_time=self.total_time,
            non_failed_credentials=self.non_failed_credentials, proxies=self.proxies, ip=self.ip
        )

    def is_connection_active(self) -> bool:
        """
        Utility function to check if the connection is alive or not

        :return: True if alive, False otherwise
        """
        if self.connected is None or \
                self.credentials is None or \
                self.target_connections is None or \
                self.proxies is None or self.ports is None or \
                self.ports is None or \
                self.non_failed_credentials is None or \
                self.ip is None:
            return False
        else:
            return True

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ConnectionSetupDTO":
        """
        Converts a dict representation of the object into a an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ConnectionSetupDTO(
            connected=d["connected"],
            credentials=list(map(lambda x: Credential.from_dict(x), d["credentials"])),
            ports=d["ports"], total_time=d["total_time"],
            non_failed_credentials=list(map(lambda x: Credential.from_dict(x), d["non_failed_credentials"])),
            proxies=list(map(lambda x: EmulationConnectionObservationState.from_dict(x), d["proxies"])),
            ip=d["ip"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        if self.credentials is None or self.non_failed_credentials is None or self.proxies is None:
            raise ValueError("At least one of the iterables is None")
        d: Dict[str, Any] = {}
        d["connected"] = self.connected
        d["credentials"] = list(map(lambda x: x.to_dict(), self.credentials))
        d["ports"] = self.ports
        d["total_time"] = self.total_time
        d["non_failed_credentials"] = list(map(lambda x: x.to_dict(), self.non_failed_credentials))
        d["ip"] = self.ip
        d["proxies"] = list(map(lambda x: x.to_dict(), self.proxies))
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "ConnectionSetupDTO":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ConnectionSetupDTO.from_dict(json.loads(json_str))
