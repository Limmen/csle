from typing import List
import random
import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.topology_config import TopologyConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.emulation_config.node_vulnerability_config import NodeVulnerabilityConfig
from csle_common.dao.emulation_config.vulnerability_type import VulnType
from csle_common.domain_randomization.topology_generator import TopologyGenerator
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.util.emulation_util import EmulationUtil
from csle_common.util.experiment_util import ExperimentUtil


class VulnerabilityGenerator:
    """
    A Utility Class for generating vulnerability configuration files
    """

    @staticmethod
    def shortlist() -> List[str]:
        """
        :return: a list of shortlist usernames for password vulnerabilities
        """
        return constants.VULNERABILITY_GENERATOR.NAMES_SHORTLIST

    @staticmethod
    def generate(topology: TopologyConfig, vulnerable_nodes : List[NodeFirewallConfig], agent_ip : str,
                 router_ip: str, subnet_prefix :str, num_flags,
                 access_vuln_types : List[VulnType]) -> VulnerabilitiesConfig:
        """
        Utility function for generating a vulnerability configuration for an emulation

        :param topology: the topology of the emulation
        :param vulnerable_nodes: the gateways of the emulation
        :param agent_ip: the ip of the agent container
        :param router_ip: the ip of the gateway container
        :param subnet_prefix: the prefix of of the subnet
        :param num_flags: the number of flags
        :param access_vuln_types: the vulnerability types that yield shell access
        :return: The created vulnerabilities config
        """
        vulnerabilities = []

        # Start by creating necessary vulns
        for vulnerable_node in vulnerable_nodes:
            ip = subnet_prefix + str(vulnerable_node)
            if ip != agent_ip and ip != router_ip:
                vuln_idx = random.randint(0, len(access_vuln_types) - 1)
                vuln_type = access_vuln_types[vuln_idx]
                if vuln_type == VulnType.WEAK_PW:
                    vuln_cfg = VulnerabilityGenerator.pw_vuln(vulnerable_node)
                    vulnerabilities.append(vuln_cfg)
                elif vuln_type == VulnType.RCE:
                    vuln_cfg = VulnerabilityGenerator.rce_vuln(vulnerable_node)
                    vulnerabilities.append(vuln_cfg)
                elif vuln_type == VulnType.SQL_INJECTION:
                    vuln_cfg = VulnerabilityGenerator.sql_injection_vuln(vulnerable_node)
                    vulnerabilities.append(vuln_cfg)
                elif vuln_type == VulnType.PRIVILEGE_ESCALATION:
                    vuln_cfg_1 = VulnerabilityGenerator.pw_vuln(vulnerable_node)
                    vulnerabilities.append(vuln_cfg_1)
                    vuln_cfg_2 = VulnerabilityGenerator.priv_esc_vuln(vulnerable_node, username=vuln_cfg_1.username,
                                                                      pw=vuln_cfg_1.pw)
                    vulnerabilities.append(vuln_cfg_2)
                else:
                    raise ValueError("Unrecognized vulnerability type")

        for node in topology.node_configs:
            # Create vuln necessary for flags and some random vulns
            if len(vulnerable_nodes) < num_flags or np.random.rand() < 0.2:
                if agent_ip not in node.get_ips() and router_ip not in node.get_ips() and node not in vulnerable_nodes:
                    vuln_idx = random.randint(0, len(access_vuln_types) - 1)
                    vuln_type = access_vuln_types[vuln_idx]
                    if vuln_type == VulnType.WEAK_PW:
                        vuln_cfg = VulnerabilityGenerator.pw_vuln(node)
                        vulnerabilities.append(vuln_cfg)
                    elif vuln_type == VulnType.RCE:
                        vuln_cfg = VulnerabilityGenerator.rce_vuln(node)
                        vulnerabilities.append(vuln_cfg)
                    elif vuln_type == VulnType.SQL_INJECTION:
                        vuln_cfg = VulnerabilityGenerator.sql_injection_vuln(node)
                        vulnerabilities.append(vuln_cfg)
                    elif vuln_type == VulnType.PRIVILEGE_ESCALATION:
                        vuln_cfg_1 = VulnerabilityGenerator.pw_vuln(node)
                        vulnerabilities.append(vuln_cfg_1)
                        vuln_cfg_2 = VulnerabilityGenerator.priv_esc_vuln(node, username=vuln_cfg_1.username,
                                                                          pw=vuln_cfg_1.pw)
                        vulnerabilities.append(vuln_cfg_2)
                    else:
                        raise ValueError("Unrecognized vulnerability type")

        vulns_cfg = VulnerabilitiesConfig(node_vulnerability_configs=vulnerabilities)
        return vulns_cfg

    @staticmethod
    def pw_vuln(node: NodeFirewallConfig) -> NodeVulnerabilityConfig:
        """
        Utility function for creating a password vulnerability config object

        :param node: the node to create the vulnerability on
        :return: the created vulnerability
        """
        pw_shortlist = VulnerabilityGenerator.shortlist()
        pw_idx = random.randint(0, len(pw_shortlist)-1)
        u = pw_shortlist[pw_idx]
        pw = pw_shortlist[pw_idx]
        vuln_config = NodeVulnerabilityConfig(name=constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS,
                                              ip= node.get_ips()[0], vuln_type=VulnType.WEAK_PW,
                                              credentials=[Credential(username=u, pw=pw)], root=True,
                                              port=constants.SSH.DEFAULT_PORT, service=constants.SSH.SERVICE_NAME,
                                              cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS, cve=None,
                                              protocol=TransportProtocol.TCP)
        return vuln_config


    @staticmethod
    def rce_vuln(node: NodeFirewallConfig) -> NodeVulnerabilityConfig:
        """
        Utility function for creating an RCE vulnerability config object

        :param node: the node to create the vulnerability on
        :return: the created vulnerability
        """
        vuln_config = NodeVulnerabilityConfig(name=constants.EXPLOIT_VULNERABILITES.SAMBACRY_EXPLOIT,
                                              ip= node.get_ips()[0], vuln_type=VulnType.WEAK_PW,
                                              credentials=[
                                                  Credential(username=constants.SAMBA.USER, pw=constants.SAMBA.PW)],
                                              root=True,
                                              port=constants.SSH.DEFAULT_PORT, service=constants.SSH.SERVICE_NAME,
                                              cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS, cve=None,
                                              protocol=TransportProtocol.TCP)
        return vuln_config

    @staticmethod
    def priv_esc_vuln(node: NodeFirewallConfig, username: str, pw: str) -> NodeVulnerabilityConfig:
        """
        Utility function for creating a Priv-Esc vulnerability config object

        :param username: the username of to do the escalation
        :param pw: the password to do the escalation
        :param node: the node to create the vulnerability on
        :return: the created vulnerability
        """
        priv_esc_cve_idx = random.randint(0, len(constants.EXPLOIT_VULNERABILITES.PRIVILEGE_ESC_VULNS) - 1)
        root =False
        vuln_config = NodeVulnerabilityConfig(
            name=constants.EXPLOIT_VULNERABILITES.CVE_2010_0426, ip= node.get_ips()[0], vuln_type=VulnType.WEAK_PW,
            credentials=[Credential(username=username, pw=pw)],
            root=root, port=constants.SSH.DEFAULT_PORT,  service=constants.CVE_2010_0426.SERVICE_NAME,
            cvss=constants.EXPLOIT_VULNERABILITES.CVE_2010_0426_CVSS,
            cve=constants.EXPLOIT_VULNERABILITES.PRIVILEGE_ESC_VULNS[priv_esc_cve_idx],
            protocol=TransportProtocol.TCP)
        return vuln_config


    @staticmethod
    def sql_injection_vuln(node: NodeFirewallConfig) -> NodeVulnerabilityConfig:
        """
        Utility function for creating a SQL-Injection vulnerability config object

        :param node: the node to create the vulnerability on
        :return: the created vulnerability
        """
        vuln_config = NodeVulnerabilityConfig(
            name=constants.EXPLOIT_VULNERABILITES.DVWA_SQL_INJECTION, ip= node.get_ips()[0],
            vuln_type=VulnType.WEAK_PW,
            credentials=[Credential(username=constants.DVWA_SQL_INJECTION.EXPLOIT_USER,
                                    pw=constants.DVWA_SQL_INJECTION.EXPLOIT_PW)],
            root=True, port=constants.SSH.DEFAULT_PORT,  service=constants.DVWA_SQL_INJECTION.SERVICE_NAME,
            cvss=constants.EXPLOIT_VULNERABILITES.DVWA_SQL_INJECTION_CVSS,
            cve=constants.EXPLOIT_VULNERABILITES.DVWA_SQL_INJECTION,
            protocol=TransportProtocol.TCP)
        return vuln_config

    @staticmethod
    def write_vuln_config(vulns_cfg: VulnerabilitiesConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param vulns_cfg: the config to write
        :param path: the path to write the configuration to
        :return: None
        """
        path = ExperimentUtil.default_vulnerabilities_path(out_dir=path)
        ExperimentUtil.write_vulns_config_file(vulns_cfg, path)


if __name__ == '__main__':
    topology, agent_ip, router_ip, vulnerable_nodes = TopologyGenerator.generate(
        num_nodes=15, subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}2", subnet_id=2)
    vulnerabilities = VulnerabilityGenerator.generate(
        topology=topology, vulnerable_nodes=vulnerable_nodes,
        agent_ip=agent_ip, router_ip=router_ip, subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}2",
        num_flags = 3, access_vuln_types=[VulnType.WEAK_PW])
    print(vulnerabilities)




