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
        self.cve_vulns : List[VulnerabilityObservationState] = []
        self.osvdb_vulns: List[VulnerabilityObservationState] = []
        self.shell_access = False
        self.shell_access_credentials : List[Credential] = []
        self.backdoor_credentials: List[Credential] = []
        self.logged_in = False
        self.root = False
        self.flags_found = set()
        self.filesystem_searched = False
        self.untried_credentials = False
        self.ssh_connections :List[ConnectionObservationState] = []
        self.ftp_connections: List[ConnectionObservationState] = []
        self.telnet_connections: List[ConnectionObservationState] = []
        self.logged_in_services = []
        self.root_services = []
        self.hostnames = []
        self.trace = None
        self.telnet_brute_tried = False
        self.ssh_brute_tried = False
        self.ftp_brute_tried = False
        self.cassandra_brute_tried = False
        self.irc_brute_tried = False
        self.mongo_brute_tried = False
        self.mysql_brute_tried = False
        self.smtp_brute_tried = False
        self.postgres_brute_tried = False
        self.tools_installed = False
        self.backdoor_installed = False
        self.reachable = set()


    def __str__(self):
        return "ip:{},os:{},shell_access:{},num_ports:{},num_cve_vuln:{},num_cred{},num_ssh_connections:{}," \
               "num_ftp_connections:{},num_telnet_connections:{}, num_osvdb_vuln:{}, hostnames:{}, trace:{}, " \
               "filesystem_searched:{},telnet_brute_tried:{},ssh_brute_tried:{},ftp_brute_tried:{}," \
               "cassandra_brute_tried:{},irc_brute_tried:{},mongo_brute_tried:{},mysql_brute_tried:{}," \
               "smtp_brute_tried:{},postgres_brute_tried:{},tools_installed:{},backdoor_installed:{}," \
               "num_backdoor_credentials:{},num_reachable_nodes:{}".format(
            self.ip, self.os,  self.shell_access, len(self.ports), len(self.cve_vulns),
            len(self.shell_access_credentials), len(self.ssh_connections), len(self.ftp_connections),
            len(self.telnet_connections), len(self.osvdb_vulns), self.hostnames, self.trace, self.filesystem_searched,
            self.telnet_brute_tried, self.ssh_brute_tried, self.ftp_brute_tried, self.cassandra_brute_tried,
            self.irc_brute_tried, self.mongo_brute_tried, self.mysql_brute_tried, self.smtp_brute_tried,
            self.postgres_brute_tried, self.tools_installed, self.backdoor_installed, len(self.backdoor_credentials),
            len(self.reachable))

    def sort_ports(self):
        self.ports = sorted(self.ports, key=lambda x: x.port, reverse=False)

    def sort_cve_vuln(self, vuln_lookup):
        self.cve_vulns = sorted(self.cve_vulns, key=lambda x: self._vuln_lookup(name=x.name, lookup_table=vuln_lookup),
                                reverse=False)

    def sort_shell_access(self, service_lookup):
        self.shell_access_credentials = sorted(self.shell_access_credentials,
                                               key=lambda x: service_lookup[x.service] if x.service is not None else x.username,
                                               reverse=False)

    def _vuln_lookup(self, name, lookup_table):
        if name in lookup_table:
            return lookup_table[name]
        else:
            return lookup_table["unknown"]

    def sort_osvdb_vuln(self):
        self.osvdb_vulns = sorted(self.osvdb_vulns, key=lambda x: x.osvdb_id, reverse=False)

    def cleanup(self):
        """
        Cleans up environment state. This method is particularly useful in cluster mode where there are
        SSH/Telnet/FTP... connections that should be cleaned up, as well as background threads.

        :return: None
        """
        for c in self.ssh_connections:
            c.cleanup()
        for c in self.ftp_connections:
            c.cleanup()
        for c in self.telnet_connections:
            c.cleanup()