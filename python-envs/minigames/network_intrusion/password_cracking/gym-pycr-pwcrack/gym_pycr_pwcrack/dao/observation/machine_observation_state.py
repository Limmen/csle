from typing import List
import copy
from gym_pycr_pwcrack.dao.observation.port_observation_state import PortObservationState
from gym_pycr_pwcrack.dao.observation.vulnerability_observation_state import VulnerabilityObservationState
from gym_pycr_pwcrack.dao.network.credential import Credential
from gym_pycr_pwcrack.dao.observation.connection_observation_state import ConnectionObservationState
from gym_pycr_pwcrack.dao.network.node import Node
from gym_pycr_pwcrack.dao.network.node_type import NodeType

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
        self.backdoor_tried = False
        self.install_tools_tried = False
        self.sambacry_tried = False
        self.shellshock_tried = False
        self.dvwa_sql_injection_tried = False
        self.cve_2015_3306_tried = False
        self.cve_2015_1427_tried = False
        self.reachable = set()


    def __str__(self):
        return "ip:{},os:{},shell_access:{},num_ports:{},num_cve_vuln:{},num_cred{},num_ssh_connections:{}," \
               "num_ftp_connections:{},num_telnet_connections:{}, num_osvdb_vuln:{}, hostnames:{}, trace:{}, " \
               "filesystem_searched:{},telnet_brute_tried:{},ssh_brute_tried:{},ftp_brute_tried:{}," \
               "cassandra_brute_tried:{},irc_brute_tried:{},mongo_brute_tried:{},mysql_brute_tried:{}," \
               "smtp_brute_tried:{},postgres_brute_tried:{},tools_installed:{},backdoor_installed:{}," \
               "num_backdoor_credentials:{},num_reachable_nodes:{},backdoor_tried:{},install_tools_tried:{}," \
               "sambacry_tried:{},shellshock_tried:{},dvwa_sql_injection_tried:{},cve_2015_3306_tried:{}," \
               "cve_2015_1427_tried:{}".format(
            self.ip, self.os,  self.shell_access, len(self.ports), len(self.cve_vulns),
            len(self.shell_access_credentials), len(self.ssh_connections), len(self.ftp_connections),
            len(self.telnet_connections), len(self.osvdb_vulns), self.hostnames, self.trace, self.filesystem_searched,
            self.telnet_brute_tried, self.ssh_brute_tried, self.ftp_brute_tried, self.cassandra_brute_tried,
            self.irc_brute_tried, self.mongo_brute_tried, self.mysql_brute_tried, self.smtp_brute_tried,
            self.postgres_brute_tried, self.tools_installed, self.backdoor_installed, len(self.backdoor_credentials),
            len(self.reachable), self.backdoor_tried, self.install_tools_tried, self.sambacry_tried,
            self.shellshock_tried, self.dvwa_sql_injection_tried, self.cve_2015_3306_tried, self.cve_2015_1427_tried)

    def sort_ports(self):
        for p in self.ports:
            p.port = int(p.port)
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


    def copy(self):
        m_copy = MachineObservationState(ip=self.ip)
        m_copy.os = self.os
        m_copy.ports = copy.deepcopy(self.ports)
        m_copy.cve_vulns = copy.deepcopy(self.cve_vulns)
        m_copy.osvdb_vulns = copy.deepcopy(self.osvdb_vulns)
        m_copy.shell_access = self.shell_access
        m_copy.shell_access_credentials = self.shell_access_credentials
        m_copy.backdoor_credentials = self.backdoor_credentials
        m_copy.logged_in = self.logged_in
        m_copy.root = self.root
        m_copy.flags_found = self.flags_found
        m_copy.filesystem_searched = self.filesystem_searched
        m_copy.untried_credentials = self.untried_credentials
        m_copy.ssh_connections = self.ssh_connections
        m_copy.ftp_connections = self.ftp_connections
        m_copy.telnet_connections = self.telnet_connections
        m_copy.logged_in_services = self.logged_in_services
        m_copy.root_services = self.root_services
        m_copy.hostnames = self.hostnames
        m_copy.trace = self.trace
        m_copy.telnet_brute_tried = self.telnet_brute_tried
        m_copy.ssh_brute_tried = self.ssh_brute_tried
        m_copy.ftp_brute_tried = self.ftp_brute_tried
        m_copy.cassandra_brute_tried = self.cassandra_brute_tried
        m_copy.irc_brute_tried = self.irc_brute_tried
        m_copy.mongo_brute_tried = self.mongo_brute_tried
        m_copy.mysql_brute_tried = self.mysql_brute_tried
        m_copy.smtp_brute_tried = self.smtp_brute_tried
        m_copy.postgres_brute_tried = self.postgres_brute_tried
        m_copy.tools_installed = self.tools_installed
        m_copy.backdoor_installed = self.backdoor_installed
        m_copy.backdoor_tried = self.backdoor_tried
        m_copy.install_tools_tried = self.install_tools_tried
        m_copy.reachable = self.reachable
        m_copy.sambacry_tried = self.sambacry_tried
        m_copy.shellshock_tried = self.shellshock_tried
        m_copy.dvwa_sql_injection_tried = self.dvwa_sql_injection_tried
        m_copy.cve_2015_3306_tried = self.cve_2015_3306_tried
        m_copy.cve_2015_1427_tried = self.cve_2015_1427_tried
        return m_copy

    def to_node(self) -> Node:
        vulnerabilities = list(map(lambda x: x.to_vulnerability(), self.cve_vulns))
        services = []
        for port in self.ports:
            services.append(port.to_network_service())
        for service in services:
            for cr in self.shell_access_credentials:
                if service.name.lower() == cr.service.lower():
                    service.credentials.append(cr)
        root_usernames = []
        for c in self.ssh_connections + self.telnet_connections + self.ftp_connections:
            if c.root:
                root_usernames.append(c.username)

        node = Node(ip=self.ip, ip_id=int(self.ip.rsplit(".", 1)[-1]), id=int(self.ip.rsplit(".", 1)[-1]),
                    type = NodeType.SERVER, os=self.os,
                    flags=self.flags_found, level=3, vulnerabilities=vulnerabilities, services=services,
                    credentials=self.shell_access_credentials, root_usernames=root_usernames, visible=False,
                    reachable_nodes=self.reachable, firewall=False)
        return node


