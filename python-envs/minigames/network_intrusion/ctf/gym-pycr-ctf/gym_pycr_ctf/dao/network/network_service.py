from typing import List
from gym_pycr_ctf.dao.network.transport_protocol import TransportProtocol
from gym_pycr_ctf.dao.network.credential import Credential
import gym_pycr_ctf.constants.constants as constants


class NetworkService:

    def __init__(self, protocol: TransportProtocol, port : int, name : str, credentials : List[Credential] = None):
        self.protocol = protocol
        self.port = port
        self.name = name
        self.credentials = credentials

    def __str__(self):
        return "protocol:{}, port:{}, name:{}, credentials: {}".format(self.protocol, self.port, self.name,
                                                                       list(map(lambda x: str(x), self.credentials)))


    def copy(self):
        return NetworkService(
            protocol=self.protocol, port=self.port, name=self.name, credentials=self.credentials
        )


    @staticmethod
    def pw_vuln_services():
        ssh_vuln_service = (NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh", credentials=[]),
                            constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS)
        ftp_vuln_service = (NetworkService(protocol=TransportProtocol.TCP, port=21, name="ftp", credentials=[]),
                            constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS)
        telnet_vuln_service = (NetworkService(protocol=TransportProtocol.TCP, port=23, name="telnet", credentials=[]),
                               constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS)
        return [ssh_vuln_service, ftp_vuln_service, telnet_vuln_service], [ssh_vuln_service, telnet_vuln_service]
