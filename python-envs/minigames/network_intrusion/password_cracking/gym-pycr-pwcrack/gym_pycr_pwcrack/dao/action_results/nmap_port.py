from gym_pycr_pwcrack.dao.action_results.nmap_port_status import NmapPortStatus
from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.dao.observation.port_observation_state import PortObservationState

class NmapPort:

    def __init__(self, port_id: int, protocol : TransportProtocol, status: NmapPortStatus = NmapPortStatus.DOWN,
                 service_name : str = "none"):
        self.port_id = port_id
        self.protocol = protocol
        self.status = status
        self.service_name = service_name


    def __str__(self):
        return "port_id:{}, protocol:{}, status:{}, service_name:{}".format(self.port_id, self.protocol, self.status,
                                                                            self.service_name)

    def to_obs(self) -> PortObservationState:
        open = self.status == NmapPortStatus.UP
        port_obs = PortObservationState(port = self.port_id, open=open, service=self.service_name,
                                        protocol=self.protocol)
        return port_obs