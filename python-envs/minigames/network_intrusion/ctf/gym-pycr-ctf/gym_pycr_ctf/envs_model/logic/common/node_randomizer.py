from typing import List, Tuple, Set
import random
from gym_pycr_ctf.dao.network.network_config import NetworkConfig
from gym_pycr_ctf.dao.network.node import Node
from gym_pycr_ctf.dao.network.node_type import NodeType
from gym_pycr_ctf.dao.container_config.node_users_config import NodeUsersConfig
from gym_pycr_ctf.dao.container_config.node_flags_config import NodeFlagsConfig
from gym_pycr_ctf.dao.container_config.node_vulnerability_config import NodeVulnerabilityConfig
from gym_pycr_ctf.dao.container_config.vulnerability_type import VulnType
from gym_pycr_ctf.dao.network.flag import Flag
from gym_pycr_ctf.dao.network.credential import Credential
from gym_pycr_ctf.dao.domain_randomization.randomization_space import RandomizationSpace
from gym_pycr_ctf.dao.network.network_service import NetworkService
from gym_pycr_ctf.dao.network.vulnerability import Vulnerability
import gym_pycr_ctf.constants.constants as constants


class NodeRandomizer:
    """
    Utility class for randomizing a given node in the infrastructure
    """

    @staticmethod
    def randomize(ip: str, reachable: Set[str], id: int, users_config: NodeUsersConfig,
                  flags_config: NodeFlagsConfig, vulns_config: NodeVulnerabilityConfig,
                  r_space: RandomizationSpace,
                  router: bool = False, agent: bool = False, gateway: bool = False) -> Node:
        """
        Randomizes a node configuration using the specified parameters and configuration space

        :param ip: the ip of the node
        :param reachable: the list of reachable nodes
        :param id: the id of the node
        :param users_config: the configuration of the users
        :param flags_config: the configuration of the flags
        :param vulns_config: the configuration of the vulnerabilities
        :param r_space: the randomization space
        :param router: the router
        :param agent: the agent
        :param gateway: the gateway
        :return: the randomized node
        """
        id = id
        ip_id = int(ip.rsplit(".", 1)[-1])
        node = NodeRandomizer.randomize_server(ip=ip, reachable=reachable, id=id, users_config=users_config,
                                               flags_config=flags_config, vulns_config=vulns_config, r_space=r_space,
                                               gateway=gateway, router = router)
        if agent:
            node.type == NodeType.HACKER
        if router:
            node.type == NodeType.ROUTER
        return node

    @staticmethod
    def randomize_server(ip: str, reachable: Set[str], id: int, users_config: NodeUsersConfig,
                         flags_config: NodeFlagsConfig, vulns_config: NodeVulnerabilityConfig,
                         r_space: RandomizationSpace,
                         gateway: bool = False, router: bool = False) -> Node:
        """
        Randomizes a server node according to the specified parameters and randomization space

        :param ip: the ip of the node
        :param reachable: the list of reachable nodes
        :param id: the id of the node
        :param users_config: the users configuration of the node
        :param flags_config: the flags configuration of the node
        :param vulns_config: the vulnerability configuration of the node
        :param r_space: the randomization space
        :param gateway: the gateway
        :param router: the router
        :return: The randomized node
        """
        type = NodeType.SERVER
        flags = NodeRandomizer.parse_flags(flags_conf=flags_config)
        vulns, n_serv, creds, n_roots = NodeRandomizer.generate_required_vulns(vuln_conf=vulns_config, gateway=gateway)
        if not router:
            vulns_blacklist = constants.EXPLOIT_VULNERABILITES.WEAK_PW_VULNS + constants.EXPLOIT_VULNERABILITES.CVE_VULNS
            vulns_blacklist = vulns_blacklist + list(map(lambda x: x.name, vulns))
            num_vulns = random.randint(0, len(r_space.vulnerabilities)-1)
            r_vulns = NodeRandomizer.random_vulnerabilities(vulns=r_space.vulnerabilities, num_vulns=num_vulns,
                                                            blacklist_vulnerabilities=vulns_blacklist)
            vulns =  vulns + r_vulns
        num_services = random.randint(0, len(r_space.services) - 1)
        services = NodeRandomizer.random_services(services=r_space.services, num_services=num_services,
                                                  blacklist_services=list(map(lambda x: x.name, n_serv)))
        services = services + n_serv
        os = NodeRandomizer.random_os(os=r_space.os)
        credentials, root_usernames = NodeRandomizer.parse_credentials(users_conf=users_config)
        credentials = credentials + creds
        root_usernames = root_usernames + n_roots
        level = 3
        visible = False
        firewall = False
        node = Node(ip=ip, ip_id=int(ip.rsplit(".", 1)[-1]), id=id,
                    type=type, os=os,
                    flags=flags, level=level, vulnerabilities=vulns, services=services,
                    credentials=credentials, root_usernames=root_usernames, visible=visible,
                    reachable_nodes=reachable, firewall=firewall)
        return node

    @staticmethod
    def parse_flags(flags_conf: NodeFlagsConfig) -> List[Flag]:
        """
        Parses the flag configuration

        :param flags_conf:
        :return: a list of the flags
        """
        flags = []
        if flags_conf is not None:
            for flag in flags_conf.flags:
                path, content, dir, id, requires_root, score = flag
                fl = Flag(name=content, id=id, path=dir, score=score, requires_root=requires_root)
                flags.append(fl)
        return flags

    @staticmethod
    def parse_credentials(users_conf: NodeUsersConfig) -> Tuple[List[Credential], List[str]]:
        """
        Parses the credential configuration

        :param users_conf: the user configuration
        :return: (list of credentials, list of users)
        """
        credentials = []
        root_usernames = []
        if users_conf is not None:
            for user in users_conf.users:
                username, pw, root = user
                credential = Credential(username=username, pw=pw, port=None, protocol=None, service=None)
                credentials.append(credential)
                if root:
                    root_usernames.append(username)
        return credentials, root_usernames

    @staticmethod
    def random_vulnerabilities(vulns: List[Vulnerability], num_vulns: int, blacklist_vulnerabilities: List[str]) \
            -> List[Vulnerability]:
        """
        Randomizes the set of vulnerabilities

        :param vulns: the list of vulnerabilities
        :param num_vulns: the number of vulnerabilities
        :param blacklist_vulnerabilities: blacklisted vulnerabilities
        :return: the randomized lsit of vulnerabilities
        """
        vulns = list(filter(lambda x: not x.name in blacklist_vulnerabilities, vulns))
        if num_vulns > len(vulns):
            sample_vulns = vulns
        else:
            sample_vulns = random.sample(vulns, num_vulns)

        return list(map(lambda x: x.copy(), sample_vulns))

    @staticmethod
    def random_services(services: List[NetworkService], num_services: int, blacklist_services: List[str]) \
            -> List[NetworkService]:
        """
        Randomizes the set of services

        :param services: the list of services
        :param num_services: the number of services
        :param blacklist_services: the blacklisted services
        :return: the randomized list of services
        """
        services = list(filter(lambda x: not x.name in blacklist_services, services))
        if num_services > len(services):
            sample_services = services
        else:
            sample_services = random.sample(services, num_services)

        return list(map(lambda x: x.copy(), sample_services))

    @staticmethod
    def random_os(os: List[str]) -> str:
        """
        Randomizes the operating system

        :param os: list of operating systems
        :return: the randomized operating system
        """
        r_idx = random.randint(0, len(os)-1)
        return os[r_idx]

    @staticmethod
    def generate_required_vulns(vuln_conf: NodeVulnerabilityConfig, gateway) \
            -> Tuple[List[NodeVulnerabilityConfig], List[NetworkService], List[Credential], List[str]]:
        """
        Generates the configuration of the required vulnerabilities

        :param vuln_conf: the vulnerability configuration
        :param gateway: the gateway of the node
        :return: vulnerabilities, services, credentials, root_usernames
        """
        if vuln_conf is not None:
            pw_vuln_services, gw_pw_vuln_services = NetworkService.pw_vuln_services()
            if vuln_conf.vuln_type == VulnType.WEAK_PW:
                if not gateway:
                    s_idx = random.randint(0, len(pw_vuln_services)-1)
                    service = pw_vuln_services[s_idx]
                else:
                    s_idx = random.randint(0, len(gw_pw_vuln_services) - 1)
                    service = gw_pw_vuln_services[s_idx]
                credential = Credential(username=vuln_conf.username, pw=vuln_conf.pw, port=service[0].port, protocol=service[0].protocol,
                                        service=service[0].name)
                vuln = Vulnerability(
                    name=service[1], port=service[0].port, credentials=[credential], cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
                    cve=None, service=service[0].name, protocol=service[0].protocol
                )
                service[0].credentials.append(credential)
                root_usernames = []
                if vuln_conf.root:
                    root_usernames.append(credential.username)
                return [vuln], [service[0]], [credential], root_usernames
            else:
                raise ValueError("Vulnerability not recognized")
        else:
            return [], [], [], []


