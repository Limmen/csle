from typing import Tuple, List, Union
from xml.etree.ElementTree import fromstring
import xml.etree.ElementTree as ET
import time
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action_results.nmap_scan_result import NmapScanResult
from gym_pycr_pwcrack.dao.action_results.nmap_host import NmapHostResult
from gym_pycr_pwcrack.dao.action_results.nmap_port_status import NmapPortStatus
from gym_pycr_pwcrack.dao.action_results.nmap_port import NmapPort
from gym_pycr_pwcrack.dao.action_results.nmap_addr_type import NmapAddrType
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.envs.logic.common.env_dynamics_util import EnvDynamicsUtil
from gym_pycr_pwcrack.dao.action_results.nmap_os import NmapOs
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.dao.action_results.nmap_vuln import NmapVuln
from gym_pycr_pwcrack.dao.action_results.nmap_brute_credentials import NmapBruteCredentials
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_pwcrack.dao.action_results.nmap_hop import NmapHop
from gym_pycr_pwcrack.dao.action_results.nmap_trace import NmapTrace
from gym_pycr_pwcrack.dao.action_results.nmap_http_enum import NmapHttpEnum
from gym_pycr_pwcrack.dao.action_results.nmap_http_grep import NmapHttpGrep
from gym_pycr_pwcrack.dao.action_results.nmap_vulscan import NmapVulscan
from gym_pycr_pwcrack.envs.logic.cluster.util.cluster_util import ClusterUtil

class NmapUtil:
    """
    Class containing utility functions for the nmap-related functionality to the Cluster
    """

    @staticmethod
    def check_nmap_action_cache(a: Action, env_config: EnvConfig, conn=None, dir: str = None,
                                machine_ip: str = None):
        """
        Checks if an nmap action is cached or not

        :param a: the action
        :param env_config: the environment configuration
        :param dir: dir
        :param machine_ip: machine_ip
        :return: None or the name of the file where the result is cached
        """
        if conn is None:
            conn = env_config.cluster_config.agent_conn
        if dir is None or dir == "":
            dir = env_config.nmap_cache_dir

        query = str(a.id.value) + "_" + str(a.index) + "_" + a.ip
        if a.subnet:
            query = str(a.id.value) + "_" + str(a.index)
        if machine_ip is not None:
            query = query + "_" + machine_ip
        query = query + constants.FILE_PATTERNS.NMAP_ACTION_RESULT_SUFFIX

        # Search through cache
        if query in env_config.nmap_cache:
            return query

        stdin, stdout, stderr = conn.exec_command(constants.COMMANDS.LIST_CACHE + dir)
        cache_list = []
        for line in stdout:
            cache_list.append(line.replace("\n", ""))
        env_config.nmap_cache = cache_list

        # Search through updated cache
        if query in env_config.nmap_cache:
            return query

        env_config.cache_misses += 1

        return None

    @staticmethod
    def check_nmap_action_cache_interactive(a: Action, env_config: EnvConfig):
        """
        Checks if an NMAP action is cached or ot using an interactive shell

        :param a: the action to check
        :param env_config:  the environment config
        :return: None if not cached, otherwise the name of the file where the result is cached
        """

        # Clear channel
        if env_config.cluster_config.agent_channel.recv_ready():
            output = env_config.cluster_config.agent_channel.recv(5000)

        # List cache
        env_config.cluster_config.agent_channel.send(constants.COMMANDS.LIST_CACHE
                                                     + env_config.nmap_cache_dir + "\n")
        result_str = ClusterUtil.read_result_interactive(env_config=env_config)
        cache_list = result_str.split('\r\n')
        cache_list = cache_list[1:-1]  # remove command ([0]) and prompt ([-1])

        # Search through cache
        query = str(a.id.value) + "_" + str(a.index) + "_" + a.ip + constants.FILE_PATTERNS.NMAP_ACTION_RESULT_SUFFIX
        if a.subnet:
            query = str(a.id.value) + "_" + str(a.index) + constants.FILE_PATTERNS.NMAP_ACTION_RESULT_SUFFIX
        for item in cache_list:
            if item == query:
                return item

        return None

    @staticmethod
    def parse_nmap_scan(file_name: str, env_config: EnvConfig, conn=None, dir: str = None) -> ET.Element:
        """
        Parses an XML file containing the result of an nmap scan

        :param file_name: name of the file to parse
        :param env_config: environment config
        :return: the parsed xml file
        """
        if conn is None:
            conn = env_config.cluster_config.agent_conn
        if dir is None or dir == "":
            dir = env_config.nmap_cache_dir

        sftp_client = conn.open_sftp()
        remote_file = sftp_client.open(dir + file_name)
        try:
            xml_tree = ET.parse(remote_file)
        finally:
            remote_file.close()
        xml_data = xml_tree.getroot()
        return xml_data

    @staticmethod
    def parse_nmap_scan_interactive(file_name: str, env_config: EnvConfig) -> ET.Element:
        """
        Parses an XML file with the result of an nmap scan using an interactive shell

        :param file_name: the name of the file to parse
        :param env_config: the environment config
        :return: the parsed XML file
        """
        env_config.cluster_config.agent_channel.send("cat " + env_config.nmap_cache_dir + file_name + "\n")
        while not env_config.cluster_config.agent_channel.recv_ready():
            time.sleep(env_config.shell_read_wait)
        output = env_config.cluster_config.agent_channel.recv(env_config.max_nmap_command_output_size)
        output_str = output.decode("utf-8")
        output_str = env_config.shell_escape.sub("", output_str)
        lines = output_str.split('\r\n')
        lines = lines[1:-1]  # remove command ([0]) and prompt ([-1])
        xml_str = "\n".join(lines)
        xml_data = fromstring(xml_str)
        return xml_data

    @staticmethod
    def parse_nmap_scan_xml(xml_data, ip, action: Action) -> NmapScanResult:
        """
        Parses an XML Tree into a DTO

        :param xml_data: the xml tree to parse
        :param ip: ip of the source of the scan
        :param action: the action of the scan
        :return: parsed nmap scan result
        """
        hosts = []
        for child in xml_data:
            if child.tag == constants.NMAP_XML.HOST:
                host = NmapUtil._parse_nmap_host_xml(child, action=action)
                hosts = NmapUtil._merge_nmap_hosts(host, hosts, action=action)
        result = NmapScanResult(hosts=hosts, ip=ip)
        return result

    @staticmethod
    def _parse_nmap_host_xml(xml_data, action: Action) -> NmapHostResult:
        """
        Parses a host-element in the XML tree

        :param xml_data: the host element
        :param action: action of the scan
        :return: parsed nmap host result
        """
        ip_addr = None
        mac_addr = None
        hostnames = []
        ports = []
        vulnerabilities = []
        credentials = []
        os = None
        os_matches = []
        status = "up"
        trace = None
        for child in list(xml_data.iter()):
            if child.tag == constants.NMAP_XML.STATUS:
                status = NmapUtil._parse_nmap_status_xml(child)
            elif child.tag == constants.NMAP_XML.ADDRESS:
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
        nmap_host_result = NmapHostResult(status=status, ip_addr=ip_addr, mac_addr=mac_addr,
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
    def _parse_nmap_ports_xml(xml_data, action: Action) -> Tuple[
        List[NmapPort], List[NmapVuln], List[NmapBruteCredentials]]:
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
    def _parse_nmap_service_name_xml(xml_data) -> str:
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
    def _parse_nmap_os_xml(xml_data) -> NmapOs:
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
    def _parse_nmap_script(xml_data, port: int, protocol: TransportProtocol, service: str, action: Action) \
            -> Tuple[Union[List[NmapVuln], List[NmapBruteCredentials], NmapHttpEnum, NmapHttpGrep, NmapVulscan],
                     NmapVuln]:
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
    def _parse_nmap_brute(xml_data, port: int, protocol: TransportProtocol, service: str, action: Action) \
            -> Tuple[List[NmapBruteCredentials], NmapVuln]:
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
    def merge_nmap_scan_result_with_state(scan_result: NmapScanResult, s: EnvState, a: Action, env_config: EnvConfig) \
            -> Tuple[EnvState, float]:
        """
        Merges a NMAP scan result with an existing observation state

        :param scan_result: the scan result
        :param s: the current state
        :param a: the action just executed
        :return: s', reward
        """
        total_new_ports, total_new_os, total_new_vuln, total_new_machines, total_new_shell_access, \
        total_new_root, total_new_flag_pts, total_new_logged_in, total_new_tools_installed, \
        total_new_backdoors_installed = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        new_m_obs = []
        for host in scan_result.hosts:
            m_obs = host.to_obs()
            # m_obs = EnvDynamicsUtil.brute_tried_flags(a=a, m_obs=m_obs)
            new_m_obs.append(m_obs)

        new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
        total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, total_new_logged_in, \
        total_new_tools_installed, total_new_backdoors_installed = \
            EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, new_m_obs, env_config=env_config,
                                                   action=a)

        s_prime = s
        s_prime.obs_state.machines = new_machines_obs

        # Use measured cost
        if env_config.action_costs.exists(action_id=a.id, ip=a.ip):
            a.cost = env_config.action_costs.get_cost(action_id=a.id, ip=a.ip)

        # Use measured # alerts
        if env_config.action_alerts.exists(action_id=a.id, ip=a.ip):
            a.alerts = env_config.action_alerts.get_alert(action_id=a.id, ip=a.ip)

        reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports, num_new_os_found=total_new_os,
                                                 num_new_cve_vuln_found=total_new_vuln,
                                                 num_new_machines=total_new_machines,
                                                 num_new_shell_access=total_new_shell_access,
                                                 num_new_root=total_new_root,
                                                 num_new_flag_pts=total_new_flag_pts,
                                                 num_new_osvdb_vuln_found=total_new_osvdb_vuln_found,
                                                 num_new_logged_in=total_new_logged_in,
                                                 num_new_tools_installed=total_new_tools_installed,
                                                 num_new_backdoors_installed=total_new_backdoors_installed,
                                                 cost=a.cost,
                                                 env_config=env_config,
                                                 alerts=a.alerts, action=a
                                                 )
        return s_prime, reward

    @staticmethod
    def nmap_scan_action_helper(s: EnvState, a: Action, env_config: EnvConfig, masscan: bool = False) \
            -> Tuple[EnvState, float, bool]:
        """
        Helper function for executing a NMAP scan action on the cluster. Implements caching.

        :param s: the current env state
        :param a: the NMAP action to execute
        :param env_config: the env config
        :return: s', reward, done
        """
        # ALL action
        if a.index == -1:
            s.obs_state.sort_machines()
            ips = list(map(lambda x: x.ip, s.obs_state.machines))
            ips_str = "_".join(ips)
            cache_filename = str(a.id.value) + "_" + str(a.index) + "_" + ips + ".xml"
            cache_id = (a.id, a.index, ips_str, a.subnet)
        # Host action
        else:
            cache_filename = str(a.id.value) + "_" + str(a.index) + "_" + a.ip + ".xml"
            cache_id = (a.id, a.index, a.ip, a.subnet)

        # Subnet action
        if a.subnet:
            cache_filename = str(a.id.value) + "_" + str(a.index) + ".xml"

        # Check in-memory cache
        if env_config.use_nmap_cache:
            cache_value = env_config.nmap_scan_cache.get(cache_id)
            if cache_value is not None:
                s.obs_state.agent_reachable.update(cache_value.reachable)
                return NmapUtil.nmap_pivot_scan_action_helper(s=s, a=a, env_config=env_config,
                                                                 partial_result=cache_value.copy(), masscan=masscan)

        # Check On-disk cache
        cache_result = None
        if env_config.use_nmap_cache:
            cache_result = NmapUtil.check_nmap_action_cache(a=a, env_config=env_config)

        # If cache miss, then execute cmd
        if cache_result is None:
            cmd = a.nmap_cmd()
            if masscan:
                cmd = a.masscan_cmd()
            if env_config.ids_router:
                last_alert_ts = ClusterUtil.get_latest_alert_ts(env_config=env_config)
            outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=cmd,
                                                                       conn=env_config.cluster_config.agent_conn)
            if env_config.ids_router:
                # alerts = ClusterUtil.check_ids_alerts(env_config=env_config)
                fast_logs = ClusterUtil.check_ids_fast_log(env_config=env_config)
                # alerts = list(filter(lambda x: x.timestamp > last_alert_ts, alerts))
                if last_alert_ts is not None:
                    fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                num_alerts = len(fast_logs)
                # for i in range(len(alerts)):
                #     if alerts[i].timestamp == fast_logs[i][1]:
                #         alerts[i].priority = fast_logs[i][0]
                ClusterUtil.write_alerts_response(sum_priorities=sum_priority_alerts, num_alerts=num_alerts,
                                                  action=a, env_config=env_config)
                env_config.action_alerts.add_alert(action_id=a.id, ip=a.ip, alert=(sum_priority_alerts, num_alerts))

            ClusterUtil.write_estimated_cost(total_time=total_time, action=a, env_config=env_config)
            env_config.action_costs.add_cost(action_id=a.id, ip=a.ip, cost=round(total_time, 1))
            cache_result = cache_filename

        # Read result
        for i in range(env_config.num_retries):
            try:
                xml_data = NmapUtil.parse_nmap_scan(file_name=cache_result, env_config=env_config)
                scan_result = NmapUtil.parse_nmap_scan_xml(xml_data, ip=env_config.hacker_ip, action=a)
                s.obs_state.agent_reachable.update(scan_result.reachable)
                break
            except Exception as e:
                scan_result = NmapScanResult(hosts=[], ip=env_config.hacker_ip)
                # print("read nmap scan exception:{}, action:{}".format(str(e), a.name))
                # ClusterUtil.delete_cache_file(file_name=cache_result, env_config=env_config)
                # outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=a.nmap_cmd(),
                #                                                            conn=env_config.cluster_config.agent_conn)
                # ClusterUtil.write_estimated_cost(total_time=total_time, action=a, env_config=env_config)
                # env_config.action_costs.add_cost(action_id=a.id, ip=a.ip, cost=round(total_time, 1))
                # time.sleep(env_config.retry_timeout)
                # try:
                #     xml_data = ClusterUtil.parse_nmap_scan(file_name=cache_result, env_config=env_config)
                #     scan_result = ClusterUtil.parse_nmap_scan_xml(xml_data)
                # except Exception as e2:
                #     scan_result = NmapScanResult(hosts = [])
                break

        if env_config.use_nmap_cache:
            env_config.nmap_scan_cache.add(cache_id, scan_result)
        return NmapUtil.nmap_pivot_scan_action_helper(s=s, a=a, env_config=env_config,
                                                         partial_result=scan_result.copy(), masscan=masscan)

    @staticmethod
    def _merge_nmap_hosts(host: NmapHostResult, hosts: List[NmapHostResult], action: Action) -> List[NmapHostResult]:
        found = False
        for h in hosts:
            if h.ip_addr == host.ip_addr:
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
        new_hosts = []

        for h in scan_result_2.hosts:
            new_host = True
            for h2 in scan_result_1.hosts:
                if h.ip_addr == h2.ip_addr:
                    new_host = False
            if new_host:
                new_hosts.append(h)

        for h in scan_result_1.hosts:
            for h2 in scan_result_2.hosts:
                if h.ip_addr == h2.ip_addr:
                    h.hostnames = list(set(h.hostnames).union(set(h2.hostnames)))
                    h.ports = list(set(h.ports).union(h2.ports))
                    h.vulnerabilities = list(set(h.vulnerabilities).union(h2.vulnerabilities))
                    h.credentials = list(set(h.credentials).union(h2.credentials))
                    if h.os == None:
                        h.os = h2.os
                    if h.trace == None:
                        h.trace = h2.trace

        scan_result_1.hosts = scan_result_1.hosts + new_hosts
        scan_result_1.reachable = list(set(scan_result_1.reachable + scan_result_2.reachable))
        return scan_result_1

    @staticmethod
    def nmap_pivot_scan_action_helper(s: EnvState, a: Action, env_config: EnvConfig, partial_result:
    NmapScanResult, masscan: bool = False) \
            -> Tuple[EnvState, float, bool]:
        hacker_ip = env_config.hacker_ip
        logged_in_ips = list(map(lambda x: x.ip, filter(lambda x: x.logged_in and x.tools_installed \
                                                                  and x.backdoor_installed,
                                                        s.obs_state.machines)))
        logged_in_ips.append(hacker_ip)
        logged_in_ips = sorted(logged_in_ips, key=lambda x: x)
        logged_in_ips_str = "_".join(logged_in_ips)

        base_cache_id = (a.id, a.index, a.ip, a.subnet)
        for ip in logged_in_ips:
            base_cache_id = base_cache_id + (ip,)
        base_cache_filename = str(a.id.value) + "_" + str(a.index) + "_" + a.ip
        if a.subnet:
            base_cache_filename = str(a.id.value) + "_" + str(a.index)
        base_cache_filename = base_cache_filename + "_" + logged_in_ips_str + ".xml"

        # Check in-memory cache
        if env_config.use_nmap_cache:
            scan_result = env_config.nmap_scan_cache.get(base_cache_id)
            if scan_result is not None:
                merged_result, total_results = scan_result
                s_prime, reward = NmapUtil.merge_nmap_scan_result_with_state(scan_result=merged_result, s=s, a=a,
                                                                                env_config=env_config)
                for res in total_results:
                    if res.ip == env_config.hacker_ip:
                        s_prime.obs_state.agent_reachable.update(res.reachable)
                    else:
                        machine = s_prime.get_machine(res.ip)
                        if machine is None:
                            pass
                        #     print("None m")
                        #     print("action:{}".format(a.name))
                        #     print("ip: {}".format(res.ip))
                        #     print("merged result machines: {}".format(
                        #         list(map(lambda x: x.ip_addr, merged_result.hosts))))
                        #     for tm in total_results:
                        #         print("total_results machines: {}".format(list(map(lambda x: x.ip_addr, tm.hosts))))
                        else:
                            machine.reachable.update(res.reachable)
                new_machines_obs_1 = []
                reachable = s.obs_state.agent_reachable
                reachable.add(env_config.router_ip)

                for machine in s_prime.obs_state.machines:
                    if machine.logged_in and machine.tools_installed and machine.backdoor_installed:
                        reachable = reachable.union(machine.reachable)

                for machine in s_prime.obs_state.machines:
                    if machine.logged_in and machine.tools_installed:
                        machine = EnvDynamicsUtil.ssh_backdoor_tried_flags(a=a, m_obs=machine)

                    if machine.ip in reachable and (machine.ip == a.ip or a.subnet):
                        machine = EnvDynamicsUtil.exploit_tried_flags(a=a, m_obs=machine)
                    new_machines_obs_1.append(machine)
                s_prime.obs_state.machines = new_machines_obs_1

                return s_prime, reward, False

        new_machines_obs = []
        total_cost = 0
        merged_scan_result = partial_result
        total_results = []

        for machine in s.obs_state.machines:
            scan_result = None
            new_m_obs = MachineObservationState(ip=machine.ip)
            cache_filename = str(a.id.value) + "_" + str(a.index) + "_" + a.ip + "_" + machine.ip + ".xml"
            if a.subnet:
                cache_filename = str(a.id.value) + "_" + str(a.index) + "_" + machine.ip + ".xml"
            cache_id = (a.id, a.index, a.ip, a.subnet, machine.ip)

            if machine.logged_in and machine.tools_installed and machine.backdoor_installed:

                # Start with ssh connections
                ssh_connections_sorted_by_root = sorted(
                    machine.ssh_connections,
                    key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.username, x.root, x.username),
                    reverse=True)
                for c in ssh_connections_sorted_by_root:

                    # Check in-memory cache
                    if env_config.use_nmap_cache:
                        scan_result = env_config.nmap_scan_cache.get(cache_id)
                        if scan_result is not None:
                            machine.reachable.update(scan_result.reachable)
                            break

                    # Check On-disk cache
                    # cwd, _, total_time = ClusterUtil.execute_ssh_cmd(cmd="pwd", conn=c.conn)
                    # cwd = cwd.decode().replace("\n", "") + "/"
                    # total_cost += total_time
                    cwd = "/home/" + c.username + "/"
                    if env_config.use_nmap_cache:
                        cache_result = NmapUtil.check_nmap_action_cache(a=a, env_config=env_config, conn=c.conn,
                                                                           dir=cwd, machine_ip=machine.ip)

                    # If cache miss, then execute cmd
                    if cache_result is None:
                        if env_config.ids_router:
                            last_alert_ts = ClusterUtil.get_latest_alert_ts(env_config=env_config)
                        cmd = a.nmap_cmd(machine_ip=machine.ip)
                        outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
                        total_cost += total_time
                        if env_config.ids_router:
                            fast_logs = ClusterUtil.check_ids_fast_log(env_config=env_config)
                            if last_alert_ts is not None:
                                fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                            sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                            num_alerts = len(fast_logs)
                            ClusterUtil.write_alerts_response(sum_priorities=sum_priority_alerts, num_alerts=num_alerts,
                                                              action=a, env_config=env_config,
                                                              conn=c.conn, dir=cwd, machine_ip=machine.ip)
                            env_config.action_alerts.pivot_scan_add_alert(action_id=a.id, ip=machine.ip,
                                                                          user=c.username,
                                                                          target_ip=machine.ip,
                                                                          alert=(sum_priority_alerts, num_alerts))
                        ClusterUtil.write_estimated_cost(total_time=total_time, action=a, env_config=env_config,
                                                         conn=c.conn, dir=cwd, machine_ip=machine.ip)
                        env_config.action_costs.pivot_scan_add_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                                    target_ip=machine.ip, cost=round(total_time, 1))

                        cache_result = cache_filename

                    # Read result
                    for i in range(env_config.num_retries):
                        try:
                            xml_data = NmapUtil.parse_nmap_scan(file_name=cache_result, env_config=env_config,
                                                                   conn=c.conn, dir=cwd)
                            scan_result = NmapUtil.parse_nmap_scan_xml(xml_data, ip=machine.ip, action=a)
                            machine.reachable.update(scan_result.reachable)
                        except Exception as e:
                            scan_result = NmapScanResult(hosts=[], ip=machine.ip)
                            break

                    if env_config.use_nmap_cache and scan_result is not None:
                        env_config.nmap_scan_cache.add(cache_id, scan_result)
                    break

                # Update state with scan result
                if merged_scan_result is not None and scan_result is not None:
                    total_results.append(scan_result)
                    merged_scan_result = NmapUtil.merge_nmap_scan_results(scan_result_1=merged_scan_result,
                                                                             scan_result_2=scan_result.copy())
                elif merged_scan_result is None:
                    total_results.append(scan_result)
                    merged_scan_result = scan_result.copy()

        if env_config.use_nmap_cache:
            env_config.nmap_scan_cache.add(base_cache_id, (merged_scan_result, total_results))
        a.cost = a.cost + total_cost
        s_prime, reward = NmapUtil.merge_nmap_scan_result_with_state(scan_result=merged_scan_result, s=s, a=a,
                                                                        env_config=env_config)
        new_machines_obs_1 = []
        reachable = s.obs_state.agent_reachable
        reachable.add(env_config.router_ip)

        for machine in s_prime.obs_state.machines:
            if machine.logged_in and machine.tools_installed and machine.backdoor_installed:
                reachable = reachable.union(machine.reachable)

        for machine in s_prime.obs_state.machines:
            if machine.logged_in and machine.tools_installed:
                machine = EnvDynamicsUtil.ssh_backdoor_tried_flags(a=a, m_obs=machine)

            if machine.ip in reachable and (machine.ip == a.ip or a.subnet):
                machine = EnvDynamicsUtil.exploit_tried_flags(a=a, m_obs=machine)
            new_machines_obs_1.append(machine)
        s_prime.obs_state.machines = new_machines_obs_1

        return s_prime, reward, False