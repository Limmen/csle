from typing import List
from csle_common.dao.emulation_config.node_traffic_config import NodeTrafficConfig
from csle_common.dao.emulation_config.client_population_config import ClientPopulationConfig


class TrafficConfig:
    """
    A DTO object representing the traffic configuration of an emulation environment
    """
    def __init__(self, node_traffic_configs : List[NodeTrafficConfig], client_population_config: ClientPopulationConfig):
        """
        Initializes the DTO

        :param node_traffic_configs: the list of node traffic configurations
        :param client_population_config: the configuration of the client population
        """
        self.node_traffic_configs = node_traffic_configs
        self.client_population_config = client_population_config

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["node_traffic_configs"] = list(map(lambda x: x.to_dict(), self.node_traffic_configs))
        d["client_population_config"] = self.client_population_config.to_dict()
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"node_traffic_configs:{','.join(list(map(lambda x: str(x), self.node_traffic_configs)))}, " \
               f"client_population_config: {self.client_population_config}"