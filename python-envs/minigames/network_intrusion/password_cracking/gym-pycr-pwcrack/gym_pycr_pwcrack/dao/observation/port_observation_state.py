from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol

class PortObservationState:

    def __init__(self, port : int, open : bool, service : int, protocol : TransportProtocol, http_enum: str = ""):
        self.port = port
        self.open = open
        self.service = service
        self.protocol = protocol
        self.http_enum = http_enum

    def __str__(self):
        return "port:{}, open:{}, service:{}, protocol:{}, http_enum:{}".format(self.port, self.open, self.service,
                                                                                self.protocol, self.http_enum)