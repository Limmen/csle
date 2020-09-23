from typing import List
from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol

class NetworkService:

    def __init__(self, protocol: TransportProtocol, port : int, name : str, credentials : List[str] = None):
        self.protocol = protocol
        self.port = port
        self.name = name
        self.credentials = credentials