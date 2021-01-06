from typing import List
from gym_pycr_pwcrack.dao.network.network_service import NetworkService
from gym_pycr_pwcrack.dao.network.vulnerability import Vulnerability

class RandomizationSpace:

    def __init__(self, services: List[NetworkService], vulnerabilities: List[Vulnerability],
                 os: List[str], min_num_nodes: int, max_num_nodes: int, min_num_flags: int, max_num_flags: int,
                 min_num_users: int, max_num_users: int):
        self.services = services
        self.vulnerabilities = vulnerabilities
        self.os=os
        self.max_num_nodes = max_num_nodes
        self.min_num_nodes = min_num_nodes
        self.min_num_flags = min_num_flags
        self.max_num_flags = max_num_flags
        self.min_num_users = min_num_users
        self.max_num_users = max_num_users

    def __str__(self):
        return "services:{}, vulnerabilities:{}, os:{}, max_num_nodes:{}. min_num_nodes:{}, min_num_flags:{}," \
               " max_num_flags:{}, min_num_users:{}, max_num_users:{}".format(
            list(map(lambda x: str(x), self.services)),
            list(map(lambda x: str(x), self.vulnerabilities)),
            list(map(lambda x: str(x), self.os)),
            self.max_num_nodes, self.min_num_nodes, self.min_num_flags, self.max_num_flags, self.min_num_users,
            self.max_num_users
        )

