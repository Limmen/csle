from typing import List, Set
import copy
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_observation.common.emulation_port_observation_state import EmulationPortObservationState
from csle_common.dao.emulation_observation.common.emulation_vulnerability_observation_state \
    import EmulationVulnerabilityObservationState
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState
from csle_common.dao.emulation_action_result.nmap_host_result import NmapHostResult
from csle_common.dao.emulation_action_result.nmap_trace import NmapTrace


class EmulationAttackerMachineObservationState:
    """
    Represent's the attacker's belief state of a component in the emulation
    """

    def __init__(self, ips : List[str]):
        """
        Initializes the state

        :param ips: the ip of the machine
        """
        assert ips is not None and len(ips) > 0
        self.ips = ips
        self.os="unknown"
        self.ports : List[EmulationPortObservationState] = []
        self.cve_vulns : List[EmulationVulnerabilityObservationState] = []
        self.osvdb_vulns: List[EmulationVulnerabilityObservationState] = []
        self.shell_access = False
        self.shell_access_credentials : List[Credential] = []
        self.backdoor_credentials: List[Credential] = []
        self.logged_in = False
        self.root = False
        self.flags_found = set()
        self.filesystem_searched = False
        self.untried_credentials = False
        self.ssh_connections :List[EmulationConnectionObservationState] = []
        self.ftp_connections: List[EmulationConnectionObservationState] = []
        self.telnet_connections: List[EmulationConnectionObservationState] = []
        self.logged_in_services : List[str] = []
        self.root_services : List[str] = []
        self.hostnames : List[str] = []
        self.trace : NmapTrace = None
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
        self.cve_2016_10033_tried = False
        self.cve_2010_0426_tried = False
        self.cve_2015_5602_tried = False
        self.reachable : Set[str] = set()


    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ips:{},os:{},shell_access:{},logged_in:{},root:{},num_ports:{},num_cve_vuln:{},num_cred:{}," \
               "num_ssh_connections:{}," \
               "num_ftp_connections:{},num_telnet_connections:{}, num_osvdb_vuln:{},hostnames:{},trace:{}, " \
               "filesystem_searched:{},telnet_brute_tried:{},ssh_brute_tried:{},ftp_brute_tried:{}," \
               "cassandra_brute_tried:{},irc_brute_tried:{},mongo_brute_tried:{},mysql_brute_tried:{}," \
               "smtp_brute_tried:{},postgres_brute_tried:{},tools_installed:{},backdoor_installed:{}," \
               "num_backdoor_credentials:{},num_reachable_nodes:{},backdoor_tried:{},install_tools_tried:{}," \
               "sambacry_tried:{},shellshock_tried:{},dvwa_sql_injection_tried:{},cve_2015_3306_tried:{}," \
               "cve_2015_1427_tried:{},cve_2016_10033_tried:{},cve_2010_0426_tried:{},cve_2015_5602_tried:{}," \
               "flags_found:{}".format(
            self.ips, self.os,  self.shell_access, self.logged_in, self.root, len(self.ports), len(self.cve_vulns),
            len(self.shell_access_credentials), len(self.ssh_connections), len(self.ftp_connections),
            len(self.telnet_connections), len(self.osvdb_vulns), self.hostnames, self.trace, self.filesystem_searched,
            self.telnet_brute_tried, self.ssh_brute_tried, self.ftp_brute_tried, self.cassandra_brute_tried,
            self.irc_brute_tried, self.mongo_brute_tried, self.mysql_brute_tried, self.smtp_brute_tried,
            self.postgres_brute_tried, self.tools_installed, self.backdoor_installed, len(self.backdoor_credentials),
            len(self.reachable), self.backdoor_tried, self.install_tools_tried, self.sambacry_tried,
            self.shellshock_tried, self.dvwa_sql_injection_tried, self.cve_2015_3306_tried, self.cve_2015_1427_tried,
            self.cve_2016_10033_tried, self.cve_2010_0426_tried, self.cve_2015_5602_tried, self.flags_found)

    def sort_ports(self) -> None:
        """
        Sorts the list of ports
        :return: None
        """
        for p in self.ports:
            p.port = int(p.port)
        self.ports = sorted(self.ports, key=lambda x: x.kafka_port, reverse=False)

    def sort_cve_vuln(self, vuln_lookup) -> None:
        """
        Sorts the list of vulnerabilities

        :param vuln_lookup: a lookup table for converting vulnerabilities between ids and names
        :return: None
        """
        self.cve_vulns = sorted(self.cve_vulns, key=lambda x: self._vuln_lookup(name=x.name, lookup_table=vuln_lookup),
                                reverse=False)

    def sort_shell_access(self, service_lookup) -> None:
        """
        Sorts the list of shell access credentials

        :param service_lookup: a lookup table for converting between service names and service ids
        :return: None
        """
        self.shell_access_credentials = sorted(
            self.shell_access_credentials,
            key=lambda x: service_lookup[x.service] if x.service is not None else x.username,
            reverse=False)

    def _vuln_lookup(self, name, lookup_table) -> int:
        """
        Looks up the id of a vulnerability in a lookup table

        :param name: the name of the vulnerability
        :param lookup_table: the lookup table
        :return: the id of the vulnerability
        """
        if name in lookup_table:
            return lookup_table[name]
        else:
            return lookup_table["unknown"]

    def sort_osvdb_vuln(self) -> None:
        """
        Sorts the OSVDB vulnerabilities

        :return: None
        """
        self.osvdb_vulns = sorted(self.osvdb_vulns, key=lambda x: x.osvdb_id, reverse=False)

    def cleanup(self):
        """
        Cleans up environment state. This method is particularly useful in emulation mode where there are
        SSH/Telnet/FTP... connections that should be cleaned up, as well as background threads.

        :return: None
        """
        for c in self.ssh_connections:
            c.cleanup()
        for c in self.ftp_connections:
            c.cleanup()
        for c in self.telnet_connections:
            c.cleanup()


    def copy(self) -> "EmulationAttackerMachineObservationState":
        """
        :return: a copy of the DTO
        """
        m_copy = EmulationAttackerMachineObservationState(ips=self.ips)
        m_copy.os = self.os
        m_copy.ports = copy.deepcopy(self.ports)
        m_copy.cve_vulns = copy.deepcopy(self.cve_vulns)
        m_copy.osvdb_vulns = copy.deepcopy(self.osvdb_vulns)
        m_copy.shell_access = self.shell_access
        m_copy.shell_access_credentials = copy.deepcopy(self.shell_access_credentials)
        m_copy.backdoor_credentials = copy.deepcopy(self.backdoor_credentials)
        m_copy.logged_in = self.logged_in
        m_copy.root = self.root
        m_copy.flags_found = copy.deepcopy(self.flags_found)
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
        m_copy.cve_2016_10033_tried = self.cve_2016_10033_tried
        m_copy.cve_2010_0426_tried = self.cve_2010_0426_tried
        m_copy.cve_2015_5602_tried = self.cve_2015_5602_tried
        return m_copy


    @staticmethod
    def from_nmap_result(nmap_host_result: NmapHostResult) -> "EmulationAttackerMachineObservationState":
        """
        Converts the NmapHostResultDTO into a a AttackerMachineObservationState

        :return: the created AttackerMachineObservationState
        """
        m_obs = EmulationAttackerMachineObservationState(ips=nmap_host_result.ips)
        ports = list(map(lambda x: x.to_obs(), nmap_host_result.ports))
        m_obs.ports = ports
        if nmap_host_result.os is not None:
            m_obs.os = nmap_host_result.os.vendor.lower()
        vulnerabilities = list(map(lambda x: x.to_obs(), nmap_host_result.vulnerabilities))
        m_obs.cve_vulns = vulnerabilities
        credentials = list(map(lambda x: x.to_obs(), nmap_host_result.credentials))
        m_obs.shell_access_credentials = credentials
        if len(credentials) > 0:
            m_obs.shell_access = True
            m_obs.untried_credentials = True
        m_obs.hostnames = nmap_host_result.hostnames
        m_obs.trace = nmap_host_result.trace
        return m_obs

    def ips_match(self, ips: List[str]) -> bool:
        """
        Checks if a list of ips overlap with the ips of this machine

        :param ips: the list of ips to check
        :return:  True if they match, False otherwise
        """
        for ip in self.ips:
            if ip in ips:
                return True
        return False

    @staticmethod
    def from_dict(d: dict) -> "EmulationAttackerMachineObservationState":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationAttackerMachineObservationState(ips=d["ips"])
        obj.os = d["os"]
        obj.ports = list(map(lambda x: EmulationPortObservationState.from_dict(x), d["ports"]))
        obj.cve_vulns = list(map(lambda x: EmulationVulnerabilityObservationState.from_dict(x), d["cve_vulns"]))
        obj.osvdb_vulns = list(map(lambda x: EmulationVulnerabilityObservationState.from_dict(x), d["osvdb_vulns"]))
        obj.shell_access = d["shell_access"]
        obj.shell_access_credentials = list(map(lambda x: Credential.from_dict(x), d["shell_access_credentials"]))
        obj.backdoor_credentials = list(map(lambda x: Credential.from_dict(x), d["backdoor_credentials"]))
        obj.logged_in = d["logged_in"]
        obj.root = d["root"]
        obj.flags_found = set(d["flags_found"])
        obj.filesystem_searched = d["filesystem_searched"]
        obj.untried_credentials = d["untried_credentials"]
        obj.logged_in_services = d["logged_in_services"]
        obj.root_services = d["root_services"]
        obj.hostnames = d["hostnames"]
        obj.trace = d["trace"]
        obj.telnet_brute_tried = d["telnet_brute_tried"]
        obj.ssh_brute_tried = d["ssh_brute_tried"]
        obj.ftp_brute_tried = d["ftp_brute_tried"]
        obj.cassandra_brute_tried = d["cassandra_brute_tried"]
        obj.irc_brute_tried = d["irc_brute_tried"]
        obj.mongo_brute_tried = d["mongo_brute_tried"]
        obj.mysql_brute_tried = d["mysql_brute_tried"]
        obj.smtp_brute_tried = d["smtp_brute_tried"]
        obj.postgres_brute_tried = d["postgres_brute_tried"]
        obj.tools_installed = d["tools_installed"]
        obj.backdoor_installed = d["backdoor_installed"]
        obj.backdoor_tried = d["backdoor_tried"]
        obj.install_tools_tried = d["install_tools_tried"]
        obj.sambacry_tried = d["sambacry_tried"]
        obj.shellshock_tried = d["shellshock_tried"]
        obj.dvwa_sql_injection_tried = d["dvwa_sql_injection_tried"]
        obj.cve_2015_3306_tried = d["cve_2015_3306_tried"]
        obj.cve_2015_1427_tried = d["cve_2015_1427_tried"]
        obj.cve_2016_10033_tried = d["cve_2016_10033_tried"]
        obj.cve_2010_0426_tried = d["cve_2010_0426_tried"]
        obj.cve_2015_5602_tried = d["cve_2015_5602_tried"]
        obj.reachable = set(d["reachable"])
        return obj

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ips"] = self.ips
        d["os"] = self.os
        d["ports"] = list(map(lambda x: x.to_dict(), self.ports))
        d["cve_vulns"] = list(map(lambda x: x.to_dict(), self.cve_vulns))
        d["osvdb_vulns"] = list(map(lambda x: x.to_dict(), self.osvdb_vulns))
        d["shell_access"] = self.shell_access
        d["shell_access_credentials"] = list(map(lambda x: x.to_dict(),
                                                 self.shell_access_credentials))
        d["backdoor_credentials"] = list(map(lambda x: x.to_dict(),
                                                 self.backdoor_credentials))
        d["logged_in"] = self.logged_in
        d["root"] = self.root
        d["flags_found"] = list(self.flags_found)
        d["filesystem_searched"] = self.filesystem_searched
        d["untried_credentials"] = self.untried_credentials
        d["logged_in_services"] = self.logged_in_services
        d["root_services"] = self.root_services
        d["hostnames"] = self.hostnames
        if self.trace is None:
            d["trace"] = None
        else:
            d["trace"] = self.trace.to_dict()
        d["telnet_brute_tried"] = self.telnet_brute_tried
        d["ssh_brute_tried"] = self.ssh_brute_tried
        d["ftp_brute_tried"] = self.ftp_brute_tried
        d["cassandra_brute_tried"] = self.cassandra_brute_tried
        d["irc_brute_tried"] = self.irc_brute_tried
        d["mongo_brute_tried"] = self.mongo_brute_tried
        d["mysql_brute_tried"] = self.mysql_brute_tried
        d["smtp_brute_tried"] = self.smtp_brute_tried
        d["postgres_brute_tried"] = self.postgres_brute_tried
        d["tools_installed"] = self.tools_installed
        d["backdoor_installed"] = self.backdoor_installed
        d["backdoor_tried"] = self.backdoor_tried
        d["install_tools_tried"] = self.install_tools_tried
        d["sambacry_tried"] = self.sambacry_tried
        d["shellshock_tried"] = self.shellshock_tried
        d["dvwa_sql_injection_tried"] = self.dvwa_sql_injection_tried
        d["cve_2015_3306_tried"] = self.cve_2015_3306_tried
        d["cve_2015_1427_tried"] = self.cve_2015_1427_tried
        d["cve_2016_10033_tried"] = self.cve_2016_10033_tried
        d["cve_2010_0426_tried"] = self.cve_2010_0426_tried
        d["cve_2015_5602_tried"] = self.cve_2015_5602_tried
        d["reachable"] = list(self.reachable)
        return d



