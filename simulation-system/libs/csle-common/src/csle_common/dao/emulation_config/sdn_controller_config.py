from typing import Dict, Any, List
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.sdn_controller_type import SDNControllerType
from csle_base.json_serializable import JSONSerializable


class SDNControllerConfig(JSONSerializable):
    """
    DTO containing configuration for the SDN controller
    """

    def __init__(self, container: NodeContainerConfig, resources: NodeResourcesConfig,
                 firewall_config: NodeFirewallConfig,
                 controller_port: int,
                 controller_type: SDNControllerType, controller_module_name: str, controller_web_api_port: int,
                 manager_log_file: str, manager_log_dir: str, manager_max_workers: int,
                 time_step_len_seconds: int = 15, version: str = "0.0.1",
                 manager_port: int = 50042):
        """
        Initializes the DTO

        :param container: the container config of the controller
        :param resources: the resources config of the controller
        :param firewall_config: the firewall config of the controller
        :param controller_port: the port of the controller
        :param controller_type: the type of the controller
        :param time_step_len_seconds: the length of a time-step in the emulation (for monitoring)
        :param controller_module_name: the name of the controller Python module
        :param controller_web_api_port: the port to run the controller's web API
        :param manager_log_dir: the directory to save log files of the manager
        :param manager_log_file: the file name for the manager logs
        :param manager_max_workers: the maximum number of gRPC workers of the manager
        :param manager_port: the port of the manager
        :param version: the version
        """
        self.container = container
        self.resources = resources
        self.firewall_config = firewall_config
        self.controller_port = controller_port
        self.time_step_len_seconds = time_step_len_seconds
        self.version = version
        self.controller_type = controller_type
        self.controller_module_name = controller_module_name
        self.controller_web_api_port = controller_web_api_port
        self.manager_log_file = manager_log_file
        self.manager_log_dir = manager_log_dir
        self.manager_max_workers = manager_max_workers
        self.manager_port = manager_port

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SDNControllerConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = SDNControllerConfig(
            container=NodeContainerConfig.from_dict(d["container"]),
            resources=NodeResourcesConfig.from_dict(d["resources"]),
            time_step_len_seconds=d["time_step_len_seconds"],
            version=d["version"], controller_type=d["controller_type"], controller_port=d["controller_port"],
            controller_web_api_port=d["controller_web_api_port"], controller_module_name=d["controller_module_name"],
            firewall_config=NodeFirewallConfig.from_dict(d["firewall_config"]), manager_port=d["manager_port"],
            manager_log_dir=d["manager_log_dir"], manager_log_file=d["manager_log_file"],
            manager_max_workers=d["manager_max_workers"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["container"] = self.container.to_dict()
        d["resources"] = self.resources.to_dict()
        d["time_step_len_seconds"] = self.time_step_len_seconds
        d["controller_type"] = self.controller_type
        d["controller_port"] = self.controller_port
        d["version"] = self.version
        d["controller_module_name"] = self.controller_module_name
        d["controller_web_api_port"] = self.controller_web_api_port
        d["firewall_config"] = self.firewall_config.to_dict()
        d["manager_port"] = self.manager_port
        d["manager_log_file"] = self.manager_log_file
        d["manager_log_dir"] = self.manager_log_dir
        d["manager_max_workers"] = self.manager_max_workers
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"container: {self.container}, " \
               f"resources: {self.resources}, time step len: {self.time_step_len_seconds}, " \
               f"controller type: {self.controller_type}, controller_port: {self.controller_port}, " \
               f"version: {self.version}, controller_module_name: {self.controller_module_name}, " \
               f"controller_web_api_port: {self.controller_web_api_port}, firewall_config: {self.firewall_config}," \
               f"manager_port: {self.manager_port}, manager_log_file: {self.manager_log_file}, " \
               f"manager_log_dir: {self.manager_log_dir}, manager_max_workers: {self.manager_max_workers}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "SDNControllerConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SDNControllerConfig.from_dict(json.loads(json_str))

    def copy(self) -> "SDNControllerConfig":
        """
        :return: a copy of the DTO
        """
        return SDNControllerConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int, physical_servers: List[str]) -> "SDNControllerConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :param physical_servers: the physical servers of the execution
        :return: the new config
        """
        config = self.copy()
        if config is None:
            raise ValueError("Obtained None and not SDNControllerConfig")
        config.container = config.container.create_execution_config(ip_first_octet=ip_first_octet,
                                                                    physical_servers=physical_servers)
        config.resources = config.resources.create_execution_config(ip_first_octet=ip_first_octet)
        config.firewall_config = config.firewall_config.create_execution_config(ip_first_octet=ip_first_octet)
        return config
