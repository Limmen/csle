"""
Class representing a node in the network, used for simulations
"""

from typing import List
from gym_pycr_ctf.dao.network.node_type import NodeType
from gym_pycr_ctf.dao.network.flag import Flag
from gym_pycr_ctf.dao.network.vulnerability import Vulnerability
from gym_pycr_ctf.dao.network.network_service import NetworkService
from gym_pycr_ctf.dao.network.credential import Credential

class Node:

    def __init__(self, ip: str, ip_id: int, id : int, type: NodeType, flags: List[Flag], level : int,
                 vulnerabilities : List[Vulnerability], services : List[NetworkService], os : str,
                 credentials : List[Credential], root_usernames : List[str], visible : bool = True,
                 reachable_nodes: List = None, firewall: bool =  False):
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
        self.root_usernames = root_usernames
        self.visible = visible
        self.reachable_nodes = reachable_nodes
        self.firewall = firewall

    def __str__(self):
        return "ip:{}, ip_id:{}, id:{}, type:{}, flags:{}, level:{}, vulnerabilities:{}, services:{}, os:{}," \
               " credentials:{}, root_usernames:{}, visible:{}, reachable_nodes:{}, firewall:{}".format(
            self.ip, self.ip_id, self.id, self.type, list(map(lambda x: str(x), self.flags)), self.level,
            list(map(lambda x: str(x), self.vulnerabilities)), list(map(lambda x: str(x), self.services)),
            self.os, list(map(lambda x: str(x), self.credentials)), self.root_usernames, self.visible,
            self.reachable_nodes, self.firewall
        )
