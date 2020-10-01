from typing import List
from gym_pycr_pwcrack.dao.network.node_type import NodeType
from gym_pycr_pwcrack.dao.network.flag import Flag
from gym_pycr_pwcrack.dao.network.vulnerability import Vulnerability
from gym_pycr_pwcrack.dao.network.network_service import NetworkService
from gym_pycr_pwcrack.dao.network.credential import Credential

class Node:

    def __init__(self, ip: str, ip_id: int, id : int, type: NodeType, flags: List[Flag], level : int,
                 vulnerabilities : List[Vulnerability], services : List[NetworkService], os : str,
                 credentials : List[Credential], root : List[str]):
        self.ip = ip
        self.ip_id = ip_id
        self.id = id
        self.type = type
        self.flags = flags
        self.level = level
        self.vulnerabilities = vulnerabilities
        self.services = services
        self.os = os
        self.credentials = credentials
        self.root = root