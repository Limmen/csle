from gym_pycr_pwcrack.dao.action_results.nmap_port_status import NmapPortStatus
from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.dao.observation.port_observation_state import PortObservationState
from gym_pycr_pwcrack.dao.action_results.nmap_http_enum import NmapHttpEnum
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.dao.action_results.nmap_http_grep import NmapHttpGrep
from gym_pycr_pwcrack.dao.action_results.nmap_vulscan import NmapVulscan

class NmapPort:

    def __init__(self, port_id: int, protocol : TransportProtocol, status: NmapPortStatus = NmapPortStatus.DOWN,
                 service_name : str = "none", http_enum: NmapHttpEnum = None,
                 http_grep: NmapHttpGrep = None, vulscan: NmapVulscan = None, service_version : str = "",
                 service_fp : str = ""):
        self.port_id = port_id
        self.protocol = protocol
        self.status = status
        self.service_name = service_name
        self.http_enum = http_enum
        self.http_grep = http_grep
        self.vulscan = vulscan
        self.service_version = service_version
        self.service_fp = service_fp

    def __str__(self):
        return "port_id:{}, protocol:{}, status:{}, service_name:{}, http_enum:{}, http_grep:{}, vulscan:{}, " \
               "service_version:{}, service_fp:{}".format(
            self.port_id, self.protocol, self.status, self.service_name, self.http_enum, self.http_grep, self.vulscan,
        self.service_version, self.service_fp)

    def to_obs(self) -> PortObservationState:
        open = self.status == NmapPortStatus.UP
        if self.service_name not in constants.SERVICES.service_lookup:
            print("unknown service:{}".format(self.service_name))
            self.service_name = "unknown"
        hp_enum = ""
        if self.http_enum is not None:
            hp_enum = self.http_enum.output
        hp_grep = ""
        if self.http_grep is not None:
            hp_grep = self.http_grep.output
        vulscan = ""
        if self.vulscan is not None:
            vulscan = self.vulscan.output
        port_obs = PortObservationState(port = self.port_id, open=open, service=self.service_name,
                                        protocol=self.protocol, http_enum=hp_enum,
                                        http_grep=hp_grep, vulscan=vulscan, version=self.service_version,
                                        fingerprint=self.service_fp)
        return port_obs