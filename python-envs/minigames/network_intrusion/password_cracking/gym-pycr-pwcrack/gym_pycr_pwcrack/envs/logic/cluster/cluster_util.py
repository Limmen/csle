from typing import Tuple, List, Union
from xml.etree.ElementTree import fromstring
import xml.etree.ElementTree as ET
import time
import paramiko
import telnetlib
import random
from ftplib import FTP
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action_results.nmap_scan_result import NmapScanResult
from gym_pycr_pwcrack.dao.action_results.nikto_scan_result import NiktoScanResult
from gym_pycr_pwcrack.dao.action_results.nikto_vuln import NiktoVuln
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
from gym_pycr_pwcrack.dao.network.credential import Credential
from gym_pycr_pwcrack.dao.action_results.nmap_hop import NmapHop
from gym_pycr_pwcrack.dao.action_results.nmap_trace import NmapTrace
from gym_pycr_pwcrack.dao.action_results.nmap_http_enum import NmapHttpEnum
from gym_pycr_pwcrack.dao.action_results.nmap_http_grep import NmapHttpGrep
from gym_pycr_pwcrack.dao.action_results.nmap_vulscan import NmapVulscan
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.action_results.ids_alert import IdsAlert

class ClusterUtil:
    """
    Class containing utility functions for the cluster-middleware
    """

    @staticmethod
    def execute_ssh_cmd(cmd : str, conn) -> Tuple[bytes, bytes, float]:
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
    def write_estimated_cost(total_time, action: Action, env_config: EnvConfig, ip : str = None,
                             user: str = None, service : str = None, conn = None, dir: str = None,
                             machine_ip :str = None) -> None:
        """
        Caches the estimated cost of an action by writing it to a file

        :param total_time: the total time of executing the action
        :param action: the action
        :param env_config: the environment config
        :param ip: ip
        :param user: user
        :param service: service
        :param conn: conn
        :param dir: dir
        :param machine_ip: machine_ip
        :return: None
        """
        if conn is None:
            conn = env_config.cluster_config.agent_conn
        if dir is None or dir == "":
            dir = env_config.nmap_cache_dir

        sftp_client = conn.open_sftp()
        file_name = dir + str(action.id.value) + "_" + str(action.index)
        if not action.subnet and action.ip is not None:
            file_name = file_name + "_" + action.ip
        elif ip is not None:
            file_name = file_name + "_" + ip
        if service is not None:
            file_name = file_name + "_" + service
        if user is not None:
            file_name = file_name + "_" + user
        if machine_ip is not None:
            file_name = file_name + "_" + machine_ip
        file_name = file_name + constants.FILE_PATTERNS.COST_FILE_SUFFIX
        remote_file = sftp_client.file(file_name, mode="w")
        try:
            remote_file.write(str(round(total_time, 1)) + "\n")
        except Exception as e:
            print("exception writing cost file:{}".format(str(e)))
        finally:
            remote_file.close()

    @staticmethod
    def write_alerts_response(sum_priorities, num_alerts, action: Action, env_config: EnvConfig, ip: str = None,
                              user: str = None, service: str = None, conn=None, dir: str = None,
                              machine_ip: str = None) -> None:
        """
        Caches the number of triggered IDS alerts of an action by writing it to a file

        :param sum_priorities: the sum of the "priority" field of the alerts
        :param num_alerts: the number of different alerts that were triggered
        :param action: the action
        :param env_config: the environment config
        :param ip: ip
        :param user: user
        :param service: service
        :param conn: conn
        :param dir: dir
        :param machine_ip: machine_ip
        :return: None
        """
        if conn is None:
            conn = env_config.cluster_config.agent_conn
        if dir is None or dir == "":
            dir = env_config.nmap_cache_dir

        sftp_client = conn.open_sftp()
        file_name = dir + str(action.id.value) + "_" + str(action.index)
        if not action.subnet and action.ip is not None:
            file_name = file_name + "_" + action.ip
        elif ip is not None:
            file_name = file_name + "_" + ip
        if service is not None:
            file_name = file_name + "_" + service
        if user is not None:
            file_name = file_name + "_" + user
        if machine_ip is not None:
            file_name = file_name + "_" + machine_ip
        file_name = file_name + constants.FILE_PATTERNS.ALERTS_FILE_SUFFIX
        remote_file = sftp_client.file(file_name, mode="w")
        try:
            remote_file.write(str(sum_priorities) + "," + str(num_alerts) + "\n")
        except Exception as e:
            print("exception writing alerts file:{}".format(str(e)))
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
        file_name = env_config.nmap_cache_dir + str(action.id.value) + "_" + str(action.index) + "_" + ip + "_" + service \
                    + "_" + user + ".txt"
        remote_file = sftp_client.file(file_name, mode="a")
        try:
            for file in files:
                remote_file.write(file + "\n")
        except Exception as e:
            print("exception writing cache:{}".format(str(e)))
        finally:
            remote_file.close()

    @staticmethod
    def write_user_command_cache(action: Action, env_config: EnvConfig, user: str, result: str,
                                     ip: str) \
            -> None:
        """
        Caches the result of a user command action

        :param action: the action
        :param env_config: the env config
        :param user: the user
        :param result: the result to cache
        :param ip: the ip
        :return: None
        """
        sftp_client = env_config.cluster_config.agent_conn.open_sftp()
        file_name = env_config.nmap_cache_dir + str(action.id.value) + "_" + str(
            action.index) + "_" + ip + \
                    "_" + user + ".txt"
        remote_file = sftp_client.file(file_name, mode="w")
        try:
            remote_file.write(result)
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
    def check_nmap_action_cache(a: Action, env_config: EnvConfig, conn = None,  dir : str = None,
                                machine_ip : str = None):
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
    def check_filesystem_action_cache(a: Action, env_config: EnvConfig, ip: str, service : str, user: str):
        """
        Checks if a filesystem action is cached or not

        :param a: the action
        :param env_config: the environment configuration
        :return: None or the name of the file where the result is cached
        """
        query = str(a.id.value) + "_" + str(a.index) + "_" + ip + "_" + service + "_" + user + ".txt"

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

        env_config.cache_misses += 1

        return None

    @staticmethod
    def check_user_action_cache(a: Action, env_config: EnvConfig, ip: str, user: str):
        """
        Checks if a user-specific action is cached or not

        :param a: the action
        :param env_config: the environment configuration
        :return: None or the name of the file where the result is cached
        """
        query = str(a.id.value) + "_" + str(a.index) + "_" + ip + "_" + user + ".txt"

        # Search through cache
        if query in env_config.user_command_cache_files_cache:
            return query

        stdin, stdout, stderr = env_config.cluster_config.agent_conn.exec_command(constants.COMMANDS.LIST_CACHE
                                                                                  + env_config.nmap_cache_dir)
        cache_list = []
        for line in stdout:
            cache_list.append(line.replace("\n", ""))
        env_config.user_command_cache_files_cache = cache_list

        # Search through updated cache
        if query in env_config.user_command_cache_files_cache:
            return query

        env_config.cache_misses += 1

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
        query = str(a.id.value) + "_" + str(a.index) + "_" + a.ip + constants.FILE_PATTERNS.NMAP_ACTION_RESULT_SUFFIX
        if a.subnet:
            query = str(a.id.value) + "_" + str(a.index) + constants.FILE_PATTERNS.NMAP_ACTION_RESULT_SUFFIX
        for item in cache_list:
            if item == query:
                return item

        return None

    @staticmethod
    def delete_cache_file(file_name: str, env_config: EnvConfig) -> Tuple[bytes, bytes, float]:
        """
        Deletes the file that contains the cached result of some operation

        :param file_name: name of the file to delete
        :param env_config: the environment config
        :return: outdata, errdata, total_time
        """
        cmd = "rm -f " + env_config.nmap_cache_dir + file_name
        return ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=env_config.cluster_config.agent_conn)

    @staticmethod
    def parse_nmap_scan(file_name: str, env_config: EnvConfig, conn = None, dir: str = None) -> ET.Element:
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
    def parse_nikto_scan(file_name: str, env_config: EnvConfig) -> ET.Element:
        """
        Parses an XML file containing the result of an nikt scan

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
                host = ClusterUtil._parse_nmap_host_xml(child, action=action)
                hosts = ClusterUtil._merge_nmap_hosts(host, hosts, action=action)
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
                ports, vulnerabilities, credentials = ClusterUtil._parse_nmap_ports_xml(child, action=action)
            elif child.tag == constants.NMAP_XML.OS:
                os_matches = ClusterUtil._parse_nmap_os_xml(child)
                os = NmapOs.get_best_match(os_matches)
            elif child.tag == constants.NMAP_XML.TRACE:
                trace = ClusterUtil._parse_nmap_trace_xml(child)
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
    def _parse_nmap_ports_xml(xml_data, action: Action) -> Tuple[List[NmapPort], List[NmapVuln], List[NmapBruteCredentials]]:
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
                        port_status = ClusterUtil._parse_nmap_port_status_xml(child_2)
                    elif child_2.tag == constants.NMAP_XML.SERVICE:
                        service_name = ClusterUtil._parse_nmap_service_name_xml(child_2)
                        service_version = ClusterUtil._parse_nmap_service_version_xml(child_2)
                        service_fp = ClusterUtil._parse_nmap_service_fp_xml(child_2)
                    elif child_2.tag == constants.NMAP_XML.SCRIPT:
                        result, brute_vuln = ClusterUtil._parse_nmap_script(child_2, port=port_id, protocol=protocol,
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
                return ClusterUtil._parse_nmap_vulners(xml_data, port=port, protocol=protocol, service=service), None
            elif xml_data.attrib[constants.NMAP_XML.ID] in constants.NMAP_XML.BRUTE_SCRIPTS:
                return ClusterUtil._parse_nmap_brute(xml_data, port=port, protocol=protocol, service=service,
                                                     action=action)
            elif xml_data.attrib[constants.NMAP_XML.ID] == constants.NMAP_XML.HTTP_ENUM_SCRIPT:
                return ClusterUtil._parse_nmap_http_enum_xml(xml_data), None
            elif xml_data.attrib[constants.NMAP_XML.ID] == constants.NMAP_XML.HTTP_GREP_SCRIPT:
                return ClusterUtil._parse_nmap_http_grep_xml(xml_data), None
            elif xml_data.attrib[constants.NMAP_XML.ID] == constants.NMAP_XML.VULSCAN_SCRIPT:
                return ClusterUtil._parse_nmap_http_vulscan_xml(xml_data), None
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
                        vuln = ClusterUtil._parse_nmap_table_vuln(c_2, port=port, protocol=protocol, service=service)
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
                                cred = ClusterUtil._parse_nmap_table_cred(c_2, port=port, protocol=protocol, service=service)
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
    def merge_nmap_scan_result_with_state(scan_result : NmapScanResult, s: EnvState, a: Action, env_config: EnvConfig) \
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
            #m_obs = EnvDynamicsUtil.brute_tried_flags(a=a, m_obs=m_obs)
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
    def nmap_scan_action_helper(s: EnvState, a: Action, env_config: EnvConfig, masscan : bool = False) \
            -> Tuple[EnvState, float, bool]:
        """
        Helper function for executing a NMAP scan action on the cluster. Implements caching.

        :param s: the current env state
        :param a: the NMAP action to execute
        :param env_config: the env config
        :return: s', reward, done
        """
        cache_filename = str(a.id.value) + "_" + str(a.index) + "_" + a.ip + ".xml"
        cache_id = (a.id, a.index, a.ip, a.subnet)
        if a.subnet:
            cache_filename = str(a.id.value) + "_" + str(a.index) + ".xml"


        # Check in-memory cache
        if env_config.use_nmap_cache:
            cache_value = env_config.nmap_scan_cache.get(cache_id)
            if cache_value is not None:
                s.obs_state.agent_reachable.update(cache_value.reachable)
                return ClusterUtil.nmap_pivot_scan_action_helper(s=s, a=a, env_config=env_config,
                                                                 partial_result=cache_value.copy(), masscan=masscan)

        # Check On-disk cache
        cache_result = None
        if env_config.use_nmap_cache:
            cache_result = ClusterUtil.check_nmap_action_cache(a=a, env_config=env_config)

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
                #alerts = ClusterUtil.check_ids_alerts(env_config=env_config)
                fast_logs = ClusterUtil.check_ids_fast_log(env_config=env_config)
                #alerts = list(filter(lambda x: x.timestamp > last_alert_ts, alerts))
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
                xml_data = ClusterUtil.parse_nmap_scan(file_name=cache_result, env_config=env_config)
                scan_result = ClusterUtil.parse_nmap_scan_xml(xml_data, ip=env_config.hacker_ip, action=a)
                s.obs_state.agent_reachable.update(scan_result.reachable)
                break
            except Exception as e:
                scan_result = NmapScanResult(hosts=[], ip=env_config.hacker_ip)
                #print("read nmap scan exception:{}, action:{}".format(str(e), a.name))
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
        return ClusterUtil.nmap_pivot_scan_action_helper(s=s, a=a, env_config=env_config,
                                                         partial_result=scan_result.copy(), masscan=masscan)


    @staticmethod
    def login_service_helper(s: EnvState, a: Action, alive_check, service_name : str,
                             env_config: EnvConfig) -> Tuple[EnvState, int, int, int, int, int, int, int,
                                                             int, float, bool]:
        """
        Helper function for logging in to a network service in the cluster

        :param s: the current state
        :param a: the action of the login
        :param alive_check:  the function to check whether current connections are alive or not
        :param service_name: name of the service to login to
        :param env_config: environment config
        :return: s_prime, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
                   total_new_shell_access, total_new_flag_pts, total_new_root, cost, new_conn, total_new_osvdb_found,
                   total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed
        """        
        total_new_ports, total_new_os, total_new_vuln, total_new_machines, total_new_shell_access, \
        total_new_root, total_new_flag_pts, total_new_osvdb_vuln_found, total_new_logged_in, \
        total_new_tools_installed, total_new_backdoors_installed = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        total_cost = 0
        target_machine = None
        non_used_credentials = []
        root = False
        for m in s.obs_state.machines:
            if m.ip == a.ip:
                target_machine = m
                target_machine = target_machine.copy()
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

        # Check cached connections
        non_used_nor_cached_credentials = []
        for cr in non_used_credentials:
            if cr.service == constants.SSH.SERVICE_NAME:
                key = (target_machine.ip, cr.username, cr.port)
                if key in s.cached_ssh_connections:
                    c = s.cached_ssh_connections[key]
                    target_machine.ssh_connections.append(c)
                    target_machine.logged_in = True
                    target_machine.root = c.root
                    if cr.service not in target_machine.logged_in_services:
                        target_machine.logged_in_services.append(cr.service)
                    if cr.service not in target_machine.root_services:
                        target_machine.root_services.append(cr.service)
                else:
                    non_used_nor_cached_credentials.append(cr)
            elif cr.service == constants.TELNET.SERVICE_NAME:
                key = (target_machine.ip, cr.username, cr.port)
                if key in s.cached_telnet_connections:
                    c = s.cached_telnet_connections[key]
                    target_machine.telnet_connections.append(c)
                    target_machine.logged_in = True
                    target_machine.root = c.root
                    if cr.service not in target_machine.logged_in_services:
                        target_machine.logged_in_services.append(cr.service)
                    if cr.service not in target_machine.root_services:
                        target_machine.root_services.append(cr.service)
                else:
                    non_used_nor_cached_credentials.append(cr)
            elif cr.service == constants.FTP.SERVICE_NAME:
                key = (target_machine.ip, cr.username, cr.port)
                if key in s.cached_ftp_connections:
                    c = s.cached_ftp_connections[key]
                    target_machine.ftp_connections.append(c)
                    target_machine.logged_in = True
                    target_machine.root = c.root
                    if cr.service not in target_machine.logged_in_services:
                        target_machine.logged_in_services.append(cr.service)
                    if cr.service not in target_machine.root_services:
                        target_machine.root_services.append(cr.service)
                else:
                    non_used_nor_cached_credentials.append(cr)

        if target_machine is None or root or len(non_used_nor_cached_credentials) == 0:
            s_prime = s
            if target_machine is not None:
                new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
                total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
                total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed = \
                    EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, [target_machine],
                                                           env_config=env_config, action=a)
                s_prime.obs_state.machines = new_machines_obs

            return s_prime, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
                   total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
                   total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed, total_cost, False

        # If not logged in and there are credentials, setup a new connection
        connected = False
        users = []
        target_connections = []
        ports = []
        proxy_connections = [ConnectionObservationState(conn=env_config.cluster_config.agent_conn,
                                                        username=env_config.cluster_config.agent_username,
                                                        root=True, port=22, service=constants.SSH.SERVICE_NAME,
                                                        proxy= None, ip=env_config.cluster_config.agent_ip)]
        for m in s.obs_state.machines:
            ssh_connections_sorted_by_root = sorted(m.ssh_connections, key=lambda x: ("ssh_backdoor" in x.username, x.root, x.username),
                                                    reverse=True)
            if len(ssh_connections_sorted_by_root) > 0:
                proxy_connections.append(ssh_connections_sorted_by_root[0])

        if service_name == constants.SSH.SERVICE_NAME:
            connected, users, target_connections, ports, cost, non_failed_credentials, proxies = ClusterUtil._ssh_setup_connection(
                a=a, env_config=env_config, credentials=non_used_nor_cached_credentials,
                proxy_connections=proxy_connections, s=s)
        elif service_name == constants.TELNET.SERVICE_NAME:
            connected, users, target_connections, tunnel_threads, forward_ports, ports, cost, non_failed_credentials, \
            proxies = \
                ClusterUtil._telnet_setup_connection(a=a, env_config=env_config,
                                                     credentials=non_used_nor_cached_credentials,
                                                     proxy_connections=proxy_connections, s=s)
        elif service_name == constants.FTP.SERVICE_NAME:
            connected, users, target_connections, tunnel_threads, forward_ports, ports, i_shells, \
            cost, non_failed_credentials, proxies = \
                ClusterUtil._ftp_setup_connection(a=a, env_config=env_config,
                                                  credentials=non_used_nor_cached_credentials,
                                                  proxy_connections=proxy_connections,
                                                  s=s)

        s_prime = s
        if len(non_failed_credentials) > 0:
            total_cost += cost
            if connected:
                root = False
                target_machine.logged_in = True
                target_machine.shell_access_credentials = non_failed_credentials
                if service_name not in target_machine.logged_in_services:
                    target_machine.logged_in_services.append(service_name)
                if service_name not in target_machine.root_services:
                    target_machine.root_services.append(service_name)
                for i in range(len(target_connections)):
                    # Check if root
                    c_root = False
                    if service_name == constants.SSH.SERVICE_NAME:
                        c_root, cost = ClusterUtil._ssh_finalize_connection(target_machine=target_machine, users=users,
                                                                      target_connections=target_connections, i=i,
                                                                      ports=ports, proxies=proxies)
                    elif service_name == constants.TELNET.SERVICE_NAME:
                        c_root, cost = ClusterUtil._telnet_finalize_connection(target_machine=target_machine, users=users,
                                                                         target_connections=target_connections,
                                                                         i=i, tunnel_threads=tunnel_threads,
                                                                         forward_ports=forward_ports, ports=ports,
                                                                               proxies=proxies)
                    elif service_name == constants.FTP.SERVICE_NAME:
                        c_root, cost = ClusterUtil._ftp_finalize_connection(target_machine=target_machine, users=users,
                                                                      target_connections=target_connections,
                                                                      i=i, tunnel_threads=tunnel_threads,
                                                                      forward_ports=forward_ports, ports=ports,
                                                                      interactive_shells=i_shells,
                                                                            proxies=proxies)
                    total_cost += cost
                    if c_root:
                        root = True
            target_machine.root = root
            new_machines_obs, total_new_ports_found, total_new_os_found, total_new_cve_vuln_found, total_new_machines, \
               total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
               total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed = \
                EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, [target_machine], env_config=env_config,
                                                       action=a)
            s_prime.obs_state.machines = new_machines_obs
        else:
            target_machine.shell_access = False
            target_machine.shell_access_credentials = []

        return s_prime, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
            total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
               total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed, total_cost, True


    @staticmethod
    def _ssh_setup_connection(a: Action, env_config: EnvConfig,
                              credentials : List[Credential], proxy_connections: List[ConnectionObservationState],
                              s: EnvState) \
            -> Tuple[bool, List[str], List, List[int], float, List[Credential]]:
        """
        Helper function for setting up a SSH connection

        :param a: the action of the connection
        :param env_config: the environment config
        :param credentials: list of credentials to try
        :param proxy_connections: list of proxy connections to try
        :param s: env state
        :return: boolean whether connected or not, list of connected users, list of connection handles, list of ports,
                 cost, non_failed_credentials
        """
        connected = False
        users = []
        target_connections = []
        proxies = []
        ports = []
        start = time.time()
        non_failed_credentials = []
        for proxy_conn in proxy_connections:
            if proxy_conn.ip != env_config.hacker_ip:
                m = s.get_machine(proxy_conn.ip)
                if m is None or a.ip not in m.reachable or m.ip == a.ip:
                    continue
            else:
                if not a.ip in s.obs_state.agent_reachable:
                    continue
            for cr in credentials:
                if cr.service == constants.SSH.SERVICE_NAME:
                    try:
                        agent_addr = (proxy_conn.ip, cr.port)
                        target_addr = (a.ip, cr.port)
                        agent_transport = proxy_conn.conn.get_transport()
                        relay_channel = agent_transport.open_channel(constants.SSH.DIRECT_CHANNEL, target_addr, agent_addr,
                                                                     timeout=3)
                        target_conn = paramiko.SSHClient()
                        target_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        target_conn.connect(a.ip, username=cr.username, password=cr.pw, sock=relay_channel,
                                            timeout=3)
                        connected = True
                        users.append(cr.username)
                        target_connections.append(target_conn)
                        proxies.append(proxy_conn)
                        ports.append(cr.port)
                        non_failed_credentials.append(cr)
                    except Exception as e:
                        print("SSH exception :{}".format(str(e)))
                        print("Target addr: {}, Source Addr: {}".format(target_addr, agent_addr))
                        print("Target ip in agent reachable: {}".format(a.ip in s.obs_state.agent_reachable))
                        print("Agent reachable:{}".format(s.obs_state.agent_reachable))
                else:
                    non_failed_credentials.append(cr)
            if connected:
                break
        end = time.time()
        total_time = end-start
        return connected, users, target_connections, ports, total_time, non_failed_credentials, proxies

    @staticmethod
    def _ssh_finalize_connection(target_machine: MachineObservationState, users: List[str],
                                 target_connections: List, i : int, ports: List[int],
                                 proxies : List) -> Tuple[bool, float]:
        """
        Helper function for finalizing a SSH connection and setting up the DTO

        :param target_machine: the target machine to connect to
        :param users: list of connected users
        :param target_connections: list of connection handles
        :param i: current index
        :param ports: list of ports of the connections
        :param proxies: proxy connections
        :return: boolean whether the connection has root privileges or not, cost
        """
        start = time.time()
        outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd="sudo -v",
                                                                   conn=target_connections[i])
        root = False
        if not "may not run sudo".format(users[i]) in errdata.decode("utf-8"):
            root = True
            target_machine.root = True
        connection_dto = ConnectionObservationState(conn=target_connections[i], username=users[i],
                                                    root=root,
                                                    service=constants.SSH.SERVICE_NAME,
                                                    port=ports[i], proxy=proxies[i], ip=target_machine.ip)
        target_machine.ssh_connections.append(connection_dto)
        end = time.time()
        total_time = end-start
        return root, total_time

    @staticmethod
    def _telnet_setup_connection(a: Action, env_config: EnvConfig,
                                 credentials : List[Credential], proxy_connections : List,
                                 s: EnvState) \
            -> Tuple[bool, List[str], List, List[ForwardTunnelThread], List[int], List[int], float, List[Credential]]:
        """
        Helper function for setting up a Telnet connection to a target machine

        :param a: the action of the connection
        :param env_config: the environment config
        :param credentials: list of credentials to try
        :param proxies: proxy connections
        :param s: env state
        :return: connected (bool), connected users, connection handles, list of tunnel threads, list of forwarded ports,
                 list of ports, cost
        """
        connected = False
        users = []
        target_connections = []
        tunnel_threads = []
        forward_ports = []
        ports = []
        start = time.time()
        non_failed_credentials = []
        proxies = []
        for proxy_conn in proxy_connections:
            if proxy_conn.ip != env_config.hacker_ip:
                m = s.get_machine(proxy_conn.ip)
                if m is None or a.ip not in m.reachable or m.ip == a.ip:
                    continue
            else:
                if not a.ip in s.obs_state.agent_reachable:
                    continue
            for cr in credentials:
                if cr.service == constants.TELNET.SERVICE_NAME:
                    try:
                        forward_port = env_config.get_port_forward_port()
                        agent_addr = (proxy_conn.ip, cr.port)
                        target_addr = (a.ip, cr.port)
                        agent_transport = proxy_conn.conn.get_transport()
                        relay_channel = agent_transport.open_channel(constants.SSH.DIRECT_CHANNEL, target_addr,
                                                                     agent_addr,
                                                                     timeout=3)
                        tunnel_thread = ForwardTunnelThread(local_port=forward_port,
                                                            remote_host=a.ip, remote_port=cr.port,
                                                            transport=agent_transport)
                        tunnel_thread.start()
                        target_conn = telnetlib.Telnet(host=constants.TELNET.LOCALHOST, port=forward_port, timeout=3)
                        target_conn.read_until(constants.TELNET.LOGIN_PROMPT, timeout=3)
                        target_conn.write((cr.username + "\n").encode())
                        target_conn.read_until(constants.TELNET.PASSWORD_PROMPT, timeout=3)
                        target_conn.write((cr.pw + "\n").encode())
                        response = target_conn.read_until(constants.TELNET.PROMPT, timeout=3)
                        response = response.decode()
                        if not constants.TELNET.INCORRECT_LOGIN in response and response != "":
                            connected = True
                            users.append(cr.username)
                            target_connections.append(target_conn)
                            proxies.append(proxy_conn)
                            tunnel_threads.append(tunnel_thread)
                            forward_ports.append(forward_port)
                            ports.append(cr.port)
                        non_failed_credentials.append(cr)
                    except Exception as e:
                        print("telnet exception:{}".format(str(e)))
                        print("Target:{} reachable from {}, {}".format(a.ip, m.ip, a.ip in m.reachable))
                        print("Target addr: {}, Source Addr: {}".format(target_addr, agent_addr))
                        print("Target ip in agent reachable: {}".format(a.ip in s.obs_state.agent_reachable))
                        print("Agent reachable:{}".format(s.obs_state.agent_reachable))
                else:
                    non_failed_credentials.append(cr)
            if connected:
                break
        end = time.time()
        total_time = end-start
        return connected, users, target_connections, tunnel_threads, forward_ports, ports, \
               total_time, non_failed_credentials, proxies

    @staticmethod
    def _telnet_finalize_connection(target_machine: MachineObservationState, users: List[str], target_connections: List, i: int,
                                    tunnel_threads: List, forward_ports : List[int], ports: List[int],
                                    proxies: List) \
            -> Tuple[bool, float]:
        """
        Helper function for finalizing a Telnet connection to a target machine and creating the DTO

        :param target_machine: the target machine to connect to
        :param users: list of connected users
        :param target_connections: list of connection handles
        :param i: current index
        :param tunnel_threads: list of tunnel threads
        :param forward_ports: list of forwarded ports
        :param ports: list of ports of the connections
        :param proxies: proxies
        :return: boolean whether the connection has root privileges or not, cost
        """
        start = time.time()
        target_connections[i].write("sudo -v\n".encode())
        response = target_connections[i].read_until(constants.TELNET.PROMPT, timeout=3)
        root = False
        if not "may not run sudo".format(users[i]) in response.decode("utf-8"):
            root = True
        connection_dto = ConnectionObservationState(conn=target_connections[i], username=users[i], root=root,
                                                    service=constants.TELNET.SERVICE_NAME, tunnel_thread=tunnel_threads[i],
                                                    tunnel_port=forward_ports[i],
                                                    port=ports[i], proxy=proxies[i], ip=target_machine.ip)
        target_machine.telnet_connections.append(connection_dto)
        end = time.time()
        total_time = end-start
        return root, total_time

    @staticmethod
    def _ftp_setup_connection(a: Action, env_config: EnvConfig,
                              credentials : List[Credential], proxy_connections : List,
                              s: EnvState) \
            -> Tuple[bool, List[str], List, List[ForwardTunnelThread], List[int], List[int], float,  List[Credential]]:
        """
        Helper function for setting up a FTP connection

        :param a: the action of the connection
        :param env_config: the environment config
        :param credentials: list of credentials to try
        :param proxy_connections: proxy connections
        :param env_state: env state
        :return: connected (bool), connected users, connection handles, list of tunnel threads, list of forwarded ports,
                 list of ports, cost, non_failed_credentials
        """
        connected = False
        users = []
        target_connections = []
        tunnel_threads = []
        forward_ports = []
        ports = []
        interactive_shells = []
        start = time.time()
        non_failed_credentials = []
        proxies = []
        for proxy_conn in proxy_connections:
            if proxy_conn.ip != env_config.hacker_ip:
                m = s.get_machine(proxy_conn.ip)
                if m is None or a.ip not in m.reachable or m.ip == a.ip:
                    continue
            else:
                if not a.ip in s.obs_state.agent_reachable:
                    continue
            for cr in credentials:
                if cr.service == constants.FTP.SERVICE_NAME:
                    try:
                        forward_port = env_config.get_port_forward_port()
                        agent_addr = (proxy_conn.ip, cr.port)
                        target_addr = (a.ip, cr.port)
                        agent_transport = proxy_conn.conn.get_transport()
                        relay_channel = agent_transport.open_channel(constants.SSH.DIRECT_CHANNEL, target_addr,
                                                                     agent_addr,
                                                                     timeout=3)
                        tunnel_thread = ForwardTunnelThread(local_port=forward_port,
                                                            remote_host=a.ip, remote_port=cr.port,
                                                            transport=agent_transport)
                        tunnel_thread.start()
                        target_conn = FTP()
                        target_conn.connect(host=constants.FTP.LOCALHOST, port=forward_port, timeout=5)
                        login_result = target_conn.login(cr.username, cr.pw)
                        if constants.FTP.INCORRECT_LOGIN not in login_result:
                            connected = True
                            users.append(cr.username)
                            target_connections.append(target_conn)
                            proxies.append(proxy_conn)
                            tunnel_threads.append(tunnel_thread)
                            forward_ports.append(forward_port)
                            ports.append(cr.port)
                            # Create LFTP connection too to be able to search file system
                            shell = proxy_conn.conn.invoke_shell()
                            # clear output
                            if shell.recv_ready():
                                shell.recv(constants.COMMON.DEFAULT_RECV_SIZE)
                            shell.send(constants.FTP.LFTP_PREFIX + cr.username + ":" + cr.pw + "@" + a.ip + "\n")
                            time.sleep(0.5)
                            # clear output
                            if shell.recv_ready():
                                o = shell.recv(constants.COMMON.DEFAULT_RECV_SIZE)
                            interactive_shells.append(shell)
                            non_failed_credentials.append(cr)
                    except Exception as e:
                        print("FTP exception: {}".format(str(e)))
                        print("Target addr: {}, Source Addr: {}".format(target_addr, agent_addr))
                        print("Target ip in agent reachable: {}".format(a.ip in s.obs_state.agent_reachable))
                        print("Agent reachable:{}".format(s.obs_state.agent_reachable))
                else:
                    non_failed_credentials.append(cr)
            if connected:
                break
        end = time.time()
        total_time = end-start
        return connected, users, target_connections, tunnel_threads, forward_ports, ports, interactive_shells, total_time, \
               non_failed_credentials, proxies

    @staticmethod
    def _ftp_finalize_connection(target_machine: MachineObservationState, users: List[str], target_connections: List, i: int,
                                 tunnel_threads: List, forward_ports: List[int], ports: List[int],
                                 interactive_shells: List, proxies: List) -> Tuple[bool, float]:
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
        :return: boolean, whether the connection has root privileges, cost
        """
        root = False
        connection_dto = ConnectionObservationState(conn=target_connections[i], username=users[i], root=root,
                                                    service=constants.FTP.SERVICE_NAME,
                                                    tunnel_thread=tunnel_threads[i],
                                                    tunnel_port=forward_ports[i],
                                                    port=ports[i],
                                                    interactive_shell = interactive_shells[i], ip=target_machine.ip,
                                                    proxy=proxies[i])
        target_machine.ftp_connections.append(connection_dto)
        return root, 0

    @staticmethod
    def _find_flag_using_ssh(machine: MachineObservationState, env_config: EnvConfig, a: Action,
                             new_m_obs: MachineObservationState) -> Tuple[MachineObservationState, float, bool]:
        """
        Utility function for using existing SSH connections to a specific machine to search the file system for flags

        :param machine: the machine to search
        :param env_config: the env config
        :param a: the action of finding the flags
        :param new_m_obs: the updated machine observation with the found flags
        :return: the updated machine observation with the found flags, cost, root
        """        
        total_cost = 0
        ssh_connections_sorted_by_root = sorted(machine.ssh_connections, key=lambda x: ("ssh_backdoor" in x.username, x.root, x.username), reverse=True)
        root_scan = False
        total_alerts = (0,0)
        for c in ssh_connections_sorted_by_root:
            cache_file = \
                ClusterUtil.check_filesystem_action_cache(a=a, env_config=env_config, ip=machine.ip,
                                                          service=constants.SSH.SERVICE_NAME,
                                                          user=c.username)
            if cache_file is not None:
                flag_paths = ClusterUtil.parse_file_scan_file(file_name=cache_file,
                                                              env_config=env_config)
            else:
                if env_config.ids_router:
                    last_alert_ts = ClusterUtil.get_latest_alert_ts(env_config=env_config)
                cmd = a.cmd[0]
                if c.root:
                    cmd = constants.COMMANDS.SUDO + " " + cmd
                for i in range(env_config.ssh_retry_find_flag):
                    outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
                    new_m_obs.filesystem_searched = True
                    if env_config.ids_router:
                        fast_logs = ClusterUtil.check_ids_fast_log(env_config=env_config)
                        if last_alert_ts is not None:
                            fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                        sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                        num_alerts = len(fast_logs)
                        ClusterUtil.write_alerts_response(sum_priorities=sum_priority_alerts, num_alerts=num_alerts,
                                                          action=a, env_config=env_config, ip=machine.ip,
                                                          user=c.username, service=constants.SSH.SERVICE_NAME)
                        env_config.action_alerts.user_ip_add_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                   service=constants.SSH.SERVICE_NAME,
                                                                   alert=(sum_priority_alerts, num_alerts))

                    ClusterUtil.write_estimated_cost(total_time=total_time, action=a,
                                                     env_config=env_config, ip=machine.ip,
                                                     user=c.username,
                                                     service=constants.SSH.SERVICE_NAME)
                    env_config.action_costs.find_add_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                          service=constants.SSH.SERVICE_NAME,
                                                          cost=float(total_time))
                    outdata_str = outdata.decode()
                    flag_paths = outdata_str.split("\n")
                    flag_paths = list(filter(lambda x: x != '', flag_paths))
                    if len(flag_paths) > 0:
                        break
                    else:
                        time.sleep(1)

                # Persist cache
                ClusterUtil.write_file_system_scan_cache(action=a, env_config=env_config,
                                                         service=constants.SSH.SERVICE_NAME, user=c.username,
                                                         files=flag_paths, ip=machine.ip)

            # Check for flags
            for fp in flag_paths:
                fp = fp.replace(".txt", "")
                if (machine.ip, fp) in env_config.flag_lookup:
                    new_m_obs.flags_found.add(env_config.flag_lookup[(machine.ip, fp)])

            # Update cost
            if env_config.action_costs.find_exists(action_id=a.id, ip=machine.ip, user=c.username,
                                                   service=constants.SSH.SERVICE_NAME):
                cost = env_config.action_costs.find_get_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                             service=constants.SSH.SERVICE_NAME)
                total_cost += cost

            # Update alerts
            if env_config.ids_router and env_config.action_alerts.user_ip_exists(action_id=a.id, ip=machine.ip,
                                                                                 user=c.username,
                                                                                 service=constants.SSH.SERVICE_NAME):
                alerts = env_config.action_alerts.user_ip_get_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                             service=constants.SSH.SERVICE_NAME)
                total_alerts = alerts

            if c.root:
                root_scan = True
                break
        return new_m_obs, total_cost, root_scan, total_alerts

    @staticmethod
    def _find_flag_using_telnet(machine: MachineObservationState, env_config: EnvConfig, a: Action,
                             new_m_obs: MachineObservationState) -> Tuple[MachineObservationState, float, bool]:
        """
        Utility function for using existing Telnet connections to a specific machine to search the file system for flags

        :param machine: the machine to search
        :param env_config: the env config
        :param a: the action of finding the flags
        :param new_m_obs: the updated machine observation with the found flags
        :return: the updated machine observation with the found flags, cost, root
        """
        total_cost = 0
        total_alerts = (0, 0)
        telnet_connections_sorted_by_root = sorted(machine.telnet_connections, key=lambda x: ("ssh_backdoor" in x.username, x.root, x.username),
                                                   reverse=True)
        root_scan = False
        for c in telnet_connections_sorted_by_root:
            cache_file = \
                ClusterUtil.check_filesystem_action_cache(a=a, env_config=env_config, ip=machine.ip,
                                                          service=constants.TELNET.SERVICE_NAME,
                                                          user=c.username)
            if cache_file is not None:
                flag_paths = ClusterUtil.parse_file_scan_file(file_name=cache_file,
                                                              env_config=env_config)
            else:
                cmd = a.cmd[0] + "\n"
                if c.root:
                    cmd = constants.COMMANDS.SUDO + " " + cmd
                if env_config.ids_router:
                    last_alert_ts = ClusterUtil.get_latest_alert_ts(env_config=env_config)
                start = time.time()
                c.conn.write(cmd.encode())
                response = c.conn.read_until(constants.TELNET.PROMPT, timeout=5)
                new_m_obs.filesystem_searched = True
                end = time.time()
                total_time = end - start
                if env_config.ids_router:
                    fast_logs = ClusterUtil.check_ids_fast_log(env_config=env_config)
                    if last_alert_ts is not None:
                        fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                    sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                    num_alerts = len(fast_logs)
                    ClusterUtil.write_alerts_response(sum_priorities=sum_priority_alerts, num_alerts=num_alerts,
                                                      action=a, env_config=env_config, ip=machine.ip,
                                                      user=c.username,
                                                      service=constants.TELNET.SERVICE_NAME)
                    env_config.action_alerts.user_ip_add_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                               service=constants.TELNET.SERVICE_NAME,
                                                               alert=(sum_priority_alerts, num_alerts))

                ClusterUtil.write_estimated_cost(total_time=total_time, action=a,
                                                 env_config=env_config, ip=machine.ip,
                                                 user=c.username,
                                                 service=constants.TELNET.SERVICE_NAME)
                env_config.action_costs.find_add_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                      service=constants.TELNET.SERVICE_NAME,
                                                      cost=float(total_time))
                flag_paths = response.decode().strip().split("\r\n")
                # Persist cache
                ClusterUtil.write_file_system_scan_cache(action=a, env_config=env_config,
                                                         service=constants.TELNET.SERVICE_NAME, user=c.username,
                                                         files=flag_paths, ip=machine.ip)
            # Check for flags
            for fp in flag_paths:
                fp = fp.replace(".txt", "")
                if (machine.ip, fp) in env_config.flag_lookup:
                    new_m_obs.flags_found.add(env_config.flag_lookup[(machine.ip, fp)])

            # Update cost
            if env_config.action_costs.find_exists(action_id=a.id, ip=machine.ip, user=c.username,
                                                   service=constants.TELNET.SERVICE_NAME):
                cost = env_config.action_costs.find_get_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                             service=constants.TELNET.SERVICE_NAME)
                total_cost += cost

            # Update alerts
            if env_config.ids_router and env_config.action_alerts.user_ip_exists(action_id=a.id, ip=machine.ip,
                                                                                 user=c.username,
                                                                                 service=constants.TELNET.SERVICE_NAME):
                alerts = env_config.action_alerts.user_ip_get_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                    service=constants.TELNET.SERVICE_NAME)
                total_alerts = alerts

            if c.root:
                root_scan = True
                break
        return new_m_obs, total_cost, root_scan, total_alerts

    @staticmethod
    def _find_flag_using_ftp(machine: MachineObservationState, env_config: EnvConfig, a: Action,
                                new_m_obs: MachineObservationState) -> Tuple[MachineObservationState, float, bool]:
        """
        Utility function for using existing FTP connections to a specific machine to search the file system for flags

        :param machine: the machine to search
        :param env_config: the env config
        :param a: the action of finding the flags
        :param new_m_obs: the updated machine observation with the found flags
        :return: the updated machine observation with the found flags, cost, root
        """
        total_cost = 0
        total_alerts = (0, 0)
        ftp_connections_sorted_by_root = sorted(machine.ftp_connections, key=lambda x: ("ssh_backdoor" in x.username, x.root, x.username), reverse=True)
        root_scan = False
        for c in ftp_connections_sorted_by_root:
            cache_file = \
                ClusterUtil.check_filesystem_action_cache(a=a, env_config=env_config, ip=machine.ip,
                                                          service=constants.FTP.SERVICE_NAME,
                                                          user=c.username)
            if cache_file is not None:
                flag_paths = ClusterUtil.parse_file_scan_file(file_name=cache_file,
                                                              env_config=env_config)
            else:
                for i in range(env_config.ftp_retry_find_flag):
                    cmd = a.alt_cmd[0] + "\n"
                    if c.root:
                        cmd = constants.COMMANDS.SUDO + " " + cmd
                    if env_config.ids_router:
                        last_alert_ts = ClusterUtil.get_latest_alert_ts(env_config=env_config)
                    start = time.time()
                    c.interactive_shell.send(cmd)
                    output = b""
                    # clear output
                    if c.interactive_shell.recv_ready():
                        c.interactive_shell.recv(constants.COMMON.DEFAULT_RECV_SIZE)
                    command_complete = False
                    timeouts = 0
                    while not command_complete:
                        while not c.interactive_shell.recv_ready():
                            if timeouts > env_config.shell_max_timeouts:
                                print("max timeouts FTP")
                                break
                            time.sleep(env_config.shell_read_wait)
                            timeouts += 1
                        if c.interactive_shell.recv_ready():
                            output += c.interactive_shell.recv(constants.COMMON.LARGE_RECV_SIZE)
                            timeouts = 0
                            if constants.FTP.LFTP_PROMPT in output.decode() \
                                    or constants.FTP.LFTP_PROMPT_2 in output.decode():
                                command_complete = True
                                end = time.time()
                                total_time = end - start
                                if env_config.ids_router:
                                    fast_logs = ClusterUtil.check_ids_fast_log(env_config=env_config)
                                    if last_alert_ts is not None:
                                        fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                                    sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                                    num_alerts = len(fast_logs)
                                    ClusterUtil.write_alerts_response(sum_priorities=sum_priority_alerts,
                                                                      num_alerts=num_alerts,
                                                                      action=a, env_config=env_config, ip=machine.ip,
                                                                      user=c.username,
                                                                      service=constants.FTP.SERVICE_NAME)
                                    env_config.action_alerts.user_ip_add_alert(action_id=a.id, ip=machine.ip,
                                                                               user=c.username,
                                                                               service=constants.FTP.SERVICE_NAME,
                                                                               alert=(sum_priority_alerts, num_alerts))

                                ClusterUtil.write_estimated_cost(total_time=total_time, action=a,
                                                                 env_config=env_config, ip=machine.ip,
                                                                 user=c.username,
                                                                 service=constants.FTP.SERVICE_NAME)
                                env_config.action_costs.find_add_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                                      service=constants.FTP.SERVICE_NAME,
                                                                      cost=float(total_time))
                        else:
                            break

                    output_str = output.decode("utf-8")
                    output_str = env_config.shell_escape.sub("", output_str)
                    output_list = output_str.split('\r\n')
                    output_list = output_list[1:-1]  # remove command ([0]) and prompt ([-1])
                    flag_paths = list(filter(lambda x: not constants.FTP.ACCESS_FAILED in x and x!= "", output_list))
                    ff = False
                    # Check for flags
                    for fp in flag_paths:
                        fp = fp.replace(".txt", "")
                        if (machine.ip, fp) in env_config.flag_lookup:
                            ff=True
                    if not ff:
                        continue
                    else:
                        break
                # Persist cache
                ClusterUtil.write_file_system_scan_cache(action=a, env_config=env_config,
                                                         service=constants.FTP.SERVICE_NAME, user=c.username,
                                                         files=flag_paths, ip=machine.ip)
            new_m_obs.filesystem_searched = True
            # Check for flags
            for fp in flag_paths:
                fp = fp.replace(".txt", "")
                if (machine.ip, fp) in env_config.flag_lookup:
                    new_m_obs.flags_found.add(env_config.flag_lookup[(machine.ip, fp)])

            # Update cost
            if env_config.action_costs.find_exists(action_id=a.id, ip=machine.ip, user=c.username,
                                                   service=constants.FTP.SERVICE_NAME):
                cost = env_config.action_costs.find_get_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                             service=constants.FTP.SERVICE_NAME)
                total_cost += cost

            # Update alerts
            if env_config.ids_router and env_config.action_alerts.user_ip_exists(action_id=a.id, ip=machine.ip,
                                                                                 user=c.username,
                                                                                 service=constants.FTP.SERVICE_NAME):
                alerts = env_config.action_alerts.user_ip_get_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                    service=constants.FTP.SERVICE_NAME)
                total_alerts = alerts

            if c.root:
                root_scan = True
                break
        return new_m_obs, total_cost, root_scan, total_alerts

    @staticmethod
    def nikto_scan_action_helper(s: EnvState, a: Action, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Helper function for executing a NIKTO web scan action on the cluster. Implements caching.

        :param s: the current env state
        :param a: the Nikto action to execute
        :param env_config: the env config
        :return: s', reward, done
        """
        cache_result = None
        cache_id = str(a.id.value) + "_" + str(a.index) + "_" + a.ip + ".xml"

        # Check in-memory cache
        if env_config.use_nikto_cache:
            cache_value = env_config.nikto_scan_cache.get(cache_id)
            if cache_value is not None:
                s_prime, reward = ClusterUtil.merge_nikto_scan_result_with_state(scan_result=cache_value, s=s, a=a,
                                                                                env_config=env_config)

                return s_prime, reward, False

        # Check On-disk cache
        if env_config.use_nmap_cache:
            cache_result = ClusterUtil.check_nmap_action_cache(a=a, env_config=env_config)

        # If cache miss, then execute cmd
        if cache_result is None:
            if env_config.ids_router:
                last_alert_ts = ClusterUtil.get_latest_alert_ts(env_config=env_config)
            outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=a.nikto_cmd(),
                                                                       conn=env_config.cluster_config.agent_conn)
            if env_config.ids_router:
                fast_logs = ClusterUtil.check_ids_fast_log(env_config=env_config)
                if last_alert_ts is not None:
                    fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                num_alerts = len(fast_logs)
                ClusterUtil.write_alerts_response(sum_priorities=sum_priority_alerts, num_alerts=num_alerts,
                                                  action=a, env_config=env_config)
                env_config.action_alerts.add_alert(action_id=a.id, ip=a.ip, alert=(sum_priority_alerts, num_alerts))

            ClusterUtil.write_estimated_cost(total_time=total_time, action=a, env_config=env_config)
            env_config.action_costs.add_cost(action_id=a.id, ip=a.ip, cost=round(total_time, 1))
            cache_result = cache_id

        # Read result
        for i in range(env_config.num_retries):
            try:
                xml_data = ClusterUtil.parse_nikto_scan(file_name=cache_result, env_config=env_config)
                scan_result = ClusterUtil.parse_nikto_scan_xml(xml_data)
                break
            except Exception as e:
                # If no webserver, Nikto outputs nothing
                scan_result = NiktoScanResult(ip=a.ip, vulnerabilities=[], port=80, sitename=a.ip)
                break

        if env_config.use_nikto_cache:
            env_config.nikto_scan_cache.add(cache_id, scan_result)
        s_prime, reward = ClusterUtil.merge_nikto_scan_result_with_state(scan_result=scan_result, s=s, a=a,
                                                                        env_config=env_config)
        return s_prime, reward, False

    @staticmethod
    def merge_nikto_scan_result_with_state(scan_result: NiktoScanResult, s: EnvState, a: Action, env_config: EnvConfig) \
            -> Tuple[EnvState, float]:
        """
        Merges a Nikto scan result with an existing observation state

        :param scan_result: the scan result
        :param s: the current state
        :param a: the action just executed
        :return: s', reward
        """
        total_new_ports, total_new_os, total_new_vuln, total_new_machines, total_new_shell_access, \
        total_new_root, total_new_flag_pts, total_new_osvdb_vuln_found, total_new_logged_in, \
        total_new_tools_installed, total_new_backdoors_installed = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        m_obs = None

        for m in s.obs_state.machines:
            if m.ip == scan_result.ip:
                m_obs = MachineObservationState(ip=m.ip)

        for vuln in scan_result.vulnerabilities:
            vuln_obs = vuln.to_obs()
            m_obs.osvdb_vulns.append(vuln_obs)

        new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
        total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, total_new_logged_in, \
        total_new_tools_installed, total_new_backdoors_installed = \
            EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, [m_obs], env_config=env_config,
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
    def parse_nikto_scan_xml(xml_data) -> NiktoScanResult:
        """
        Parses an XML Tree with Nikto Scan Result into a Nikto Scan DTO

        :param xml_data: the xml tree of Nikto Scan Result to parse
        :return: parsed nikto scan result
        """
        result = None
        for child in xml_data:
            if child.tag == constants.NIKTO_XML.SCANDETAILS:
                result = ClusterUtil._parse_nikto_scandetails(child)
            elif child.tag == constants.NIKTO_XML.ITEM:
                result = ClusterUtil._parse_nikto_scandetails(xml_data)
            elif child.tag == constants.NIKTO_XML.NIKTOSCAN:
                result = ClusterUtil.parse_nikto_scan(xml_data)
        return result

    @staticmethod
    def _parse_nikto_scandetails(xml_data) -> NiktoScanResult:
        """
        Parses a host-element in the XML tree

        :param xml_data: the host element
        :return: parsed nikto scan result
        """
        target_ip = ""
        targetport = ""
        sitename=""
        vulnerabilities = []

        if constants.NIKTO_XML.TARGETPORT in xml_data.keys():
            targetport = xml_data.attrib[constants.NIKTO_XML.TARGETPORT]
        if constants.NIKTO_XML.TARGETIP in xml_data.keys():
            target_ip = xml_data.attrib[constants. NIKTO_XML.TARGETIP]
        if constants.NIKTO_XML.SITENAME in xml_data.keys():
            sitename = xml_data.attrib[constants.NIKTO_XML.SITENAME]

        for child in list(xml_data.iter()):
            if child.tag == constants.NIKTO_XML.ITEM:
                vuln = ClusterUtil._parse_nmap_status_xml(child)
        nikto_scan_result = NiktoScanResult(vulnerabilities=vulnerabilities,
                                            port=targetport, ip=target_ip)
        return nikto_scan_result

    @staticmethod
    def _parse_nikto_item(xml_data) -> NiktoVuln:
        """
        Parses a item in the XML tree of a Nikto scan

        :param xml_data: the item element
        :return: parsed nikto vuln
        """
        id = "",
        osvdb_id = None
        method = ""
        iplink = ""
        namelink = ""
        uri = ""
        description = ""

        if constants.NIKTO_XML.METHOD in xml_data.keys():
            method = xml_data.attrib[constants.NIKTO_XML.METHOD]
        if constants.NIKTO_XML.OSVDB_ID in xml_data.keys():
            method = int(xml_data.attrib[constants.NIKTO_XML.OSVDB_ID])
        if constants.NIKTO_XML.ITEM_ID in xml_data.keys():
            id = int(xml_data.attrib[constants.NIKTO_XML.ITEM_ID])

        for child in list(xml_data.iter()):
            if child.tag == constants.NIKTO_XML.DESCR:
                description = child.text
            elif child.tag == constants.NIKTO_XML.URI:
                uri = child.text
            elif child.tag == constants.NIKTO_XML.NAMELINK:
                namelink = child.text
            elif child.tag == constants.NIKTO_XML.IPLINK:
                iplink = child.text

        nikto_vuln = NiktoVuln(id=id, osvdb_id=osvdb_id, method=method, iplink=iplink, namelink=namelink,
                               uri=uri, description=description)

        return nikto_vuln


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
                hop = ClusterUtil._parse_nmap_hop_xml(child)
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
    def parse_tools_installed_file(file_name: str, env_config: EnvConfig) -> List[str]:
        """
        Parses a file containing cached results of a install-tools action

        :param file_name: name of the file to parse
        :param env_config: environment config
        :return: a list of files
        """
        sftp_client = env_config.cluster_config.agent_conn.open_sftp()
        remote_file = sftp_client.open(env_config.nmap_cache_dir + file_name)
        installed = False
        try:
            data = remote_file.read()
            data = data.decode()
            installed = bool(int(data))
        finally:
            remote_file.close()
        return installed

    @staticmethod
    def _parse_tools_installed_check_result(result: str) -> bool:
        """
        Checks the output result of a tools install action to see whether the action was successful or not.

        :param result: the result to check
        :return: True if sucessful otherwise False
        """
        return ("will be installed" in result or "already installed" in result or "already the newest version" in result)

    @staticmethod
    def install_tools_helper(s: EnvState, a: Action, env_config: EnvConfig) -> bool:
        """
        Uses compromised machines with root access to install tools

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        new_machines_obs = []
        total_cost = 0
        total_alerts = (0,0)
        for machine in s.obs_state.machines:
            new_m_obs = MachineObservationState(ip=machine.ip)
            installed = False
            if machine.logged_in and machine.root and not machine.tools_installed:
                # Start with ssh connections
                ssh_root_connections = filter(lambda x: x.root, machine.ssh_connections)
                ssh_root_connections = sorted(ssh_root_connections, key=lambda x: x.username)
                ssh_cost = 0
                for c in ssh_root_connections:
                    key = (machine.ip, c.username)
                    if env_config.use_user_command_cache and env_config.user_command_cache.get(key) is not None:
                        cache_m_obs, cost = env_config.user_command_cache.get(key)
                        new_m_obs.tools_installed = cache_m_obs.tools_installed
                        new_machines_obs.append(new_m_obs)
                        total_cost += cost
                        if new_m_obs.tools_installed:
                            break
                        else:
                            continue

                    cache_file = \
                        ClusterUtil.check_user_action_cache(a=a, env_config=env_config, ip=machine.ip,
                                                            user=c.username)
                    if cache_file is not None:
                        installed = ClusterUtil.parse_tools_installed_file(file_name=cache_file,
                                                                           env_config=env_config)
                        new_m_obs.tools_installed = installed
                    else:
                        cmd = a.cmd[0]
                        if env_config.ids_router:
                            last_alert_ts = ClusterUtil.get_latest_alert_ts(env_config=env_config)
                        for i in range(env_config.retry_install_tools):
                            outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
                            outdata = outdata.decode()
                            ssh_cost += float(total_time)
                            if ClusterUtil._parse_tools_installed_check_result(result=outdata):
                                installed = True
                                new_m_obs.tools_installed = True
                            else:
                                print("tools installed failed result. out:{}, err:{}".format(outdata, errdata))
                            if installed:
                                break

                        # try to download seclists
                        seclists_installed = ClusterUtil._check_if_seclists_is_installed(conn=c.conn, telnet=False)
                        if not seclists_installed:
                            cmd = a.cmd[1]
                            outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
                            ssh_cost += float(total_time)

                        if env_config.ids_router:
                            fast_logs = ClusterUtil.check_ids_fast_log(env_config=env_config)
                            if last_alert_ts is not None:
                                fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                            sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                            num_alerts = len(fast_logs)
                            ssh_alerts = (sum_priority_alerts, num_alerts)
                            ClusterUtil.write_alerts_response(sum_priorities=sum_priority_alerts, num_alerts=num_alerts,
                                                              action=a, env_config=env_config, ip=machine.ip,
                                                              user=c.username)
                            env_config.action_alerts.user_ip_add_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                       service=constants.SSH.SERVICE_NAME,
                                                                       alert=ssh_alerts)
                            total_alerts = (total_alerts[0] + ssh_alerts[0], total_alerts[1]+ ssh_alerts[1])
                        ClusterUtil.write_estimated_cost(total_time=total_time, action=a,
                                                         env_config=env_config, ip=machine.ip,
                                                         user=c.username)
                        env_config.action_costs.install_add_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                                 cost=float(total_time))
                        # Persist cache
                        ClusterUtil.write_user_command_cache(action=a, env_config=env_config, user=c.username,
                                                             result=str(int(installed)), ip=machine.ip)

                    new_machines_obs.append(new_m_obs)
                    # Update cache
                    if env_config.use_user_command_cache:
                        env_config.user_command_cache.add(key, (new_m_obs, total_cost))

                    if installed:
                        break

                total_cost += ssh_cost

                # Telnet connections
                telnet_cost = 0
                if installed:
                    continue
                telnet_root_connections = filter(lambda x: x.root, machine.telnet_connections)
                telnet_root_connections = sorted(telnet_root_connections, key=lambda x: x.username)
                for c in telnet_root_connections:
                    key = (machine.ip, c.username)
                    if env_config.use_user_command_cache and env_config.user_command_cache.get(key) is not None:
                        cache_m_obs, cost = env_config.user_command_cache.get(key)
                        new_m_obs.tools_installed = cache_m_obs.tools_installed
                        new_machines_obs.append(new_m_obs)
                        total_cost += cost
                        if new_m_obs.tools_installed:
                            break
                        else:
                            continue

                    cache_file = \
                        ClusterUtil.check_user_action_cache(a=a, env_config=env_config, ip=machine.ip,
                                                            user=c.username)
                    if cache_file is not None:
                        installed = ClusterUtil.parse_tools_installed_file(file_name=cache_file,
                                                                           env_config=env_config)
                        new_m_obs.tools_installed = installed
                    else:

                        # Install packages
                        cmd = a.cmd[0] + "\n"
                        start = time.time()
                        if env_config.ids_router:
                            last_alert_ts = ClusterUtil.get_latest_alert_ts(env_config=env_config)
                        for i in range(env_config.retry_install_tools):
                            c.conn.write(cmd.encode())
                            response = c.conn.read_until(constants.TELNET.PROMPT, timeout=25)
                            response = response.decode()
                            end = time.time()
                            total_time = end - start
                            telnet_cost += float(total_time)
                            if ClusterUtil._parse_tools_installed_check_result(result=response):
                                installed = True
                                new_m_obs.tools_installed = True
                            else:
                                print("tools installed failed result.{}".format(response))
                            if installed:
                                break

                        seclists_installed = ClusterUtil._check_if_seclists_is_installed(conn=c.conn, telnet=True)
                        if not seclists_installed:
                            # Try to download SecLists
                            cmd = a.cmd[1] + "\n"
                            start = time.time()
                            c.conn.write(cmd.encode())
                            response = c.conn.read_until(constants.TELNET.PROMPT, timeout=2000)
                            response = response.decode()
                            end = time.time()
                            total_time = end - start
                            telnet_cost += float(total_time)

                        if env_config.ids_router:
                            fast_logs = ClusterUtil.check_ids_fast_log(env_config=env_config)
                            if last_alert_ts is not None:
                                fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                            sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                            num_alerts = len(fast_logs)
                            telnet_alerts = (sum_priority_alerts, num_alerts)
                            ClusterUtil.write_alerts_response(sum_priorities=sum_priority_alerts, num_alerts=num_alerts,
                                                              action=a, env_config=env_config, ip=machine.ip,
                                                              user=c.username, service=constants.TELNET.SERVICE_NAME)
                            env_config.action_alerts.user_ip_add_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                       service=constants.TELNET.SERVICE_NAME,
                                                                       alert=telnet_alerts)
                            total_alerts = (total_alerts[0] + telnet_alerts[0], total_alerts[1] + telnet_alerts[1])

                        ClusterUtil.write_estimated_cost(total_time=total_time, action=a,
                                                         env_config=env_config, ip=machine.ip,
                                                         user=c.username)
                        env_config.action_costs.install_add_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                                 cost=float(total_time))
                        # Persist cache
                        ClusterUtil.write_user_command_cache(action=a, env_config=env_config, user=c.username,
                                                             result=str(int(installed)), ip=machine.ip)

                    new_machines_obs.append(new_m_obs)

                    # Update cache
                    if env_config.use_user_command_cache:
                        env_config.user_command_cache.add(key, (new_m_obs, total_cost))

                    if installed:
                        break

                new_m_obs.install_tools_tried = True

                total_cost += telnet_cost
        new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
        total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, total_new_logged_in, \
        total_new_tools_installed, total_new_backdoors_installed = \
            EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, new_machines_obs, env_config=env_config,
                                                   action=a)
        s_prime = s
        s_prime.obs_state.machines = new_machines_obs

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
                                                 cost=total_cost,
                                                 env_config=env_config,
                                                 alerts=total_alerts, action=a)
        return s, reward, False

    @staticmethod
    def merge_nmap_scan_results(scan_result_1: NmapScanResult, scan_result_2: NmapScanResult)-> NmapScanResult:
        new_hosts = []

        for h in scan_result_2.hosts:
            new_host = True
            for h2 in scan_result_1. hosts:
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
                s_prime, reward = ClusterUtil.merge_nmap_scan_result_with_state(scan_result=merged_result, s=s, a=a,
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
                        machine = EnvDynamicsUtil.brute_tried_flags(a=a, m_obs=machine)
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
                ssh_connections_sorted_by_root = sorted(machine.ssh_connections, key=lambda x: ("ssh_backdoor" in x.username, x.root, x.username), reverse=True)
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
                        cache_result = ClusterUtil.check_nmap_action_cache(a=a, env_config=env_config, conn=c.conn,
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
                                                              conn=c.conn, dir=cwd, machine_ip = machine.ip)
                            env_config.action_alerts.pivot_scan_add_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                        target_ip=machine.ip, alert=(sum_priority_alerts, num_alerts))
                        ClusterUtil.write_estimated_cost(total_time=total_time, action=a, env_config=env_config,
                                                         conn=c.conn, dir=cwd, machine_ip=machine.ip)
                        env_config.action_costs.pivot_scan_add_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                                    target_ip=machine.ip, cost=round(total_time, 1))

                        cache_result = cache_filename

                    # Read result
                    for i in range(env_config.num_retries):
                        try:
                            xml_data = ClusterUtil.parse_nmap_scan(file_name=cache_result, env_config=env_config,
                                                                   conn=c.conn, dir=cwd)
                            scan_result = ClusterUtil.parse_nmap_scan_xml(xml_data, ip=machine.ip, action=a)
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
                    merged_scan_result = ClusterUtil.merge_nmap_scan_results(scan_result_1=merged_scan_result,
                                                                             scan_result_2=scan_result.copy())
                elif merged_scan_result is None:
                    total_results.append(scan_result)
                    merged_scan_result = scan_result.copy()

        if env_config.use_nmap_cache:
            env_config.nmap_scan_cache.add(base_cache_id, (merged_scan_result, total_results))
        a.cost = a.cost + total_cost
        s_prime, reward = ClusterUtil.merge_nmap_scan_result_with_state(scan_result=merged_scan_result, s=s, a=a,
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
                machine = EnvDynamicsUtil.brute_tried_flags(a=a, m_obs=machine)
            new_machines_obs_1.append(machine)
        s_prime.obs_state.machines = new_machines_obs_1

        return s_prime, reward, False

    @staticmethod
    def _check_if_ssh_server_is_running(conn, telnet: bool = False) -> bool:
        """
        Checks if an ssh server is running on the machine

        :param conn: the connection to use for the command
        :param telnet: whether the connection is a telnet connection
        :return: True if server is running, else false
        """
        cmd= "service ssh status"
        if not telnet:
            outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=conn)
            return "is running" in outdata.decode() or "is running" in errdata.decode()
        else:
            cmd = cmd + "\n"
            conn.write(cmd.encode())
            response = conn.read_until(constants.TELNET.PROMPT, timeout=5)
            return "is running" in response.decode()

    @staticmethod
    def _list_all_users(c: ConnectionObservationState, env_config: EnvConfig, telnet : bool = False) \
            -> List:
        """
        List all users on a machine

        :param c: the connection to user for the command
        :param telnet: whether it is a telnet connection
        :param env_config: env config
        :return: list of users
        """
        cache_id = ("list_users", c.ip, c.root)
        cache_file_name = "list_users_" + c.ip + "_" + str(c.root)

        # check in-memory cache
        if env_config.filesystem_scan_cache.get(cache_id) is not None:
            return env_config.filesystem_scan_cache.get(cache_id)

        if not telnet:
            # check file cache
            sftp_client = c.conn.open_sftp()
            cwd = "/home/" + c.username + "/"
            remote_file = None
            try:
                remote_file = sftp_client.open(cwd + cache_file_name, mode="r")
                users = []
                data = remote_file.read()
                data = data.decode()
                users = data.split("\n")
                users = list(filter(lambda x: x != '', users))
                if len(users) > 0:
                    # cache result
                    env_config.filesystem_scan_cache.add(cache_id, users)
                    return users
            except Exception as e:
                pass
            finally:
                if remote_file is not None:
                    remote_file.close()

        cmd = constants.SHELL.LIST_ALL_USERS
        for i in range(env_config.retry_find_users):
            if not telnet:
                outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
                outdata = outdata.decode()
                errdata = errdata.decode()
                users = outdata.split("\n")
                users = list(filter(lambda x: x != '', users))
            else:
                cmd = cmd + "\n"
                c.conn.write(cmd.encode())
                response = c.conn.read_until(constants.TELNET.PROMPT, timeout=5)
                response = response.decode()
                users = response.split("\n")
                users = list(map(lambda x: x.replace("\r", ""), users))
                users = list(filter(lambda x: x != '', users))
            if len(users) == 0:
                continue
            else:
                break
        if len(users) == 0:
            raise ValueError("users empty, ip:{}, telnet:{}, root:{}, username:{}".format(c.ip, telnet, c.root,
                                                                                          c.username))

        backdoor_exists = False
        for user in users:
            if constants.SSH_BACKDOOR.BACKDOOR_PREFIX in user:
                backdoor_exists = True

        if backdoor_exists:
            # cache result in-memory
            env_config.filesystem_scan_cache.add(cache_id, users)

        if not telnet and backdoor_exists:
            # cache result on-disk
            sftp_client = c.conn.open_sftp()
            remote_file = None
            try:
                remote_file = sftp_client.file(cwd + cache_file_name, mode="a")
                for user in users:
                    remote_file.write(user + "\n")
            except Exception as e:
                print("Error writing list of users cache: {}, file:{}, ip:{}".format(str(e), cwd + cache_file_name, c.ip))
            finally:
                if remote_file is not None:
                    remote_file.close()
        return users

    @staticmethod
    def execute_ssh_backdoor_helper(s: EnvState, a: Action, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Uses compromised machines with root access to setup SSH backdoor

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        username = constants.SSH_BACKDOOR.BACKDOOR_PREFIX + "_" + str(random.randint(0, 100000))
        pw = constants.SSH_BACKDOOR.DEFAULT_PW
        new_machines_obs = []
        total_cost = 0
        total_alerts = (0,0)
        for machine in s.obs_state.machines:
            new_m_obs = MachineObservationState(ip=machine.ip)
            backdoor_created = False
            if machine.logged_in and machine.root and machine.tools_installed and not machine.backdoor_installed:
                new_m_obs.backdoor_tried = True
                # Check cached connections
                for cr in s.cached_backdoor_credentials.values():
                    if (machine.ip, cr.username, cr.port) in s.cached_ssh_connections:
                        conn_dto = s.cached_ssh_connections[(machine.ip, cr.username, cr.port)]
                        connection_dto = ConnectionObservationState(conn=conn_dto.conn, username=cr.username,
                                                                    root=machine.root,
                                                                    service=constants.SSH.SERVICE_NAME,
                                                                    port=cr.port, ip=machine.ip)
                        new_m_obs.shell_access_credentials.append(cr)
                        new_m_obs.backdoor_credentials.append(cr)
                        new_m_obs.ssh_connections.append(connection_dto)
                        new_m_obs.backdoor_installed = True
                        new_machines_obs.append(new_m_obs)
                        backdoor_created = True

                if backdoor_created:
                    continue

                # Try first to setup new ssh connections
                ssh_root_connections = list(filter(lambda x: x.root, machine.ssh_connections))
                ssh_root_connections = sorted(ssh_root_connections, key=lambda x: x.username)
                ssh_cost = 0
                for c in ssh_root_connections:
                    try:
                        users = ClusterUtil._list_all_users(c, env_config=env_config)
                        users = sorted(users, key=lambda x: x)
                        user_exists = False
                        for user in users:
                            if constants.SSH_BACKDOOR.BACKDOOR_PREFIX in user:
                                user_exists = True
                                username = user

                        if not user_exists:
                            # Create user
                            create_user_cmd = a.cmd[1].format(username, pw, username)
                            outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=create_user_cmd, conn=c.conn)
                            ssh_cost += float(total_time)

                        credential = Credential(username=username, pw=pw, port=22, service="ssh")

                        # Start SSH Server
                        ssh_running = ClusterUtil._check_if_ssh_server_is_running(c.conn)
                        if not ssh_running:
                            start_ssh_cmd = a.cmd[0]
                            outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=start_ssh_cmd, conn=c.conn)
                            ssh_cost += float(total_time)

                        # Create SSH connection
                        new_m_obs.shell_access_credentials.append(credential)
                        new_m_obs.backdoor_credentials.append(credential)
                        a.ip = machine.ip
                        connected, users, target_connections, ports, total_time, non_failed_credentials, proxies = \
                            ClusterUtil._ssh_setup_connection(a=a, env_config=env_config, credentials=[credential],
                                                              proxy_connections=[c.proxy], s=s)
                        ssh_cost += total_time

                        connection_dto = ConnectionObservationState(conn=target_connections[0],
                                                                    username=credential.username,
                                                                    root=machine.root,
                                                                    service=constants.SSH.SERVICE_NAME,
                                                                    port=credential.port,
                                                                    proxy=proxies[0], ip=machine.ip)
                        new_m_obs.ssh_connections.append(connection_dto)
                        new_m_obs.backdoor_installed = True
                        new_machines_obs.append(new_m_obs)
                        backdoor_created = True
                    except Exception as e:
                        pass
                        # raise ValueError("Creating Backdoor Exception: {}, target:{}, proxy:{}".format(str(e), a.ip,
                        #                                                                                c.proxy.ip))

                    if backdoor_created:
                        break

                total_cost += ssh_cost

                # Telnet connections
                telnet_cost = 0
                if backdoor_created:
                    continue
                telnet_root_connections = filter(lambda x: x.root, machine.telnet_connections)
                telnet_root_connections = sorted(telnet_root_connections, key=lambda x: x.username)
                for c in telnet_root_connections:
                    try:
                        users = ClusterUtil._list_all_users(c, env_config=env_config, telnet=True)
                        user_exists = False
                        for user in users:
                            if constants.SSH_BACKDOOR.BACKDOOR_PREFIX in user:
                                user_exists = True
                                username = user

                        credential = Credential(username=username, pw=pw, port=22, service="ssh")

                        if not user_exists:
                            # Create user
                            create_user_cmd = a.cmd[1].format(username, pw, username) + "\n"
                            c.conn.write(create_user_cmd.encode())
                            response = c.conn.read_until(constants.TELNET.PROMPT, timeout=5)

                        ssh_running = ClusterUtil._check_if_ssh_server_is_running(c.conn, telnet=True)
                        if not ssh_running:
                            # Start SSH Server
                            start_ssh_cmd = a.cmd[0] + "\n"
                            c.conn.write(start_ssh_cmd.encode())
                            response = c.conn.read_until(constants.TELNET.PROMPT, timeout=5)

                        # Create SSH connection
                        new_m_obs.shell_access_credentials.append(credential)
                        new_m_obs.backdoor_credentials.append(credential)
                        a.ip = machine.ip
                        connected, users, target_connections, ports, total_time, non_failed_credentials, proxies = \
                            ClusterUtil._ssh_setup_connection(a=a, env_config=env_config, credentials=[credential],
                                                              proxy_connections=[c.proxy], s=s)
                        telnet_cost += total_time
                        connection_dto = ConnectionObservationState(conn=target_connections[0],
                                                                    username=credential.username,
                                                                    root=machine.root,
                                                                    service=constants.SSH.SERVICE_NAME,
                                                                    port=credential.port,
                                                                    proxy=proxies[0], ip=machine.ip)
                        new_m_obs.ssh_connections.append(connection_dto)
                        new_m_obs.backdoor_installed = True
                        new_machines_obs.append(new_m_obs)
                        backdoor_created = True
                    except Exception as e:
                        pass
                        # raise ValueError("Creating Backdoor Exception: {}, target:{}, proxy:{}".format(str(e), a.ip,
                        #                                                                                c.proxy.ip))
                    if backdoor_created:
                        break

                total_cost += telnet_cost
        # if not backdoor_created:
        #     print("failed to create backdoor, target:{}".format(a.ip))
        new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
        total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, total_new_logged_in, \
        total_new_tools_installed, total_new_backdoors_installed = \
            EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, new_machines_obs, env_config=env_config,
                                                   action=a)
        s_prime = s
        s_prime.obs_state.machines = new_machines_obs

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
                                                 cost=total_cost,
                                                 env_config=env_config,
                                                 alerts=total_alerts, action=a)
        return s, reward, False

    @staticmethod
    def _check_if_seclists_is_installed(conn, telnet: bool = False) -> bool:
        """
        Checks if seclists are downloaded

        :param conn: the connection to use for the command
        :param telnet: whether the connection is a telnet connection
        :return: True if downloaded, else false
        """
        cmd = constants.SHELL.CHECK_FOR_SECLISTS
        if not telnet:
            for i in range(8):
                outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=conn)
                checklists_installed = "file exists" in outdata.decode() or "file exists" in errdata.decode()
                if checklists_installed:
                    break
                else:
                    print("checklists not installed:{}, {}".format(outdata.decode(), errdata.decode()))
            return checklists_installed
        else:
            cmd = cmd + "\n"
            conn.write(cmd.encode())
            response = conn.read_until(constants.TELNET.PROMPT, timeout=5)
            return "file exists" in response.decode()

    @staticmethod
    def execute_service_login_helper(s: EnvState, a: Action, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Executes a service login on the cluster using previously found credentials

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        total_cost = 0
        total_new_ports = 0
        total_new_os = 0
        total_new_cve_vuln = 0
        total_new_machines = 0
        total_new_shell_access = 0
        total_new_flag_pts = 0
        total_new_root = 0
        total_new_osvdb_vuln = 0
        total_new_logins = 0
        total_new_tools_installed = 0
        total_new_backdoors_installed = 0
        s_prime = s
        new_conn = False

        if env_config.ids_router:
            last_alert_ts = ClusterUtil.get_latest_alert_ts(env_config=env_config)

        for machine in s.obs_state.machines:
            a.ip = machine.ip
            s_1, t_n_p_1, t_n_os_1, t_n_v_1, t_n_m_1, \
            t_n_s_a_1, t_n_f_p_1, t_n_r_1, t_n_o_v_1, t_n_l_i_1, t_n_t_i_1, t_n_b_i_1, ssh_cost, \
            new_conn_ssh = ClusterUtil.login_service_helper(
                s=s_prime, a=a, alive_check=EnvDynamicsUtil.check_if_ssh_connection_is_alive,
                service_name=constants.SSH.SERVICE_NAME, env_config=env_config)
            s_2, t_n_p_2, t_n_os_2, t_n_v_2, t_n_m_2, \
            t_n_s_a_2, t_n_f_p_2, t_n_r_2, t_n_o_v_2, t_n_l_i_2, t_n_t_i_2, t_n_b_i_2, ftp_cost, \
            new_conn_ftp = ClusterUtil.login_service_helper(
                s=s_1, a=a, alive_check=EnvDynamicsUtil.check_if_ftp_connection_is_alive,
                service_name=constants.FTP.SERVICE_NAME, env_config=env_config)
            s_3, t_n_p_3, t_n_os_3, t_n_v_3, t_n_m_3, \
            t_n_s_a_3, t_n_f_p_3, t_n_r_3, t_n_o_v_3, t_n_l_i_3, t_n_t_i_3, t_n_b_i_3, telnet_cost, \
            new_conn_telnet = ClusterUtil.login_service_helper(
                s=s_2, a=a, alive_check=EnvDynamicsUtil.check_if_telnet_connection_is_alive,
                service_name=constants.TELNET.SERVICE_NAME, env_config=env_config)
            total_cost = total_cost + ssh_cost + ftp_cost + telnet_cost
            total_new_ports = total_new_ports + t_n_p_1 + t_n_p_2 + t_n_p_3
            total_new_os = total_new_os + t_n_os_1 + t_n_os_2 + t_n_os_3
            total_new_cve_vuln = total_new_cve_vuln + t_n_v_1 + t_n_v_2 + t_n_v_3
            total_new_machines = total_new_machines + t_n_m_1 + t_n_m_2 + t_n_m_3
            total_new_shell_access = total_new_shell_access + t_n_s_a_1 + t_n_s_a_2 + t_n_s_a_3
            total_new_flag_pts = total_new_flag_pts + t_n_f_p_1 + t_n_f_p_2 + t_n_f_p_3
            total_new_root = total_new_root + t_n_r_1 + t_n_r_2 + t_n_r_3
            total_new_osvdb_vuln = total_new_osvdb_vuln + t_n_o_v_1 + t_n_o_v_2 + t_n_o_v_3
            total_new_logins = total_new_logins + t_n_l_i_1 + t_n_l_i_2 + t_n_l_i_3
            total_new_tools_installed = total_new_tools_installed + t_n_t_i_1 + t_n_t_i_2 + t_n_t_i_3
            total_new_backdoors_installed = total_new_backdoors_installed + t_n_b_i_1 + t_n_b_i_2 + t_n_b_i_3

            s_prime = s_3
            if new_conn_ssh or new_conn_ftp or new_conn_telnet:
                new_conn = True

            for m in s_prime.obs_state.machines:
                if m.ip == a.ip:
                    m.untried_credentials = False

        # Update cost cache
        total_cost = round(total_cost, 1)
        if new_conn:
            env_config.action_costs.service_add_cost(action_id=a.id, ip=env_config.cluster_config.agent_ip,
                                                     cost=float(total_cost))

        # Update alerts cache
        if env_config.ids_router and new_conn:
            fast_logs = ClusterUtil.check_ids_fast_log(env_config=env_config)
            if last_alert_ts is not None:
                fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
            sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
            num_alerts = len(fast_logs)
            env_config.action_alerts.add_alert(action_id=a.id, ip=env_config.cluster_config.agent_ip,
                                                       alert=(sum_priority_alerts, num_alerts))

        a.ip = ""

        # Use measured cost
        if env_config.action_costs.service_exists(action_id=a.id, ip=env_config.cluster_config.agent_ip):
            a.cost = env_config.action_costs.service_get_cost(action_id=a.id, ip=env_config.cluster_config.agent_ip)

        # Use measured alerts
        if env_config.action_alerts.exists(action_id=a.id, ip=env_config.cluster_config.agent_ip):
            a.alerts = env_config.action_alerts.get_alert(action_id=a.id, ip=env_config.cluster_config.agent_ip)

        reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports, num_new_os_found=total_new_os,
                                                 num_new_cve_vuln_found=total_new_cve_vuln,
                                                 num_new_machines=total_new_machines,
                                                 num_new_shell_access=total_new_shell_access,
                                                 num_new_root=total_new_root,
                                                 num_new_flag_pts=total_new_flag_pts,
                                                 num_new_osvdb_vuln_found=total_new_osvdb_vuln,
                                                 num_new_logged_in=total_new_logins,
                                                 num_new_tools_installed=total_new_tools_installed,
                                                 num_new_backdoors_installed=total_new_backdoors_installed,
                                                 cost=a.cost,
                                                 env_config=env_config,
                                                 alerts=a.alerts, action=a)
        return s_prime, reward, False

    @staticmethod
    def get_latest_alert_ts(env_config: EnvConfig):
        if not env_config.ids_router:
            raise AssertionError("Can only read alert files if IDS router is enabled")
        stdin, stdout, stderr = env_config.cluster_config.router_conn.exec_command(
            constants.IDS_ROUTER.TAIL_ALERTS_LATEST_COMMAND + " " + constants.IDS_ROUTER.ALERTS_FILE)
        alerts = []
        for line in stdout:
            a_str = line.replace("\n", "")
            alerts.append(IdsAlert.parse_from_str(a_str))
        if len(alerts) == 0:
            # retry once
            stdin, stdout, stderr = env_config.cluster_config.router_conn.exec_command(
                constants.IDS_ROUTER.TAIL_ALERTS_LATEST_COMMAND + " " + constants.IDS_ROUTER.ALERTS_FILE)
            alerts = []
            for line in stdout:
                a_str = line.replace("\n", "")
                alerts.append(IdsAlert.parse_from_str(a_str))
            if len(alerts) == 0:
                return None
            else:
                return alerts[0].timestamp
        else:
            return alerts[0].timestamp

    @staticmethod
    def check_ids_alerts(env_config: EnvConfig) -> List[IdsAlert]:
        if not env_config.ids_router:
            raise AssertionError("Can only read alert files if IDS router is enabled")
        stdin, stdout, stderr = env_config.cluster_config.router_conn.exec_command(
            constants.IDS_ROUTER.TAIL_ALERTS_COMMAND + " " + constants.IDS_ROUTER.ALERTS_FILE)
        alerts = []
        for line in stdout:
            a_str = line.replace("\n", "")
            alerts.append(IdsAlert.parse_from_str(a_str))
        return alerts

    @staticmethod
    def check_ids_fast_log(env_config: EnvConfig) -> List[IdsAlert]:
        if not env_config.ids_router:
            raise AssertionError("Can only read alert files if IDS router is enabled")
        stdin, stdout, stderr = env_config.cluster_config.router_conn.exec_command(
            constants.IDS_ROUTER.TAIL_FAST_LOG_COMMAND + " " + constants.IDS_ROUTER.FAST_LOG_FILE)
        fast_logs = []
        for line in stdout:
            a_str = line.replace("\n", "")
            priority, ts = IdsAlert.fast_log_parse(a_str)
            fast_logs.append((priority, ts))
        return fast_logs