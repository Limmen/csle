from typing import List
import csle_common.constants.constants as constants
from csle_common.dao.network.node import Node
from csle_common.dao.network.flag import Flag
from csle_common.dao.network.node_type import NodeType
from csle_common.dao.network.network_config import NetworkConfig
from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.dao.network.network_service import NetworkService
from csle_common.dao.network.transport_protocol import TransportProtocol
from csle_common.dao.network.vulnerability import Vulnerability
from csle_common.dao.network.credential import Credential
from csle_common.dao.state_representation.state_type import StateType
from gym_csle_ctf.dao.network.env_config import csleEnvConfig
from gym_csle_ctf.dao.render.render_config import RenderConfig
from gym_csle_ctf.dao.action.attacker.attacker_action_config import AttackerActionConfig
from gym_csle_ctf.dao.action.attacker.attacker_nmap_actions import AttackerNMAPActions
from gym_csle_ctf.dao.action.attacker.attacker_nikto_actions import AttackerNIKTOActions
from gym_csle_ctf.dao.action.attacker.attacker_masscan_actions import AttackerMasscanActions
from gym_csle_ctf.dao.action.attacker.attacker_network_service_actions import AttackerNetworkServiceActions
from gym_csle_ctf.dao.action.attacker.attacker_shell_actions import AttackerShellActions
from gym_csle_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_csle_ctf.dao.action.defender.defender_action_config import DefenderActionConfig
from gym_csle_ctf.dao.action.defender.defender_action_id import DefenderActionId
from gym_csle_ctf.dao.action.defender.defender_stopping_actions import DefenderStoppingActions
from gym_csle_ctf.dao.action.attacker.attacker_stopping_actions import AttackerStoppingActions

class CSLECTFLevel5Base:
    """
    Base configuration of level 5 of the CSLECTF environment. (Mainly used when running in simulation mode
    and all the config of the environment have to be hardcoded)
    """
    @staticmethod
    def nodes() -> List[Node]:
        """
        Returns the configuration of all nodes in the environment

        :return: list of node configs
        """
        nodes = [Node(ip="172.18.5.10", ip_id=10, id=1, type=NodeType.ROUTER, flags=[], level=2, services=[],
                      reachable_nodes=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                  "172.18.5.191", "172.18.5.10"]),
                      os="linux", vulnerabilities=[], credentials=[
                Credential(username="admin", pw="admin1235912"),
                Credential(username="jessica", pw="water")
            ], firewall=True,
                      root_usernames=["admin"]),
                 Node(ip="172.18.5.2", ip_id=2, id=2, type=NodeType.SERVER,
                      reachable_nodes=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                       "172.18.5.191", "172.18.5.10", "172.18.5.54"]),
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
                 Node(ip="172.18.5.3", ip_id=3, id=3, type=NodeType.SERVER, os="linux",
                      reachable_nodes=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                       "172.18.5.191", "172.18.5.10", "172.18.5.74", "172.18.5.61"]),
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
                 Node(ip="172.18.5.21", ip_id=21, id=4, type=NodeType.SERVER, flags=[], level=3, os="linux",
                      reachable_nodes=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                       "172.18.5.191", "172.18.5.10"]),
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
                 Node(ip="172.18.5.79", ip_id=79, id=5, type=NodeType.SERVER,
                      reachable_nodes=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                       "172.18.5.191", "172.18.5.10"]),
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
                 Node(ip="172.18.5.54", ip_id=54, id=6, type=NodeType.SERVER,
                      reachable_nodes=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                       "172.18.5.191", "172.18.5.10", "172.18.5.54"]),
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

                 Node(ip="172.18.5.74", ip_id=74, id=7, type=NodeType.SERVER,
                      reachable_nodes=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                       "172.18.5.191", "172.18.5.10", "172.18.5.61", "172.18.5.74",
                                       "172.18.5.101", "172.18.5.62"]),
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

                 Node(ip="172.18.5.61", ip_id=61, id=8, type=NodeType.SERVER, os="linux",
                      reachable_nodes=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                       "172.18.5.191", "172.18.5.10", "172.18.5.61", "172.18.5.74"]),
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

                 Node(ip="172.18.5.62", ip_id=62, id=9, type=NodeType.SERVER, os="linux",
                      reachable_nodes=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                       "172.18.5.191", "172.18.5.10", "172.18.5.61", "172.18.5.74",
                                       "172.18.5.101", "172.18.5.62", "172.18.5.7"]),
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

                 Node(ip="172.18.5.101", ip_id=101, id=10, type=NodeType.SERVER, flags=[], level=5, os="linux",
                      reachable_nodes=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                       "172.18.5.191", "172.18.5.10", "172.18.5.61", "172.18.5.74",
                                       "172.18.5.101", "172.18.5.62"]),
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

                 Node(ip="172.18.5.7", ip_id=7, id=11, type=NodeType.SERVER,
                      reachable_nodes=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                       "172.18.5.191", "172.18.5.10", "172.18.5.61", "172.18.5.74",
                                       "172.18.5.101", "172.18.5.62", "172.18.5.7"]),
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

                 Node(ip="172.18.5.191", ip_id=191, id=12, type=NodeType.HACKER, flags=[], level=1, services=[],
                      reachable_nodes=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                       "172.18.5.191", "172.18.5.10"]),
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
        subnet_mask = "172.18.5.0/24"
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
        hacker_ip = "172.18.5.191"
        return hacker_ip

    @staticmethod
    def router_ip() -> str:
        """
        :return: the agent's default gw
        """
        router_ip = "172.18.5.10"
        return router_ip

    @staticmethod
    def flags_lookup() -> str:
        """
        :return: dict with the flags
        """
        flags_lookup = {}
        flags_lookup[("172.18.5.2", "/tmp/flag2")] = Flag(name="flag2", path="/tmp", id=2, requires_root=False, score=1)
        flags_lookup[("172.18.5.3", "/root/flag1")] = Flag(name="flag1", path="/root", id=1, requires_root=True,
                                                           score=1)
        flags_lookup[("172.18.5.79", "/tmp/flag3")] = Flag(name="flag3", path="/tmp", id=3, requires_root=False,
                                                           score=1)
        flags_lookup[("172.18.5.54", "/tmp/flag4")] = Flag(name="flag4", path="/tmp", id=4, requires_root=False,
                                                           score=1)
        flags_lookup[("172.18.5.61", "/root/flag5")] = Flag(name="flag5", path="/root", id=5, requires_root=True,
                                                           score=1)
        flags_lookup[("172.18.5.7", "/tmp/flag6")] = Flag(name="flag6", path="/tmp", id=6, requires_root=False,
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
            nodes = CSLECTFLevel5Base.nodes()
            adj_matrix = CSLECTFLevel5Base.adj_matrix()
            agent_reachable = CSLECTFLevel5Base.agent_reachable()
        network_conf = NetworkConfig(subnet_mask=CSLECTFLevel5Base.subnet_mask(),
                                     nodes=nodes,
                                     adj_matrix=adj_matrix,
                                     flags_lookup = CSLECTFLevel5Base.flags_lookup(),
                                     agent_reachable=agent_reachable,
                                     vulnerable_nodes=set(["172.18.5.3", "172.18.5.79", "172.18.5.2",
                                                           "172.18.5.54", "172.18.5.74", "172.18.5.61",
                                                           "172.18.5.62", "172.18.5.7"]))
        return network_conf

    @staticmethod
    def agent_reachable() -> set():
        reachable = set(["172.18.5.10", "172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79"])
        return reachable

    @staticmethod
    def emulation_config() -> EmulationConfig:
        """
        :return: the default emulation config
        """
        emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.5.191",
                                         agent_username="agent", agent_pw="agent", server_connection=True,
                                         server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
                                         server_username="kim")
        return emulation_config

    @staticmethod
    def attacker_all_actions_conf(num_nodes: int, subnet_mask: str, hacker_ip: str) -> AttackerActionConfig:
        """
        :param num_nodes: max number of nodes to consider (whole subnetwork in most general case)
        :param subnet_mask: subnet mask of the network
        :param hacker_ip: ip of the agent
        :return: the action config
        """
        attacker_actions = []

        # Host actions
        for idx in range(num_nodes):
            attacker_actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.PING_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.UDP_PORT_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.TCP_FIN_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.TCP_NULL_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.TCP_XMAS_TREE_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.NMAP_VULNERS(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=idx, subnet=False))
            attacker_actions.append(AttackerNIKTOActions.NIKTO_WEB_HOST_SCAN(index=idx))
            attacker_actions.append(AttackerMasscanActions.MASSCAN_HOST_SCAN(index=idx, subnet=False, host_ip = hacker_ip))
            attacker_actions.append(AttackerNMAPActions.FIREWALK(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.HTTP_ENUM(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.HTTP_GREP(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.VULSCAN(index=idx, subnet=False))
            attacker_actions.append(AttackerNMAPActions.FINGER(index=idx, subnet=False))

        # Subnet actions
        attacker_actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.PING_SCAN(index=num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.UDP_PORT_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.TCP_CON_NON_STEALTH_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.TCP_FIN_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.TCP_NULL_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.TCP_XMAS_TREE_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.OS_DETECTION_SCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.NMAP_VULNERS(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.IRC_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNetworkServiceActions.SERVICE_LOGIN(index=num_nodes + 1))
        attacker_actions.append(AttackerShellActions.FIND_FLAG(index=num_nodes + 1))
        attacker_actions.append(AttackerMasscanActions.MASSCAN_HOST_SCAN(index=num_nodes + 1, subnet=True,
                                                                host_ip=hacker_ip, ip=subnet_mask))
        attacker_actions.append(AttackerNMAPActions.FIREWALK(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.HTTP_ENUM(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.HTTP_GREP(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.VULSCAN(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerNMAPActions.FINGER(num_nodes + 1, ip=subnet_mask, subnet=True))
        attacker_actions.append(AttackerShellActions.INSTALL_TOOLS(index=num_nodes + 1))
        attacker_actions.append(AttackerShellActions.SSH_BACKDOOR(index=num_nodes + 1))

        attacker_actions.append(AttackerStoppingActions.STOP(index=num_nodes + 1))
        attacker_actions.append(AttackerStoppingActions.CONTINUE(index=num_nodes + 1))

        attacker_actions = sorted(attacker_actions, key=lambda x: (x.id.value, x.index))
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
            AttackerActionId.FINGER_HOST, AttackerActionId.FINGER_SUBNET,
        ]
        network_service_action_ids = [AttackerActionId.NETWORK_SERVICE_LOGIN]
        shell_action_ids = [AttackerActionId.FIND_FLAG, AttackerActionId.INSTALL_TOOLS, AttackerActionId.SSH_BACKDOOR]
        nikto_action_ids = [AttackerActionId.NIKTO_WEB_HOST_SCAN]
        masscan_action_ids = [AttackerActionId.MASSCAN_HOST_SCAN, AttackerActionId.MASSCAN_SUBNET_SCAN]
        stopping_action_ids = [AttackerActionId.STOP, AttackerActionId.CONTINUE]
        attacker_action_config = AttackerActionConfig(num_indices=num_nodes + 1, actions=attacker_actions,
                                                      nmap_action_ids=nmap_action_ids,
                                                      network_service_action_ids=network_service_action_ids,
                                                      shell_action_ids=shell_action_ids,
                                                      nikto_action_ids=nikto_action_ids,
                                                      masscan_action_ids=masscan_action_ids,
                                                      stopping_action_ids=stopping_action_ids)
        return attacker_action_config

    @staticmethod
    def defender_all_actions_conf(num_nodes: int, subnet_mask: str) -> DefenderActionConfig:
        """
        :param num_nodes: max number of nodes to consider (whole subnetwork in most general case)
        :param subnet_mask: subnet mask of the network
        :return: the action config
        """
        defender_actions = []

        # Host actions
        for idx in range(num_nodes):
            # actions.append(AttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=idx, subnet=False))
            pass

        # Subnet actions
        defender_actions.append(DefenderStoppingActions.STOP(index=num_nodes + 1))
        defender_actions.append(DefenderStoppingActions.CONTINUE(index=num_nodes + 1))

        defender_actions = sorted(defender_actions, key=lambda x: (x.id.value, x.index))
        stopping_action_ids = [
            DefenderActionId.STOP, DefenderActionId.CONTINUE
        ]
        defender_action_config = DefenderActionConfig(
            num_indices=num_nodes + 1, actions=defender_actions, stopping_action_ids=stopping_action_ids)
        return defender_action_config

    @staticmethod
    def render_conf() -> RenderConfig:
        """
        :return: the render config
        """
        render_config = RenderConfig(num_levels=6, num_nodes_per_level=4)
        return render_config

    @staticmethod
    def env_config(network_conf : NetworkConfig, attacker_action_conf: AttackerActionConfig,
                   defender_action_conf: DefenderActionConfig,
                   emulation_config: EmulationConfig,
                   render_conf: RenderConfig) -> csleEnvConfig:
        """
        :param network_conf: the network config
        :param attacker_action_conf: the attacker's action config
        :param defender_action_conf: the defender's action config
        :param emulation_config: the emulation config
        :param render_conf: the render config
        :return: The complete environment config
        """
        env_config = csleEnvConfig(network_conf=network_conf, attacker_action_conf=attacker_action_conf, attacker_num_ports_obs=10, attacker_num_vuln_obs=10,
                                   attacker_num_sh_obs=3, num_nodes = CSLECTFLevel5Base.num_nodes(), render_config=render_conf,
                                   env_mode=EnvMode.SIMULATION,
                                   emulation_config=emulation_config,
                                   simulate_detection=True, detection_reward=10, base_detection_p=0.05,
                                   hacker_ip=CSLECTFLevel5Base.hacker_ip(), state_type=StateType.BASE,
                                   router_ip=CSLECTFLevel5Base.router_ip())
        env_config.ping_scan_miss_p = 0.0
        env_config.udp_port_scan_miss_p = 0.0
        env_config.syn_stealth_scan_miss_p = 0.0
        env_config.os_scan_miss_p = 0.0
        env_config.vulners_miss_p = 0.0
        env_config.num_flags = 6
        env_config.blacklist_ips = ["172.18.5.1", "172.18.5.254"]
        env_config.ids_router = True
        return env_config
