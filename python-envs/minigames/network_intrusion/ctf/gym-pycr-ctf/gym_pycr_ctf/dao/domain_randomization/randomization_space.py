from typing import List
from gym_pycr_ctf.dao.network.network_service import NetworkService
from gym_pycr_ctf.dao.network.vulnerability import Vulnerability

class RandomizationSpace:
    """
    Object representing a randomization space
    """

    def __init__(self, services: List[NetworkService], vulnerabilities: List[Vulnerability],
                 os: List[str], min_num_nodes: int, max_num_nodes: int, min_num_flags: int, max_num_flags: int,
                 min_num_users: int, max_num_users: int):
        """
        Initializes the randomization space

        :param services: the list of services to randomize
        :param vulnerabilities: the list of vulnerabilities to randomize
        :param os: the operating system
        :param min_num_nodes: the minimum number of nodes for randomization
        :param max_num_nodes: the maximum number of nodes for randomization
        :param min_num_flags: the minimum number of flags for randomization
        :param max_num_flags: the maximum number of flags for randomization
        :param min_num_users: the minimum number of users for randomization
        :param max_num_users: the maximum number of users for randomization
        """
        self.services = services
        self.vulnerabilities = vulnerabilities
        self.os=os
        self.max_num_nodes = max_num_nodes
        self.min_num_nodes = min_num_nodes
        self.min_num_flags = min_num_flags
        self.max_num_flags = max_num_flags
        self.min_num_users = min_num_users
        self.max_num_users = max_num_users

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "services:{}, vulnerabilities:{}, os:{}, max_num_nodes:{}. min_num_nodes:{}, min_num_flags:{}," \
               " max_num_flags:{}, min_num_users:{}, max_num_users:{}".format(
            list(map(lambda x: str(x), self.services)),
            list(map(lambda x: str(x), self.vulnerabilities)),
            list(map(lambda x: str(x), self.os)),
            self.max_num_nodes, self.min_num_nodes, self.min_num_flags, self.max_num_flags, self.min_num_users,
            self.max_num_users
        )

