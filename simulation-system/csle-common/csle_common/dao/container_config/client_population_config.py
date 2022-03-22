from typing import List
from csle_common.dao.container_config.client_population_process_type import ClientPopulationProcessType
from csle_common.dao.container_config.container_network import ContainerNetwork


class ClientPopulationConfig:
    """
    A DTO object representing the configuration of the client population of an emulation
    """

    def __init__(self, ip: str, networks: List[ContainerNetwork], client_process_type: ClientPopulationProcessType,
                 lamb: float, mu: float, client_manager_port: int, num_commands: int = 5,
                 client_time_step_len_seconds: int = 1):
        """
        Creates a ClientPopulationConfig DTO Object

        :param ip: the ip of the client container
        :param networks: a list of networks in the emulation that are accessible for external networks
        :param client_process_type: the type of client arrival process (e.g. a Poisson process)
        :param lamb: the lambda parameter of the arrival process
        :param mu: the service-time parameter of the arrivals
        :param client_time_step_len_seconds: time-step length to measure the arrival process
        """
        self.networks = networks
        self.ip = ip
        self.client_process_type = client_process_type
        self.lamb = lamb
        self.mu = mu
        self.client_manager_port = client_manager_port
        self.num_commands = num_commands
        self.client_time_step_len_seconds = client_time_step_len_seconds


    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["client_population_process_type"] = self.client_process_type.name
        d["lamb"] = self.lamb
        d["mu"] = self.mu
        d["networks"] = list(map(lambda x: x.to_dict(), self.networks))
        d["num_commands"] = self.num_commands
        d["client_manager_port"] = self.client_manager_port
        d["client_time_step_len_seconds"] = self.client_time_step_len_seconds
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, client_population_process_type: {self.client_process_type.name}, lamb:{self.lamb}, " \
               f"mu:{self.mu}, self.networks:{list(map(lambda x: str(x), self.networks))}, " \
               f"client_manager_port: {self.client_manager_port}, num_commands:{self.num_commands}, " \
               f"client_time_step_len_seconds: {self.client_time_step_len_seconds}"