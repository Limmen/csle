from typing import List
from gym_pycr_pwcrack.dao.container_config.node_vulnerability_config import NodeVulnerabilityConfig

class VulnerabilitiesConfig:

    def __init__(self, vulnerabilities : List[NodeVulnerabilityConfig]):
        self.vulnerabilities = vulnerabilities