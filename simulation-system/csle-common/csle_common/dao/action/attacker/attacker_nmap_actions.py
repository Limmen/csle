from typing import List
import csle_common.constants.constants as constants
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.attacker.attacker_action_type import AttackerActionType
from csle_common.dao.action.attacker.attacker_action_id import AttackerActionId
from csle_common.dao.action.attacker.attacker_action import AttackerActionOutcome


class AttackerNMAPActions:
    """
    Class containing Attacker NMAP actions
    """

    @staticmethod
    def TCP_SYN_STEALTH_SCAN(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a TCP SYN scan

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = AttackerActionId.TCP_SYN_STEALTH_SCAN_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.TCP_SYN_STEALTH_SCAN_SUBNET

        if index == -1:
            id = AttackerActionId.TCP_SYN_STEALTH_SCAN_ALL

        cmd = ["sudo nmap -sS -p- " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="TCP SYN (Stealth) Scan", cmds=cmd,
                              type=AttackerActionType.RECON,
                              descr="A stealthy and fast TCP SYN scan to detect open TCP ports on the subnet",
                              ips=ips, subnet=subnet, index=index,
                              action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def PING_SCAN(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a Ping scan

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ip of the machine or subnet to apply the action to
        :return: the action
        """
        id = AttackerActionId.PING_SCAN_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.PING_SCAN_SUBNET

        if index == -1:
            id = AttackerActionId.PING_SCAN_ALL

        cmd = ["sudo nmap -sP " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="Ping Scan", cmds=cmd,
                              type=AttackerActionType.RECON,
                              descr="A host discovery scan, it is quick because it only checks of hosts are up with Ping, without "
                     "scanning the ports.",
                              ips=ips, subnet=subnet, index=index,
                              action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def UDP_PORT_SCAN(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a UDP port scan

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = AttackerActionId.UDP_PORT_SCAN_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.UDP_PORT_SCAN_SUBNET

        if index == -1:
            id = AttackerActionId.UDP_PORT_SCAN_ALL

        cmd = ["sudo nmap -sU -p- " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="UDP Port Scan", cmds=cmd,
                              type=AttackerActionType.RECON,
                              descr="", index=index,
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def TCP_CON_NON_STEALTH_SCAN(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a TCP CON (non-stealthy) scan

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = AttackerActionId.TCP_CON_NON_STEALTH_SCAN_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET

        if index == -1:
            id = AttackerActionId.TCP_CON_NON_STEALTH_SCAN_ALL

        cmd = ["sudo nmap -sT -p- " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="TCP Connection (Non-Stealth) Scan", cmds=cmd,
                              type=AttackerActionType.RECON, index=index,
                              descr="A non-stealthy and fast TCP SYN scan to detect open TCP ports on the subnet",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def TCP_FIN_SCAN(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a TCP FIN scan

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = AttackerActionId.TCP_FIN_SCAN_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.TCP_FIN_SCAN_SUBNET

        if index == -1:
            id = AttackerActionId.TCP_FIN_SCAN_ALL

        cmd = ["sudo nmap -sF -p- " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="FIN Scan",
                              cmds=cmd,
                              type=AttackerActionType.RECON, index=index,
                              descr="A special type of TCP port scan using FIN, can avoid IDS and firewalls that block SYN scans",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def TCP_NULL_SCAN(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a TCP Null scan

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = AttackerActionId.TCP_NULL_SCAN_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.TCP_NULL_SCAN_SUBNET

        if index == -1:
            id = AttackerActionId.TCP_NULL_SCAN_ALL

        if index == -1:
            id = AttackerActionId.TCP_NULL_SCAN_ALL

        cmd = ["sudo nmap -sN -p- " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="Null Scan",
                              cmds=cmd, index=index,
                              type=AttackerActionType.RECON,
                              descr="A special type of TCP port scan using Null, can avoid IDS and firewalls that block SYN scans",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def TCP_XMAS_TREE_SCAN(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a TCP XMAS TREE scan

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = AttackerActionId.TCP_XMAS_TREE_SCAN_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.TCP_XMAS_TREE_SCAN_SUBNET

        if index == -1:
            id = AttackerActionId.TCP_XMAS_TREE_SCAN_ALL

        cmd = ["sudo nmap -sX -p- " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="Xmas Tree Scan",
                              cmds=cmd, type=AttackerActionType.RECON, index=index,
                              descr="A special type of TCP port scan using XMas Tree, "
                     "can avoid IDS and firewalls that block SYN scans",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def OS_DETECTION_SCAN(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a OS detection scan

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = AttackerActionId.OS_DETECTION_SCAN_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.OS_DETECTION_SCAN_SUBNET

        if index == -1:
            id = AttackerActionId.OS_DETECTION_SCAN_ALL

        cmd = ["sudo nmap -O --osscan-guess --max-os-tries 1 " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="OS detection scan",
                              cmds=cmd, type=AttackerActionType.RECON,
                              descr="OS detection/guess scan", index=index,
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def VULSCAN(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a vulnerability scan using the VULSCAN script

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = AttackerActionId.VULSCAN_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.VULSCAN_SUBNET

        if index == -1:
            id = AttackerActionId.VULSCAN_ALL

        cmd = ["sudo nmap -sV --script=vulscan/vulscan.nse " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="vulscan.nse vulnerability scanner",
                              cmds=cmd, type=AttackerActionType.RECON, index=index,
                              descr="Uses a vulcan.nse script to turn NMAP into a vulnerability scanner",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def NMAP_VULNERS(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a vulnerability scan using the Vulners script

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ip of the machine or subnet to apply the action to
        :return: the action
        """
        id = AttackerActionId.NMAP_VULNERS_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.NMAP_VULNERS_SUBNET

        if index == -1:
            id = AttackerActionId.NMAP_VULNERS_ALL

        cmd = ["sudo nmap -sV --script vulners.nse " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="nmap_vulners vulnerability scanner",
                              cmds=cmd, type=AttackerActionType.RECON, index=index,
                              descr="Uses vulners.nse script to turn NMAP into a vulnerability scanner",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def TELNET_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against telnet

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        telnet_args = constants.NMAP.TELNET_BRUTE_HOST
        id = AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET
            telnet_args = constants.NMAP.TELNET_BRUTE_SUBNET

        if index == -1:
            id = AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL

        cmd = ["sudo nmap " + telnet_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="Telnet dictionary attack for username=pw",
                              cmds=cmd, type=AttackerActionType.EXPLOIT, index=index,
                              descr="A dictionary attack that tries common passwords and usernames "
                                    "for Telnet where username=password",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.SHELL_ACCESS,
                              vulnerability=constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS,
                              backdoor=False)

    @staticmethod
    def SSH_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against ssh

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ip of the machine or subnet to apply the action to
        :return: the action
        """
        ssh_args = constants.NMAP.SSH_BRUTE_HOST
        id = AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET
            ssh_args = constants.NMAP.SSH_BRUTE_SUBNET

        if index == -1:
            id = AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL

        cmd = ["sudo nmap " + ssh_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="SSH dictionary attack for username=pw",
                              cmds=cmd, type=AttackerActionType.EXPLOIT, index=index,
                              descr="A dictionary attack that tries common passwords and usernames"
                      "for SSH where username=password",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.SHELL_ACCESS,
                              vulnerability=constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS,
                              backdoor=False)

    @staticmethod
    def FTP_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against ftp

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ip of the machine or subnet to apply the action to
        :return: the action
        """
        ftp_args = constants.NMAP.FTP_BRUTE_HOST
        id = AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET
            ftp_args = constants.NMAP.FTP_BRUTE_SUBNET

        if index == -1:
            id = AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL

        cmd = ["sudo nmap " + ftp_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="FTP dictionary attack for username=pw",
                              cmds=cmd, type=AttackerActionType.EXPLOIT,
                              descr="A dictionary attack that tries common passwords and usernames"
                                    "for FTP where username=password", index=index,
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.SHELL_ACCESS,
                              vulnerability=constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS,
                              backdoor=False)

    @staticmethod
    def CASSANDRA_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against cassandra

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        cassandra_args = constants.NMAP.CASSANDRA_BRUTE_HOST
        id = AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []

        if subnet:
            id = AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET
            cassandra_args = constants.NMAP.CASSANDRA_BRUTE_SUBNET

        if index == -1:
            id = AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL

        cmd = ["sudo nmap " + cassandra_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="Cassandra dictionary attack for username=pw",
                              cmds=cmd, type=AttackerActionType.EXPLOIT,
                              descr="A dictionary attack that tries common passwords and usernames"
                                    "for Cassandra where username=password", index=index,
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.SHELL_ACCESS,
                              vulnerability=constants.EXPLOIT_VULNERABILITES.CASSANDRA_DICTS_SAME_USER_PASS,
                              backdoor=False)

    @staticmethod
    def IRC_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against irc

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        irc_args = constants.NMAP.IRC_BRUTE_HOST
        id = AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if subnet:
            id = AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET
            irc_args = constants.NMAP.IRC_BRUTE_SUBNET

        if index == -1:
            id = AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL

        cmd = ["sudo nmap " + irc_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="IRC dictionary attack for username=pw",
                              cmds=cmd, type=AttackerActionType.EXPLOIT,
                              descr="A dictionary attack that tries common passwords and usernames"
                                    "for IRC where username=password", index=index,
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.SHELL_ACCESS,
                              vulnerability=constants.EXPLOIT_VULNERABILITES.IRC_DICTS_SAME_USER_PASS,
                              backdoor=False)

    @staticmethod
    def MONGO_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against mongo

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        mongo_args = constants.NMAP.MONGO_BRUTE_HOST
        id = AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []

        if subnet:
            mongo_args = constants.NMAP.MONGO_BRUTE_SUBNET
            id = AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET

        if index == -1:
            id = AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL

        cmd = ["sudo nmap " + mongo_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="MongoDB dictionary attack for username=pw",
                              cmds=cmd, type=AttackerActionType.EXPLOIT, index=index,
                              descr="A dictionary attack that tries common passwords and usernames"
                                    "for MongoDB where username=password",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.SHELL_ACCESS,
                              vulnerability=constants.EXPLOIT_VULNERABILITES.MONGO_DICTS_SAME_USER_PASS,
                              backdoor=False)

    @staticmethod
    def MYSQL_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against mysql

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ip of the machines or subnets to apply the action to
        :return: the action
        """
        mysql_args = constants.NMAP.MYSQL_BRUTE_HOST
        id = AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if subnet:
            mysql_args = constants.NMAP.MYSQL_BRUTE_SUBNET
            id = AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET

        if index == -1:
            id = AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL

        cmd = ["sudo nmap " + mysql_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="MySQL dictionary attack for username=pw",
                              cmds=cmd, type=AttackerActionType.EXPLOIT, index=index,
                              descr="A dictionary attack that tries common passwords and usernames"
                                    "for MySQL where username=password",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.SHELL_ACCESS,
                              vulnerability=constants.EXPLOIT_VULNERABILITES.MYSQL_DICTS_SAME_USER_PASS,
                              backdoor=False)

    @staticmethod
    def SMTP_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against smtp

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        smtp_args = constants.NMAP.SMTP_BRUTE_HOST
        id = AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if subnet:
            smtp_args = constants.NMAP.SMTP_BRUTE_SUBNET
            id = AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET

        if index == -1:
            id = AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL

        cmd = ["sudo nmap " + smtp_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="SMTP dictionary attack for username=pw",
                              cmds=cmd, type=AttackerActionType.EXPLOIT, index=index,
                              descr="A dictionary attack that tries common passwords and usernames"
                                    "for SMTP where username=password",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.SHELL_ACCESS,
                              vulnerability=constants.EXPLOIT_VULNERABILITES.SMTP_DICTS_SAME_USER_PASS,
                              backdoor=False)

    @staticmethod
    def POSTGRES_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ips:List[str] = None) -> AttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against postgres

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        postgres_args = constants.NMAP.POSTGRES_BRUTE_HOST
        id = AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if subnet:
            postgres_args = constants.NMAP.POSTGRES_BRUTE_SUBNET
            id = AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET

        if index == -1:
            id = AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL

        cmd = ["sudo nmap " + postgres_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="Postgres dictionary attack for username=pw",
                              cmds=cmd, type=AttackerActionType.EXPLOIT, index=index,
                              descr="A dictionary attack that tries common passwords and usernames"
                                    "for Postgres where username=password",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.SHELL_ACCESS,
                              vulnerability=constants.EXPLOIT_VULNERABILITES.POSTGRES_DICTS_SAME_USER_PASS,
                              backdoor=False)

    @staticmethod
    def FIREWALK(index: int, subnet=True, ips: List[str] = None) -> AttackerAction:
        """
        Runs a firewalk scan to try to identify and bypass firewalls

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        firewalk_args = constants.NMAP.FIREWALK_HOST
        id = AttackerActionId.FIREWALK_HOST
        if ips is None:
            ips = []
        if subnet:
            firewalk_args = constants.NMAP.FIREWALK_HOST
            id = AttackerActionId.FIREWALK_SUBNET

        if index == -1:
            id = AttackerActionId.FIREWALK_ALL

        cmd = ["sudo nmap " + firewalk_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="Firewalk scan",
                              cmds=cmd, type=AttackerActionType.RECON, index=index,
                              descr="Tries to discover firewall rules using an IP TTL expiration technique "
                            "known as firewalking.",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def HTTP_ENUM(index: int, subnet=True, ips: List[str] = None) -> AttackerAction:
        """
        Runs a HTTP enumeration scan

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        http_enum_args = constants.NMAP.HTTP_ENUM
        id = AttackerActionId.HTTP_ENUM_HOST
        if ips is None:
            ips = []
        if subnet:
            http_enum_args = constants.NMAP.HTTP_ENUM
            id = AttackerActionId.HTTP_ENUM_SUBNET

        if index == -1:
            id = AttackerActionId.HTTP_ENUM_ALL

        cmd = ["sudo nmap " + http_enum_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="HTTP Enum",
                              cmds=cmd, type=AttackerActionType.RECON, index=index,
                              descr="Enumerates directories used by popular web applications and servers.",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def HTTP_GREP(index: int, subnet=True, ips: List[str] = None) -> AttackerAction:
        """
        Runs a HTTP grep scan

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        http_grep_args = constants.NMAP.HTTP_GREP
        id = AttackerActionId.HTTP_GREP_HOST

        if ips is None:
            ips = []

        if subnet:
            http_grep_args = constants.NMAP.HTTP_GREP
            id = AttackerActionId.HTTP_GREP_SUBNET

        if index == -1:
            id = AttackerActionId.HTTP_GREP_ALL

        cmd = ["sudo nmap " + http_grep_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="HTTP Grep",
                              cmds=cmd, type=AttackerActionType.RECON, index=index,
                              descr="Spiders a website and attempts to match all pages and urls to find ips and emails.",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)

    @staticmethod
    def FINGER(index: int, subnet=True, ips: List[str] = None) -> AttackerAction:
        """
        Runs a fingerprint scan

        :param index: index of the machine to apply the action to
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        finger_args = constants.NMAP.FINGER
        id = AttackerActionId.FINGER_HOST

        if ips is None:
            ips = []

        if subnet:
            finger_args = constants.NMAP.FINGER
            id = AttackerActionId.FINGER_SUBNET

        if index == -1:
            id = AttackerActionId.FINGER_ALL

        cmd = ["sudo nmap " + finger_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return AttackerAction(id=id, name="Finger",
                              cmds=cmd, type=AttackerActionType.RECON, index=index,
                              descr="Attempts to retrieve a list of usernames using the finger service.",
                              ips=ips, subnet=subnet, action_outcome=AttackerActionOutcome.INFORMATION_GATHERING,
                              backdoor=False)
