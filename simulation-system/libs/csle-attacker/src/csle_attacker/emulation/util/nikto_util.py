import xml.etree.ElementTree as ET
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.util.env_dynamics_util import EnvDynamicsUtil
from csle_common.dao.emulation_observation.attacker.emulation_attacker_machine_observation_state \
    import EmulationAttackerMachineObservationState
import csle_common.constants.constants as constants
from csle_common.dao.emulation_action_result.nikto_scan_result \
    import NiktoScanResult
from csle_common.dao.emulation_action_result.nikto_vuln import NiktoVuln
from csle_common.util.emulation_util import EmulationUtil
from csle_attacker.emulation.util.nmap_util import NmapUtil
from csle_common.logging.log import Logger


class NiktoUtil:
    """
    Class containing utility functions for the nikto-related functionality to the emulation
    """

    @staticmethod
    def parse_nikto_scan(file_name: str, emulation_env_config: EmulationEnvConfig) -> ET.Element:
        """
        Parses an XML file containing the result of an nikt scan

        :param file_name: name of the file to parse
        :param emulation_env_config: environment config
        :return: the parsed xml file
        """
        sftp_client = emulation_env_config.get_hacker_connection().open_sftp()
        remote_file = sftp_client.open(constants.NMAP.RESULTS_DIR + file_name)
        try:
            xml_tree = ET.parse(remote_file)
        finally:
            remote_file.close()
        xml_data = xml_tree.getroot()
        return xml_data

    @staticmethod
    def nikto_scan_action_helper(s: EmulationEnvState, a: EmulationAttackerAction) \
            -> EmulationEnvState:
        """
        Helper function for executing a NIKTO web scan action on the emulation. Implements caching.

        :param s: the current env state
        :param a: the Nikto action to execute
        :param emulation_env_config: the emulation env config
        :return: s', reward, done
        """
        cmds, file_names = a.nikto_cmds()
        outdata, errdata, total_time = EmulationUtil.execute_ssh_cmds(
            cmds=cmds, conn=s.emulation_env_config.get_hacker_connection())
        EmulationUtil.log_measured_action_time(total_time=total_time, action=a,
                                               emulation_env_config=s.emulation_env_config)

        # Read result
        scan_result = NiktoScanResult(ip=a.ips[0], vulnerabilities=[], port=80, sitename=a.ips[0])
        for file_name in file_names:
            for i in range(constants.ENV_CONSTANTS.NUM_RETRIES):
                try:
                    xml_data = NiktoUtil.parse_nikto_scan(
                        file_name=file_name, emulation_env_config=s.emulation_env_config)
                    scan_result = NiktoUtil.parse_nikto_scan_xml(xml_data)
                    s = NiktoUtil.merge_nikto_scan_result_with_state(
                        scan_result=scan_result, s=s, a=a)
                    break
                except Exception as e:
                    Logger.__call__().get_logger().warning(
                        f"There was an error parsing the Nikto scan output: {e}, {repr(e)}")
        s_prime = s
        return s_prime

    @staticmethod
    def merge_nikto_scan_result_with_state(scan_result: NiktoScanResult, s: EmulationEnvState,
                                           a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Merges a Nikto scan result with an existing observation state

        :param scan_result: the scan result
        :param s: the current state
        :param a: the action just executed
        :return: s', reward, done
        """
        m_obs = None

        for m in s.attacker_obs_state.machines:
            if m.ips == scan_result.ip:
                m_obs = EmulationAttackerMachineObservationState(ips=m.ips)

        if m_obs is None:
            raise ValueError(f"Unknown IP: {scan_result.ip}")
        else:
            for vuln in scan_result.vulnerabilities:
                vuln_obs = vuln.to_obs()
                m_obs.osvdb_vulns.append(vuln_obs)

            attacker_machine_observations = EnvDynamicsUtil.merge_new_obs_with_old(
                s.attacker_obs_state.machines, [m_obs], emulation_env_config=s.emulation_env_config, action=a)
            s_prime = s
            s_prime.attacker_obs_state.machines = attacker_machine_observations

            return s_prime

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
                NiktoUtil.parse_nikto_scan_xml(xml_data)
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
        vulnerabilities = []

        if constants.NIKTO_XML.TARGETPORT in xml_data.keys():
            targetport = xml_data.attrib[constants.NIKTO_XML.TARGETPORT]
        if constants.NIKTO_XML.TARGETIP in xml_data.keys():
            target_ip = xml_data.attrib[constants.NIKTO_XML.TARGETIP]

        for child in list(xml_data.iter()):
            if child.tag == constants.NIKTO_XML.ITEM:
                vuln = NiktoUtil._parse_nikto_item(NmapUtil._parse_nmap_status_xml(child))
                vulnerabilities.append(vuln)
        nikto_scan_result = NiktoScanResult(vulnerabilities=vulnerabilities, port=targetport,
                                            ip=target_ip, sitename=target_ip)
        return nikto_scan_result

    @staticmethod
    def _parse_nikto_item(xml_data) -> NiktoVuln:
        """
        Parses a item in the XML tree of a Nikto scan

        :param xml_data: the item element
        :return: parsed nikto vuln
        """
        id = ""
        osvdb_id = None
        method = ""
        iplink = ""
        namelink = ""
        uri = ""
        description = ""

        if constants.NIKTO_XML.METHOD in xml_data.keys():
            method = xml_data.attrib[constants.NIKTO_XML.METHOD]
        if constants.NIKTO_XML.OSVDB_ID in xml_data.keys():
            osvdb_id = int(xml_data.attrib[constants.NIKTO_XML.OSVDB_ID])
        if constants.NIKTO_XML.ITEM_ID in xml_data.keys():
            id = str(int(xml_data.attrib[constants.NIKTO_XML.ITEM_ID]))

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
