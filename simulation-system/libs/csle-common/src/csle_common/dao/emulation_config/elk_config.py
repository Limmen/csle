from typing import Dict, Any, List
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_base.json_serializable import JSONSerializable


class ElkConfig(JSONSerializable):
    """
    Represents the configuration of an ELK node in CSLE
    """

    def __init__(self, container: NodeContainerConfig, resources: NodeResourcesConfig,
                 firewall_config: NodeFirewallConfig,
                 elk_manager_log_file: str, elk_manager_log_dir: str, elk_manager_max_workers: int,
                 elastic_port: int = 9200, kibana_port: int = 5601, logstash_port: int = 5044,
                 time_step_len_seconds: int = 15, elk_manager_port: int = 50045, version: str = "0.0.1") -> None:
        """
        Initializes the DTO

        :param container: the container for the ELK stack
        :param network: the network
        :param elastic_port: the port that the Elastic db server is listening to
        :param kibana_port: the port that the kibana web server listens to
        :param logstash_port: the port that the logstash beat interface listens to
        :param elk_manager_port: the default port for the gRPC manager
        :param time_step_len_seconds: the length of a time-step (period for logging)
        :param firewall_config: the firewall configuration
        :param container: the container
        :param version: the version
        :param elk_manager_log_file: the log file of the elk manager
        :param elk_manager_log_dir: the log dir of the elk manager
        :param elk_manager_max_workers: the maximum number of GRPC workers for the elk maanger
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
        self.elk_manager_log_file = elk_manager_log_file
        self.elk_manager_log_dir = elk_manager_log_dir
        self.elk_manager_max_workers = elk_manager_max_workers

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
            firewall_config=NodeFirewallConfig.from_dict(d["firewall_config"]),
            elk_manager_max_workers=d["elk_manager_max_workers"],
            elk_manager_log_dir=d["elk_manager_log_dir"],
            elk_manager_log_file=d["elk_manager_log_file"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["container"] = self.container.to_dict()
        d["resources"] = self.resources.to_dict()
        d["elastic_port"] = self.elastic_port
        d["kibana_port"] = self.kibana_port
        d["logstash_port"] = self.logstash_port
        d["elk_manager_port"] = self.elk_manager_port
        d["time_step_len_seconds"] = self.time_step_len_seconds
        d["version"] = self.version
        d["firewall_config"] = self.firewall_config.to_dict()
        d["elk_manager_log_file"] = self.elk_manager_log_file
        d["elk_manager_log_dir"] = self.elk_manager_log_dir
        d["elk_manager_max_workers"] = self.elk_manager_max_workers
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"container: {self.container}, " \
               f"elastic port:{self.elastic_port}, version: {self.version}, resources: {self.resources}, " \
               f"kibana port: {self.kibana_port}, logstash_port: {self.logstash_port} " \
               f"elk_manager_port:{self.elk_manager_port}, time_step_len_seconds: {self.time_step_len_seconds}, " \
               f"firewall_config: {self.firewall_config}, " \
               f"elk_manager_log_file: {self.elk_manager_log_file}, " \
               f"elk_manager_log_dir: {self.elk_manager_log_dir}, " \
               f"elk_manager_max_workers: {self.elk_manager_max_workers}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "ElkConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ElkConfig.from_dict(json.loads(json_str))

    def copy(self) -> "ElkConfig":
        """
        :return: a copy of the DTO
        """
        return ElkConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int, physical_servers: List[str]) -> "ElkConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :param physical_servers: the physical servers where the execution is deployedn
        :return: the new config
        """
        config = self.copy()
        config.container = config.container.create_execution_config(ip_first_octet=ip_first_octet,
                                                                    physical_servers=physical_servers)
        config.resources = config.resources.create_execution_config(ip_first_octet=ip_first_octet)
        config.firewall_config = config.firewall_config.create_execution_config(ip_first_octet=ip_first_octet)
        return config

    @staticmethod
    def schema() -> "ElkConfig":
        """
        :return: get the schema of the DTO
        """
        return ElkConfig(container=NodeContainerConfig.schema(), resources=NodeResourcesConfig.schema(),
                         firewall_config=NodeFirewallConfig.schema(), elk_manager_log_file="elk_manager.log",
                         elk_manager_log_dir="/", elk_manager_max_workers=10)
