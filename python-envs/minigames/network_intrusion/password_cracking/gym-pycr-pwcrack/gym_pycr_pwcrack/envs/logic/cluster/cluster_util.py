from typing import Union, List
from xml.etree.ElementTree import fromstring
import xml.etree.ElementTree as ET
import time
import paramiko
import telnetlib
from ftplib import FTP
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
from gym_pycr_pwcrack.dao.observation.connection_observation_state import ConnectionObservationState
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_pwcrack.envs.logic.cluster.forward_tunnel_thread import ForwardTunnelThread

class ClusterUtil:
    """
    Class containing utility functions for the cluster-middleware
    """

    @staticmethod
    def execute_ssh_cmd(cmd : str, conn) -> Union[bytes, bytes, float]:
        """
        Executes an action on the cluster over a ssh connection,
        this is a synchronous operation that waits for the completion of the action before returning

        :param cmd: the command to execute
        :param conn: the ssh connection
        :return: outdata, errdata, total_time
        """
        transport_conn = conn.get_transport()
        session = transport_conn.open_session()
        start = time.time()
        session.exec_command(cmd)
        outdata, errdata = b'', b''
        # Wait for completion
        while True:
            # Reading from output streams
            while session.recv_ready():
                outdata += session.recv(1000)
            while session.recv_stderr_ready():
                errdata += session.recv_stderr(1000)

            # Check for completion
            if session.exit_status_ready():
                break
        end = time.time()
        total_time = end-start
        return outdata, errdata, total_time

    @staticmethod
    def write_estimated_cost(total_time, action: Action, env_config: EnvConfig) -> None:
        """
        Caches the estimated cost of an action by writing it to a file

        :param total_time: the total time of executing the action
        :param action: the action
        :param env_config: the environment config
        :return: None
        """
        sftp_client = env_config.cluster_config.agent_conn.open_sftp()
        file_name = env_config.nmap_cache_dir + str(action.id.value)
        if not action.subnet:
            file_name = file_name + "_" + action.ip
        file_name = file_name + constants.FILE_PATTERNS.COST_FILE_SUFFIX
        remote_file = sftp_client.file(file_name, mode="w")
        try:
            remote_file.write(str(round(total_time, 1)) + "\n")
        finally:
            remote_file.close()

    @staticmethod
    def write_file_system_scan_cache(action: Action, env_config: EnvConfig, service: str, user: str,files: List[str],
                                     ip : str) \
            -> None:
        """
        Caches the result of a file system scan
        :param action: the action
        :param env_config: the env config
        :param service: the service used to connect to the file system
        :param user: the user
        :param files: the result to cache
        :param ip: the ip
        :return: None
        """
        sftp_client = env_config.cluster_config.agent_conn.open_sftp()
        file_name = env_config.nmap_cache_dir + str(action.id.value) + "_" + ip + "_" + service \
                    + "_" + user + ".txt"
        remote_file = sftp_client.file(file_name, mode="w")
        try:
            for file in files:
                remote_file.write(file + "\n")
        finally:
            remote_file.close()

    @staticmethod
    def execute_cmd_interactive(a: Action, env_config: EnvConfig) -> None:
        """
        Executes an action on the cluster using an interactive shell (non synchronous)

        :param a: action to execute
        :param env_config: environment config
        :return: None
        """
        env_config.cluster_config.agent_channel.send(a.cmd[0] + "\n")

    @staticmethod
    def read_result_interactive(env_config : EnvConfig) -> str:
        """
        Reads the result of an action executed in interactive mode

        :param env_config: the environment config
        :return: the result
        """
        while not env_config.cluster_config.agent_channel.recv_ready():
            time.sleep(env_config.shell_read_wait)
        output = env_config.cluster_config.agent_channel.recv(constants.COMMON.LARGE_RECV_SIZE)
        output_str = output.decode("utf-8")
        output_str = env_config.shell_escape.sub("", output_str)
        return output_str

    @staticmethod
    def check_nmap_action_cache(a: Action, env_config: EnvConfig):
        """
        Checks if an nmap action is cached or not

        :param a: the action
        :param env_config: the environment configuration
        :return: None or the name of the file where the result is cached
        """
        query = str(a.id.value) + "_" + a.ip + constants.FILE_PATTERNS.NMAP_ACTION_RESULT_SUFFIX
        if a.subnet:
            query = str(a.id.value) + constants.FILE_PATTERNS.NMAP_ACTION_RESULT_SUFFIX

        # Search through cache
        if query in env_config.nmap_cache:
            return query

        stdin, stdout, stderr = env_config.cluster_config.agent_conn.exec_command(constants.COMMANDS.LIST_CACHE
                                                                                  + env_config.nmap_cache_dir)
        cache_list = []
        for line in stdout:
            cache_list.append(line.replace("\n", ""))
        env_config.nmap_cache = cache_list

        # Search through updated cache
        if query in env_config.nmap_cache:
            return query

        return None

    @staticmethod
    def check_filesystem_action_cache(a: Action, env_config: EnvConfig, ip: str, service : str, user: str):
        """
        Checks if an nmap action is cached or not

        :param a: the action
        :param env_config: the environment configuration
        :return: None or the name of the file where the result is cached
        """
        query = str(a.id.value) + "_" + ip + "_" + service + "_" + user + ".txt"

        # Search through cache
        if query in env_config.filesystem_file_cache:
            return query

        stdin, stdout, stderr = env_config.cluster_config.agent_conn.exec_command(constants.COMMANDS.LIST_CACHE
                                                                                  + env_config.nmap_cache_dir)
        cache_list = []
        for line in stdout:
            cache_list.append(line.replace("\n", ""))
        env_config.filesystem_file_cache = cache_list

        # Search through updated cache
        if query in env_config.filesystem_file_cache:
            return query

        return None

    @staticmethod
    def parse_file_scan_file(file_name: str, env_config: EnvConfig) -> List[str]:
        """
        Parses a file containing cached results of a file scan on a server

        :param file_name: name of the file to parse
        :param env_config: environment config
        :return: a list of files
        """
        sftp_client = env_config.cluster_config.agent_conn.open_sftp()
        remote_file = sftp_client.open(env_config.nmap_cache_dir + file_name)
        files = []
        try:
            data = remote_file.read()
            data = data.decode()
            files = data.split("\n")
        finally:
            remote_file.close()
        return files

    @staticmethod
    def check_nmap_action_cache_interactive(a : Action, env_config : EnvConfig):
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
        query = str(a.id.value) + "_" + a.ip + constants.FILE_PATTERNS.NMAP_ACTION_RESULT_SUFFIX
        if a.subnet:
            query = str(a.id.value) + constants.FILE_PATTERNS.NMAP_ACTION_RESULT_SUFFIX
        for item in cache_list:
            if item == query:
                return item

        return None

    @staticmethod
    def delete_cache_file(file_name: str, env_config: EnvConfig) -> Union[bytes, bytes, float]:
        """
        Deletes the file that contains the cached result of some operation

        :param file_name: name of the file to delete
        :param env_config: the environment config
        :return: outdata, errdata, total_time
        """
        cmd = "rm -f " + env_config.nmap_cache_dir + file_name
        return ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=env_config.cluster_config.agent_conn)

    @staticmethod
    def parse_nmap_scan(file_name: str, env_config: EnvConfig) -> ET.Element:
        """
        Parases an XML file containing the result of an nmap scan

        :param file_name: name of the file to parse
        :param env_config: environment config
        :return: the parsed xml file
        """
        sftp_client = env_config.cluster_config.agent_conn.open_sftp()
        remote_file = sftp_client.open(env_config.nmap_cache_dir + file_name)
        try:
            xml_tree = ET.parse(remote_file)
        finally:
            remote_file.close()
        xml_data = xml_tree.getroot()
        return xml_data

    @staticmethod
    def parse_nmap_scan_interactive(file_name : str, env_config : EnvConfig) -> ET.Element:
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
    def parse_nmap_scan_xml(xml_data) -> NmapScanResult:
        """
        Parses an XML Tree into a DTO

        :param xml_data: the xml tree to parse
        :return: parsed nmap scan result
        """
        hosts = []
        for child in xml_data:
            if child.tag == constants.NMAP_XML.HOST:
                host = ClusterUtil._parse_nmap_host_xml(child)
                hosts.append(host)
        result = NmapScanResult(hosts=hosts)
        return result


    @staticmethod
    def _parse_nmap_host_xml(xml_data) -> NmapHostResult:
        """
        Parses a host-element in the XML tree

        :param xml_data: the host element
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
        for child in list(xml_data.iter()):
            if child.tag == constants.NMAP_XML.STATUS:
                status = ClusterUtil._parse_nmap_status_xml(child)
            elif child.tag == constants.NMAP_XML.ADDRESS:
                addr, type = ClusterUtil._parse_nmap_address_xml(child)
                if type == NmapAddrType.MAC:
                    mac_addr = addr
                else:
                    ip_addr = addr
            elif child.tag == constants.NMAP_XML.HOSTNAMES:
                hostnames = ClusterUtil._parse_nmap_hostnames_xml(child)
            elif child.tag == constants.NMAP_XML.PORTS:
                ports, vulnerabilities, credentials = ClusterUtil._parse_nmap_ports_xml(child)
            elif child.tag == constants.NMAP_XML.OS:
                os_matches = ClusterUtil._parse_nmap_os_xml(child)
                os = NmapOs.get_best_match(os_matches)
        nmap_host_result = NmapHostResult(status=status, ip_addr=ip_addr, mac_addr=mac_addr,
                                          hostnames=hostnames, ports=ports, os=os, os_matches=os_matches,
                                          vulnerabilities=vulnerabilities, credentials=credentials)
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
    def _parse_nmap_address_xml(xml_data) -> Union[str, NmapAddrType]:
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
    def _parse_nmap_ports_xml(xml_data) -> Union[List[NmapPort], List[NmapVuln], List[NmapBruteCredentials]]:
        """
        Parses a ports XML element in the XML tree

        :param xml_data: the ports XML element
        :return: (List NmapPort, List NmapVuln, ListNmapBruteCredentials)
        """
        ports = []
        vulnerabilities = []
        credentials = []
        for child in list(xml_data.iter()):
            if child.tag == constants.NMAP_XML.PORT:
                port_status = NmapPortStatus.DOWN
                protocol = TransportProtocol._from_str(child.attrib["protocol"])
                port_id = child.attrib[constants.NMAP_XML.PORT_ID]
                service_name = constants.NMAP_XML.UNKNOWN
                for child_2 in list(child.iter()):
                    if child_2.tag == constants.NMAP_XML.STATE:
                        port_status = ClusterUtil._parse_nmap_port_status_xml(child_2)
                    elif child_2.tag == constants.NMAP_XML.SERVICE:
                        service_name = ClusterUtil._parse_nmap_service_name_xml(child_2)
                    elif child_2.tag == constants.NMAP_XML.SCRIPT:
                        result = ClusterUtil._parse_nmap_script(child_2, port=port_id, protocol=protocol,
                                                                service=service_name)
                        if len(result) > 0:
                            if isinstance(result[0], NmapVuln):
                                vulnerabilities = result
                            elif isinstance(result[0], NmapBruteCredentials):
                                credentials = result
                if port_status == NmapPortStatus.UP:
                    port = NmapPort(port_id=port_id, protocol=protocol, status=port_status, service_name=service_name)
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
    def _parse_nmap_script(xml_data, port: int, protocol: TransportProtocol, service: str) \
            -> Union[List[NmapVuln], List[NmapBruteCredentials]]:
        """
        Parses a XML script element

        :param xml_data: the XML script element
        :param port: the port of the parent element
        :param protocol: the protocol of the parent element
        :param service: the service running on the port
        :return: a list of parsed nmap vulnerabilities or a list of parsed credentials
        """
        if constants.NMAP_XML.ID in xml_data.keys():
            if xml_data.attrib[constants.NMAP_XML.ID] == constants.NMAP_XML.VULNERS_SCRIPT_ID:
                return ClusterUtil._parse_nmap_vulners(xml_data, port=port, protocol=protocol, service=service)
            elif xml_data.attrib[constants.NMAP_XML.ID] in constants.NMAP_XML.BRUTE_SCRIPTS:
                return ClusterUtil._parse_nmap_telnet_brute(xml_data, port=port, protocol=protocol, service=service)
        return []

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
                        vuln = ClusterUtil._parse_nmap_table_vuln(c_2, port=port, protocol=protocol, service=service)
                        vulnerabilities.append(vuln)
                break
        return vulnerabilities

    @staticmethod
    def _parse_nmap_telnet_brute(xml_data, port: int, protocol: TransportProtocol, service: str) \
            -> List[NmapBruteCredentials]:
        """
        Parses a XML result from a telnet brute force dictionary scan

        :param xml_data: the XML script element
        :param port: the port of the parent element
        :param protocol: the protocol of the parent element
        :param service: the service running on the port
        :return: a list of found credentials
        """
        credentials = []
        for child in list(xml_data.iter())[1:]:
            if child.tag == constants.NMAP_XML.TABLE:
                if constants.NMAP_XML.KEY in child.keys():
                    if child.attrib[constants.NMAP_XML.KEY] == constants.NMAP_XML.ACCOUNTS:
                        for c_2 in list(child.iter())[1:]:
                            if c_2.tag == constants.NMAP_XML.TABLE:
                                cred = ClusterUtil._parse_nmap_table_cred(c_2, port=port, protocol=protocol, service=service)
                                credentials.append(cred)
                        break
        return credentials

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
    def merge_scan_result_with_state(scan_result : NmapScanResult, s: EnvState, a: Action, env_config: EnvConfig) \
            -> Union[EnvState, float]:
        """
        Merges a NMAP scan result with an existing observation state

        :param scan_result: the scan result
        :param s: the current state
        :param a: the action just executed
        :return: s', reward
        """
        total_new_ports, total_new_os, total_new_vuln, total_new_machines, total_new_shell_access, \
        total_new_root, total_new_flag_pts = 0, 0, 0, 0, 0, 0, 0
        new_m_obs = []

        for host in scan_result.hosts:
            m_obs = host.to_obs()
            new_m_obs.append(m_obs)

        new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
        total_new_shell_access, total_new_flag_pts, total_new_root = \
            EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, new_m_obs, env_config=env_config)
        s_prime = s
        s_prime.obs_state.machines = new_machines_obs

        # Use measured cost
        if env_config.action_costs.exists(action_id=a.id, ip=a.ip):
            a.cost = env_config.action_costs.get_cost(action_id=a.id, ip=a.ip)
        reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports, num_new_os_found=total_new_os,
                                                 num_new_vuln_found=total_new_vuln,
                                                 num_new_machines=total_new_machines,
                                                 num_new_shell_access=total_new_shell_access,
                                                 num_new_root=total_new_root,
                                                 num_new_flag_pts=total_new_flag_pts,
                                                 cost=a.cost)
        return s_prime, reward

    @staticmethod
    def nmap_scan_action_helper(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, float, bool]:
        """
        Helpe function for executing a NMAP scan action on the cluster. Implements caching.

        :param s: the current env state
        :param a: the NMAP action to execute
        :param env_config: the env config
        :return: s', reward, done
        """
        cache_id = str(a.id.value) + "_" + a.ip + ".xml"
        if a.subnet:
            cache_id = str(a.id.value) + ".xml"

        # Check in-memory cache
        if env_config.use_nmap_cache:
            cache_value = env_config.nmap_scan_cache.get(cache_id)
            if cache_value is not None:
                s_prime, reward = ClusterUtil.merge_scan_result_with_state(scan_result=cache_value, s=s, a=a,
                                                                           env_config=env_config)
                return s_prime, reward, False

        # Check On-disk cache
        if env_config.use_nmap_cache:
            cache_result = ClusterUtil.check_nmap_action_cache(a=a, env_config=env_config)

        # If cache miss, then execute cmd
        if cache_result is None:
            outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=a.cmd[0],
                                                                       conn=env_config.cluster_config.agent_conn)
            ClusterUtil.write_estimated_cost(total_time=total_time, action=a, env_config=env_config)
            env_config.action_costs.add_cost(action_id=a.id, ip=a.ip, cost=round(total_time,1))
            cache_result = cache_id

        # Read result
        for i in range(env_config.num_retries):
            try:
                xml_data = ClusterUtil.parse_nmap_scan(file_name=cache_result, env_config=env_config)
                break
            except Exception as e:
                ClusterUtil.delete_cache_file(file_name=cache_result, env_config=env_config)
                outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=a.cmd[0],
                                                                           conn=env_config.cluster_config.agent_conn)
                ClusterUtil.write_estimated_cost(total_time=total_time, action=a, env_config=env_config)
                env_config.action_costs.add_cost(action_id=a.id, ip=a.ip, cost=round(total_time, 1))
                time.sleep(env_config.retry_timeout)
                xml_data = ClusterUtil.parse_nmap_scan(file_name=cache_result, env_config=env_config)
                break

        scan_result = ClusterUtil.parse_nmap_scan_xml(xml_data)
        if env_config.use_nmap_cache:
            env_config.nmap_scan_cache.add(cache_id, scan_result)
        s_prime, reward = ClusterUtil.merge_scan_result_with_state(scan_result=scan_result, s=s, a=a,
                                                                   env_config=env_config)
        return s_prime, reward, False


    @staticmethod
    def login_service_helper(s: EnvState, a: Action, alive_check, service_name : str,
                             env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Helper function for logging in to a network service in the cluster

        :param s: the current state
        :param a: the action of the login
        :param alive_check:  the function to check whether current connections are alive or not
        :param service_name: name of the service to login to
        :param env_config: environment config
        :return: s_prime, reward, done
        """
        total_new_ports, total_new_os, total_new_vuln, total_new_machines, total_new_shell_access, \
        total_new_root, total_new_flag_pts = 0, 0, 0, 0, 0, 0, 0
        target_machine = None
        non_used_credentials = []
        root = False
        for m in s.obs_state.machines:
            if m.ip == a.ip:
                target_machine = m
                break

        # Check if already logged in
        if target_machine is not None:
            alive_connections = []
            root = False
            connected = False
            connections = []
            if service_name == constants.TELNET.SERVICE_NAME:
                connections = target_machine.telnet_connections
            elif service_name == constants.SSH.SERVICE_NAME:
                connections = target_machine.ssh_connections
            elif service_name == constants.FTP.SERVICE_NAME:
                connections = target_machine.ftp_connections
            for c in connections:
                if alive_check(c.conn):
                    connected = True
                    alive_connections.append(c)
                    if c.root:
                        root = c.root
                else:
                    if c.tunnel_thread is not None:
                        # stop the tunnel thread that does port forwarding
                        c.tunnel_thread.forward_server.shutdown()
            if len(target_machine.logged_in_services) == 1 and target_machine.logged_in_services[0] == service_name:
                target_machine.logged_in = connected
            if len(target_machine.root_services) == 1 and target_machine.root_services[0] == service_name:
                target_machine.root = root
            if not connected and service_name in target_machine.logged_in_services:
                target_machine.logged_in_services.remove(service_name)
            if not root and service_name in target_machine.root_services:
                target_machine.root_services.remove(service_name)
            non_used_credentials = []
            root = False
            for cr in target_machine.shell_access_credentials:
                if cr.service == service_name:
                    already_logged_in = False
                    for c in alive_connections:
                        if not root and c.root:
                            root = True
                        if c.username == cr.username:
                            already_logged_in = True
                    if not already_logged_in:
                        non_used_credentials.append(cr)

            if service_name == constants.TELNET.SERVICE_NAME:
                target_machine.telnet_connections = alive_connections
            elif service_name == constants.SSH.SERVICE_NAME:
                target_machine.ssh_connections = alive_connections
            elif service_name == constants.FTP.SERVICE_NAME:
                target_machine.ftp_connections = alive_connections

        if target_machine is None or root or len(non_used_credentials) == 0:
            s_prime = s
            if target_machine is not None:
                new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
                total_new_shell_access, total_new_flag_pts, total_new_root = \
                    EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, [target_machine],
                                                           env_config=env_config)
                s_prime.obs_state.machines = new_machines_obs

            # Use measured cost
            if env_config.action_costs.exists(action_id=a.id, ip=a.ip):
                a.cost = env_config.action_costs.get_cost(action_id=a.id, ip=a.ip)
            reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports, num_new_os_found=total_new_os,
                                                     num_new_vuln_found=total_new_vuln,
                                                     num_new_machines=total_new_machines,
                                                     num_new_shell_access=total_new_shell_access,
                                                     num_new_root=total_new_root,
                                                     num_new_flag_pts=total_new_flag_pts,
                                                     cost=a.cost)
            return s_prime, reward, False

        # If not logged in and there are credentials, setup a new connection
        connected = False
        users = []
        target_connections = []
        ports = []
        if service_name == constants.SSH.SERVICE_NAME:
            connected, users, target_connections, ports = ClusterUtil._ssh_setup_connection(
                target_machine=target_machine, a=a, env_config=env_config)
        elif service_name == constants.TELNET.SERVICE_NAME:
            connected, users, target_connections, tunnel_threads, forward_ports, ports = \
                ClusterUtil._telnet_setup_connection(target_machine=target_machine, a=a, env_config=env_config)
        elif service_name == constants.FTP.SERVICE_NAME:
            connected, users, target_connections, tunnel_threads, forward_ports, ports, i_shells = \
                ClusterUtil._ftp_setup_connection(target_machine=target_machine, a=a, env_config=env_config)
        s_prime = s
        if connected:
            root = False
            target_machine.logged_in = True
            if service_name not in target_machine.logged_in_services:
                target_machine.logged_in_services.append(service_name)
            if service_name not in target_machine.root_services:
                target_machine.root_services.append(service_name)
            for i in range(len(target_connections)):
                # Check if root
                c_root = False
                if service_name == constants.SSH.SERVICE_NAME:
                    c_root = ClusterUtil._ssh_finalize_connection(target_machine=target_machine, users=users,
                                                                  target_connections=target_connections, i=i,
                                                                  ports=ports)
                elif service_name == constants.TELNET.SERVICE_NAME:
                    c_root = ClusterUtil._telnet_finalize_connection(target_machine=target_machine, users=users,
                                                                     target_connections=target_connections,
                                                                     i=i, tunnel_threads=tunnel_threads,
                                                                     forward_ports=forward_ports, ports=ports)
                elif service_name == constants.FTP.SERVICE_NAME:
                    c_root = ClusterUtil._ftp_finalize_connection(target_machine=target_machine, users=users,
                                                                  target_connections=target_connections,
                                                                  i=i, tunnel_threads=tunnel_threads,
                                                                  forward_ports=forward_ports, ports=ports,
                                                                  interactive_shells=i_shells)
                if c_root:
                    root = True

            target_machine.root = root
            new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
            total_new_shell_access, total_new_flag_pts, total_new_root = \
                EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, [target_machine], env_config=env_config)
            s_prime.obs_state.machines = new_machines_obs

        # Use measured cost
        if env_config.action_costs.exists(action_id=a.id, ip=a.ip):
            a.cost = env_config.action_costs.get_cost(action_id=a.id, ip=a.ip)
        reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports, num_new_os_found=total_new_os,
                                                 num_new_vuln_found=total_new_vuln,
                                                 num_new_machines=total_new_machines,
                                                 num_new_shell_access=total_new_shell_access,
                                                 num_new_root=total_new_root,
                                                 num_new_flag_pts=total_new_flag_pts,
                                                 cost=a.cost)
        return s_prime, reward, False


    @staticmethod
    def _ssh_setup_connection(target_machine: MachineObservationState, a: Action, env_config: EnvConfig) \
            -> Union[bool, List[str], List, List[int]]:
        """
        Helper function for setting up a SSH connection

        :param target_machine: the target machine to connect to
        :param a: the action of the connection
        :param env_config: the environment config
        :return: boolean whether connected or not, list of connected users, list of connection handles, list of ports
        """
        connected = False
        users = []
        target_connections = []
        ports = []
        for cr in target_machine.shell_access_credentials:
            if cr.service == constants.SSH.SERVICE_NAME:
                try:
                    agent_addr = (env_config.cluster_config.agent_ip, cr.port)
                    target_addr = (a.ip, cr.port)
                    agent_transport = env_config.cluster_config.agent_conn.get_transport()
                    relay_channel = agent_transport.open_channel(constants.SSH.DIRECT_CHANNEL, target_addr, agent_addr)
                    target_conn = paramiko.SSHClient()
                    target_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    target_conn.connect(a.ip, username=cr.username, password=cr.pw, sock=relay_channel)
                    connected = True
                    users.append(cr.username)
                    target_connections.append(target_conn)
                    ports.append(cr.port)
                except:
                    pass
        return connected, users, target_connections, ports

    @staticmethod
    def _ssh_finalize_connection(target_machine: MachineObservationState, users: List[str],
                                 target_connections: List, i : int, ports: List[int]) -> bool:
        """
        Helper function for finalizing a SSH connection and setting up the DTO

        :param target_machine: the target machine to connect to
        :param users: list of connected users
        :param target_connections: list of connection handles
        :param i: current index
        :param ports: list of ports of the connections
        :return: boolean whether the connection has root privileges or not
        """
        outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd="sudo -v",
                                                                   conn=target_connections[i])
        root = False
        if not "Sorry, user {} may not run sudo".format(users[i]) in errdata.decode("utf-8"):
            root = True
            target_machine.root = True
        connection_dto = ConnectionObservationState(conn=target_connections[i], username=users[i],
                                                    root=root,
                                                    service=constants.SSH.SERVICE_NAME,
                                                    port=ports[i])
        target_machine.ssh_connections.append(connection_dto)
        return root

    @staticmethod
    def _telnet_setup_connection(target_machine: MachineObservationState, a: Action, env_config: EnvConfig) \
            -> Union[bool, List[str], List, List[ForwardTunnelThread], List[int], List[int]]:
        """
        Helper function for setting up a Telnet connection to a target machine

        :param target_machine: the target machine to connect to
        :param a: the action of the connection
        :param env_config: the environment config
        :return: connected (bool), connected users, connection handles, list of tunnel threads, list of forwarded ports,
                 list of ports
        """
        connected = False
        users = []
        target_connections = []
        tunnel_threads = []
        forward_ports = []
        ports = []
        for cr in target_machine.shell_access_credentials:
            if cr.service == constants.TELNET.SERVICE_NAME:
                try:
                    forward_port = env_config.get_port_forward_port()
                    tunnel_thread = ForwardTunnelThread(local_port=forward_port,
                                                        remote_host=a.ip, remote_port=cr.port,
                                                        transport=env_config.cluster_config.agent_conn.get_transport())
                    tunnel_thread.start()
                    target_conn = telnetlib.Telnet(host=constants.TELNET.LOCALHOST, port=forward_port)
                    target_conn.read_until(constants.TELNET.LOGIN_PROMPT, timeout=5)
                    target_conn.write((cr.username + "\n").encode())
                    target_conn.read_until(constants.TELNET.PASSWORD_PROMPT, timeout=5)
                    target_conn.write((cr.pw + "\n").encode())
                    response = target_conn.read_until(constants.TELNET.PROMPT, timeout=5)
                    if not constants.TELNET.INCORRECT_LOGIN in response.decode("utf-8"):
                        connected = True
                        users.append(cr.username)
                        target_connections.append(target_conn)
                        tunnel_threads.append(tunnel_thread)
                        forward_ports.append(forward_port)
                        ports.append(cr.port)
                except Exception as e:
                    print("telnet exception:{}".format(str(e)))
                    pass
        return connected, users, target_connections, tunnel_threads, forward_ports, ports

    @staticmethod
    def _telnet_finalize_connection(target_machine: MachineObservationState, users: List[str], target_connections: List, i: int,
                                    tunnel_threads: List, forward_ports : List[int], ports: List[int]) -> bool:
        """
        Helper function for finalizing a Telnet connection to a target machine and creating the DTO

        :param target_machine: the target machine to connect to
        :param users: list of connected users
        :param target_connections: list of connection handles
        :param i: current index
        :param tunnel_threads: list of tunnel threads
        :param forward_ports: list of forwarded ports
        :param ports: list of ports of the connections
        :return: boolean whether the connection has root privileges or not
        """
        target_connections[i].write("sudo -v\n".encode())
        response = target_connections[i].read_until(constants.TELNET.PROMPT, timeout=5)
        root = False
        if not "Sorry, user {} may not run sudo".format(users[i]) in response.decode("utf-8"):
            root = True
        connection_dto = ConnectionObservationState(conn=target_connections[i], username=users[i], root=root,
                                                    service=constants.TELNET.SERVICE_NAME, tunnel_thread=tunnel_threads[i],
                                                    tunnel_port=forward_ports[i],
                                                    port=ports[i])
        target_machine.telnet_connections.append(connection_dto)
        return root

    @staticmethod
    def _ftp_setup_connection(target_machine: MachineObservationState, a: Action, env_config: EnvConfig) \
            -> Union[bool, List[str], List, List[ForwardTunnelThread], List[int], List[int]]:
        """
        Helper function for setting up a FTP connection

        :param target_machine: the target machine to connect to
        :param a: the action of the connection
        :param env_config: the environment config
        :return: connected (bool), connected users, connection handles, list of tunnel threads, list of forwarded ports,
                 list of ports
        """
        connected = False
        users = []
        target_connections = []
        tunnel_threads = []
        forward_ports = []
        ports = []
        interactive_shells = []
        for cr in target_machine.shell_access_credentials:
            if cr.service == constants.FTP.SERVICE_NAME:
                try:
                    forward_port = env_config.get_port_forward_port()
                    tunnel_thread = ForwardTunnelThread(local_port=forward_port,
                                                        remote_host=a.ip, remote_port=cr.port,
                                                        transport=env_config.cluster_config.agent_conn.get_transport())
                    tunnel_thread.start()
                    target_conn = FTP()
                    target_conn.connect(host=constants.FTP.LOCALHOST, port=forward_port, timeout=5)
                    login_result = target_conn.login(cr.username, cr.pw)
                    if constants.FTP.INCORRECT_LOGIN not in login_result:
                        connected = True
                        users.append(cr.username)
                        target_connections.append(target_conn)
                        tunnel_threads.append(tunnel_thread)
                        forward_ports.append(forward_port)
                        ports.append(cr.port)
                        # Create LFTP connection too to be able to search file system
                        shell = env_config.cluster_config.agent_conn.invoke_shell()
                        # clear output
                        if shell.recv_ready():
                            shell.recv(constants.COMMON.DEFAULT_RECV_SIZE)
                        shell.send(constants.FTP.LFTP_PREFIX + cr.username + ":" + cr.pw + "@" + a.ip + "\n")
                        time.sleep(0.2)
                        # clear output
                        if shell.recv_ready():
                            o = shell.recv(constants.COMMON.DEFAULT_RECV_SIZE)
                        interactive_shells.append(shell)
                except Exception as e:
                    print("FTP exception: {}".format(str(e)))

        return connected, users, target_connections, tunnel_threads, forward_ports, ports, interactive_shells

    @staticmethod
    def _ftp_finalize_connection(target_machine: MachineObservationState, users: List[str], target_connections: List, i: int,
                                 tunnel_threads: List, forward_ports: List[int], ports: List[int],
                                 interactive_shells: List) -> bool:
        """
        Helper function for creating the connection DTO for FTP

        :param target_machine: the target machine to connect to
        :param users: list of users that are connected
        :param target_connections: list of connections to the target
        :param i: current index
        :param tunnel_threads: list of tunnel threads to the target
        :param forward_ports: list of forwarded ports to the target
        :param ports: list of ports of the connections
        :param interactive_shells: shells for LFTP
        :return: boolean, whether the connection has root privileges
        """
        root = False
        connection_dto = ConnectionObservationState(conn=target_connections[i], username=users[i], root=root,
                                                    service=constants.FTP.SERVICE_NAME,
                                                    tunnel_thread=tunnel_threads[i],
                                                    tunnel_port=forward_ports[i],
                                                    port=ports[i],
                                                    interactive_shell = interactive_shells[i])
        target_machine.ftp_connections.append(connection_dto)
        return root
