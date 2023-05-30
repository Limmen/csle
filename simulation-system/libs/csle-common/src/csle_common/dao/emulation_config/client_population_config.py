from typing import List, Dict, Any
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig
from csle_collector.client_manager.dao.eptmp_arrival_config import EPTMPArrivalConfig
from csle_collector.client_manager.dao.spiking_arrival_config import SpikingArrivalConfig
from csle_collector.client_manager.dao.sine_arrival_config import SineArrivalConfig
from csle_collector.client_manager.dao.piece_wise_constant_arrival_config import PieceWiseConstantArrivalConfig
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.util.general_util import GeneralUtil


class ClientPopulationConfig:
    """
    A DTO object representing the configuration of the client population of an emulation
    """

    def __init__(self, ip: str, networks: List[ContainerNetwork],
                 client_manager_port: int, client_manager_log_file: str,
                 client_manager_log_dir: str, client_manager_max_workers: int,
                 arrival_config: ArrivalConfig,  num_commands: int = 5,
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
        :param arrival_config: configuration of the arrival process
        """
        self.networks = networks
        self.ip = ip
        self.client_manager_port = client_manager_port
        self.num_commands = num_commands
        self.client_time_step_len_seconds = client_time_step_len_seconds
        self.client_manager_log_dir = client_manager_log_dir
        self.client_manager_log_file = client_manager_log_file
        self.client_manager_max_workers = client_manager_max_workers
        self.docker_gw_bridge_ip = docker_gw_bridge_ip
        self.physical_host_ip = physical_host_ip
        self.arrival_config = arrival_config

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClientPopulationConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        if d["arrival_config"]["client_arrival_type"] == ClientArrivalType.CONSTANT.value:
            arrival_config = ConstantArrivalConfig.from_dict(d["arrival_config"])
        elif d["arrival_config"]["client_arrival_type"] == ClientArrivalType.EPTMP.value:
            arrival_config = EPTMPArrivalConfig.from_dict(d["arrival_config"])
        elif d["arrival_config"]["client_arrival_type"] == ClientArrivalType.SPIKING.value:
            arrival_config = SpikingArrivalConfig.from_dict(d["arrival_config"])
        elif d["arrival_config"]["client_arrival_type"] == ClientArrivalType.SINE_MODULATED.value:
            arrival_config = SineArrivalConfig.from_dict(d["arrival_config"])
        elif d["arrival_config"]["client_arrival_type"] == ClientArrivalType.PIECE_WISE_CONSTANT.value:
            arrival_config = PieceWiseConstantArrivalConfig.from_dict(d["arrival_config"])
        else:
            raise ValueError("Arrival config not recognized")
        obj = ClientPopulationConfig(
            ip=d["ip"],
            networks=list(map(lambda x: ContainerNetwork.from_dict(x), d["networks"])),
            client_manager_port=d["client_manager_port"],
            num_commands=d["num_commands"], client_time_step_len_seconds=d["client_time_step_len_seconds"],
            client_manager_log_dir=d["client_manager_log_dir"], client_manager_log_file=d["client_manager_log_file"],
            client_manager_max_workers=d["client_manager_max_workers"],
            docker_gw_bridge_ip=d["docker_gw_bridge_ip"], physical_host_ip=d["physical_host_ip"],
            arrival_config=arrival_config)
        return obj

    def no_clients(self) -> "ClientPopulationConfig":
        """
        :return: A version of the config with no clients
        """
        return ClientPopulationConfig(
            ip=self.ip,
            networks=self.networks,
            client_manager_port=self.client_manager_port,
            num_commands=0, client_time_step_len_seconds=self.client_time_step_len_seconds,
            client_manager_log_file="client_manager.log", client_manager_log_dir="/", client_manager_max_workers=10,
            docker_gw_bridge_ip=self.docker_gw_bridge_ip, physical_host_ip=self.physical_host_ip,
            arrival_config=ConstantArrivalConfig(lamb=0, mu=0)
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["networks"] = list(map(lambda x: x.to_dict(), self.networks))
        d["num_commands"] = self.num_commands
        d["client_manager_port"] = self.client_manager_port
        d["client_time_step_len_seconds"] = self.client_time_step_len_seconds
        d["client_manager_log_file"] = self.client_manager_log_file
        d["client_manager_log_dir"] = self.client_manager_log_dir
        d["client_manager_max_workers"] = self.client_manager_max_workers
        d["docker_gw_bridge_ip"] = self.docker_gw_bridge_ip
        d["physical_host_ip"] = self.physical_host_ip
        d["arrival_config"] = self.arrival_config.to_dict()
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, " \
               f"networks:{list(map(lambda x: str(x), self.networks))}, " \
               f"client_manager_port: {self.client_manager_port}, num_commands:{self.num_commands}, " \
               f"client_time_step_len_seconds: {self.client_time_step_len_seconds}," \
               f"client_manager_log_file: {self.client_manager_log_file}, " \
               f"client_manager_log_dir: {self.client_manager_log_dir}, " \
               f"client_manager_max_workers: {self.client_manager_max_workers}, " \
               f"docker_gw_bridge_ip:{self.docker_gw_bridge_ip}, physical_host_ip: {self.physical_host_ip}," \
               f"arrival_config: {self.arrival_config}"

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
        return config
