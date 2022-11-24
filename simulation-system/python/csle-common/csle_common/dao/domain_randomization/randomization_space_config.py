from typing import List
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig


class RandomizationSpaceConfig:
    """
    DTO representing a randomization space configuratio
    """

    def __init__(self, emulation_confs: List[EmulationEnvConfig], min_num_nodes: int = 4,
                 max_num_nodes: int = 4, min_num_flags: int = 1, max_num_flags: int = 1,
                 min_num_users: int = 1, max_num_users: int = 1,
                 services=None, vulnerabilities=None, os: str = None,
                 use_base_randomization: bool = False) -> None:
        """
        Creates a randomization space config according to the given parameters

        :param network_confs: the network configurations of the environment
        :param min_num_nodes: the minimum number of nodes in a sampled MDP
        :param max_num_nodes: the maximum number of nodes in a sampled MDP
        :param min_num_flags: the minimum number of flags in a sampled MDP
        :param max_num_flags: the maximum number of flags in a sampled MDP
        :param min_num_users: the minimum number of users in a sampled MDP
        :param max_num_users: the maximum number of users in a sampled MDP
        :param services: the list of possible services to include in the sampled MDP
        :param vulnerabilities: the list of possible vulnerabilities to include in the sampled MDP
        :param os: the list of possible operating systems to include in the sampled MDP
        :param use_base_randomization: boolean flag whether to use a base set of services/vulnerabilities
        :return: the created randomization space
        """
        self.emulation_confs = emulation_confs
        self.min_num_nodes = min_num_nodes
        self.max_num_nodes = max_num_nodes
        self.min_num_flags = min_num_flags
        self.max_num_flags = max_num_flags
        self.min_num_users = min_num_users
        self.services = services
        self.max_num_users = max_num_users
        self.vulnerabilities = vulnerabilities
        self.os = os
        self.use_base_randomization = use_base_randomization

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"min_num_nodes: {self.min_num_nodes}, max_num_nodes: {self.max_num_nodes}, " \
               f"min_num_flags:{self.min_num_flags}, max_num_flags: {self.max_num_flags}, " \
               f"min_num_users: {self.min_num_users}, max_num_users: {self.max_num_users}, " \
               f"services:{list(map(lambda x: str(x), self.services))}," \
               f"vulnerabilities: {list(map(lambda x: str(x), self.vulnerabilities))}, " \
               f"use_base_randomization: {self.use_base_randomization}," \
               f"network_confs:{list(map(lambda x: str(x), self.emulation_confs))}," \
               f"os:{list(map(lambda x: str(x), self.os))}"
