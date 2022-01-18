import os
from csle_common.envs_model.config.generator.vuln_generator import VulnerabilityGenerator
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.util.experiments_util import util
from csle_common.dao.container_config.pw_vulnerability_config import PwVulnerabilityConfig
from csle_common.dao.container_config.vulnerability_type import VulnType
from csle_common.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
import csle_common.constants.constants as constants


def default_vulns(network_id: int = 4) -> VulnerabilitiesConfig:
    """
    :param network_id: the network id
    :return: the VulnerabilitiesConfig of the emulation
    """
    vulns = [
        PwVulnerabilityConfig(node_internal_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              vuln_type=VulnType.WEAK_PW, username="l_hopital", pw="l_hopital",
                              root=True),
        PwVulnerabilityConfig(node_internal_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              vuln_type=VulnType.WEAK_PW, username="euler", pw="euler",
                              root=False),
        PwVulnerabilityConfig(node_internal_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              vuln_type=VulnType.WEAK_PW, username="pi", pw="pi",
                              root=True),
        PwVulnerabilityConfig(node_internal_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              vuln_type=VulnType.WEAK_PW, username="puppet", pw="puppet",
                              root=False),
        PwVulnerabilityConfig(node_internal_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              vuln_type=VulnType.WEAK_PW, username="admin", pw="admin",
                              root=True)
    ]
    vulns_config = VulnerabilitiesConfig(vulnerabilities=vulns)
    return vulns_config


# Generates the vulnerabilities.json configuration file
if __name__ == '__main__':
    network_id = 4
    if not os.path.exists(util.default_vulnerabilities_path()):
        VulnerabilityGenerator.write_vuln_config(default_vulns(network_id=network_id))
    vuln_config = util.read_vulns_config(util.default_vulnerabilities_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                       agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    VulnerabilityGenerator.create_vulns(vuln_cfg=vuln_config, emulation_config=emulation_config)
