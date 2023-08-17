from typing import List, Dict, Any
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.client import Client
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.util.general_util import GeneralUtil
from csle_base.json_serializable import JSONSerializable


class ClientPopulationConfig(JSONSerializable):
    """
    A DTO object representing the configuration of the client population of an emulation
    """

    def __init__(self, ip: str, networks: List[ContainerNetwork],
                 client_manager_port: int, client_manager_log_file: str,
                 client_manager_log_dir: str, client_manager_max_workers: int,
                 clients: List[Client], workflows_config: WorkflowsConfig,
                 client_time_step_len_seconds: int = 1,
                 docker_gw_bridge_ip: str = "", physical_host_ip: str = ""):
        """
        Creates a ClientPopulationConfig DTO Object

        :param ip: the ip of the client container
        :param networks: a list of networks in the emulation that are accessible for external networks
        :param client_time_step_len_seconds: time-step length to measure the arrival process
        :param client_manager_log_file: the log file of the client manager
        :param client_manager_log_dir: the log dir of the client manager
        :param client_manager_max_workers: the maximum number of GRPC workers for the client manager
        :param docker_gw_bridge_ip: IP to reach the container from the host network
        :param physical_host_ip: IP of the physical host where the container is running
        :param clients: list of client configurations
        :param workflows_config: the workflows configurations
        """
        self.networks = networks
        self.ip = ip
        self.client_manager_port = client_manager_port
        self.client_time_step_len_seconds = client_time_step_len_seconds
        self.client_manager_log_dir = client_manager_log_dir
        self.client_manager_log_file = client_manager_log_file
        self.client_manager_max_workers = client_manager_max_workers
        self.docker_gw_bridge_ip = docker_gw_bridge_ip
        self.physical_host_ip = physical_host_ip
        self.clients = clients
        self.workflows_config = workflows_config

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClientPopulationConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ClientPopulationConfig(
            ip=d["ip"],
            networks=list(map(lambda x: ContainerNetwork.from_dict(x), d["networks"])),
            client_manager_port=d["client_manager_port"],
            client_time_step_len_seconds=d["client_time_step_len_seconds"],
            client_manager_log_dir=d["client_manager_log_dir"], client_manager_log_file=d["client_manager_log_file"],
            client_manager_max_workers=d["client_manager_max_workers"],
            docker_gw_bridge_ip=d["docker_gw_bridge_ip"], physical_host_ip=d["physical_host_ip"],
            clients=list(map(lambda x: Client.from_dict(x), d["clients"])),
            workflows_config=WorkflowsConfig.from_dict(d["workflows_config"])
        )
        return obj

    def no_clients(self) -> "ClientPopulationConfig":
        """
        :return: A version of the config with no clients
        """
        return ClientPopulationConfig(
            ip=self.ip,
            networks=self.networks,
            client_manager_port=self.client_manager_port,
            client_time_step_len_seconds=self.client_time_step_len_seconds,
            client_manager_log_file="client_manager.log", client_manager_log_dir="/", client_manager_max_workers=10,
            docker_gw_bridge_ip=self.docker_gw_bridge_ip, physical_host_ip=self.physical_host_ip,
            clients=[Client(id=0, arrival_config=ConstantArrivalConfig(lamb=0), mu=0, exponential_service_time=True,
                            workflow_distribution=[1])],
            workflows_config=WorkflowsConfig(
                workflow_markov_chains=[WorkflowMarkovChain(
                    initial_state=0, transition_matrix=[[0.8, 0.2], [0, 1]], id=0)],
                workflow_services=[WorkflowService(ips_and_commands=[('localhost', "echo ' '")], id=0)])
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["ip"] = self.ip
        d["networks"] = list(map(lambda x: x.to_dict(), self.networks))
        d["client_manager_port"] = self.client_manager_port
        d["client_time_step_len_seconds"] = self.client_time_step_len_seconds
        d["client_manager_log_file"] = self.client_manager_log_file
        d["client_manager_log_dir"] = self.client_manager_log_dir
        d["client_manager_max_workers"] = self.client_manager_max_workers
        d["docker_gw_bridge_ip"] = self.docker_gw_bridge_ip
        d["physical_host_ip"] = self.physical_host_ip
        d["clients"] = list(map(lambda x: x.to_dict(), self.clients))
        d["workflows_config"] = self.workflows_config.to_dict()
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, " \
               f"networks:{list(map(lambda x: str(x), self.networks))}, " \
               f"client_manager_port: {self.client_manager_port}, " \
               f"client_time_step_len_seconds: {self.client_time_step_len_seconds}," \
               f"client_manager_log_file: {self.client_manager_log_file}, " \
               f"client_manager_log_dir: {self.client_manager_log_dir}, " \
               f"client_manager_max_workers: {self.client_manager_max_workers}, " \
               f"docker_gw_bridge_ip:{self.docker_gw_bridge_ip}, physical_host_ip: {self.physical_host_ip}," \
               f"clients:{list(map(lambda x: str(x), self.clients))}, workflows_config: {self.workflows_config}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "ClientPopulationConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ClientPopulationConfig.from_dict(json.loads(json_str))

    def copy(self) -> "ClientPopulationConfig":
        """
        :return: a copy of the DTO
        """
        return ClientPopulationConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "ClientPopulationConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.ip = GeneralUtil.replace_first_octet_of_ip(ip=config.ip, ip_first_octet=ip_first_octet)
        config.networks = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet),
                                   config.networks))
        config.workflows_config = config.workflows_config.create_execution_config(ip_first_octet=ip_first_octet)
        return config
