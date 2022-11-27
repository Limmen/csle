from typing import List
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState
from csle_common.dao.emulation_config.credential import Credential
from csle_common.tunneling.forward_tunnel_thread import ForwardTunnelThread


class ConnectionSetupDTO:
    """
    DTO class containing information for setting up connections in the emulation
    """

    def __init__(self, connected: bool = False, credentials: List[Credential] = None,
                 target_connections: List = None,
                 tunnel_threads: List[ForwardTunnelThread] = None, forward_ports: List[int] = None,
                 ports: List[int] = None, interactive_shells: List = None, total_time: float = 0.0,
                 non_failed_credentials: List[Credential] = None,
                 proxies: List[EmulationConnectionObservationState] = None, ip: str = None):
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
