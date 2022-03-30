from typing import List
import copy
from csle_common.dao.emulation_observation.common.emulation_port_observation_state \
    import EmulationPortObservationState
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState


class EmulationDefenderMachineObservationState:
    """
    Represent's the defender's belief state of a component in the emulation
    """

    def __init__(self, ips : List[str]):
        """
        Initializes the DTO

        :param ips: the ip of the machine
        """
        self.ips = ips
        self.os="unknown"
        self.ports : List[EmulationPortObservationState] = []
        self.ssh_connections :List[EmulationConnectionObservationState] = []
        self.num_open_connections = 0
        self.num_failed_login_attempts = 0
        self.num_users = 0
        self.num_logged_in_users = 0
        self.num_login_events = 0
        self.num_processes = 0
        self.num_open_connections_recent = 0
        self.num_failed_login_attempts_recent = 0
        self.num_users_recent = 0
        self.num_logged_in_users_recent = 0
        self.num_login_events_recent = 0
        self.num_processes_recent = 0
        self.num_pids = 0
        self.num_pids_recent = 0
        self.cpu_percent = 0.0
        self.cpu_percent_recent = 0.0
        self.mem_current = 0.0
        self.mem_current_recent = 0.0
        self.mem_total = 0.0
        self.mem_total_recent = 0.0
        self.mem_percent = 0.0
        self.mem_percent_recent = 0.0
        self.blk_read = 0
        self.blk_read_recent = 0
        self.blk_write = 0
        self.blk_write_recent = 0
        self.net_rx = 0
        self.net_rx_recent = 0
        self.net_tx = 0
        self.net_tx_recent = 0

    def from_dict(self, d: dict) -> "EmulationDefenderMachineObservationState":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict representation
        :return: the object instance
        """
        obj = EmulationDefenderMachineObservationState(ips=d["ips"])
        obj.os = d["os"]
        obj.ports=list(map(lambda x: EmulationPortObservationState.from_dict(x), d["ports"]))
        obj.ssh_connections=list(map(lambda x: EmulationConnectionObservationState.from_dict(x), d["ssh_connections"]))
        obj.num_open_connections = d["num_open_connections"]
        obj.num_failed_login_attempts = d["num_failed_login_attempts"]
        obj.num_users = d["num_users"]
        obj.num_logged_in_users = d["num_logged_in_users"]
        obj.num_login_events = d["num_login_events"]
        obj.num_processes = d["num_processes"]
        obj.num_open_connections_recent = d["num_open_connections_recent"]
        obj.num_failed_login_attempts_recent = d["num_failed_login_attempts_recent"]
        obj.num_users_recent = d["num_users_recent"]
        obj.num_logged_in_users_recent = d["num_logged_in_users_recent"]
        obj.num_login_events_recent = d["num_login_events_recent"]
        obj.num_processes_recent = d["num_processes_recent"]
        obj.num_pids = d["num_pids"]
        obj.num_pids_recent = d["num_pids_recent"]
        obj.cpu_percent = d["cpu_percent"]
        obj.cpu_percent_recent = d["cpu_percent_recent"]
        obj.mem_current = d["mem_current"]
        obj.mem_current_recent = d["mem_current_recent"]
        obj.mem_total = d["mem_total"]
        obj.mem_total_recent = d["mem_total_recent"]
        obj.mem_percent = d["mem_percent"]
        obj.mem_percent_recent = d["mem_percent_recent"]
        obj.blk_read = d["blk_read"]
        obj.blk_read_recent = d["blk_read_recent"]
        obj.blk_write = d["blk_write"]
        obj.blk_write_recent = d["blk_write_recent"]
        obj.net_rx = d["net_rx"]
        obj.net_rx_recent = d["net_rx_recent"]
        obj.net_tx = d["net_tx"]
        obj.net_tx_recent = d["net_tx_recent"]
        return obj

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ips"] = self.ips
        d["os"] = self.os
        d["ports"] = list(map(lambda x: x.to_dict(), self.ports))
        d["ssh_connections"] = list(map(lambda x: x.to_dict(), self.ssh_connections))
        d["num_open_connections"] = self.num_open_connections
        d["num_failed_login_attempts"] = self.num_failed_login_attempts
        d["num_users"] = self.num_users
        d["num_logged_in_users"] = self.num_logged_in_users
        d["num_login_events"] = self.num_login_events
        d["num_processes"] = self.num_processes
        d["num_open_connections_recent"] = self.num_open_connections_recent
        d["num_failed_login_attempts_recent"] = self.num_failed_login_attempts_recent
        d["num_users_recent"] = self.num_users_recent
        d["num_logged_in_users_recent"] = self.num_logged_in_users_recent
        d["num_login_events_recent"] = self.num_login_events_recent
        d["num_pids"] = self.num_pids
        d["num_pids_recent"] = self.num_pids_recent
        d["cpu_percent"] = self.cpu_percent
        d["cpu_percent_recent"] = self.cpu_percent_recent
        d["mem_current"] = self.mem_current
        d["mem_current_recent"] = self.mem_current_recent
        d["mem_total"] = self.mem_total
        d["mem_total_recent"] = self.mem_total_recent
        d["mem_percent"] = self.mem_percent
        d["mem_percent_recent"] = self.mem_percent_recent
        d["blk_read"] = self.blk_read
        d["blk_read_recent"] = self.blk_read_recent
        d["blk_write"] = self.blk_write
        d["blk_write_recent"] = self.blk_write_recent
        d["net_rx"] = self.net_rx
        d["net_rx_recent"] = self.net_rx_recent
        d["net_tx"] = self.net_tx
        d["net_tx_recent"] = self.net_tx_recent
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ips},os:{self.os},num_ports:{len(self.ports)}," \
               f"num_ssh_connections:{len(self.ssh_connections)}," \
               f"num_open_connections:{self.num_open_connections}," \
               f"num_failed_login_attempts:{self.num_failed_login_attempts},num_users:{self.num_users}," \
               f"num_logged_in_users:{self.num_logged_in_users},num_login_events:{self.num_login_events}," \
               f"num_processes:{self.num_processes}," \
               f"num_open_connections_recent:{self.num_open_connections_recent}," \
               f"num_failed_login_attempts_recent:{self.num_failed_login_attempts_recent}," \
               f"num_users_recent:{self.num_users_recent}," \
               f"num_logged_in_users_recent:{self.num_logged_in_users_recent}," \
               f"num_login_events_recent:{self.num_login_events_recent}," \
               f"num_processes_recent:{self.num_processes_recent}, " \
               f"num_pids:{self.num_pids}, cpu_percent:{self.cpu_percent}, mem_current:{self.mem_current}, " \
               f"mem_total: {self.mem_total}, mem_percent: {self.mem_percent}, blk_read: {self.blk_read}," \
               f"blk_write: {self.blk_write}, net_rx: {self.net_rx}, net_tx: {self.net_tx}," \
               f"num_pids_recent: {self.num_pids_recent}, cpu_percent_recent:{self.cpu_percent_recent}, " \
               f"mem_current_recent:{self.mem_current_recent}, mem_total_recent: {self.mem_total_recent}, " \
               f"mem_percent_recent:{self.mem_percent_recent}, blk_read_recent:{self.blk_read_recent}," \
               f"blk_write_recent:{self.blk_write_recent}, net_rx_recent:{self.net_rx_recent}, " \
               f"net_tx_recent:{self.net_tx_recent}"

    def sort_ports(self) -> None:
        """
        Sorts the list of ports

        :return: None
        """
        for p in self.ports:
            p.port = int(p.port)
        self.ports = sorted(self.ports, key=lambda x: x.kafka_port, reverse=False)

    def cleanup(self) -> None:
        """
        Cleans up environment state. This method is particularly useful in emulation mode where there are
        SSH/Telnet/FTP... connections that should be cleaned up, as well as background threads.

        :return: None
        """
        for c in self.ssh_connections:
            c.cleanup()

    def copy(self) -> "EmulationDefenderMachineObservationState":
        """
        :return: a copy of the object
        """
        m_copy = EmulationDefenderMachineObservationState(ips=self.ips)
        m_copy.os = self.os
        m_copy.ports = copy.deepcopy(self.ports)
        m_copy.ssh_connections = self.ssh_connections
        m_copy.num_open_connections = self.num_open_connections
        m_copy.num_failed_login_attempts = self.num_failed_login_attempts
        m_copy.num_users = self.num_users
        m_copy.num_logged_in_users = self.num_logged_in_users
        m_copy.num_login_events = self.num_login_events
        m_copy.num_processes = self.num_processes
        m_copy.num_open_connections_recent = self.num_open_connections_recent
        m_copy.num_failed_login_attempts_recent = self.num_failed_login_attempts_recent
        m_copy.num_users_recent = self.num_users_recent
        m_copy.num_logged_in_users_recent = self.num_login_events_recent
        m_copy.num_login_events_recent = self.num_login_events_recent
        m_copy.num_processes_recent = self.num_processes_recent
        m_copy.num_pids = self.num_pids
        m_copy.num_pids_recent = self.num_pids_recent
        m_copy.cpu_percent = self.cpu_percent
        m_copy.cpu_percent_recent = self.cpu_percent_recent
        m_copy.mem_current = self.mem_current
        m_copy.mem_current_recent = self.mem_current_recent
        m_copy.mem_total = self.mem_total
        m_copy.mem_total_recent = self.mem_total_recent
        m_copy.mem_percent = self.mem_percent
        m_copy.mem_percent_recent = self.mem_percent_recent
        m_copy.blk_read = self.blk_read
        m_copy.blk_read_recent = self.blk_read_recent
        m_copy.blk_write = self.blk_write
        m_copy.blk_write_recent = self.blk_write_recent
        m_copy.net_rx = self.net_rx
        m_copy.net_rx_recent = self.net_rx_recent
        m_copy.net_tx = self.net_tx
        m_copy.net_tx_recent = self.net_tx_recent
        return m_copy




