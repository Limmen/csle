from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol

class NetworkService:

    def __init__(self, protocol: TransportProtocol, port : int, name : str):
        self.protocol = protocol
        self.port = port
        self.name = name