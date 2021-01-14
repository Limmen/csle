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

class PyCrPwCrackLevel2Base:
    """
    Base configuration of level 2 of the PyCrPwCrack environment. (Mainly used when running in simulation mode
    and all the config of the environment have to be hardcoded)
    """
    @staticmethod
    def nodes() -> List[Node]:
        """
        Returns the configuration of all nodes in the environment

        :return: list of node configs
        """
        nodes = [Node(ip="172.18.2.10", ip_id=10, id=1, type=NodeType.ROUTER, flags=[], level=2, services=[],
                      reachable_nodes=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                  "172.18.2.191", "172.18.2.10"]),
                      os="linux", vulnerabilities=[], credentials=[
                Credential(username="admin", pw="admin1235912"),
                Credential(username="jessica", pw="water")
            ], firewall=True,
                      root_usernames=["admin"]),
                 Node(ip="172.18.2.2", ip_id=2, id=2, type=NodeType.SERVER,
                      reachable_nodes=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                       "172.18.2.191", "172.18.2.10", "172.18.2.54"]),
                      flags=[Flag(name="flag2", path="/tmp", id=2, requires_root=False, score=1)], level=3, os="linux",
                      credentials=[
                          Credential(username="admin", pw="test32121"),
                          Credential(username="puppet", pw="puppet"),
                          Credential(username="user1", pw="123123")
                      ],
                      firewall=True,
                      root_usernames=["puppet", "user1"],
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
                                                       protocol=TransportProtocol.TCP,
                                                       service=constants.SSH.SERVICE_NAME)
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
                 Node(ip="172.18.2.3", ip_id=3, id=3, type=NodeType.SERVER, os="linux",
                      reachable_nodes=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                       "172.18.2.191", "172.18.2.10", "172.18.2.74", "172.18.2.61"]),
                      flags=[Flag(name="flag1", path="/root", id=1, requires_root=True, score=1)], level=3,
                      credentials=[
                          Credential(username="admin", pw="admin"),
                          Credential(username="john", pw="doe"),
                          Credential(username="vagrant", pw="test_pw1")
                      ],
                      firewall=True,
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
                         Vulnerability(name=constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS, cve=None,
                                       cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS, credentials=[
                             Credential(username="admin", pw="admin", service=constants.TELNET.SERVICE_NAME)
                         ],
                                       port=23, protocol=TransportProtocol.TCP, service=constants.TELNET.SERVICE_NAME)
                     ]
                      ),
                 Node(ip="172.18.2.21", ip_id=21, id=4, type=NodeType.SERVER, flags=[], level=3, os="linux",
                      reachable_nodes=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                       "172.18.2.191", "172.18.2.10"]),
                      credentials=[
                          Credential(username="admin", pw="admin31151x"),
                          Credential(username="test", pw="qwerty"),
                          Credential(username="oracle", pw="abc123")
                      ],
                      root_usernames=["admin", "test"],
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
                 Node(ip="172.18.2.79", ip_id=79, id=5, type=NodeType.SERVER,
                      reachable_nodes=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                       "172.18.2.191", "172.18.2.10"]),
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
                 Node(ip="172.18.2.54", ip_id=54, id=6, type=NodeType.SERVER,
                      reachable_nodes=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                       "172.18.2.191", "172.18.2.10", "172.18.2.54"]),
                      flags=[Flag(name="flag4", path="/tmp", id=4, requires_root=False, score=1)], level=4, os="linux",
                      credentials=[
                          Credential(username="vagrant", pw="vagrant"),
                          Credential(username="trent", pw="xe125@41!341")
                      ],
                      root_usernames=["vagrant"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh",
                                         credentials=[
                                             Credential(username="vagrant", pw="vagrant", port=22,
                                                        protocol=TransportProtocol.TCP, service="ssh"),
                                             Credential(username="trent", pw="xe125@41!341",
                                                        protocol=TransportProtocol.TCP, service="ssh")
                                         ]),
                          NetworkService(protocol=TransportProtocol.TCP, port=53, name="domain", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=123, name="ntp", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=53, name="domain", credentials=[]),
                      ],
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS,
                                        cve=None, cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
                                        service=constants.SSH.SERVICE_NAME,
                                        credentials=[
                                            Credential(username="vagrant", pw="vagrant",
                                                       protocol=TransportProtocol.TCP,
                                                       service=constants.SSH.SERVICE_NAME)
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

                 Node(ip="172.18.2.74", ip_id=74, id=7, type=NodeType.SERVER,
                      reachable_nodes=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                       "172.18.2.191", "172.18.2.10", "172.18.2.61", "172.18.2.74",
                                       "172.18.2.101", "172.18.2.62"]),
                      flags=[], level=4, os="linux",
                      credentials=[
                          Credential(username="administrator", pw="administrator"),
                      ],
                      root_usernames=["administrator"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh",
                                         credentials=[
                                             Credential(username="administrator", pw="administrator", port=22,
                                                        protocol=TransportProtocol.TCP, service="ssh")
                                         ]),
                          NetworkService(protocol=TransportProtocol.TCP, port=6667, name="irc", credentials=[])
                      ],
                      firewall=True,
                      vulnerabilities=[
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS, cve=None,
                                        cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
                                        service=constants.SSH.SERVICE_NAME,
                                        credentials=[
                                            Credential(username="administrator", pw="administrator",
                                                       protocol=TransportProtocol.TCP,
                                                       service=constants.SSH.SERVICE_NAME)
                                        ],
                                        port=22, protocol=TransportProtocol.TCP),
                          Vulnerability(name="CVE-2014-9278", cve="CVE-2014-9278", cvss=4.0, credentials=[],
                                        port=22, protocol=TransportProtocol.TCP)
                      ]
                      ),

                 Node(ip="172.18.2.61", ip_id=61, id=8, type=NodeType.SERVER, os="linux",
                      reachable_nodes=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                       "172.18.2.191", "172.18.2.10", "172.18.2.61", "172.18.2.74"]),
                      flags=[Flag(name="flag5", path="/root", id=5, requires_root=True, score=1)], level=4,
                      credentials=[
                          Credential(username="adm", pw="adm")
                      ],
                      root_usernames=["adm"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=23, name="telnet",
                                         credentials=[
                                             Credential(username="adm", pw="adm",
                                                        port=23, protocol=TransportProtocol.TCP, service="telnet")
                                         ]),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=26257, name="cockroachdb", credentials=[])
                      ], vulnerabilities=[
                         Vulnerability(name=constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS, cve=None,
                                       cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS, credentials=[
                             Credential(username="adm", pw="adm", service=constants.TELNET.SERVICE_NAME)
                         ], port=23, protocol=TransportProtocol.TCP, service=constants.TELNET.SERVICE_NAME)
                     ]
                      ),

                 Node(ip="172.18.2.62", ip_id=62, id=9, type=NodeType.SERVER, os="linux",
                      reachable_nodes=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                       "172.18.2.191", "172.18.2.10", "172.18.2.61", "172.18.2.74",
                                       "172.18.2.101", "172.18.2.62", "172.18.2.7"]),
                      flags=[], level=5,
                      credentials=[
                          Credential(username="guest", pw="guest")
                      ],
                      root_usernames=["guest"],
                      firewall=True,
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=23, name="telnet",
                                         credentials=[
                                             Credential(username="guest", pw="guest",
                                                        port=23, protocol=TransportProtocol.TCP, service="telnet")
                                         ]),
                          NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=5432, name="postgresql", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=8080, name="http", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=4848, name="glassfish", credentials=[])
                      ], vulnerabilities=[
                         Vulnerability(name=constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS, cve=None,
                                       cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS, credentials=[
                             Credential(username="guest", pw="guest", service=constants.TELNET.SERVICE_NAME)
                         ], port=23, protocol=TransportProtocol.TCP, service=constants.TELNET.SERVICE_NAME)
                     ]
                      ),

                 Node(ip="172.18.2.101", ip_id=101, id=10, type=NodeType.SERVER, flags=[], level=5, os="linux",
                      reachable_nodes=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                       "172.18.2.191", "172.18.2.10", "172.18.2.61", "172.18.2.74",
                                       "172.18.2.101", "172.18.2.62"]),
                      credentials=[
                          Credential(username="zidane", pw="1b12ha9")
                      ],
                      root_usernames=["zidane"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=2181, name="kafka", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=5432, name="postgresql", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=6667, name="irc", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=123, name="ntp", credentials=[]),
                          NetworkService(protocol=TransportProtocol.UDP, port=161, name="snmp", credentials=[])
                      ],
                      vulnerabilities=[]),

                 Node(ip="172.18.2.7", ip_id=7, id=11, type=NodeType.SERVER,
                      reachable_nodes=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                       "172.18.2.191", "172.18.2.10", "172.18.2.61", "172.18.2.74",
                                       "172.18.2.101", "172.18.2.62", "172.18.2.7"]),
                      flags=[Flag(name="flag6", path="/tmp", id=6, requires_root=False, score=1)], level=6,
                      os="linux",
                      credentials=[
                          Credential(username="ec2-user", pw="ec2-user"),
                          Credential(username="zlatan", pw="pi12195e"),
                          Credential(username="kennedy", pw="eul1145x")
                      ],
                      root_usernames=["ec2-user", "zlatan"],
                      services=[
                          NetworkService(protocol=TransportProtocol.TCP, port=21, name="ftp",
                                         credentials=[
                                             Credential(username="ec2-user", pw="ec2-user",
                                                        port=21, protocol=TransportProtocol.TCP, service="ftp"),
                                             Credential(username="zlatan", pw="pi12195e",
                                                        port=21, protocol=TransportProtocol.TCP, service="ftp"),
                                             Credential(username="kennedy", pw="eul1145x",
                                                        port=21, protocol=TransportProtocol.TCP, service="ftp")
                                         ]),
                          NetworkService(protocol=TransportProtocol.TCP, port=79, name="finger", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=8080, name="http", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=26257, name="cockroachdb", credentials=[]),
                          NetworkService(protocol=TransportProtocol.TCP, port=2181, name="kafka", credentials=[]),
                      ],
                      vulnerabilities=[
                          Vulnerability(name="CVE-2014-9278", cve="CVE-2014-9278", cvss=4.0, credentials=[],
                                        port=22,
                                        protocol=TransportProtocol.TCP),
                          Vulnerability(name=constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS, cve=None,
                                        cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS,
                                        credentials=[
                              Credential(username="ec2-user", pw="ec2-user", service=constants.FTP.SERVICE_NAME)
                          ],
                                        port=21, protocol=TransportProtocol.TCP, service=constants.FTP.SERVICE_NAME)
                      ]
                      ),

                 Node(ip="172.18.2.191", ip_id=191, id=12, type=NodeType.HACKER, flags=[], level=1, services=[],
                      reachable_nodes=set(["172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                                       "172.18.2.191", "172.18.2.10"]),
                      os="linux", vulnerabilities=[],
                      credentials=[
                          Credential(username="agent", pw="agent")
                      ],
                      root_usernames=["agent"]),

                 ]
        return nodes

    @staticmethod
    def adj_matrix() -> List:
        """
        Returns the adjacency matrix that defines the topology

        :return: adjacency matrix
        """
        adj_matrix = [
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1], # router
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], # ssh1
            [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], # telnet1
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # honeypot1
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # ftp1
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # ssh2
            [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0], # ssh3
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # telnet2
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],  # telnet3
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # honeypot2
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # ftp2
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #hacker
        ]
        return adj_matrix

    @staticmethod
    def subnet_mask() -> str:
        """
        :return: the subnet mask
        """
        subnet_mask = "172.18.2.0/24"
        return subnet_mask

    @staticmethod
    def num_nodes() -> int:
        """
        :return: num nodes
        """
        return 11

    @staticmethod
    def hacker_ip() -> str:
        """
        :return: the subnet mask
        """
        hacker_ip = "172.18.2.191"
        return hacker_ip

    @staticmethod
    def router_ip() -> str:
        """
        :return: the agent's default gw
        """
        router_ip = "172.18.2.10"
        return router_ip

    @staticmethod
    def flags_lookup() -> str:
        """
        :return: dict with the flags
        """
        flags_lookup = {}
        flags_lookup[("172.18.2.2", "/tmp/flag2")] = Flag(name="flag2", path="/tmp", id=2, requires_root=False, score=1)
        flags_lookup[("172.18.2.3", "/root/flag1")] = Flag(name="flag1", path="/root", id=1, requires_root=True,
                                                           score=1)
        flags_lookup[("172.18.2.79", "/tmp/flag3")] = Flag(name="flag3", path="/tmp", id=3, requires_root=False,
                                                           score=1)
        flags_lookup[("172.18.2.54", "/tmp/flag4")] = Flag(name="flag4", path="/tmp", id=4, requires_root=False,
                                                           score=1)
        flags_lookup[("172.18.2.61", "/root/flag5")] = Flag(name="flag5", path="/root", id=5, requires_root=True,
                                                           score=1)
        flags_lookup[("172.18.2.7", "/tmp/flag6")] = Flag(name="flag6", path="/tmp", id=6, requires_root=False,
                                                            score=1)
        return flags_lookup

    @staticmethod
    def network_conf(generate: bool = False) -> NetworkConfig:
        """
        :return: The network configuration
        """
        nodes = []
        adj_matrix = []
        agent_reachable = set()
        if not generate:
            nodes = PyCrPwCrackLevel2Base.nodes()
            adj_matrix = PyCrPwCrackLevel2Base.adj_matrix()
            agent_reachable = PyCrPwCrackLevel2Base.agent_reachable()
        network_conf = NetworkConfig(subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                     nodes=nodes,
                                     adj_matrix=adj_matrix,
                                     flags_lookup = PyCrPwCrackLevel2Base.flags_lookup(),
                                     agent_reachable=agent_reachable,
                                     vulnerable_nodes = set(["172.18.2.3", "172.18.2.79", "172.18.2.2",
                                                             "172.18.2.54", "172.18.2.74", "172.18.2.61",
                                                             "172.18.2.62", "172.18.2.7"]))
        return network_conf

    @staticmethod
    def agent_reachable() -> set():
        reachable = set(["172.18.2.10", "172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79"])
        return reachable

    @staticmethod
    def cluster_conf() -> ClusterConfig:
        """
        :return: the default cluster config
        """
        cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.2.191",
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
        actions.append(NetworkServiceActions.SERVICE_LOGIN(index=num_nodes+1))
        actions.append(ShellActions.FIND_FLAG(index=num_nodes+1))
        actions.append(MasscanActions.MASSCAN_HOST_SCAN(index=num_nodes+1, subnet=True,
                                                        host_ip=hacker_ip, ip=subnet_mask))
        actions.append(NMAPActions.FIREWALK(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.HTTP_ENUM(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.HTTP_GREP(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.VULSCAN(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(NMAPActions.FINGER(num_nodes+1, ip=subnet_mask, subnet=True))
        actions.append(ShellActions.INSTALL_TOOLS(index=num_nodes+1))
        actions.append(ShellActions.SSH_BACKDOOR(index=num_nodes+1))

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
            ActionId.FINGER_HOST, ActionId.FINGER_SUBNET,
        ]
        network_service_action_ids = [ActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [ActionId.FIND_FLAG, ActionId.INSTALL_TOOLS, ActionId.SSH_BACKDOOR]
        nikto_action_ids = [ActionId.NIKTO_WEB_HOST_SCAN]
        masscan_action_ids = [ActionId.MASSCAN_HOST_SCAN, ActionId.MASSCAN_SUBNET_SCAN]
        action_config = ActionConfig(num_indices=num_nodes, actions=actions, nmap_action_ids=nmap_action_ids,
                                     network_service_action_ids=network_service_action_ids,
                                     shell_action_ids=shell_action_ids, nikto_action_ids=nikto_action_ids,
                                     masscan_action_ids=masscan_action_ids)
        return action_config

    @staticmethod
    def render_conf() -> RenderConfig:
        """
        :return: the render config
        """
        render_config = RenderConfig(num_levels=6, num_nodes_per_level=4)
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
                               num_sh=3, num_nodes = PyCrPwCrackLevel2Base.num_nodes(), render_config=render_conf,
                               env_mode=EnvMode.SIMULATION,
                               cluster_config=cluster_conf,
                               simulate_detection=True, detection_reward=10, base_detection_p=0.05,
                               hacker_ip=PyCrPwCrackLevel2Base.hacker_ip(), state_type=StateType.BASE,
                               router_ip=PyCrPwCrackLevel2Base.router_ip())
        env_config.ping_scan_miss_p = 0.0
        env_config.udp_port_scan_miss_p = 0.0
        env_config.syn_stealth_scan_miss_p = 0.0
        env_config.os_scan_miss_p = 0.0
        env_config.vulners_miss_p = 0.0
        env_config.num_flags = 6
        env_config.blacklist_ips = ["172.18.2.1"]
        env_config.ids_router = False
        return env_config

if __name__ == '__main__':
    network_conf = PyCrPwCrackLevel2Base.network_conf()
    network_conf._shortest_path()
