from typing import Tuple
import xml.etree.ElementTree as ET
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.action import Action
from gym_pycr_ctf.dao.action_results.nikto_scan_result import NiktoScanResult
from gym_pycr_ctf.dao.action_results.nikto_vuln import NiktoVuln
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.envs.logic.common.env_dynamics_util import EnvDynamicsUtil
import gym_pycr_ctf.constants.constants as constants
from gym_pycr_ctf.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_ctf.envs.logic.cluster.util.cluster_util import ClusterUtil
from gym_pycr_ctf.envs.logic.cluster.util.nmap_util import NmapUtil

class NiktoUtil:
    """
    Class containing utility functions for the nikto-related functionality to the Cluster
    """

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
                s_prime, reward = NiktoUtil.merge_nikto_scan_result_with_state(scan_result=cache_value, s=s, a=a,
                                                                                 env_config=env_config)

                return s_prime, reward, False

        # Check On-disk cache
        if env_config.use_nmap_cache:
            cache_result = NmapUtil.check_nmap_action_cache(a=a, env_config=env_config)

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
                xml_data = NiktoUtil.parse_nikto_scan(file_name=cache_result, env_config=env_config)
                scan_result = NiktoUtil.parse_nikto_scan_xml(xml_data)
                break
            except Exception as e:
                # If no webserver, Nikto outputs nothing
                scan_result = NiktoScanResult(ip=a.ip, vulnerabilities=[], port=80, sitename=a.ip)
                break

        if env_config.use_nikto_cache:
            env_config.nikto_scan_cache.add(cache_id, scan_result)
        s_prime, reward = NiktoUtil.merge_nikto_scan_result_with_state(scan_result=scan_result, s=s, a=a,
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
                result = NiktoUtil._parse_nikto_scandetails(child)
            elif child.tag == constants.NIKTO_XML.ITEM:
                result = NiktoUtil._parse_nikto_scandetails(xml_data)
            elif child.tag == constants.NIKTO_XML.NIKTOSCAN:
                result = NiktoUtil.parse_nikto_scan(xml_data)
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
        sitename = ""
        vulnerabilities = []

        if constants.NIKTO_XML.TARGETPORT in xml_data.keys():
            targetport = xml_data.attrib[constants.NIKTO_XML.TARGETPORT]
        if constants.NIKTO_XML.TARGETIP in xml_data.keys():
            target_ip = xml_data.attrib[constants.NIKTO_XML.TARGETIP]
        if constants.NIKTO_XML.SITENAME in xml_data.keys():
            sitename = xml_data.attrib[constants.NIKTO_XML.SITENAME]

        for child in list(xml_data.iter()):
            if child.tag == constants.NIKTO_XML.ITEM:
                vuln = NmapUtil._parse_nmap_status_xml(child)
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