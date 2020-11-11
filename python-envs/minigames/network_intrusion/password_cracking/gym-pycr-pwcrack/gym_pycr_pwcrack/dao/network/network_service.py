from typing import List
from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.dao.network.credential import Credential

class NetworkService:

    def __init__(self, protocol: TransportProtocol, port : int, name : str, credentials : List[Credential] = None):
        self.protocol = protocol
        self.port = port
        self.name = name
        self.credentials = credentials