import os
from pycr_common.envs_model.config.generator.vuln_generator import VulnerabilityGenerator
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.util.experiments_util import util
from pycr_common.dao.container_config.pw_vulnerability_config import PwVulnerabilityConfig
from pycr_common.dao.container_config.vulnerability_type import VulnType
from pycr_common.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from pycr_common.dao.container_config.rce_vulnerability_config import RceVulnerabilityConfig
from pycr_common.dao.container_config.sql_injection_vulnerability_config import SQLInjectionVulnerabilityConfig
from pycr_common.dao.container_config.priv_esc_vulnerability_config import PrivEscVulnerabilityConfig
import pycr_common.constants.constants as constants


def default_vulns():
    vulns = [
        PwVulnerabilityConfig(node_ip="172.18.9.79", vuln_type=VulnType.WEAK_PW, username="l_hopital", pw="l_hopital",
                          root=True),
        PwVulnerabilityConfig(node_ip="172.18.9.79", vuln_type=VulnType.WEAK_PW, username="euler", pw="euler",
                              root=False),
        PwVulnerabilityConfig(node_ip="172.18.9.79", vuln_type=VulnType.WEAK_PW, username="pi", pw="pi",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.9.2", vuln_type=VulnType.WEAK_PW, username="puppet", pw="puppet",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.9.3", vuln_type=VulnType.WEAK_PW, username="admin", pw="admin",
                              root=True),
        RceVulnerabilityConfig(node_ip="172.18.9.54", vuln_type=VulnType.RCE),
        SQLInjectionVulnerabilityConfig(node_ip="172.18.9.74", vuln_type=VulnType.SQL_INJECTION,
                                        username="pablo", pw="0d107d09f5bbe40cade3de5c71e9e9b7", root=True),
        PwVulnerabilityConfig(node_ip="172.18.9.61", vuln_type=VulnType.WEAK_PW, username="adm",
                              pw="adm", root=False),
        PrivEscVulnerabilityConfig(node_ip="172.18.9.61", vuln_type=VulnType.PRIVILEGE_ESCALATION,
                                   username="alan", pw="alan", root=False, cve="2010-1427"),
        RceVulnerabilityConfig(node_ip="172.18.9.62", vuln_type=VulnType.RCE),
        RceVulnerabilityConfig(node_ip="172.18.9.7", vuln_type=VulnType.RCE),
        RceVulnerabilityConfig(node_ip="172.18.9.178", vuln_type=VulnType.RCE),
        PwVulnerabilityConfig(node_ip="172.18.9.25", vuln_type=VulnType.WEAK_PW, username="donald", pw="donald",
                              root=False),
        PrivEscVulnerabilityConfig(node_ip="172.18.9.25", vuln_type=VulnType.PRIVILEGE_ESCALATION,
                                   username="donald", pw="donald", root=False, cve="2015-5602"),
        RceVulnerabilityConfig(node_ip="172.18.9.28", vuln_type=VulnType.RCE)
    ]
    vulns_config = VulnerabilitiesConfig(vulnerabilities=vulns)
    return vulns_config

if __name__ == '__main__':
    if not os.path.exists(util.default_vulnerabilities_path()):
        VulnerabilityGenerator.write_vuln_config(default_vulns())
    vuln_config = util.read_vulns_config(util.default_vulnerabilities_path())
    emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username=constants.PYCR_ADMIN.USER,
                                     agent_pw=constants.PYCR_ADMIN.PW, server_connection=False)
    VulnerabilityGenerator.create_vulns(vuln_cfg=vuln_config, emulation_config=emulation_config)