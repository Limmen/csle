from typing import Dict, Any
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig


class ElkConfig:
    """
    Represents the configuration of an ELK node in CSLE
    """

    def __init__(self, container: NodeContainerConfig, resources: NodeResourcesConfig,
                 firewall_config: NodeFirewallConfig,
                 elastic_port: int= 9200, kibana_port = 5601, logstash_port = 5044,
                 time_step_len_seconds = 15, elk_manager_port = 50045, version: str = "0.0.1") -> None:
        """
        Initializes the DTO

        :param container: the container for the Kafka server
        :param network: the network
        :param elastic_port: the port that the Kafka server is listening to
        :param kibana_port: the port that the kibana web server listens to
        :param logstash_port: the port that the logstash beat interface listens to
        :param elk_manager_port: the default port for the gRPC manager
        :param time_step_len_seconds: the length of a time-step (period for logging)
        :param firewall_config: the firewall configuration
        :param container: the container
        :param version: the version
        """
        self.elastic_port = elastic_port
        self.kibana_port = kibana_port
        self.logstash_port = logstash_port
        self.elk_manager_port = elk_manager_port
        self.time_step_len_seconds = time_step_len_seconds
        self.version = version
        self.container = container
        self.resources = resources
        self.firewall_config = firewall_config

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ElkConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ElkConfig(
            container=NodeContainerConfig.from_dict(d["container"]),
            resources=NodeResourcesConfig.from_dict(d["resources"]),
            elastic_port=d["elastic_port"], kibana_port=d["kibana_port"], logstash_port=d["logstash_port"],
            time_step_len_seconds=d["time_step_len_seconds"],
            elk_manager_port=d["elk_manager_port"],
            version=d["version"],
            firewall_config=NodeFirewallConfig.from_dict(d["firewall_config"])
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["container"] = self.container.to_dict()
        d["resources"] = self.resources.to_dict()
        d["elastic_port"] = self.elastic_port
        d["kibana_port"] = self.kibana_port
        d["logstash_port"] = self.logstash_port
        d["elk_manager_port"] = self.elk_manager_port
        d["time_step_len_seconds"] = self.time_step_len_seconds
        d["version"] = self.version
        d["firewall_config"] = self.firewall_config.to_dict()
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"container: {self.container}, " \
               f"kafka port:{self.elastic_port}, version: {self.version}, resources: {self.resources}, " \
               f"kibana port: {self.kibana_port}, logstash_port: {self.logstash_port} " \
               f"elk_manager_port:{self.elk_manager_port}, time_step_len_seconds: {self.time_step_len_seconds}, " \               
               f"firewall_config: {self.firewall_config}"

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    def copy(self) -> "ElkConfig":
        """
        :return: a copy of the DTO
        """
        return ElkConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "ElkConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.container = config.container.create_execution_config(ip_first_octet=ip_first_octet)
        config.resources = config.resources.create_execution_config(ip_first_octet=ip_first_octet)
        config.firewall_config = config.firewall_config.create_execution_config(ip_first_octet=ip_first_octet)
        return config

    @staticmethod
    def schema() -> "ElkConfig":
        """
        :return: get the schema of the DTO
        """
        return ElkConfig(container=NodeContainerConfig.schema(), resources=NodeResourcesConfig.schema(),
                             firewall_config=NodeFirewallConfig.schema())

