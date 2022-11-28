from typing import List, Dict, Any
from csle_common.dao.emulation_config.client_population_process_type import ClientPopulationProcessType
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.util.general_util import GeneralUtil


class ClientPopulationConfig:
    """
    A DTO object representing the configuration of the client population of an emulation
    """

    def __init__(self, ip: str, networks: List[ContainerNetwork], client_process_type: ClientPopulationProcessType,
                 lamb: float, mu: float, client_manager_port: int, client_manager_log_file: str,
                 client_manager_log_dir: str, client_manager_max_workers: int,
                 num_commands: int = 5,
                 client_time_step_len_seconds: int = 1, time_scaling_factor: float = 0.01,
                 period_scaling_factor: float = 20):
        """
        Creates a ClientPopulationConfig DTO Object

        :param ip: the ip of the client container
        :param networks: a list of networks in the emulation that are accessible for external networks
        :param client_process_type: the type of client arrival process (e.g. a Poisson process)
        :param lamb: the lambda parameter of the arrival process
        :param mu: the service-time parameter of the arrivals
        :param client_time_step_len_seconds: time-step length to measure the arrival process
        :param time_scaling_factor: the time-scaling factor for sine-modulated arrival processes
        :param period_scaling_factor: the period-scaling factor for sine-modulated arrival processes
        :param client_manager_log_file: the log file of the client manager
        :param client_manager_log_dir: the log dir of the client manager
        :param client_manager_max_workers: the maximum number of GRPC workers for the client manager
        """
        self.networks = networks
        self.ip = ip
        self.client_process_type = client_process_type
        self.lamb = lamb
        self.mu = mu
        self.client_manager_port = client_manager_port
        self.num_commands = num_commands
        self.client_time_step_len_seconds = client_time_step_len_seconds
        self.time_scaling_factor = time_scaling_factor
        self.period_scaling_factor = period_scaling_factor
        self.client_manager_log_dir = client_manager_log_dir
        self.client_manager_log_file = client_manager_log_file
        self.client_manager_max_workers = client_manager_max_workers

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
            client_process_type=d["client_process_type"],
            lamb=d["lamb"], mu=d["mu"], client_manager_port=d["client_manager_port"],
            num_commands=d["num_commands"], client_time_step_len_seconds=d["client_time_step_len_seconds"],
            period_scaling_factor=d["period_scaling_factor"], time_scaling_factor=d["time_scaling_factor"],
            client_manager_log_dir=d["client_manager_log_dir"], client_manager_log_file=d["client_manager_log_file"],
            client_manager_max_workers=d["client_manager_max_workers"]
        )
        return obj

    def no_clients(self) -> "ClientPopulationConfig":
        """
        :return: A version of the config with no clients
        """
        return ClientPopulationConfig(
            ip=self.ip,
            networks=self.networks,
            client_process_type=self.client_process_type,
            lamb=0, mu=0, client_manager_port=self.client_manager_port,
            num_commands=0, client_time_step_len_seconds=self.client_time_step_len_seconds,
            period_scaling_factor=self.period_scaling_factor, time_scaling_factor=self.time_scaling_factor,
            client_manager_log_file="client_manager.log", client_manager_log_dir="/", client_manager_max_workers=10
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["client_process_type"] = self.client_process_type
        d["lamb"] = self.lamb
        d["mu"] = self.mu
        d["networks"] = list(map(lambda x: x.to_dict(), self.networks))
        d["num_commands"] = self.num_commands
        d["client_manager_port"] = self.client_manager_port
        d["client_time_step_len_seconds"] = self.client_time_step_len_seconds
        d["time_scaling_factor"] = self.time_scaling_factor
        d["period_scaling_factor"] = self.period_scaling_factor
        d["client_manager_log_file"] = self.client_manager_log_file
        d["client_manager_log_dir"] = self.client_manager_log_dir
        d["client_manager_max_workers"] = self.client_manager_max_workers
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, client_population_process_type: {self.client_process_type}, lamb:{self.lamb}, " \
               f"mu:{self.mu}, self.networks:{list(map(lambda x: str(x), self.networks))}, " \
               f"client_manager_port: {self.client_manager_port}, num_commands:{self.num_commands}, " \
               f"client_time_step_len_seconds: {self.client_time_step_len_seconds}," \
               f"time_scaling_factor: {self.time_scaling_factor}, " \
               f"period_scaling_factor: {self.period_scaling_factor}," \
               f"client_manager_log_file: {self.client_manager_log_file}, " \
               f"client_manager_log_dir: {self.client_manager_log_dir}, " \
               f"client_manager_max_workers: {self.client_manager_max_workers}"

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
