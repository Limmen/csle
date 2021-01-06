from typing import List, Tuple, Set
import random
from gym_pycr_pwcrack.dao.network.network_config import NetworkConfig
from gym_pycr_pwcrack.dao.network.node import Node
from gym_pycr_pwcrack.dao.network.node_type import NodeType
from gym_pycr_pwcrack.dao.container_config.node_users_config import NodeUsersConfig
from gym_pycr_pwcrack.dao.container_config.node_flags_config import NodeFlagsConfig
from gym_pycr_pwcrack.dao.container_config.node_vulnerability_config import NodeVulnerabilityConfig
from gym_pycr_pwcrack.dao.container_config.vulnerability_type import VulnType
from gym_pycr_pwcrack.dao.network.flag import Flag
from gym_pycr_pwcrack.dao.network.credential import Credential
from gym_pycr_pwcrack.dao.domain_randomization.randomization_space import RandomizationSpace
from gym_pycr_pwcrack.dao.network.network_service import NetworkService
from gym_pycr_pwcrack.dao.network.vulnerability import Vulnerability
import gym_pycr_pwcrack.constants.constants as constants

class NodeRandomizer:

    @staticmethod
    def randomize(ip: str, reachable: Set[str], id: int, users_config: NodeUsersConfig,
                  flags_config: NodeFlagsConfig, vulns_config: NodeVulnerabilityConfig,
                  r_space: RandomizationSpace,
                  router: bool = False, agent: bool = False, gateway: bool = False):
        id = id
        ip_id = int(ip.rsplit(".", 1)[-1])
        return NodeRandomizer.randomize_server(ip=ip, reachable=reachable, id=id, users_config=users_config,
                                               flags_config=flags_config, vulns_config=vulns_config, r_space=r_space,
                                               gateway=gateway, router = router)
        # if router:
        #     pass
        # elif agent:
        #     pass
        # else:
        #     return NodeRandomizer.randomize_server(ip=ip, reachable=reachable, id=id, users_config=users_config,
        #                                     flags_config=flags_config, vulns_config=vulns_config, r_space=r_space,
        #                                     gateway=gateway)

    @staticmethod
    def randomize_server(ip: str, reachable: Set[str], id: int, users_config: NodeUsersConfig,
                         flags_config: NodeFlagsConfig, vulns_config: NodeVulnerabilityConfig,
                         r_space: RandomizationSpace,
                         gateway: bool = False, router: bool = False) -> Node:
        type = NodeType.SERVER
        flags = NodeRandomizer.parse_flags(flags_conf=flags_config)
        vulns, n_serv, creds, n_roots = NodeRandomizer.generate_required_vulns(vuln_conf=vulns_config, gateway=gateway)
        # if not router:
        #     r_vulns = NodeRandomizer.random_vulnerabilities(vulns=r_space.vulnerabilities, num_vulns=1)
        #     vulns =  vulns + r_vulns
        services = NodeRandomizer.random_services(services=r_space.services, num_services=1)
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
    def perturb(network_conf: NetworkConfig):
        pass

    @staticmethod
    def parse_flags(flags_conf: NodeFlagsConfig) -> List[Flag]:
        flags = []
        if flags_conf is not None:
            for flag in flags_conf.flags:
                path, content, dir, id, requires_root, score = flag
                fl = Flag(name=content, id=id, path=dir, score=score, requires_root=requires_root)
                flags.append(fl)
        return flags

    @staticmethod
    def parse_credentials(users_conf: NodeUsersConfig) -> Tuple[List[Credential], List[str]]:
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
    def random_vulnerabilities(vulns: List[Vulnerability], num_vulns: int) -> List[Vulnerability]:
        if num_vulns > len(vulns):
            sample_vulns = vulns
        else:
            sample_vulns = random.sample(vulns, num_vulns)

        return list(map(lambda x: x.copy(), sample_vulns))

    @staticmethod
    def random_services(services: List[NetworkService], num_services: int) -> List[NetworkService]:
        if num_services > len(services):
            sample_services = services
        else:
            sample_services = random.sample(services, num_services)

        return list(map(lambda x: x.copy(), sample_services))

    @staticmethod
    def random_os(os: List[str]):
        r_idx = random.randint(0, len(os)-1)
        return os[r_idx]

    @staticmethod
    def generate_required_vulns(vuln_conf: NodeVulnerabilityConfig, gateway):
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


