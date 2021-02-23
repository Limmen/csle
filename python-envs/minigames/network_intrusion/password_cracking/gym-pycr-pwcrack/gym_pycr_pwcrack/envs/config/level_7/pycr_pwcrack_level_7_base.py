from typing import List
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.network.node import Node
from gym_pycr_pwcrack.dao.network.flag import Flag
from gym_pycr_pwcrack.dao.network.node_type import NodeType
from gym_pycr_pwcrack.dao.network.network_config import NetworkConfig
from gym_pycr_pwcrack.dao.render.render_config import RenderConfig
from gym_pycr_pwcrack.dao.network.env_mode import EnvMode
from gym_pycr_pwcrack.dao.action.action_config import ActionConfig
from gym_pycr_pwcrack.dao.action.nmap_actions import NMAPActions
from gym_pycr_pwcrack.dao.action.nikto_actions import NIKTOActions
from gym_pycr_pwcrack.dao.action.masscan_actions import MasscanActions
from gym_pycr_pwcrack.dao.action.network_service_actions import NetworkServiceActions
from gym_pycr_pwcrack.dao.action.shell_actions import ShellActions
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.network.network_service import NetworkService
from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.dao.network.vulnerability import Vulnerability
from gym_pycr_pwcrack.dao.network.credential import Credential
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.state_representation.state_type import StateType
import gym_pycr_pwcrack.constants.constants as constants

class PyCrPwCrackLevel7Base:
    """
    Base configuration of level 1 of the PyCrPwCrack environment. (Mainly used when running in simulation mode
    and all the config of the environment have to be hardcoded)
    """
    @staticmethod
    def nodes() -> List[Node]:
        """
        Returns the configuration of all nodes in the environment

        :return: list of node configs
        """
        nodes = [Node(ip="172.18.7.10", ip_id=10, id=1, type=NodeType.ROUTER, flags=[], level=2, services=[],
                      os="linux", vulnerabilities=[], credentials=[
                Credential(username="admin", pw="admin"),
                Credential(username="jessica", pw="water")
            ], reachable_nodes = set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79",
                                      "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.31", "172.18.7.42",
                                      "172.18.7.37", "172.18.7.82"]),
                      root_usernames=["admin"]),
                 Node(ip="172.18.7.2", ip_id=2, id=2, type=NodeType.SERVER, reachable_nodes =
                 set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191", "172.18.7.10",
                      "172.18.7.19", "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82"]),
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
                 Node(ip="172.18.7.3", ip_id=3, id=3, type=NodeType.SERVER, os="linux",
                      reachable_nodes = set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                         "172.18.7.10", "172.18.7.19", "172.18.7.31", "172.18.7.42", "172.18.7.37",
                                             "172.18.7.82"]),
                      flags=[Flag(name="flag1", path="/root", id=1, requires_root=True, score=1)], level=3,
                      credentials=[
                          Credential(username="admin", pw="admin"),
                          Credential(username="john", pw="doe"),
                          Credential(username="vagrant", pw="test_pw1")
                      ],
                      root_usernames=["admin", "john"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
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
                 Node(ip="172.18.7.21", ip_id=21, id=4, type=NodeType.SERVER, flags=[], level=3, os="linux",
                      credentials=[
                          Credential(username="admin", pw="admin"),
                          Credential(username="test", pw="qwerty"),
                          Credential(username="oracle", pw="abc123")
                      ],
                      root_usernames=["admin", "test"],
                      reachable_nodes = set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                             "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19",
                                             "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
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
                 Node(ip="172.18.7.79", ip_id=79, id=5, type=NodeType.SERVER,
                      reachable_nodes = set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                         "172.18.7.10", "172.18.7.19", "172.18.7.31", "172.18.7.42", "172.18.7.37",
                                             "172.18.7.82"]),
                      flags=[Flag(name="flag3", path="/tmp", id=3, requires_root=False, score=1)], level=3,
                      os="linux",
                      credentials=[
                          Credential(username="l_hopital", pw="l_hopital"),
                          Credential(username="euler", pw="euler"),
                          Credential(username="pi", pw="pi")
                      ],
                      root_usernames=["l_hopital", "pi"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
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
                 Node(ip="172.18.7.19", ip_id=19, id=6, type=NodeType.SERVER,
                      flags=[Flag(name="flag4", path="/tmp", id=4, requires_root=False, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="karl", pw="gustaf"),
                          Credential(username="steven", pw="carragher")
                      ],
                      root_usernames=["karl"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=139, name="netbios-ssn", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=445, name="microsoft-ds", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=123, name="ntp", credentials=[])
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.SAMBACRY_EXPLOIT,
                                        cve=constants.EXPLOIT_VULNERABILITES.SAMBACRY_EXPLOIT, cvss=9.8,
                                        credentials=[
                                            Credential(username=constants.SAMBA.USER, pw=constants.SAMBA.PW,
                                                       service=constants.SAMBA.SERVICE_NAME)
                                        ],
                                        port=constants.SAMBA.PORT,
                                        protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.31", ip_id=31, id=7, type=NodeType.SERVER,
                      flags=[Flag(name="flag5", path="/tmp", id=5, requires_root=False, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="stefan", pw="zweig")
                      ],
                      root_usernames=["stefan"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[])
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.SHELLSHOCK_EXPLOIT,
                                        cve=constants.EXPLOIT_VULNERABILITES.SHELLSHOCK_EXPLOIT, cvss=9.8,
                                        credentials=[
                                            Credential(username=constants.SHELLSHOCK.BACKDOOR_USER,
                                                       pw=constants.SHELLSHOCK.BACKDOOR_PW,
                                                       service=constants.SHELLSHOCK.SERVICE_NAME)
                                        ],
                                        port=constants.SHELLSHOCK.PORT,
                                        protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.42", ip_id=42, id=8, type=NodeType.SERVER,
                      flags=[Flag(name="flag6", path="/tmp", id=6, requires_root=False, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="roy", pw="neruda"),
                          Credential(username="pablo", pw="0d107d09f5bbe40cade3de5c71e9e9b7")
                      ],
                      root_usernames=["pablo"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[])
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.DVWA_SQL_INJECTION,
                                        cve=constants.EXPLOIT_VULNERABILITES.DVWA_SQL_INJECTION, cvss=9.5,
                                        credentials=[
                                            Credential(username="pablo", pw="0d107d09f5bbe40cade3de5c71e9e9b7",
                                                       service="http")
                                        ],
                                        port=80, protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.37", ip_id=37, id=9, type=NodeType.SERVER,
                      flags=[Flag(name="flag7", path="/tmp", id=7, requires_root=False, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="john", pw="conway"),
                      ],
                      root_usernames=["john"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=21, name="ftp", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=161, name="snmp", credentials=[])
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.CVE_2015_3306,
                                        cve=constants.EXPLOIT_VULNERABILITES.CVE_2015_3306, cvss=9.8,
                                        credentials=[
                                            Credential(username=constants.CVE_2015_3306.BACKDOOR_USER,
                                                       pw=constants.CVE_2015_3306.BACKDOOR_PW,
                                                       service=constants.CVE_2015_3306.SERVICE_NAME)
                                        ],
                                        port=21, protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.82", ip_id=82, id=10, type=NodeType.SERVER,
                      flags=[Flag(name="flag8", path="/tmp", id=8, requires_root=False, score=1)],
                      level=3, os="linux",
                      credentials=[
                          Credential(username="john", pw="nash"),
                      ],
                      root_usernames=["john"],
                      reachable_nodes=set(["172.18.7.2", "172.18.7.3", "172.18.7.21",
                                           "172.18.7.79", "172.18.7.191", "172.18.7.10", "172.18.7.19", "172.18.7.21",
                                           "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82"]),
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                          NetworkService(protocol=TransportProtocol.TCP, port=9300, name="vrace", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=9200, name="wap-wsp", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=161, name="snmp", credentials=[])
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.CVE_2015_3306,
                                        cve=constants.EXPLOIT_VULNERABILITES.CVE_2015_3306, cvss=9.8,
                                        credentials=[
                                            Credential(username=constants.CVE_2015_3306.BACKDOOR_USER,
                                                       pw=constants.CVE_2015_3306.BACKDOOR_PW,
                                                       service=constants.CVE_2015_3306.SERVICE_NAME)
                                        ],
                                        port=21, protocol=TransportProtocol.TCP)
                      ]),
                 Node(ip="172.18.7.191", ip_id=191, id=11, type=NodeType.HACKER, flags=[], level=1, services=[],
                      os="linux", vulnerabilities=[],
                      reachable_nodes =set(["172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79", "172.18.7.191",
                                            "172.18.7.10", "172.18.7.19", "172.18.7.31", "172.18.7.42", "172.18.7.37",
                                            "172.18.7.82"]),
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
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        return adj_matrix

    @staticmethod
    def subnet_mask() -> str:
        """
        :return: the subnet mask
        """
        subnet_mask = "172.18.7.0/24"
        return subnet_mask

    @staticmethod
    def num_nodes() -> int:
        """
        :return: num nodes
        """
        return 10

    @staticmethod
    def hacker_ip() -> str:
        """
        :return: the agent's ip
        """
        hacker_ip = "172.18.7.191"
        return hacker_ip

    @staticmethod
    def router_ip() -> str:
        """
        :return: the agent's default gw
        """
        router_ip = "172.18.7.10"
        return router_ip

    @staticmethod
    def flags_lookup() -> str:
        """
        :return: dict with the flags
        """
        flags_lookup = {}
        flags_lookup[("172.18.7.2", "/tmp/flag2")] = Flag(name="flag2", path="/tmp", id=2, requires_root=False, score=1)
        flags_lookup[("172.18.7.3", "/root/flag1")] = Flag(name="flag1", path="/root", id=1, requires_root=True, score=1)
        flags_lookup[("172.18.7.79", "/tmp/flag3")] = Flag(name="flag3", path="/tmp", id=3, requires_root=False, score=1)
        flags_lookup[("172.18.7.19", "/tmp/flag4")] = Flag(name="flag4", path="/tmp", id=4, requires_root=False, score=1)
        flags_lookup[("172.18.7.31", "/tmp/flag5")] = Flag(name="flag5", path="/tmp", id=5, requires_root=False, score=1)
        flags_lookup[("172.18.7.42", "/tmp/flag6")] = Flag(name="flag6", path="/tmp", id=6, requires_root=False, score=1)
        flags_lookup[("172.18.7.37", "/tmp/flag7")] = Flag(name="flag7", path="/tmp", id=7, requires_root=False, score=1)
        flags_lookup[("172.18.7.82", "/tmp/flag8")] = Flag(name="flag8", path="/tmp", id=8, requires_root=False, score=1)
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
            nodes = PyCrPwCrackLevel7Base.nodes()
            adj_matrix = PyCrPwCrackLevel7Base.adj_matrix()
            reachable = PyCrPwCrackLevel7Base.agent_reachable()
        network_conf = NetworkConfig(subnet_mask=PyCrPwCrackLevel7Base.subnet_mask(),
                                     nodes=nodes,
                                     adj_matrix=adj_matrix,
                                     flags_lookup = PyCrPwCrackLevel7Base.flags_lookup(),
                                     agent_reachable=reachable,
                                     vulnerable_nodes = set(["172.18.7.3", "172.18.7.79", "172.18.7.2", "172.18.7.19",
                                                             "172.18.7.31", "172.18.7.42", "172.18.7.37",
                                                             "172.18.7.82"]))
        return network_conf

    @staticmethod
    def agent_reachable() -> set():
        reachable = set(["172.18.7.10", "172.18.7.2", "172.18.7.3", "172.18.7.21", "172.18.7.79","172.18.7.19",
                         "172.18.7.31", "172.18.7.42", "172.18.7.37", "172.18.7.82"])
        return reachable

    @staticmethod
    def cluster_conf() -> ClusterConfig:
        """
        :return: the default cluster config
        """
        cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.7.191",
                                       agent_username="agent", agent_pw="agent", server_connection=True,
                                       server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
                                       server_username="kim")
        return cluster_config

    @staticmethod
    def all_actions_conf(num_nodes: int, subnet_mask: str, hacker_ip: str) -> ActionConfig:
        """
        :param num_nodes: max number of nodes to consider (whole subnetwork in most general case)
        :param subnet_mask: subnet mask of the network
        :param hacker_ip: ip of the agent
        :return: the action config
        """
        actions = []

        # Host actions
        for idx in range(num_nodes):
            actions.append(NMAPActions.TCP_SYN_STEALTH_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.PING_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.UDP_PORT_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.TCP_CON_NON_STEALTH_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.TCP_FIN_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.TCP_NULL_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.TCP_XMAS_TREE_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.OS_DETECTION_SCAN(index=idx, subnet=False))
            actions.append(NMAPActions.NMAP_VULNERS(index=idx, subnet=False))
            actions.append(NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            actions.append(NIKTOActions.NIKTO_WEB_HOST_SCAN(index=idx))
            actions.append(MasscanActions.MASSCAN_HOST_SCAN(index=idx, subnet=False, host_ip = hacker_ip))
            actions.append(NMAPActions.FIREWALK(index=idx, subnet=False))
            actions.append(NMAPActions.HTTP_ENUM(index=idx, subnet=False))
            actions.append(NMAPActions.HTTP_GREP(index=idx, subnet=False))
            actions.append(NMAPActions.VULSCAN(index=idx, subnet=False))
            actions.append(NMAPActions.FINGER(index=idx, subnet=False))
            actions.append(ShellActions.SAMBACRY_EXPLOIT(index=idx))
            actions.append(ShellActions.SHELLSHOCK_EXPLOIT(index=idx))
            actions.append(ShellActions.DVWA_SQL_INJECTION(index=idx))
            actions.append(ShellActions.CVE_2015_3306_EXPLOIT(index=idx))
            actions.append(ShellActions.CVE_2015_1427_EXPLOIT(index=idx))

        # Subnet actions
        actions.append(NMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.PING_SCAN(index=num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.UDP_PORT_SCAN(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.TCP_CON_NON_STEALTH_SCAN(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.TCP_FIN_SCAN(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.TCP_NULL_SCAN(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.TCP_XMAS_TREE_SCAN(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.OS_DETECTION_SCAN(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.NMAP_VULNERS(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.IRC_SAME_USER_PASS_DICTIONARY(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(ShellActions.FIND_FLAG(index=num_nodes+1))
        actions.append(NetworkServiceActions.SERVICE_LOGIN(index=num_nodes+1))
        actions.append(MasscanActions.MASSCAN_HOST_SCAN(index=num_nodes+1, subnet=True,
                                                        host_ip=hacker_ip, ip=subnet_mask))
        actions.append(NMAPActions.FIREWALK(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.HTTP_ENUM(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.HTTP_GREP(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.VULSCAN(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.FINGER(num_nodes+1, ip=subnet_mask, subnet=True))

        actions = sorted(actions, key=lambda x: (x.id.value, x.index))
        nmap_action_ids = [
            ActionId.TCP_SYN_STEALTH_SCAN_HOST, ActionId.TCP_SYN_STEALTH_SCAN_SUBNET,
            ActionId.PING_SCAN_HOST, ActionId.PING_SCAN_SUBNET,
            ActionId.UDP_PORT_SCAN_HOST, ActionId.UDP_PORT_SCAN_SUBNET,
            ActionId.TCP_CON_NON_STEALTH_SCAN_HOST, ActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET,
            ActionId.TCP_FIN_SCAN_HOST, ActionId.TCP_FIN_SCAN_SUBNET,
            ActionId.TCP_NULL_SCAN_HOST, ActionId.TCP_NULL_SCAN_SUBNET,
            ActionId.TCP_XMAS_TREE_SCAN_HOST, ActionId.TCP_XMAS_TREE_SCAN_SUBNET,
            ActionId.OS_DETECTION_SCAN_HOST, ActionId.OS_DETECTION_SCAN_SUBNET,
            ActionId.NMAP_VULNERS_HOST, ActionId.NMAP_VULNERS_SUBNET,
            ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST, ActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST, ActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST, ActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST, ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST, ActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST, ActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST, ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST, ActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST, ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET,
            ActionId.FIREWALK_HOST, ActionId.FIREWALK_SUBNET,
            ActionId.HTTP_ENUM_HOST, ActionId.HTTP_ENUM_SUBNET,
            ActionId.HTTP_GREP_HOST, ActionId.HTTP_GREP_SUBNET,
            ActionId.VULSCAN_HOST, ActionId.VULSCAN_SUBNET,
            ActionId.FINGER_HOST, ActionId.FINGER_SUBNET
        ]
        network_service_action_ids = [ActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [ActionId.FIND_FLAG, ActionId.SAMBACRY_EXPLOIT, ActionId.SHELLSHOCK_EXPLOIT,
                            ActionId.DVWA_SQL_INJECTION, ActionId.CVE_2015_3306_EXPLOIT, ActionId.CVE_2015_1427_EXPLOIT]
        nikto_action_ids = [ActionId.NIKTO_WEB_HOST_SCAN]
        masscan_action_ids = [ActionId.MASSCAN_HOST_SCAN, ActionId.MASSCAN_SUBNET_SCAN]
        action_config = ActionConfig(num_indices=num_nodes+1, actions=actions, nmap_action_ids=nmap_action_ids,
                                     network_service_action_ids=network_service_action_ids,
                                     shell_action_ids=shell_action_ids, nikto_action_ids=nikto_action_ids,
                                     masscan_action_ids=masscan_action_ids)
        return action_config

    @staticmethod
    def render_conf() -> RenderConfig:
        """
        :return: the render config
        """
        render_config = RenderConfig(num_levels = 3, num_nodes_per_level = 9)
        return render_config

    @staticmethod
    def env_config(network_conf : NetworkConfig, action_conf: ActionConfig, cluster_conf: ClusterConfig,
                   render_conf: RenderConfig) -> EnvConfig:
        """
        :param network_conf: the network config
        :param action_conf: the action config
        :param cluster_conf: the cluster config
        :param render_conf: the render config
        :return: The complete environment config
        """
        env_config = EnvConfig(network_conf=network_conf, action_conf=action_conf, num_ports=10, num_vuln=10,
                               num_nodes = PyCrPwCrackLevel7Base.num_nodes(), num_sh=3, render_config=render_conf, env_mode=EnvMode.SIMULATION,
                               cluster_config=cluster_conf,
                               simulate_detection=True, detection_reward=10, base_detection_p=0.05,
                               hacker_ip=PyCrPwCrackLevel7Base.hacker_ip(), state_type=StateType.BASE,
                               router_ip=PyCrPwCrackLevel7Base.router_ip())
        env_config.ping_scan_miss_p = 0.0
        env_config.udp_port_scan_miss_p = 0.0
        env_config.syn_stealth_scan_miss_p = 0.0
        env_config.os_scan_miss_p = 0.0
        env_config.vulners_miss_p = 0.0
        env_config.num_flags = 8
        env_config.blacklist_ips = ["172.18.7.1"]
        env_config.ids_router = True
        return env_config
