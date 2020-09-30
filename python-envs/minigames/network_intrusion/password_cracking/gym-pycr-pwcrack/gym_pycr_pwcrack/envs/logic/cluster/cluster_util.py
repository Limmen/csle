from typing import Union, List
import time
from xml.etree.ElementTree import fromstring
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action_results.nmap_scan_result import NmapScanResult
from gym_pycr_pwcrack.dao.action_results.nmap_host import NmapHostResult
from gym_pycr_pwcrack.dao.action_results.nmap_port_status import NmapPortStatus
from gym_pycr_pwcrack.dao.action_results.nmap_port import NmapPort
from gym_pycr_pwcrack.dao.action_results.nmap_addr_type import NmapAddrType
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.envs.logic.common.env_dynamics_util import EnvDynamicsUtil

class ClusterUtil:
    """
    Class containing utility functions for the cluster-middleware
    """


    @staticmethod
    def execute_cmd(a : Action, env_config : EnvConfig):
        env_config.cluster_config.agent_channel.send(a.cmd[0] + "\n")

    @staticmethod
    def read_result(env_config : EnvConfig) -> str:
        while not env_config.cluster_config.agent_channel.recv_ready():
            time.sleep(env_config.shell_read_wait)
        output = env_config.cluster_config.agent_channel.recv(5000)
        output_str = output.decode("utf-8")
        output_str = env_config.shell_escape.sub("", output_str)
        return output_str


    @staticmethod
    def check_nmap_action_cache(a : Action, env_config : EnvConfig):

        # Clear channel
        if env_config.cluster_config.agent_channel.recv_ready():
            output = env_config.cluster_config.agent_channel.recv(5000)

        # List cache
        env_config.cluster_config.agent_channel.send("ls -1 " + env_config.nmap_cache_dir + "\n")
        result_str = ClusterUtil.read_result(env_config=env_config)
        cache_list = result_str.split('\r\n')
        cache_list = cache_list[1:-1]  # remove command ([0]) and prompt ([-1])

        # Search through cache
        query = str(a.id.value) + "_" + a.ip + ".xml"
        if a.subnet:
            query = str(a.id.value) + ".xml"
        for item in cache_list:
            if item == query:
                return item

        return None

    @staticmethod
    def parse_nmap_scan(file_name : str, env_config : EnvConfig):
        print("parsing file:{}".format(file_name))
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
        hosts = []
        for child in xml_data:
            if child.tag == "host":
                host = ClusterUtil._parse_nmap_host_xml(child)
                hosts.append(host)
        result = NmapScanResult(hosts=hosts)
        return result


    @staticmethod
    def _parse_nmap_host_xml(xml_data) -> NmapHostResult:
        ip_addr = None
        mac_addr = None
        hostnames = []
        ports = []
        for child in list(xml_data.iter()):
            if child.tag == "status":
                status = ClusterUtil._parse_nmap_status_xml(child)
            elif child.tag == "address":
                addr, type = ClusterUtil._parse_nmap_address_xml(child)
                if type == NmapAddrType.MAC:
                    mac_addr = addr
                else:
                    ip_addr = addr
            elif child.tag == "hostnames":
                hostnames = ClusterUtil._parse_nmap_hostnames_xml(child)
            elif child.tag == "ports":
                ports = ClusterUtil._parse_nmap_ports_xml(child)
        nmap_host_result = NmapHostResult(status=status, ip_addr=ip_addr, mac_addr=mac_addr,
                                          hostnames=hostnames, ports=ports)
        return nmap_host_result


    @staticmethod
    def _parse_nmap_status_xml(xml_data) -> NmapPortStatus:
        status = NmapPortStatus.DOWN
        status_val = xml_data.attrib["state"]
        if status_val == "up":
            status = NmapPortStatus.UP
        return status

    @staticmethod
    def _parse_nmap_address_xml(xml_data) -> Union[str, NmapAddrType]:
        type = NmapAddrType.IP
        addr = xml_data.attrib["addr"]
        addrtype_val = xml_data.attrib["addrtype"]
        if "ip" in addrtype_val:
            type = NmapAddrType.IP
        elif "mac" in addrtype_val:
            type = NmapAddrType.MAC
        return addr, type


    @staticmethod
    def _parse_nmap_hostnames_xml(xml_data) -> List[str]:
        hostnames = []
        for child in list(xml_data.iter()):
            if child.tag == "hostname":
                hostnames.append(child.attrib["name"])
        return hostnames

    @staticmethod
    def _parse_nmap_ports_xml(xml_data) -> List[NmapPort]:
        ports = []
        for child in list(xml_data.iter()):
            if child.tag == "port":
                port_status = NmapPortStatus.DOWN
                protocol = TransportProtocol._from_str(child.attrib["protocol"])
                port_id = child.attrib["portid"]
                service_name = "none"
                for child_2 in list(child.iter()):
                    if child_2.tag == "state":
                        port_status = ClusterUtil._parse_nmap_port_status_xml(child_2)
                    elif child_2.tag == "service":
                        service_name = ClusterUtil._parse_nmap_service_name_xml(child_2)
                port = NmapPort(port_id=port_id, protocol=protocol, status=port_status, service_name=service_name)
                ports.append(port)
        return ports


    @staticmethod
    def _parse_nmap_service_name_xml(xml_data) -> str:
        return xml_data.attrib["name"]

    @staticmethod
    def _parse_nmap_port_status_xml(xml_data) -> NmapPortStatus:
        port_status = NmapPortStatus.DOWN
        if xml_data.attrib["state"] == "open":
            port_status = NmapPortStatus.UP
        return port_status

    @staticmethod
    def merge_scan_result_with_state(scan_result : NmapScanResult, s: EnvState,
                                     a: Action):
        total_new_ports, total_new_os, total_new_vuln, total_new_machines, total_new_shell_access, \
        total_new_root, total_new_flag_pts = 0, 0, 0, 0, 0, 0, 0
        new_m_obs = []

        for host in scan_result.hosts:
            m_obs = host.to_obs()
            new_m_obs.append(m_obs)

        new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
        total_new_shell_access, total_new_flag_pts = \
            EnvDynamicsUtil.merge_new_obs_with_old(s.obs_state.machines, new_m_obs)
        s_prime = s
        s_prime.obs_state.machines = new_machines_obs

        reward = EnvDynamicsUtil.reward_function(num_new_ports_found=total_new_ports, num_new_os_found=total_new_os,
                                                 num_new_vuln_found=total_new_vuln,
                                                 num_new_machines=total_new_machines,
                                                 num_new_shell_access=total_new_shell_access,
                                                 num_new_root=total_new_root,
                                                 num_new_flag_pts=total_new_flag_pts,
                                                 cost=a.cost)
        return s_prime, reward