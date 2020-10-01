from typing import List
from gym_pycr_pwcrack.dao.observation.port_observation_state import PortObservationState
from gym_pycr_pwcrack.dao.observation.vulnerability_observation_state import VulnerabilityObservationState
from gym_pycr_pwcrack.dao.network.credential import Credential
from gym_pycr_pwcrack.dao.observation.connection_observation_state import ConnectionObservationState

class MachineObservationState:

    def __init__(self, ip : str):
        self.ip = ip
        self.os="unknown"
        self.ports : List[PortObservationState] = []
        self.vuln : List[VulnerabilityObservationState] = []
        self.shell_access = False
        self.shell_access_credentials : List[Credential] = []
        self.logged_in = False
        self.root = False
        self.flags_found = set()
        self.ssh_connections :List[ConnectionObservationState] = []
        self.ftp_connections: List[ConnectionObservationState] = []
        self.telnet_connections: List[ConnectionObservationState] = []

    def __str__(self):
        return "ip:{},os:{},shell_access:{},num_ports:{},num_vuln:{},num_cred{},num_ssh_connections:{}," \
               "num_ftp_connections:{},num_telnet_connections:{}".format(self.ip, self.os, self.shell_access, len(self.ports),
                                                  len(self.vuln),  len(self.shell_access_credentials),
                                                  len(self.ssh_connections), len(self.ftp_connections),
                                                                         len(self.telnet_connections))

    def sort_ports(self):
        self.ports = sorted(self.ports, key=lambda x: x.port, reverse=False)

    def sort_vuln(self, vuln_lookup):
        self.vuln = sorted(self.vuln, key=lambda x: vuln_lookup[x.name], reverse=False)

    def sort_shell_access(self, service_lookup):
        self.shell_access_credentials = sorted(self.shell_access_credentials, key=lambda x: service_lookup[x.service], reverse=False)