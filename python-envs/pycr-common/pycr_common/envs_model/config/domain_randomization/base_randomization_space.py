from typing import List
import pycr_common.constants.constants as constants
from pycr_common.dao.network.network_service import NetworkService
from pycr_common.dao.network.transport_protocol import TransportProtocol
from pycr_common.dao.network.vulnerability import Vulnerability
from pycr_common.dao.network.credential import Credential


class BaseRandomizationSpace:
    """
    Class representing the base domain randomization space
    """

    @staticmethod
    def base_services() -> List[NetworkService]:
        """
        :return: A list of base services
        """
        services = [
            NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh",
                           credentials=[
                               Credential(username="admin", pw="test32121", port=22,
                                          protocol=TransportProtocol.TCP, service="ssh"),
                               Credential(username="puppet", pw="puppet",
                                          protocol=TransportProtocol.TCP, service="ssh"),
                               Credential(username="user1", pw="123123",
                                          protocol=TransportProtocol.TCP, service="ssh")
                           ]),
            NetworkService(protocol=TransportProtocol.TCP, port=53, name="domain", credentials=[]),
            NetworkService(protocol=TransportProtocol.TCP, port=80, name="http", credentials=[]),
            NetworkService(protocol=TransportProtocol.TCP, port=9042, name="cassandra", credentials=[]),
            NetworkService(protocol=TransportProtocol.TCP, port=9160, name="cassandra", credentials=[]),
            NetworkService(protocol=TransportProtocol.UDP, port=53, name="domain", credentials=[]),
            NetworkService(protocol=TransportProtocol.TCP, port=25, name="smtp", credentials=[]),
            NetworkService(protocol=TransportProtocol.TCP, port=2181, name="kafka", credentials=[]),
            NetworkService(protocol=TransportProtocol.TCP, port=5432, name="postgresql", credentials=[]),
            NetworkService(protocol=TransportProtocol.TCP, port=6667, name="irc", credentials=[]),
            NetworkService(protocol=TransportProtocol.TCP, port=9092, name="kafka", credentials=[]),
            NetworkService(protocol=TransportProtocol.TCP, port=38969, name="kafka", credentials=[]),
            NetworkService(protocol=TransportProtocol.TCP, port=42843, name="kafka", credentials=[]),
            NetworkService(protocol=TransportProtocol.UDP, port=123, name="ntp", credentials=[]),
            NetworkService(protocol=TransportProtocol.UDP, port=161, name="snmp", credentials=[]),
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
            NetworkService(protocol=TransportProtocol.TCP, port=27017, name="mongod", credentials=[])
        ]
        return services

    @staticmethod
    def base_vulns() -> List[Vulnerability]:
        """
        :return: a list of base vulnerabilities
        """
        vulns = [
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
                          port=53, protocol=TransportProtocol.TCP),
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
                          port=53, protocol=TransportProtocol.TCP),
            Vulnerability(name="CVE-2020-15523", cve="CVE-2020-15523", cvss=6.9, credentials=[], port=80,
                          protocol=TransportProtocol.TCP),
            Vulnerability(name="CVE-2020-14422", cve="CVE-2020-14422", cvss=4.3, credentials=[], port=80,
                          protocol=TransportProtocol.TCP),
            Vulnerability(name=constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS,
                          cve=None, cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS, credentials=[
                    Credential(username="admin", pw="admin", service=constants.TELNET.SERVICE_NAME)
                ],
                          port=23, protocol=TransportProtocol.TCP, service=constants.TELNET.SERVICE_NAME),
            Vulnerability(name="CVE-2014-9278", cve="CVE-2014-9278", cvss=4.0, credentials=[],
                          port=22,
                          protocol=TransportProtocol.TCP),
            Vulnerability(name=constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS, cve=None,
                          cvss=constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS, credentials=[
                    Credential(username="pi", pw="pi", service=constants.FTP.SERVICE_NAME)
                ],
                          port=21, protocol=TransportProtocol.TCP, service=constants.FTP.SERVICE_NAME)
        ]
        return vulns

    @staticmethod
    def base_os() -> List[str]:
        """
        :return: a list of base operating systems
        """
        return list(constants.OS.os_lookup.keys())