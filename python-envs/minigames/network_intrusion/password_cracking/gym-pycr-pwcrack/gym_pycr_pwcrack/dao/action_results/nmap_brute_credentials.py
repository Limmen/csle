from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.dao.network.credential import Credential

class NmapBruteCredentials:

    def __init__(self, username : str, pw: str, state: str, port: int, protocol: TransportProtocol, service: str):
        self.username = username
        self.pw = pw
        self.state = state
        self.port = port
        self.protocol = protocol
        self.service = service

    def __str__(self):
        return "username:{},pw:{},state:{},port:{},protocol:{},service:{}".format(
            self.username, self.pw, self.state, self.port, self.protocol, self.service)


    def to_obs(self):
        return Credential(username=self.username, pw=self.pw, port=self.port, service=self.service,
                                          protocol=self.protocol)