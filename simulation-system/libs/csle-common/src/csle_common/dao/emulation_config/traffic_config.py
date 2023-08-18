from typing import List, Dict, Any, Union
from csle_common.dao.emulation_config.node_traffic_config import NodeTrafficConfig
from csle_common.dao.emulation_config.client_population_config import ClientPopulationConfig
from csle_base.json_serializable import JSONSerializable


class TrafficConfig(JSONSerializable):
    """
    A DTO object representing the traffic configuration of an emulation environment
    """
    def __init__(self, node_traffic_configs: List[NodeTrafficConfig],
                 client_population_config: ClientPopulationConfig) -> None:
        """
        Initializes the DTO

        :param node_traffic_configs: the list of node traffic configurations
        :param client_population_config: the configuration of the client population
        """
        self.node_traffic_configs = node_traffic_configs
        self.client_population_config = client_population_config

    def get_node_traffic_config_by_ip(self, ip: str) -> Union[NodeTrafficConfig, None]:
        """
        Gets a node traffic config with a specific IP

        :param ip: the ip
        :return: the node traffic config or None
        """
        for node_traffic_config in self.node_traffic_configs:
            if node_traffic_config.ip == ip or ip == node_traffic_config.docker_gw_bridge_ip:
                return node_traffic_config
        return None

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TrafficConfig":
        """
        Converts a dict representation of the object into a an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = TrafficConfig(
            node_traffic_configs=list(map(lambda x: NodeTrafficConfig.from_dict(x), d["node_traffic_configs"])),
            client_population_config=ClientPopulationConfig.from_dict(d["client_population_config"]))
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["node_traffic_configs"] = list(map(lambda x: x.to_dict(), self.node_traffic_configs))
        d["client_population_config"] = self.client_population_config.to_dict()
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"node_traffic_configs:{','.join(list(map(lambda x: str(x), self.node_traffic_configs)))}, " \
               f"client_population_config: {self.client_population_config}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "TrafficConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return TrafficConfig.from_dict(json.loads(json_str))

    def copy(self) -> "TrafficConfig":
        """
        :return: a copy of the DTO
        """
        return TrafficConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "TrafficConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.client_population_config = config.client_population_config.create_execution_config(
            ip_first_octet=ip_first_octet)
        config.node_traffic_configs = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet),
                                               config.node_traffic_configs))
        return config
