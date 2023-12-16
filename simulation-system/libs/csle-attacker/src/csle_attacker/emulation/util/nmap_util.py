from typing import Tuple, List, Union, Any
import time
import threading
import xml.etree.ElementTree as ET
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action \
    import EmulationAttackerAction
from csle_common.util.env_dynamics_util import EnvDynamicsUtil
from csle_common.dao.emulation_observation.attacker.emulation_attacker_machine_observation_state \
    import EmulationAttackerMachineObservationState
import csle_common.constants.constants as constants
from csle_common.dao.emulation_action_result.nmap_scan_result import NmapScanResult
from csle_common.dao.emulation_action_result.nmap_host_result import NmapHostResult
from csle_common.dao.emulation_action_result.nmap_port_status import NmapPortStatus
from csle_common.dao.emulation_action_result.nmap_host_status import NmapHostStatus
from csle_common.dao.emulation_action_result.nmap_port import NmapPort
from csle_common.dao.emulation_action_result.nmap_addr_type import NmapAddrType
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_action_result.nmap_os import NmapOs
from csle_common.dao.emulation_action_result.nmap_vuln import NmapVuln
from csle_common.dao.emulation_action_result.nmap_brute_credentials import NmapBruteCredentials
from csle_common.dao.emulation_action_result.nmap_hop import NmapHop
from csle_common.dao.emulation_action_result.nmap_trace import NmapTrace
from csle_common.dao.emulation_action_result.nmap_http_enum import NmapHttpEnum
from csle_common.dao.emulation_action_result.nmap_http_grep import NmapHttpGrep
from csle_common.dao.emulation_action_result.nmap_vulscan import NmapVulscan
from csle_common.util.emulation_util import EmulationUtil
from csle_common.util.connection_util import ConnectionUtil
from csle_common.logging.log import Logger


class NmapUtil:
    """
    Class containing utility functions for the nmap-related functionality to the emulation
    """

    @staticmethod
    def parse_nmap_scan(file_name: str, emulation_env_config: EmulationEnvConfig, conn=None, dir: str = "") \
            -> ET.Element:
        """
        Parses an XML file containing the result of an nmap scan

        :param file_name: name of the file to parse
        :param conn: the SSH connection to use for parsing
        :param dir: the directory to parse the XML file
        :param emulation_env_config: environment config
        :return: the parsed xml file
        """
        if conn is None:
            conn = emulation_env_config.get_hacker_connection()
        if dir is None or dir == "":
            dir = constants.NMAP.RESULTS_DIR

        sftp_client = conn.open_sftp()
        file_name = str(dir + file_name).strip()
        remote_file = sftp_client.open(file_name)
        try:
            xml_tree = ET.parse(remote_file)
        finally:
            remote_file.close()
        xml_data = xml_tree.getroot()
        return xml_data

    @staticmethod
    def parse_nmap_scan_xml(xml_data, ips: List[str], action: EmulationAttackerAction) -> NmapScanResult:
        """
        Parses an XML Tree into a DTO

        :param xml_data: the xml tree to parse
        :param ips: ips of the source of the scan
        :param action: the action of the scan
        :return: parsed nmap scan result
        """
        hosts: List[NmapHostResult] = []
        for child in xml_data:
            if child.tag == constants.NMAP_XML.HOST:
                host = NmapUtil._parse_nmap_host_xml(child, action=action)
                hosts = NmapUtil._merge_nmap_hosts(host, hosts)
        result = NmapScanResult(hosts=hosts, ips=ips)
        return result

    @staticmethod
    def _parse_nmap_host_xml(xml_data, action: EmulationAttackerAction) -> NmapHostResult:
        """
        Parses a host-element in the XML tree

        :param xml_data: the host element
        :param action: action of the scan
        :return: parsed nmap host result
        """
        ip_addr = None
        mac_addr = None
        hostnames = []
        ports: List[NmapPort] = []
        vulnerabilities: List[NmapVuln] = []
        credentials: List[NmapBruteCredentials] = []
        os = None
        os_matches = []
        status = NmapHostStatus.UP
        trace = None
        for child in list(xml_data.iter()):
            if child.tag == constants.NMAP_XML.ADDRESS:
                addr, type = NmapUtil._parse_nmap_address_xml(child)
                if type == NmapAddrType.MAC:
                    mac_addr = addr
                else:
                    ip_addr = addr
            elif child.tag == constants.NMAP_XML.HOSTNAMES:
                hostnames = NmapUtil._parse_nmap_hostnames_xml(child)
            elif child.tag == constants.NMAP_XML.PORTS:
                ports, vulnerabilities, credentials = NmapUtil._parse_nmap_ports_xml(child, action=action)
            elif child.tag == constants.NMAP_XML.OS:
                os_matches = NmapUtil._parse_nmap_os_xml(child)
                os = NmapOs.get_best_match(os_matches)
            elif child.tag == constants.NMAP_XML.TRACE:
                trace = NmapUtil._parse_nmap_trace_xml(child)
        nmap_host_result = NmapHostResult(status=status, ips=[ip_addr], mac_addr=mac_addr,
                                          hostnames=hostnames, ports=ports, os=os, os_matches=os_matches,
                                          vulnerabilities=vulnerabilities, credentials=credentials, trace=trace)
        return nmap_host_result

    @staticmethod
    def _parse_nmap_status_xml(xml_data) -> NmapPortStatus:
        """
        Parses a status element in the xml tree

        :param xml_data: the status XML element
        :return: parsed Nmap Port-Status DTO
        """
        status = NmapPortStatus.DOWN
        status_val = xml_data.attrib[constants.NMAP_XML.STATE]
        if status_val == constants.NMAP_XML.STATUS_UP:
            status = NmapPortStatus.UP
        return status

    @staticmethod
    def _parse_nmap_address_xml(xml_data) -> Tuple[str, NmapAddrType]:
        """
        Parses a address element in the xml tree

        :param xml_data: the address XML element
        :return: (address, addresstype)
        """
        type = NmapAddrType.IP
        addr = xml_data.attrib[constants.NMAP_XML.ADDR]
        addrtype_val = xml_data.attrib[constants.NMAP_XML.ADDR_TYPE]
        if constants.NMAP_XML.IP in addrtype_val:
            type = NmapAddrType.IP
        elif constants.NMAP_XML.MAC in addrtype_val:
            type = NmapAddrType.MAC
        return addr, type

    @staticmethod
    def _parse_nmap_hostnames_xml(xml_data) -> List[str]:
        """
        Parses a hostnames element in the XML tree

        :param xml_data: the hostnames XML element
        :return: a list of hostnames
        """
        hostnames = []
        for child in list(xml_data.iter()):
            if child.tag == constants.NMAP_XML.HOSTNAME:
                hostnames.append(child.attrib[constants.NMAP_XML.NAME])
        return hostnames

    @staticmethod
    def _parse_nmap_ports_xml(xml_data, action: EmulationAttackerAction) \
            -> Tuple[List[NmapPort], List[NmapVuln], List[NmapBruteCredentials]]:
        """
        Parses a ports XML element in the XML tree

        :param xml_data: the ports XML element
        :param action: action of the scan
        :return: (List NmapPort, List NmapVuln, ListNmapBruteCredentials)
        """
        ports = []
        vulnerabilities = []
        credentials = []
        http_enum = None
        http_grep = None
        vulscan = None
        for child in list(xml_data.iter()):
            if child.tag == constants.NMAP_XML.PORT:
                port_status = NmapPortStatus.DOWN
                protocol = TransportProtocol._from_str(child.attrib["protocol"])
                port_id = child.attrib[constants.NMAP_XML.PORT_ID]
                service_name = constants.NMAP_XML.UNKNOWN
                service_version = ""
                service_fp = ""
                for child_2 in list(child.iter()):
                    if child_2.tag == constants.NMAP_XML.STATE:
                        port_status = NmapUtil._parse_nmap_port_status_xml(child_2)
                    elif child_2.tag == constants.NMAP_XML.SERVICE:
                        service_name = NmapUtil._parse_nmap_service_name_xml(child_2)
                        service_version = NmapUtil._parse_nmap_service_version_xml(child_2)
                        service_fp = NmapUtil._parse_nmap_service_fp_xml(child_2)
                    elif child_2.tag == constants.NMAP_XML.SCRIPT:
                        result, brute_vuln = NmapUtil._parse_nmap_script(child_2, port=port_id, protocol=protocol,
                                                                         service=service_name, action=action)
                        if result is not None:
                            if isinstance(result, list) and len(result) > 0 and isinstance(result[0], NmapVuln):
                                vulnerabilities = result
                            elif isinstance(result, list) and len(result) > 0 \
                                    and isinstance(result[0], NmapBruteCredentials):
                                credentials = result
                                if brute_vuln is not None:
                                    vulnerabilities.append(brute_vuln)
                            elif isinstance(result, NmapHttpEnum):
                                http_enum = result
                            elif isinstance(result, NmapHttpGrep):
                                http_grep = result
                            elif isinstance(result, NmapVulscan):
                                vulscan = result
                if port_status == NmapPortStatus.UP:
                    port = NmapPort(port_id=port_id, protocol=protocol, status=port_status, service_name=service_name,
                                    http_enum=http_enum, http_grep=http_grep, vulscan=vulscan,
                                    service_version=service_version, service_fp=service_fp)
                    ports.append(port)
        return ports, vulnerabilities, credentials

    @staticmethod
    def _parse_nmap_service_name_xml(xml_data) -> Union[str, Any]:
        """
        Parses a XML service name element

        :param xml_data: the XML service element
        :return: the name of the service
        """
        return xml_data.attrib[constants.NMAP_XML.NAME]

    @staticmethod
    def _parse_nmap_service_version_xml(xml_data) -> str:
        """
        Parses a XML service element

        :param xml_data: the XML service element
        :return: the version of the service
        """
        version = ""
        if constants.NMAP_XML.VERSION in xml_data.keys():
            version = xml_data.attrib[constants.NMAP_XML.VERSION]
        return version

    @staticmethod
    def _parse_nmap_service_fp_xml(xml_data) -> str:
        """
        Parses a XML service element

        :param xml_data: the XML service element
        :return: the fingerprint of the service
        """
        servicefp = ""
        if constants.NMAP_XML.SERVICEFP in xml_data.keys():
            servicefp = xml_data.attrib[constants.NMAP_XML.SERVICEFP]
        return servicefp

    @staticmethod
    def _parse_nmap_port_status_xml(xml_data) -> NmapPortStatus:
        """
        Parses a XML port status element

        :param xml_data: the XML port status element
        :return: the parsed port status
        """
        port_status = NmapPortStatus.DOWN
        if xml_data.attrib[constants.NMAP_XML.STATE] == constants.NMAP_XML.OPEN_STATE:
            port_status = NmapPortStatus.UP
        return port_status

    @staticmethod
    def _parse_nmap_os_xml(xml_data) -> List[NmapOs]:
        """
        Parses NMAP OS XML element

        :param xml_data: the XML OS element
        :return: Parsed NmapOS
        """
        os_matches = []
        for child in list(xml_data.iter()):
            if child.tag == constants.NMAP_XML.OS_MATCH:
                name = child.attrib[constants.NMAP_XML.NAME]
                accuracy = int(child.attrib[constants.NMAP_XML.ACCURACY])
                t_acc_cmp = 0
                vendor = ""
                osfamily = ""
                for c2 in list(child.iter()):
                    if c2.tag == constants.NMAP_XML.OS_CLASS:
                        t_acc = int(c2.attrib[constants.NMAP_XML.ACCURACY])
                        if t_acc > t_acc_cmp:
                            vendor = c2.attrib[constants.NMAP_XML.VENDOR]
                            osfamily = c2.attrib[constants.NMAP_XML.OS_FAMILY]
                            t_acc_cmp = t_acc

                os_match = NmapOs(name=name, vendor=vendor, osfamily=osfamily, accuracy=accuracy)
                os_matches.append(os_match)
        return os_matches

    @staticmethod
    def _parse_nmap_table_vuln(xml_data, port: int, protocol: TransportProtocol, service: str) -> NmapVuln:
        """
        Parses a Table XML element with vulnerabilities

        :param xml_data: the XML table element
        :param port: the port element parent
        :param protocol: the protocol of the parent
        :param service: the service running on the port
        :return: parsed Nmap vulnerability
        """
        cvss = constants.VULNERABILITIES.default_cvss
        id = ""
        for child in list(xml_data.iter()):
            if child.tag == constants.NMAP_XML.ELEM:
                if constants.NMAP_XML.KEY in child.keys():
                    if child.attrib[constants.NMAP_XML.KEY] == constants.NMAP_XML.CVSS:
                        cvss = float(child.text)
                    elif child.attrib[constants.NMAP_XML.KEY] == constants.NMAP_XML.ID:
                        id = child.text
        vuln = NmapVuln(name=id, port=port, protocol=protocol, cvss=cvss, service=service)
        return vuln

    @staticmethod
    def _parse_nmap_script(xml_data, port: int, protocol: TransportProtocol, service: str,
                           action: EmulationAttackerAction) \
            -> Tuple[Union[List[NmapVuln], List[NmapBruteCredentials], NmapHttpEnum, NmapHttpGrep, NmapVulscan, None],
                     Union[NmapVuln, None]]:
        """
        Parses a XML script element

        :param xml_data: the XML script element
        :param port: the port of the parent element
        :param protocol: the protocol of the parent element
        :param service: the service running on the port
        :param action: action of the scan
        :return: a list of parsed nmap vulnerabilities or a list of parsed credentials and maybe a vuln
        """
        if constants.NMAP_XML.ID in xml_data.keys():
            if xml_data.attrib[constants.NMAP_XML.ID] == constants.NMAP_XML.VULNERS_SCRIPT_ID:
                return NmapUtil._parse_nmap_vulners(xml_data, port=port, protocol=protocol, service=service), None
            elif xml_data.attrib[constants.NMAP_XML.ID] in constants.NMAP_XML.BRUTE_SCRIPTS:
                return NmapUtil._parse_nmap_brute(xml_data, port=port, protocol=protocol, service=service,
                                                  action=action)
            elif xml_data.attrib[constants.NMAP_XML.ID] == constants.NMAP_XML.HTTP_ENUM_SCRIPT:
                return NmapUtil._parse_nmap_http_enum_xml(xml_data), None
            elif xml_data.attrib[constants.NMAP_XML.ID] == constants.NMAP_XML.HTTP_GREP_SCRIPT:
                return NmapUtil._parse_nmap_http_grep_xml(xml_data), None
            elif xml_data.attrib[constants.NMAP_XML.ID] == constants.NMAP_XML.VULSCAN_SCRIPT:
                return NmapUtil._parse_nmap_http_vulscan_xml(xml_data), None
        return None, None

    @staticmethod
    def _parse_nmap_vulners(xml_data, port: int, protocol: TransportProtocol, service: str) -> List[NmapVuln]:
        """
        Parses a XML result from a vulners scan

        :param xml_data: the XML script element
        :param port: the port of the parent element
        :param protocol: the protocol of the parent element
        :param service: the service running on the port
        :return: a list of parsed nmap vulnerabilities
        """
        vulnerabilities = []
        for child in list(xml_data.iter())[1:]:
            if child.tag == constants.NMAP_XML.TABLE:
                for c_2 in list(child.iter())[1:]:
                    if c_2.tag == constants.NMAP_XML.TABLE:
                        vuln = NmapUtil._parse_nmap_table_vuln(c_2, port=port, protocol=protocol, service=service)
                        vulnerabilities.append(vuln)
                break
        return vulnerabilities

    @staticmethod
    def _parse_nmap_brute(xml_data, port: int, protocol: TransportProtocol, service: str,
                          action: EmulationAttackerAction) -> Tuple[List[NmapBruteCredentials], NmapVuln]:
        """
        Parses a XML result from a brute force dictionary scan

        :param xml_data: the XML script element
        :param port: the port of the parent element
        :param protocol: the protocol of the parent element
        :param service: the service running on the port
        :return: a list of found credentials, vulnerability
        """
        credentials = []
        for child in list(xml_data.iter())[1:]:
            if child.tag == constants.NMAP_XML.TABLE:
                if constants.NMAP_XML.KEY in child.keys():
                    if child.attrib[constants.NMAP_XML.KEY] == constants.NMAP_XML.ACCOUNTS:
                        for c_2 in list(child.iter())[1:]:
                            if c_2.tag == constants.NMAP_XML.TABLE:
                                cred = NmapUtil._parse_nmap_table_cred(c_2, port=port, protocol=protocol,
                                                                       service=service)
                                credentials.append(cred)
                        break
        vulnerability = None
        if len(credentials) > 0:
            vuln_name = EnvDynamicsUtil.exploit_get_vuln_name(a=action)
            service_name = EnvDynamicsUtil.exploit_get_service_name(a=action)
            credentials_1 = list(map(lambda x: x.to_obs(), credentials))
            vulnerability = NmapVuln(name=vuln_name, port=port, protocol=protocol,
                                     cvss=EnvDynamicsUtil.exploit_get_vuln_cvss(a=action),
                                     service=service_name, credentials=credentials_1)
        return credentials, vulnerability

    @staticmethod
    def _parse_nmap_table_cred(xml_data, port: int, protocol: TransportProtocol, service: str) -> NmapBruteCredentials:
        """
        Parses a Table XML element with credentials

        :param xml_data: the XML table element
        :param port: the port element parent
        :param protocol: the protocol of the parent
        :param service: the service running on the port
        :return: parsed Nmap credentials
        """
        username = ""
        pw = ""
        state = ""
        for child in list(xml_data.iter()):
            if child.tag == constants.NMAP_XML.ELEM:
                if constants.NMAP_XML.KEY in child.keys():
                    if child.attrib[constants.NMAP_XML.KEY] == constants.NMAP_XML.USERNAME:
                        username = child.text
                    elif child.attrib[constants.NMAP_XML.KEY] == constants.NMAP_XML.PASSWORD:
                        pw = child.text
                    elif child.attrib[constants.NMAP_XML.KEY] == constants.NMAP_XML.STATE:
                        state = child.text
        credentials = NmapBruteCredentials(username=username, pw=pw, state=state, port=int(port), protocol=protocol,
                                           service=service)
        return credentials

    @staticmethod
    def merge_nmap_scan_result_with_state(scan_result: NmapScanResult, s: EmulationEnvState,
                                          a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Merges a NMAP scan result with an existing observation state

        :param scan_result: the scan result
        :param s: the current state
        :param a: the action just executed
        :return: s'
        """

        new_m_obs = []
        for host in scan_result.hosts:
            m_obs = EmulationAttackerMachineObservationState.from_nmap_result(host)
            # m_obs = EnvDynamicsUtil.brute_tried_flags(a=a, m_obs=m_obs)
            new_m_obs.append(m_obs)

        attacker_machine_observations = EnvDynamicsUtil.merge_new_obs_with_old(
            s.attacker_obs_state.machines, new_m_obs, action=a, emulation_env_config=s.emulation_env_config)

        s_prime = s
        s_prime.attacker_obs_state.machines = attacker_machine_observations
        s_prime.attacker_obs_state.sort_machines()
        s_prime.defender_obs_state.sort_machines()
        return s_prime

    @staticmethod
    def nmap_scan_action_helper(s: EmulationEnvState, a: EmulationAttackerAction,
                                masscan: bool = False) -> EmulationEnvState:
        """
        Helper function for executing a NMAP scan action on the emulation. Implements caching.

        :param s: the current env state
        :param a: the NMAP action to execute
        :param masscan: whether it is a masscan or not
        :return: s'
        """
        # If cache miss, then execute cmd
        cmds, file_names = a.nmap_cmds()
        if masscan:
            cmds = a.masscan_cmds()

        Logger.__call__().get_logger().info(
            f"Running NMAP scan on container: {s.emulation_env_config.containers_config.agent_ip}, commands: "
            f"{','.join(cmds)}")
        results = EmulationUtil.execute_ssh_cmds(cmds=cmds, conn=s.emulation_env_config.get_hacker_connection())
        total_time = sum(list(map(lambda x: x[2], results)))

        EmulationUtil.log_measured_action_time(total_time=total_time, action=a,
                                               emulation_env_config=s.emulation_env_config)

        # Read results
        scan_result = NmapScanResult(hosts=[], ips=[s.emulation_env_config.containers_config.agent_ip])
        for file_name in file_names:
            for i in range(constants.ENV_CONSTANTS.NUM_RETRIES):
                xml_data = NmapUtil.parse_nmap_scan(file_name=file_name,
                                                    emulation_env_config=s.emulation_env_config)
                scan_result_new = NmapUtil.parse_nmap_scan_xml(
                    xml_data, ips=[s.emulation_env_config.containers_config.agent_ip], action=a)
                s.attacker_obs_state.agent_reachable.update(scan_result.reachable)
                scan_result = NmapUtil.merge_nmap_scan_results(scan_result, scan_result_new)
        return NmapUtil.nmap_pivot_scan_action_helper(s=s, a=a, partial_result=scan_result.copy())

    @staticmethod
    def _merge_nmap_hosts(host: NmapHostResult, hosts: List[NmapHostResult]) -> List[NmapHostResult]:
        """
        Merge nmap host results

        :param host: a host to merge with an existing list of hosts
        :param hosts: the list of hosts to merge with the new host
        :return: the merged list
        """
        found = False
        for h in hosts:
            if h.ips_match(host.ips):
                found = True
                vulnerabilities = list(set(h.vulnerabilities).union(host.vulnerabilities))
                h.vulnerabilities = vulnerabilities
                ports = list(set(h.ports).union(host.ports))
                h.ports = ports
        if not found:
            hosts.append(host)
        return hosts

    @staticmethod
    def _parse_nmap_trace_xml(xml_data) -> NmapTrace:
        """
        Parses a trace XML element in the XML tree

        :param xml_data: the trace XML element
        :return: NmapTrace
        """
        hops = []
        for child in list(xml_data.iter()):
            if child.tag == constants.NMAP_XML.HOP:
                hop = NmapUtil._parse_nmap_hop_xml(child)
                hops.append(hop)
        nmap_trace = NmapTrace(hops=hops)
        return nmap_trace

    @staticmethod
    def _parse_nmap_hop_xml(xml_data) -> NmapHop:
        """
        Parses a hop XML element in the XML tree

        :param xml_data: the hop XML element
        :return: NmapHop
        """
        ttl = 0
        ip = ""
        rtt = 0.0
        host = ""
        if constants.NMAP_XML.IPADDR in xml_data.keys():
            ip = xml_data.attrib[constants.NMAP_XML.IPADDR]
        if constants.NMAP_XML.RTT in xml_data.keys():
            rtt = float(xml_data.attrib[constants.NMAP_XML.RTT])
        if constants.NMAP_XML.TTL in xml_data.keys():
            ttl = int(xml_data.attrib[constants.NMAP_XML.TTL])
        if constants.NMAP_XML.HOST in xml_data.keys():
            host = xml_data.attrib[constants.NMAP_XML.HOST]
        nmap_hop = NmapHop(ttl=ttl, ipaddr=ip, rtt=rtt, host=host)
        return nmap_hop

    @staticmethod
    def _parse_nmap_http_enum_xml(xml_data) -> NmapHttpEnum:
        """
        Parses a http enum XML element in the XML tree

        :param xml_data: the http enum XML element
        :return: HttpEnum
        """
        output = ""
        if constants.NMAP_XML.OUTPUT in xml_data.keys():
            output = xml_data.attrib[constants.NMAP_XML.OUTPUT]
        nmap_http_enum = NmapHttpEnum(output=output)
        return nmap_http_enum

    @staticmethod
    def _parse_nmap_http_grep_xml(xml_data) -> NmapHttpGrep:
        """
        Parses a http grep XML element in the XML tree

        :param xml_data: the http grep XML element
        :return: NmapHttpGrep
        """
        output = ""
        if constants.NMAP_XML.OUTPUT in xml_data.keys():
            output = xml_data.attrib[constants.NMAP_XML.OUTPUT]
        nmap_http_grep = NmapHttpGrep(output=output)
        return nmap_http_grep

    @staticmethod
    def _parse_nmap_http_vulscan_xml(xml_data) -> NmapVulscan:
        """
        Parses a vulscan XML element in the XML tree

        :param xml_data: the vulscan XML element
        :return: NmapVulScan
        """
        output = ""
        if constants.NMAP_XML.OUTPUT in xml_data.keys():
            output = xml_data.attrib[constants.NMAP_XML.OUTPUT]
        nmap_vulscan = NmapVulscan(output=output)
        return nmap_vulscan

    @staticmethod
    def merge_nmap_scan_results(scan_result_1: NmapScanResult, scan_result_2: NmapScanResult) -> NmapScanResult:
        """
        Merges two nmap scan results

        :param scan_result_1: the first result to merge
        :param scan_result_2: the second result to merge
        :return: the merged result
        """
        new_hosts = []

        for h in scan_result_2.hosts:
            new_host = True
            for h2 in scan_result_1.hosts:
                if h.ips_match(h2.ips):
                    new_host = False
            if new_host:
                new_hosts.append(h)

        for h in scan_result_1.hosts:
            for h2 in scan_result_2.hosts:
                if h.ips_match(h2.ips):
                    h.hostnames = list(set(h.hostnames).union(set(h2.hostnames)))
                    h.ports = list(set(h.ports).union(h2.ports))
                    h.vulnerabilities = list(set(h.vulnerabilities).union(h2.vulnerabilities))
                    h.credentials = list(set(h.credentials).union(h2.credentials))
                    if h.os is None:
                        h.os = h2.os
                    if h.trace is None:
                        h.trace = h2.trace

        scan_result_1.hosts = scan_result_1.hosts + new_hosts
        scan_result_1.reachable = list(set(scan_result_1.reachable + scan_result_2.reachable))
        return scan_result_1

    @staticmethod
    def nmap_pivot_scan_action_helper(s: EmulationEnvState, a: EmulationAttackerAction,
                                      partial_result: NmapScanResult) -> EmulationEnvState:
        """
        Performs an NMAP pivot scan, utilizing many compromised hosts

        :param s: the curretn state
        :param a: the attacker scan action
        :param partial_result: the initial result before pivoting
        :return: the new state
        """
        merged_scan_result = partial_result
        total_results: List[NmapScanResult] = []
        threads = []
        for machine in s.attacker_obs_state.machines:
            if machine.logged_in and machine.tools_installed and machine.backdoor_installed:
                thread = PivotNMAPScanThread(machine=machine, s=s, a=a)
                thread.start()
                threads.append(thread)
        for thread in threads:
            thread.join()
        for i in range(len(threads)):
            if merged_scan_result is not None and threads[i].scan_result is not None:
                total_results.append(threads[i].scan_result)
                merged_scan_result = NmapUtil.merge_nmap_scan_results(scan_result_1=merged_scan_result,
                                                                      scan_result_2=threads[i].scan_result.copy())
            elif merged_scan_result is None:
                total_results.append(threads[i].scan_result)
                merged_scan_result = threads[i].scan_result.copy()

        s_prime = NmapUtil.merge_nmap_scan_result_with_state(scan_result=merged_scan_result, s=s, a=a)
        new_machines_obs_1 = []
        reachable = s.attacker_obs_state.agent_reachable
        reachable.add(s.emulation_env_config.containers_config.router_ip)

        for machine in s_prime.attacker_obs_state.machines:
            if machine.logged_in and machine.tools_installed and machine.backdoor_installed:
                reachable = reachable.union(machine.reachable)

        for machine in s_prime.attacker_obs_state.machines:
            if machine.logged_in and machine.tools_installed:
                machine = EnvDynamicsUtil.ssh_backdoor_tried_flags(a=a, m_obs=machine)

            if machine.ips_match(reachable) and (machine.ips_match(a.ips) or a.index == -1):
                machine = EnvDynamicsUtil.exploit_tried_flags(a=a, m_obs=machine)

            valid_ips = True
            for ip in machine.ips:
                if int(ip.split(".")[-1]) == 1:
                    valid_ips = False
            if valid_ips:
                new_machines_obs_1.append(machine)
        s_prime.attacker_obs_state.machines = new_machines_obs_1
        s_prime.attacker_obs_state.sort_machines()
        s_prime.defender_obs_state.sort_machines()
        return s_prime


class PivotNMAPScanThread(threading.Thread):
    """
    Thread for asynchronous nmap scanning
    """

    def __init__(self, machine: EmulationAttackerMachineObservationState, a: EmulationAttackerAction,
                 s: EmulationEnvState):
        """
        Initializes the thread

        :param machine: the machine to do the details on
        :param a: the scanning action
        :param s: the current environment state
        """
        threading.Thread.__init__(self)
        self.machine = machine
        self.a = a
        self.s = s
        self.total_time = 0
        self.scan_result: NmapScanResult = NmapScanResult(hosts=[], ips=[])

    def run(self) -> None:
        """
        Main loop of the thread; performs the scanning

        :return: None
        """
        ssh_connections_alive = []
        for c in self.machine.ssh_connections:
            try:
                EmulationUtil.execute_ssh_cmds(cmds=[constants.COMMANDS.LS], conn=c.conn)
                ssh_connections_alive.append(c)
            except Exception as e:
                Logger.__call__().get_logger().debug(f"There was an error connecting to {str(e)}, {repr(e)}")
                new_conn = ConnectionUtil.reconnect_ssh(c)
                ssh_connections_alive.append(new_conn)
        self.machine.ssh_connections = ssh_connections_alive
        ssh_connections_sorted_by_root = sorted(
            self.machine.ssh_connections,
            key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.credential.username, x.root,
                           x.credential.username),
            reverse=True)
        for c in ssh_connections_sorted_by_root:
            cwd = "/home/" + c.credential.username + "/"
            cmds, file_names = self.a.nmap_cmds(machine_ips=self.machine.ips)
            results = []
            c2 = c
            for i in range(constants.ENV_CONSTANTS.NUM_RETRIES):
                try:
                    Logger.__call__().get_logger().info(
                        f"Running NMAP scan on container(s): {self.machine.ips}, commands: "
                        f"{','.join(cmds)}")
                    results = EmulationUtil.execute_ssh_cmds(cmds=cmds, conn=c2.conn)
                    break
                except Exception as e:
                    Logger.__call__().get_logger().warning(
                        f"exception execution commands for ip:{c.ip}, "
                        f"username: {c.credential.username}, conn: {c.conn}, "
                        f"transport: {c.conn.get_transport()}, active: {c.conn.get_transport().is_active()},"
                        f"{str(e)}, {repr(e)}")
                    c2 = ConnectionUtil.reconnect_ssh(c2)
                    time.sleep(constants.ENV_CONSTANTS.SLEEP_RETRY)
            total_time = sum(list(map(lambda x: x[2], results)))
            EmulationUtil.log_measured_action_time(
                total_time=total_time, action=self.a, emulation_env_config=self.s.emulation_env_config)

            # Read result
            scan_result = NmapScanResult(hosts=[], ips=self.machine.ips)
            for file_name in file_names:
                for i in range(constants.ENV_CONSTANTS.NUM_RETRIES):
                    try:
                        xml_data = NmapUtil.parse_nmap_scan(
                            file_name=file_name, emulation_env_config=self.s.emulation_env_config,
                            conn=c.conn, dir=cwd)
                        new_scan_result = NmapUtil.parse_nmap_scan_xml(xml_data, ips=self.machine.ips, action=self.a)
                        scan_result = NmapUtil.merge_nmap_scan_results(scan_result_1=scan_result,
                                                                       scan_result_2=new_scan_result)
                        self.machine.reachable.update(scan_result.reachable)
                    except Exception as e:
                        Logger.__call__().get_logger().warning(
                            f"There was an exception parsing the file:{file_name} on ip:{c.ip}, error:{e}")
                        time.sleep(constants.ENV_CONSTANTS.SLEEP_RETRY)
            self.scan_result = scan_result
            break
