from typing import List
from csle_common.dao.container_config.node_traffic_config import NodeTrafficConfig


class TrafficConfig:
    """
    A DTO object representing the traffic configuration of an emulation environment
    """
    def __init__(self, node_traffic_configs : List[NodeTrafficConfig]):
        """
        Initializes the DTO

        :param node_traffic_configs: the list of node traffic configurations
        """
        self.node_traffic_configs = node_traffic_configs

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["node_traffic_configs"] = list(map(lambda x: x.to_dict(), self.node_traffic_configs))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "node_traffic_configs:{}".format(",".join(list(map(lambda x: str(x), self.node_traffic_configs))))