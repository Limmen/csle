from typing import List
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.node import Node
from gym_pycr_ctf.dao.network.flag import Flag
from gym_pycr_ctf.dao.network.node_type import NodeType
from gym_pycr_ctf.dao.network.network_config import NetworkConfig
from gym_pycr_ctf.dao.render.render_config import RenderConfig
from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.action.attacker.attacker_action_config import AttackerActionConfig
from gym_pycr_ctf.dao.action.attacker.attacker_nmap_actions import AttackerNMAPActions
from gym_pycr_ctf.dao.action.attacker.attacker_nikto_actions import AttackerNIKTOActions
from gym_pycr_ctf.dao.action.attacker.attacker_masscan_actions import AttackerMasscanActions
from gym_pycr_ctf.dao.action.attacker.attacker_network_service_actions import AttackerNetworkServiceActions
from gym_pycr_ctf.dao.action.attacker.attacker_shell_actions import AttackerShellActions
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.network.network_service import NetworkService
from gym_pycr_ctf.dao.network.transport_protocol import TransportProtocol
from gym_pycr_ctf.dao.network.vulnerability import Vulnerability
from gym_pycr_ctf.dao.network.credential import Credential
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_pycr_ctf.dao.state_representation.state_type import StateType
import gym_pycr_ctf.constants.constants as constants

class PyCrCTFLevel4Base:
    """
    Base configuration of level 1 of the PyCrCTF environment. (Mainly used when running in simulation mode
    and all the config of the environment have to be hardcoded)
    """
    @staticmethod
    def nodes() -> List[Node]:
        """
        Returns the configuration of all nodes in the environment

        :return: list of node configs
        """
        nodes = [Node(ip="172.18.4.10", ip_id=10, id=1, type=NodeType.ROUTER, flags=[], level=2, services=[],
                      os="linux", vulnerabilities=[], credentials=[
                Credential(username="admin", pw="admin"),
                Credential(username="jessica", pw="water")
            ], reachable_nodes = set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79",
                                  "172.18.4.191", "172.18.4.10"]),
                      root_usernames=["admin"]),
                 Node(ip="172.18.4.2", ip_id=2, id=2, type=NodeType.SERVER, reachable_nodes =
                 set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79", "172.18.4.191", "172.18.4.10"]),
                      flags=[Flag(name="flag2", path="/tmp", id=2, requires_root=False, score=1)], level=3, os="linux",
                      credentials=[
                          Credential(username="admin", pw="test32121"),
                          Credential(username="puppet", pw="puppet"),
                          Credential(username="user1", pw="123123")
                      ],
                      root_usernames=["admin", "user1"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh",
                                         credentials=[
                                             Credential(username="admin", pw="test32121", port=22,
                                                        protocol = TransportProtocol.TCP, service = "ssh"),
                                             Credential(username="puppet", pw="puppet",
                                                        protocol = TransportProtocol.TCP, service = "ssh"),
                                             Credential(username="user1", pw="123123",
                                                        protocol = TransportProtocol.TCP, service = "ssh")
                                         ]),
                          NetworkService(protocol=TransportProtocol.TCP, port=53, name="domain", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=9042, name="cassandra", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=9160, name="cassandra", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=53, name="domain", credentials=[]),
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS, cve=None,
                                        cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
                                        service=constants.SSH.SERVICE_NAME,
                                        credentials=[
                                            Credential(username="puppet", pw="puppet",
                                                       protocol=TransportProtocol.TCP, service=constants.SSH.SERVICE_NAME)
                                        ],
                                        port=22, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2014-9278", cve="CVE-2014-9278", cvss=4.0, credentials=[],
                                        port=22, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8620", cve="CVE-2020-8620", cvss=5.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8617", cve="CVE-2020-8617", cvss=5.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8616", cve="CVE-2020-8616", cvss=5.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2019-6470", cve="CVE-2019-6470", cvss=5.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8623", cve="CVE-2020-8623", cvss=4.3, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8621", cve="CVE-2020-8621", cvss=4.3, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8624", cve="CVE-2020-8624", cvss=4.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8622", cve="CVE-2020-8622", cvss=4.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8619", cve="CVE-2020-8619", cvss=4.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2020-8618", cve="CVE-2020-8618", cvss=4.0, credentials=[],
                                        port=53, protocol=TransportProtocol.TCP)
                      ]
                      ),
                 Node(ip="172.18.4.3", ip_id=3, id=3, type=NodeType.SERVER, os="linux",
                      reachable_nodes = set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79", "172.18.4.191",
                                         "172.18.4.10"]),
                      flags=[Flag(name="flag1", path="/root", id=1, requires_root=True, score=1)], level=3,
                      credentials=[
                          Credential(username="admin", pw="admin"),
                          Credential(username="john", pw="doe"),
                          Credential(username="vagrant", pw="test_pw1")
                      ],
                      root_usernames=["admin", "john"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=23, name="telnet",
                                         credentials=[
                                             Credential(username="admin", pw="admin",
                                                        port=23, protocol=TransportProtocol.TCP, service="telnet"),
                                             Credential(username="john", pw="doe",
                                                        port=23, protocol=TransportProtocol.TCP, service="telnet"),
                                             Credential(username="vagrant", pw="test_pw1",
                                                        port=23, protocol=TransportProtocol.TCP, service="telnet")
                                         ]),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[])
                      ], vulnerabilities=[
                         Vulnerability(name="CVE-2020-15523", cve="CVE-2020-15523", cvss=6.9, credentials=[], port=80,
                                       protocol=TransportProtocol.TCP),
                         Vulnerability(name="CVE-2020-14422", cve="CVE-2020-14422", cvss=4.3, credentials=[], port=80,
                                       protocol=TransportProtocol.TCP),
                         Vulnerability(name=constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS,
                                       cve=None, cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS, credentials=[
                             Credential(username="admin", pw="admin", service=constants.TELNET.SERVICE_NAME)
                         ],
                                       port=23, protocol=TransportProtocol.TCP, service=constants.TELNET.SERVICE_NAME)
                     ]
                      ),
                 Node(ip="172.18.4.21", ip_id=21, id=4, type=NodeType.SERVER, flags=[], level=3, os="linux",
                      credentials=[
                          Credential(username="admin", pw="admin"),
                          Credential(username="test", pw="qwerty"),
                          Credential(username="oracle", pw="abc123")
                      ],
                      root_usernames=["admin", "test"], reachable_nodes = set(["172.18.4.2", "172.18.4.3", "172.18.4.21",
                                                                 "172.18.4.79", "172.18.4.191", "172.18.4.10"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=25, name="smtp", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=2181, name="kafka", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=5432, name="postgresql", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=6667, name="irc", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=9092, name="kafka", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=38969, name="kafka", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=42843, name="kafka", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=123, name="ntp", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=161, name="snmp", credentials=[])
                      ],
                      vulnerabilities=[]),
                 Node(ip="172.18.4.79", ip_id=79, id=5, type=NodeType.SERVER,
                      reachable_nodes = set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79", "172.18.4.191",
                                         "172.18.4.10"]),
                      flags=[Flag(name="flag3", path="/tmp", id=3, requires_root=False, score=1)], level=3,
                      os="linux",
                      credentials=[
                          Credential(username="l_hopital", pw="l_hopital"),
                          Credential(username="euler", pw="euler"),
                          Credential(username="pi", pw="pi")
                      ],
                      root_usernames=["l_hopital", "pi"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=21, name="ftp",
                                         credentials=[
                                             Credential(username="l_hopital", pw="l_hopital",
                                                        port=21, protocol=TransportProtocol.TCP, service="ftp"),
                                             Credential(username="euler", pw="euler",
                                                        port=21, protocol=TransportProtocol.TCP, service="ftp"),
                                             Credential(username="pi", pw="pi",
                                                        port=21, protocol=TransportProtocol.TCP, service="ftp")
                                         ]),
                          NetworkService(protocol=TransportProtocol.TCP, port=79, name="finger", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=8009, name="ajp13", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=8080, name="http", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=10011, name="teamspeak", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=10022, name="teamspeak", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=30033, name="teamspeak", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=27017, name="mongod", credentials=[]),
                      ],
                      vulnerabilities=[
                          Vulnerability(name="CVE-2014-9278", cve="CVE-2014-9278", cvss=4.0, credentials=[],
                                        port=22,
                                        protocol=TransportProtocol.TCP),
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS, cve=None,
                                        cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS, credentials=[
                              Credential(username="pi", pw="pi", service=constants.FTP.SERVICE_NAME)
                          ],
                                        port=21, protocol=TransportProtocol.TCP, service=constants.FTP.SERVICE_NAME)
                      ]
                      ),
                 Node(ip="172.18.4.191", ip_id=191, id=6, type=NodeType.HACKER, flags=[], level=1, services=[],
                      os="linux", vulnerabilities=[], reachable_nodes =set(["172.18.4.2", "172.18.4.3", "172.18.4.21",
                                                                         "172.18.4.79", "172.18.4.191", "172.18.4.10"]),
                      credentials=[
                          Credential(username="agent", pw="agent")
                      ],
                      root_usernames=["agent"])]
        return nodes

    @staticmethod
    def adj_matrix() -> List:
        """
        Returns the adjacency matrix that defines the topology

        :return: adjacency matrix
        """
        adj_matrix = [
            [0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
        ]
        return adj_matrix

    @staticmethod
    def subnet_mask() -> str:
        """
        :return: the subnet mask
        """
        subnet_mask = "172.18.4.0/24"
        return subnet_mask

    @staticmethod
    def num_nodes() -> int:
        """
        :return: num nodes
        """
        return 5

    @staticmethod
    def hacker_ip() -> str:
        """
        :return: the agent's ip
        """
        hacker_ip = "172.18.4.191"
        return hacker_ip

    @staticmethod
    def router_ip() -> str:
        """
        :return: the agent's default gw
        """
        router_ip = "172.18.4.10"
        return router_ip

    @staticmethod
    def flags_lookup() -> str:
        """
        :return: dict with the flags
        """
        flags_lookup = {}
        flags_lookup[("172.18.4.2", "/tmp/flag2")] = Flag(name="flag2", path="/tmp", id=2, requires_root=False, score=1)
        flags_lookup[("172.18.4.3", "/root/flag1")] = Flag(name="flag1", path="/root", id=1, requires_root=True, score=1)
        flags_lookup[("172.18.4.79", "/tmp/flag3")] = Flag(name="flag3", path="/tmp", id=3, requires_root=False, score=1)
        return flags_lookup

    @staticmethod
    def network_conf(generate: bool = False) -> NetworkConfig:
        """
        :return: The network configuration
        """
        nodes = []
        adj_matrix = []
        reachable = set()
        if not generate:
            nodes = PyCrCTFLevel4Base.nodes()
            adj_matrix = PyCrCTFLevel4Base.adj_matrix()
            reachable = PyCrCTFLevel4Base.agent_reachable()
        network_conf = NetworkConfig(subnet_mask=PyCrCTFLevel4Base.subnet_mask(),
                                     nodes=nodes,
                                     adj_matrix=adj_matrix,
                                     flags_lookup = PyCrCTFLevel4Base.flags_lookup(),
                                     agent_reachable=reachable,
                                     vulnerable_nodes = set(["172.18.1.3", "172.18.1.79", "172.18.1.2"]))
        return network_conf

    @staticmethod
    def agent_reachable() -> set():
        reachable = set(["172.18.4.10", "172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79"])
        return reachable

    @staticmethod
    def emulation_config() -> EmulationConfig:
        """
        :return: the default emulation config
        """
        emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
                                         agent_username="agent", agent_pw="agent", server_connection=True,
                                         server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
                                         server_username="kim")
        return emulation_config

    @staticmethod
    def all_actions_conf(num_nodes: int, subnet_mask: str, hacker_ip: str) -> AttackerActionConfig:
        """
        :param num_nodes: max number of nodes to consider (whole subnetwork in most general case)
        :param subnet_mask: subnet mask of the network
        :param hacker_ip: ip of the agent
        :return: the action config
        """
        actions = []

        # Host actions
        for idx in range(num_nodes):
            actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.PING_SCAN(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.UDP_PORT_SCAN(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.TCP_FIN_SCAN(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.TCP_NULL_SCAN(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.TCP_XMAS_TREE_SCAN(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.NMAP_VULNERS(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(AttackerNIKTOActions.NIKTO_WEB_HOST_SCAN(index=idx))
            actions.append(AttackerMasscanActions.MASSCAN_HOST_SCAN(index=idx, subnet=False, host_ip = hacker_ip))
            actions.append(AttackerNMAPActions.FIREWALK(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.HTTP_ENUM(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.HTTP_GREP(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.VULSCAN(index=idx, subnet=False))
            actions.append(AttackerNMAPActions.FINGER(index=idx, subnet=False))

        # Subnet actions
        actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.PING_SCAN(index=num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.UDP_PORT_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.TCP_FIN_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.TCP_NULL_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.TCP_XMAS_TREE_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.NMAP_VULNERS(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerShellActions.FIND_FLAG(index=num_nodes + 1))
        actions.append(AttackerNetworkServiceActions.SERVICE_LOGIN(index=num_nodes + 1))
        actions.append(AttackerMasscanActions.MASSCAN_HOST_SCAN(index=num_nodes + 1, subnet=True,
                                                                host_ip=hacker_ip, ip=subnet_mask))
        actions.append(AttackerNMAPActions.FIREWALK(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.HTTP_ENUM(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.HTTP_GREP(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.VULSCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        actions.append(AttackerNMAPActions.FINGER(num_nodes + 1, ip=subnet_mask, subnet=True))

        actions = sorted(actions, key=lambda x: (x.id.value, x.index))
        nmap_action_ids = [
            AttackerActionId.TCP_SYN_STEALTH_SCAN_HOST, AttackerActionId.TCP_SYN_STEALTH_SCAN_SUBNET,
            AttackerActionId.PING_SCAN_HOST, AttackerActionId.PING_SCAN_SUBNET,
            AttackerActionId.UDP_PORT_SCAN_HOST, AttackerActionId.UDP_PORT_SCAN_SUBNET,
            AttackerActionId.TCP_CON_NON_STEALTH_SCAN_HOST, AttackerActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET,
            AttackerActionId.TCP_FIN_SCAN_HOST, AttackerActionId.TCP_FIN_SCAN_SUBNET,
            AttackerActionId.TCP_NULL_SCAN_HOST, AttackerActionId.TCP_NULL_SCAN_SUBNET,
            AttackerActionId.TCP_XMAS_TREE_SCAN_HOST, AttackerActionId.TCP_XMAS_TREE_SCAN_SUBNET,
            AttackerActionId.OS_DETECTION_SCAN_HOST, AttackerActionId.OS_DETECTION_SCAN_SUBNET,
            AttackerActionId.NMAP_VULNERS_HOST, AttackerActionId.NMAP_VULNERS_SUBNET,
            AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST, AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET,
            AttackerActionId.FIREWALK_HOST, AttackerActionId.FIREWALK_SUBNET,
            AttackerActionId.HTTP_ENUM_HOST, AttackerActionId.HTTP_ENUM_SUBNET,
            AttackerActionId.HTTP_GREP_HOST, AttackerActionId.HTTP_GREP_SUBNET,
            AttackerActionId.VULSCAN_HOST, AttackerActionId.VULSCAN_SUBNET,
            AttackerActionId.FINGER_HOST, AttackerActionId.FINGER_SUBNET
        ]
        network_service_action_ids = [AttackerActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [AttackerActionId.FIND_FLAG]
        nikto_action_ids = [AttackerActionId.NIKTO_WEB_HOST_SCAN]
        masscan_action_ids = [AttackerActionId.MASSCAN_HOST_SCAN, AttackerActionId.MASSCAN_SUBNET_SCAN]
        action_config = AttackerActionConfig(num_indices=num_nodes + 1, actions=actions, nmap_action_ids=nmap_action_ids,
                                             network_service_action_ids=network_service_action_ids,
                                             shell_action_ids=shell_action_ids, nikto_action_ids=nikto_action_ids,
                                             masscan_action_ids=masscan_action_ids)
        return action_config

    @staticmethod
    def render_conf() -> RenderConfig:
        """
        :return: the render config
        """
        render_config = RenderConfig(num_levels = 3, num_nodes_per_level = 4)
        return render_config

    @staticmethod
    def env_config(network_conf : NetworkConfig, action_conf: AttackerActionConfig, emulation_config: EmulationConfig,
                   render_conf: RenderConfig) -> EnvConfig:
        """
        :param network_conf: the network config
        :param action_conf: the action config
        :param emulation_config: the emulation config
        :param render_conf: the render config
        :return: The complete environment config
        """
        env_config = EnvConfig(network_conf=network_conf, attacker_action_conf=action_conf, num_ports=10, num_vuln=10,
                               num_nodes = PyCrCTFLevel4Base.num_nodes(), num_sh=3, render_config=render_conf, env_mode=EnvMode.SIMULATION,
                               emulation_config=emulation_config,
                               simulate_detection=True, detection_reward=10, base_detection_p=0.05,
                               hacker_ip=PyCrCTFLevel4Base.hacker_ip(), state_type=StateType.BASE,
                               router_ip=PyCrCTFLevel4Base.router_ip())
        env_config.ping_scan_miss_p = 0.0
        env_config.udp_port_scan_miss_p = 0.0
        env_config.syn_stealth_scan_miss_p = 0.0
        env_config.os_scan_miss_p = 0.0
        env_config.vulners_miss_p = 0.0
        env_config.num_flags = 3
        env_config.blacklist_ips = ["172.18.4.1", "172.18.4.254"]
        env_config.ids_router = True
        return env_config
