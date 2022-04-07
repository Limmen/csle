from typing import List, Dict, Any
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

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TrafficConfig":
        """
        Converts a dict representation of the object into a an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = TrafficConfig(
            node_traffic_configs=list(map(lambda x: NodeTrafficConfig.from_dict(x), d["node_traffic_configs"])),
            client_population_config=d["client_population_config"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
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