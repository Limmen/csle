import os
from pycr_common.envs_model.config.generator.vuln_generator import VulnerabilityGenerator
from pycr_common.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.dao.container_config.pw_vulnerability_config import PwVulnerabilityConfig
from pycr_common.dao.container_config.vulnerability_type import VulnType
from gym_pycr_ctf.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig

def default_vulns():
    vulns = [
        PwVulnerabilityConfig(node_ip="172.18.5.79", vuln_type=VulnType.WEAK_PW, username="l_hopital", pw="l_hopital",
                          root=True),
        PwVulnerabilityConfig(node_ip="172.18.5.79", vuln_type=VulnType.WEAK_PW, username="euler", pw="euler",
                              root=False),
        PwVulnerabilityConfig(node_ip="172.18.5.79", vuln_type=VulnType.WEAK_PW, username="pi", pw="pi",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.5.2", vuln_type=VulnType.WEAK_PW, username="puppet", pw="puppet",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.5.3", vuln_type=VulnType.WEAK_PW, username="admin", pw="admin",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.5.54", vuln_type=VulnType.WEAK_PW, username="vagrant", pw="vagrant",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.5.74", vuln_type=VulnType.WEAK_PW, username="administrator", pw="administrator",
                              root=True),
        PwVulnerabilityConfig(node_ip="172.18.5.61", vuln_type=VulnType.WEAK_PW, username="adm",
                              pw="adm", root=True),
        PwVulnerabilityConfig(node_ip="172.18.5.62", vuln_type=VulnType.WEAK_PW, username="guest", pw="guest", root=True),
        PwVulnerabilityConfig(node_ip="172.18.5.7", vuln_type=VulnType.WEAK_PW, username="ec2-user", pw="ec2-user",
                              root=True)
    ]
    vulns_config = VulnerabilitiesConfig(vulnerabilities=vulns)
    return vulns_config

if __name__ == '__main__':
    if not os.path.exists(util.default_vulnerabilities_path()):
        VulnerabilityGenerator.write_vuln_config(default_vulns())
    vuln_config = util.read_vulns_config(util.default_vulnerabilities_path())
    emulation_config = EmulationConfig(agent_ip="172.18.5.191", agent_username="pycr_admin",
                                     agent_pw="pycr@admin-pw_191", server_connection=False)
    VulnerabilityGenerator.create_vulns(vuln_cfg=vuln_config, emulation_config=emulation_config)