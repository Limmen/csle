"""
Class representing a node in the network, used for simulations
"""

from typing import List
from gym_pycr_ctf.dao.network.node_type import NodeType
from gym_pycr_ctf.dao.network.flag import Flag
from gym_pycr_ctf.dao.network.vulnerability import Vulnerability
from gym_pycr_ctf.dao.network.network_service import NetworkService
from gym_pycr_ctf.dao.network.credential import Credential
from gym_pycr_ctf.dao.observation.defender.defender_machine_observation_state import DefenderMachineObservationState
from gym_pycr_ctf.dao.observation.common.port_observation_state import PortObservationState


class Node:
    """
    DTO class that represents a node in the network
    """

    def __init__(self, ip: str, ip_id: int, id : int, type: NodeType, flags: List[Flag], level : int,
                 vulnerabilities : List[Vulnerability], services : List[NetworkService], os : str,
                 credentials : List[Credential], root_usernames : List[str], visible : bool = True,
                 reachable_nodes: List = None, firewall: bool =  False):
        """
        Initializes the DTO

        :param ip: the ip of the node
        :param ip_id: the id of the node's ip
        :param id: the id of the node
        :param type: the type of the node
        :param flags: the set of flags in the node
        :param level: the level of the node
        :param vulnerabilities: the set of vulnerabilities of the node
        :param services: the set of services of the node
        :param os: the operating system of the node
        :param credentials: the list of credentials of the node
        :param root_usernames: the list of root usernames at the node
        :param visible: whether the node is visible or not
        :param reachable_nodes: the set of nodes reachable from this node
        :param firewall: whether this node has a firewall or not
        """
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

    def __str__(self) -> str:
        """
        :return: a string representation of the node
        """
        return "ip:{}, ip_id:{}, id:{}, type:{}, flags:{}, level:{}, vulnerabilities:{}, services:{}, os:{}," \
               " credentials:{}, root_usernames:{}, visible:{}, reachable_nodes:{}, firewall:{}".format(
            self.ip, self.ip_id, self.id, self.type, list(map(lambda x: str(x), self.flags)), self.level,
            list(map(lambda x: str(x), self.vulnerabilities)), list(map(lambda x: str(x), self.services)),
            self.os, list(map(lambda x: str(x), self.credentials)), self.root_usernames, self.visible,
            self.reachable_nodes, self.firewall
        )

    def to_defender_machine_obs(self, service_lookup: dict) -> DefenderMachineObservationState:
        """
        Converts the node to a defender machine observation

        :param service_lookup: a service lookup table
        :return: the defender machine observation
        """
        d_obs = DefenderMachineObservationState(self.ip)
        d_obs.os = self.os
        d_obs.num_flags = len(self.flags)
        d_obs.ports = list(map(lambda x: PortObservationState.from_network_service(x, service_lookup), self.services))
        return d_obs

