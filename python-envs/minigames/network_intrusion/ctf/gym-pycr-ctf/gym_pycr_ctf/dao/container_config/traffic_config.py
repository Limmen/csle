from typing import List
from gym_pycr_ctf.dao.container_config.node_traffic_config import NodeTrafficConfig

class TrafficConfig:

    def __init__(self, node_traffic_configs : List[NodeTrafficConfig]):
        self.node_traffic_configs = node_traffic_configs