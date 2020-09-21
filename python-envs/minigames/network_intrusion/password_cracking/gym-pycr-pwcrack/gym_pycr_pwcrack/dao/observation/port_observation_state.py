from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol

class PortObservationState:

    def __init__(self, port : int, open : bool, service : int, protocol : TransportProtocol):
        self.port = port
        self.open = open
        self.service = service
        self.protocol = protocol