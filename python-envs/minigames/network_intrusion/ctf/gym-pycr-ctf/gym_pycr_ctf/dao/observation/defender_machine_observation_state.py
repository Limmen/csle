from typing import List
import copy
from gym_pycr_ctf.dao.observation.port_observation_state import PortObservationState
from gym_pycr_ctf.dao.observation.connection_observation_state import ConnectionObservationState


class DefenderMachineObservationState:
    """
    Represent's the defender's belief state of a component in the infrastructure
    """

    def __init__(self, ip : str):
        self.ip = ip
        self.os="unknown"
        self.ports : List[PortObservationState] = []
        self.ssh_connections :List[ConnectionObservationState] = []


    def __str__(self):
        return "ip:{},os:{},num_ports:{},num_ssh_connections:{}," \
               "".format(self.ip, self.os, len(self.ports), len(self.ssh_connections))

    def sort_ports(self):
        for p in self.ports:
            p.port = int(p.port)
        self.ports = sorted(self.ports, key=lambda x: x.port, reverse=False)


    def cleanup(self):
        """
        Cleans up environment state. This method is particularly useful in emulation mode where there are
        SSH/Telnet/FTP... connections that should be cleaned up, as well as background threads.

        :return: None
        """
        for c in self.ssh_connections:
            c.cleanup()


    def copy(self):
        m_copy = DefenderMachineObservationState(ip=self.ip)
        m_copy.os = self.os
        m_copy.ports = copy.deepcopy(self.ports)
        m_copy.ssh_connections = self.ssh_connections
        return m_copy



