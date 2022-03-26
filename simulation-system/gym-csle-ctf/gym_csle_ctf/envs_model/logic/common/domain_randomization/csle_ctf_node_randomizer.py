from typing import List, Tuple, Set
import random
import csle_common.constants.constants as constants
from csle_common.dao.network.node import Node
from csle_common.dao.network.node_type import NodeType
from csle_common.dao.container_config.vulnerability_type import VulnType
from csle_common.dao.network.flag import Flag
from csle_common.dao.network.credential import Credential
from csle_common.dao.network.network_service import NetworkService
from csle_common.dao.network.vulnerability import Vulnerability
from csle_common.dao.container_config.node_users_config import NodeUsersConfig
from csle_common.dao.container_config.node_flags_config import NodeFlagsConfig
from csle_common.dao.container_config.node_vulnerability_config import NodeVulnerabilityConfig
from csle_common.envs_model.logic.domain_randomization.csle_node_randomizer import CSLENodeRandomizer
from gym_csle_ctf.dao.domain_randomization.csle_ctf_node_randomizer_config import CSLECTFNodeRandomizerConfig


class CSLECTFNodeRandomizer(CSLENodeRandomizer):
    """
    Utility class for randomizing a given node in the infrastructure
    """

    @staticmethod
    def randomize(config: CSLECTFNodeRandomizerConfig) -> Node:
        """
        Randomizes a node configuration using the specified parameters and configuration space

        :param config: the config of the node randomization
        :return: the randomized node
        """
        node = CSLECTFNodeRandomizer.randomize_server(config=config)
        if config.agent:
            node.type == NodeType.HACKER
        if config.router:
            node.type == NodeType.ROUTER
        return node

    @staticmethod
    def randomize_server(config: CSLECTFNodeRandomizerConfig) -> Node:
        """
        Randomizes a server node according to the specified parameters and randomization space

        :param config: the config of the node randomization
        :return: The randomized node
        """
        type = NodeType.SERVER
        flags = CSLECTFNodeRandomizer.parse_flags(flags_conf=config.flags_config)
        vulns, n_serv, creds, n_roots = CSLECTFNodeRandomizer.generate_required_vulns(vuln_conf=config.vulns_config,
                                                                                      gateway=config.gateway)
        if not config.router:
            vulns_blacklist = constants.EXPLOIT_VULNERABILITES.WEAK_PW_VULNS + constants.EXPLOIT_VULNERABILITES.CVE_VULNS
            vulns_blacklist = vulns_blacklist + list(map(lambda x: x.name, vulns))
            num_vulns = random.randint(0, len(config.r_space.vulnerabilities)-1)
            r_vulns = CSLECTFNodeRandomizer.random_vulnerabilities(vulns=config.r_space.vulnerabilities,
                                                                   num_vulns=num_vulns,
                                                                   blacklist_vulnerabilities=vulns_blacklist)
            vulns =  vulns + r_vulns
        num_services = random.randint(0, len(config.r_space.services) - 1)
        services = CSLECTFNodeRandomizer.random_services(services=config.r_space.services, num_services=num_services,
                                                         blacklist_services=list(map(lambda x: x.name, n_serv)))
        services = services + n_serv
        os = CSLECTFNodeRandomizer.random_os(os=config.r_space.os)
        credentials, root_usernames = CSLECTFNodeRandomizer.parse_credentials(users_conf=config.users_config)
        credentials = credentials + creds
        root_usernames = root_usernames + n_roots
        level = 3
        visible = False
        firewall = False
        node = Node(ips=config.ip, ip_ids=int(config.ip.rsplit(".", 1)[-1]), id=config.id,
                    type=type, os=os,
                    flags=flags, level=level, vulnerabilities=vulns, services=services,
                    credentials=credentials, root_usernames=root_usernames, visible=visible,
                    reachable_nodes=config.reachable, firewall=firewall)
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
                credential = Credential(username=vuln_conf.username, pw=vuln_conf.pw, port=service[0].kafka_port, protocol=service[0].protocol,
                                        service=service[0].name)
                vuln = Vulnerability(
                    name=service[1], port=service[0].kafka_port, credentials=[credential], cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
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


