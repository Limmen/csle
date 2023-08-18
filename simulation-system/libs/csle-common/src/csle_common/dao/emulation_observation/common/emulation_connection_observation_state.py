from typing import Optional, Dict, Any
from csle_common.dao.emulation_config.credential import Credential
from csle_base.json_serializable import JSONSerializable


class EmulationConnectionObservationState(JSONSerializable):
    """
    A DTO representing a connection observation in the emulation
    """

    def __init__(self, conn, credential: Credential, root: bool, service: str, port: int, tunnel_thread=None,
                 tunnel_port: Optional[int] = None, interactive_shell=None,
                 proxy: Optional["EmulationConnectionObservationState"] = None, ip: Optional[str] = None):
        """
        Intializes the DTO

        :param conn: the connection object
        :param credential: the credential of the connection
        :param root: whether the connection is root or not
        :param service: the service of the connection
        :param port: the port of the connection
        :param tunnel_thread: the tunnel thread for the connection
        :param tunnel_port: the tunnel port of the connection
        :param interactive_shell: an interactive shell of the connection
        :param proxy: a proxy for the connection
        :param ip: the ip of the connection
        """
        self.conn = conn
        self.credential = credential
        self.root = root
        self.port = port
        self.service = service
        self.tunnel_thread = tunnel_thread
        self.tunnel_port = tunnel_port
        self.interactive_shell = interactive_shell
        self.proxy = proxy
        self.ip = ip

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationConnectionObservationState":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationConnectionObservationState(
            conn=None, credential=Credential.from_dict(d["credential"]), root=d["root"], port=d["port"],
            service=d["service"], tunnel_port=d["tunnel_port"], tunnel_thread=None, interactive_shell=None, ip=d["ip"],
            proxy=None)
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict represnetation of the object
        """
        d: Dict[str, Any] = {}
        d["credential"] = self.credential.to_dict()
        d["root"] = self.root
        d["port"] = self.port
        d["service"] = self.service
        d["ip"] = self.ip
        d["tunnel_port"] = self.tunnel_port
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the connection observation
        """
        return "credential:{},root:{},service:{},port:{}".format(self.credential, self.root, self.service, self.port)

    def __eq__(self, other) -> bool:
        """
        Checks for equality with another connection

        :param other: the other connection to compare with
        :return: True if equal, otherwise False
        """
        if not isinstance(other, EmulationConnectionObservationState):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (self.credential.username == other.credential.username and self.root == other.root
                and self.service == other.service and self.port == other.port and self.ip == other.ip)

    def __hash__(self) -> int:
        """
        :return: a hash representation of the object
        """
        return (hash(self.credential.username) + 31 * hash(self.root) + 31 * hash(self.service) + 31 *
                hash(self.port) + 31 * hash(self.ip))

    def cleanup(self) -> None:
        """
        Utility function for cleaning up the connection.

        :return: None
        """

        if self.tunnel_thread is not None:
            try:
                self.tunnel_thread.shutdown()
            except Exception:
                pass
            self.tunnel_thread = None
        if self.interactive_shell is not None:
            try:
                self.interactive_shell.close()
            except Exception:
                pass
            self.interactive_shell = None
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = None
        if self.proxy is not None:
            try:
                self.proxy.cleanup()
            except Exception:
                pass
            self.proxy = None

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationConnectionObservationState":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationConnectionObservationState.from_dict(json.loads(json_str))

    def num_attributes(self) -> int:
        """
        :return: The number of attribute of the DTO
        """
        return 9 + self.credential.num_attributes()

    @staticmethod
    def schema() -> "EmulationConnectionObservationState":
        """
        :return: get the schema of the DTO
        """
        return EmulationConnectionObservationState(conn=None, credential=Credential.schema(), root=False, service="",
                                                   port=-1, tunnel_thread=None, tunnel_port=-1,
                                                   interactive_shell=False, proxy=None, ip="")
