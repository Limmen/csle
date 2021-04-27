from typing import List
from gym_pycr_ctf.dao.container_config.node_traffic_config import NodeTrafficConfig


class TrafficConfig:
    """
    A DTO object representing the traffic configuration of an emulation environment
    """
    def __init__(self, node_traffic_configs : List[NodeTrafficConfig]):
        self.node_traffic_configs = node_traffic_configs

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "node_traffic_configs:{}".format(",".join(list(map(lambda x: str(x), self.node_traffic_configs))))