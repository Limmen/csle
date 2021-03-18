from typing import List
from gym_pycr_ctf.dao.container_config.node_firewall_config import NodeFirewallConfig

class Topology:

    def __init__(self, node_configs: List[NodeFirewallConfig], subnetwork: str):
        self.node_configs = node_configs
        self.subnetwork = subnetwork