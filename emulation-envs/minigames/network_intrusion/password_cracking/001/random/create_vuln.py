from gym_pycr_pwcrack.envs.config.generator.vuln_generator import VulnerabilityGenerator
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.util.experiments_util import util

def apply_config():
    vuln_config = util.read_vulns_config(util.default_vulnerabilities_path())
    containers_config = util.read_containers_config(util.default_containers_path())

    cluster_config = ClusterConfig(agent_ip=containers_config.agent_ip, agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    VulnerabilityGenerator.create_vulns(vuln_cfg=vuln_config, cluster_config=cluster_config)


if __name__ == '__main__':
    apply_config()