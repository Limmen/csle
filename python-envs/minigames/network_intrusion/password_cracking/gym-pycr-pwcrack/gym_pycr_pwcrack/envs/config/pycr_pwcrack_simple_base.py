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
from gym_pycr_pwcrack.dao.action.network_service_actions import NetworkServiceActions
from gym_pycr_pwcrack.dao.action.shell_actions import ShellActions
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.network.network_service import NetworkService
from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.dao.network.vulnerability import Vulnerability
from gym_pycr_pwcrack.dao.network.credential import Credential

class PyCrPwCrackSimpleBase:
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
        nodes = [Node(ip="172.18.1.10", ip_id=10, id=1, type=NodeType.ROUTER, flags=[], level=2, services=[],
                      os="linux", vulnerabilities=[], credentials=[
                Credential(username="admin", pw="admin"),
                Credential(username="jessica", pw="water")
            ],
                      root=["admin"]),
                 Node(ip="172.18.1.2", ip_id=2, id=2, type=NodeType.SERVER,
                      flags=[Flag(name="flag2", path="/tmp", id=2, requires_root=False, score=1)], level=3, os="linux",
                      credentials=[
                          Credential(username="admin", pw="test32121"),
                          Credential(username="puppet", pw="puppet"),
                          Credential(username="user1", pw="123123")
                      ],
                      root=["admin", "user1"],
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
                          Vulnerability(name="ssh-weak-password", cve=None, cvss=10.0, service="ssh",
                                        credentials=[
                                            Credential(username="puppet", pw="puppet",
                                                       protocol=TransportProtocol.TCP, service="ssh")
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
                 Node(ip="172.18.1.3", ip_id=3, id=3, type=NodeType.SERVER, os="linux",
                      flags=[Flag(name="flag1", path="/root", id=1, requires_root=True, score=1)], level=3,
                      credentials=[
                          Credential(username="admin", pw="admin"),
                          Credential(username="john", pw="doe"),
                          Credential(username="vagrant", pw="test_pw1")
                      ],
                      root=["admin", "john"],
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
                         Vulnerability(name="telnet-weak-password", cve=None, cvss=10.0, credentials=[
                             Credential(username="admin", pw="admin")
                         ],
                                       port=23, protocol=TransportProtocol.TCP, service="telnet")
                     ]
                      ),
                 Node(ip="172.18.1.21", ip_id=21, id=4, type=NodeType.SERVER, flags=[], level=3, os="linux",
                      credentials=[
                          Credential(username="admin", pw="admin"),
                          Credential(username="test", pw="qwerty"),
                          Credential(username="oracle", pw="abc123")
                      ],
                      root=["admin", "test"],
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
                 Node(ip="172.18.1.79", ip_id=79, id=5, type=NodeType.SERVER,
                      flags=[Flag(name="flag3", path="/tmp", id=3, requires_root=False, score=1)], level=3,
                      os="linux",
                      credentials=[
                          Credential(username="l_hopital", pw="l_hopital"),
                          Credential(username="euler", pw="euler"),
                          Credential(username="pi", pw="pi")
                      ],
                      root=["l_hopital", "pi"],
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
                          Vulnerability(name="ftp-weak-password", cve=None, cvss=10.0, credentials=[
                              Credential(username="pi", pw="pi")
                          ],
                                        port=21, protocol=TransportProtocol.TCP, service="ftp")
                      ]
                      ),
                 Node(ip="172.18.1.191", ip_id=191, id=6, type=NodeType.HACKER, flags=[], level=1, services=[],
                      os="linux", vulnerabilities=[],
                      credentials=[
                          Credential(username="agent", pw="agent")
                      ],
                      root=["agent"])]
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
        subnet_mask = "172.18.1.0/24"
        return subnet_mask

    @staticmethod
    def network_conf() -> NetworkConfig:
        """
        :return: The network configuration
        """
        network_conf = NetworkConfig(subnet_mask=PyCrPwCrackSimpleBase.subnet_mask(),
                                     nodes=PyCrPwCrackSimpleBase.nodes(),
                                     adj_matrix=PyCrPwCrackSimpleBase.adj_matrix())
        return network_conf

    @staticmethod
    def cluster_conf() -> ClusterConfig:
        """
        :return: the default cluster config
        """
        cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
                                       agent_username="agent", agent_pw="agent", server_connection=True,
                                       server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
                                       server_username="kim")
        return cluster_config

    @staticmethod
    def action_conf(network_conf : NetworkConfig) -> ActionConfig:
        """
        :param network_conf: the network config
        :return: the action config
        """
        action_config = ActionConfig(actions=[

            # --- ReCon ---

            # TCP SYN Stealth Scan
            NMAPActions.TCP_SYN_STEALTH_SCAN(index=len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.TCP_SYN_STEALTH_SCAN(index=0, subnet=False),
            NMAPActions.TCP_SYN_STEALTH_SCAN(index=1, subnet=False),
            NMAPActions.TCP_SYN_STEALTH_SCAN(index=2, subnet=False),
            NMAPActions.TCP_SYN_STEALTH_SCAN(index=3, subnet=False),
            NMAPActions.TCP_SYN_STEALTH_SCAN(index=4, subnet=False),

            # Ping Scan
            NMAPActions.PING_SCAN(index=len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.PING_SCAN(index=0, subnet=False),
            NMAPActions.PING_SCAN(index=1, subnet=False),
            NMAPActions.PING_SCAN(index=2, subnet=False),
            NMAPActions.PING_SCAN(index=3, subnet=False),
            NMAPActions.PING_SCAN(index=4, subnet=False),

            # UDP Port Scan
            NMAPActions.UDP_PORT_SCAN(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.UDP_PORT_SCAN(index=0, subnet=False),
            NMAPActions.UDP_PORT_SCAN(index=1, subnet=False),
            NMAPActions.UDP_PORT_SCAN(index=2, subnet=False),
            NMAPActions.UDP_PORT_SCAN(index=3, subnet=False),
            NMAPActions.UDP_PORT_SCAN(index=4, subnet=False),

            # TCP CON Non-stealth Scan
            NMAPActions.TCP_CON_NON_STEALTH_SCAN(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.TCP_CON_NON_STEALTH_SCAN(index=0, subnet=False),
            NMAPActions.TCP_CON_NON_STEALTH_SCAN(index=1, subnet=False),
            NMAPActions.TCP_CON_NON_STEALTH_SCAN(index=2, subnet=False),
            NMAPActions.TCP_CON_NON_STEALTH_SCAN(index=3, subnet=False),
            NMAPActions.TCP_CON_NON_STEALTH_SCAN(index=4, subnet=False),

            # TCP FIN Scan
            NMAPActions.TCP_FIN_SCAN(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.TCP_FIN_SCAN(index=0, subnet=False),
            NMAPActions.TCP_FIN_SCAN(index=1, subnet=False),
            NMAPActions.TCP_FIN_SCAN(index=2, subnet=False),
            NMAPActions.TCP_FIN_SCAN(index=3, subnet=False),
            NMAPActions.TCP_FIN_SCAN(index=4, subnet=False),

            # TCP Null Scan
            NMAPActions.TCP_NULL_SCAN(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.TCP_NULL_SCAN(index=0, subnet=False),
            NMAPActions.TCP_NULL_SCAN(index=1, subnet=False),
            NMAPActions.TCP_NULL_SCAN(index=2, subnet=False),
            NMAPActions.TCP_NULL_SCAN(index=3, subnet=False),
            NMAPActions.TCP_NULL_SCAN(index=4, subnet=False),

            # TCP XMAS Tree Scan
            NMAPActions.TCP_XMAS_TREE_SCAN(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.TCP_XMAS_TREE_SCAN(index=0, subnet=False),
            NMAPActions.TCP_XMAS_TREE_SCAN(index=1, subnet=False),
            NMAPActions.TCP_XMAS_TREE_SCAN(index=2, subnet=False),
            NMAPActions.TCP_XMAS_TREE_SCAN(index=3, subnet=False),
            NMAPActions.TCP_XMAS_TREE_SCAN(index=4, subnet=False),

            # OS Detection Scan
            NMAPActions.OS_DETECTION_SCAN(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.OS_DETECTION_SCAN(index=0, subnet=False),
            NMAPActions.OS_DETECTION_SCAN(index=1, subnet=False),
            NMAPActions.OS_DETECTION_SCAN(index=2, subnet=False),
            NMAPActions.OS_DETECTION_SCAN(index=3, subnet=False),
            NMAPActions.OS_DETECTION_SCAN(index=4, subnet=False),

            NMAPActions.NMAP_VULNERS(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.NMAP_VULNERS(index=0, subnet=False),
            NMAPActions.NMAP_VULNERS(index=1, subnet=False),
            NMAPActions.NMAP_VULNERS(index=2, subnet=False),
            NMAPActions.NMAP_VULNERS(index=3, subnet=False),
            NMAPActions.NMAP_VULNERS(index=4, subnet=False),

            # --- Exploits ---

            # Telnet
            NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=0, subnet=False),
            NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=1, subnet=False),
            NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=2, subnet=False),
            NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=3, subnet=False),
            NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=4, subnet=False),

            # SSH
            NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=0, subnet=False),
            NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=1, subnet=False),
            NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=2, subnet=False),
            NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=3, subnet=False),
            NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=4, subnet=False),

            # FTP
            NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=0, subnet=False),
            NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=1, subnet=False),
            NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=2, subnet=False),
            NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=3, subnet=False),
            NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=4, subnet=False),

            # Cassandra
            NMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=0, subnet=False),
            NMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=1, subnet=False),
            NMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=2, subnet=False),
            NMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=3, subnet=False),
            NMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(index=4, subnet=False),

            # IRC
            NMAPActions.IRC_SAME_USER_PASS_DICTIONARY(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=0, subnet=False),
            NMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=1, subnet=False),
            NMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=2, subnet=False),
            NMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=3, subnet=False),
            NMAPActions.IRC_SAME_USER_PASS_DICTIONARY(index=4, subnet=False),

            # Mongo
            NMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=0, subnet=False),
            NMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=1, subnet=False),
            NMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=2, subnet=False),
            NMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=3, subnet=False),
            NMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(index=4, subnet=False),

            # MySql
            NMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=0, subnet=False),
            NMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=1, subnet=False),
            NMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=2, subnet=False),
            NMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=3, subnet=False),
            NMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(index=4, subnet=False),

            # STMP
            NMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=0, subnet=False),
            NMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=1, subnet=False),
            NMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=2, subnet=False),
            NMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=3, subnet=False),
            NMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(index=4, subnet=False),

            # Postgres
            NMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(len(network_conf.nodes), ip=network_conf.subnet_mask, subnet=True),
            NMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=0, subnet=False),
            NMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=1, subnet=False),
            NMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=2, subnet=False),
            NMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=3, subnet=False),
            NMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(index=4, subnet=False),

            # --- Post-Exploits ---

            # Network Service Login
            NetworkServiceActions.SERVICE_LOGIN(index=0),
            NetworkServiceActions.SERVICE_LOGIN(index=1),
            NetworkServiceActions.SERVICE_LOGIN(index=2),
            NetworkServiceActions.SERVICE_LOGIN(index=3),
            NetworkServiceActions.SERVICE_LOGIN(index=4),

            # Search file system for flag
            ShellActions.FIND_FLAG()
        ])
        return action_config

    @staticmethod
    def render_conf() -> RenderConfig:
        """
        :return: the render config
        """
        render_config = RenderConfig()
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
                               num_sh=3, render_config=render_conf, env_mode=EnvMode.SIMULATION,
                               cluster_config=cluster_conf,
                               simulate_detection=True, detection_reward=10, base_detection_p=0.05,
                               hacker_ip="172.18.1.191")
        env_config.ping_scan_miss_p = 0.02
        env_config.udp_port_scan_miss_p = 0.07
        env_config.syn_stealth_scan_miss_p = 0.04
        env_config.os_scan_miss_p = 0.08
        env_config.vulners_miss_p = 0.09
        env_config.num_flags = 3
        return env_config
