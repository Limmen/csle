from typing import List
import copy
import datetime
from gym_pycr_ctf.dao.observation.common.port_observation_state import PortObservationState
from gym_pycr_ctf.dao.observation.common.connection_observation_state import ConnectionObservationState
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig


class DefenderMachineObservationState:
    """
    Represent's the defender's belief state of a component in the infrastructure
    """

    def __init__(self, ip : str):
        self.ip = ip
        self.os="unknown"
        self.ports : List[PortObservationState] = []
        self.ssh_connections :List[ConnectionObservationState] = []
        self.emulation_config : EmulationConfig = None
        self.num_flags = 0
        self.num_open_connections = 0
        self.num_failed_login_attempts = 0
        self.num_users = 0
        self.num_logged_in_users = 0
        self.num_login_events = 0
        self.uptime = 0
        self.num_processes = 0
        self.failed_auth_last_ts = datetime.datetime.now().timestamp()
        self.login_last_ts = datetime.datetime.now().timestamp()

    def __str__(self):
        return "ip:{},os:{},num_ports:{},num_ssh_connections:{},num_flags:{}," \
               "num_open_connections:{},num_failed_login_attempts:{},num_users:{}," \
               "num_logged_in_users:{},num_login_events:{},uptime:{},num_processes:{}," \
               "failed_auth_last_ts:{},login_last_ts:{}" \
               "".format(self.ip, self.os, len(self.ports), len(self.ssh_connections),
                         self.num_flags, self.num_open_connections, self.num_failed_login_attempts,
                         self.num_failed_login_attempts, self.num_users, self.num_logged_in_users,
                         self.num_login_events, self.uptime, self.num_processes, self.failed_auth_last_ts,
                         self.login_last_ts)

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
        m_copy.num_flags = self.num_flags
        m_copy.num_open_connections = self.num_open_connections
        m_copy.num_failed_login_attempts = self.num_failed_login_attempts
        m_copy.num_users = self.num_users
        m_copy.num_logged_in_users = self.num_logged_in_users
        m_copy.num_login_events = self.num_login_events
        m_copy.uptime = self.uptime
        m_copy.num_processes = self.num_processes
        m_copy.failed_auth_last_ts = self.failed_auth_last_ts
        m_copy.login_last_ts = self.login_last_ts
        return m_copy



