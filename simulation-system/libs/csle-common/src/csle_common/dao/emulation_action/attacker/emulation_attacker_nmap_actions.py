from typing import Optional, List
import csle_common.constants.constants as constants
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome


class EmulationAttackerNMAPActions:
    """
    Class containing Attacker NMAP actions in the emulation
    """

    @staticmethod
    def TCP_SYN_STEALTH_SCAN(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a TCP SYN scan

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_ALL

        cmd = ["sudo nmap -sS -p- " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="TCP SYN (Stealth) Scan", cmds=cmd,
                                       type=EmulationAttackerActionType.RECON,
                                       descr="A stealthy and fast TCP SYN scan to detect open TCP ports on the subnet",
                                       ips=ips, index=index,
                                       action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                       backdoor=False)

    @staticmethod
    def PING_SCAN(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a Ping scan

        :param index: index of the machine to apply the action to
        :param ips: ip of the machine or subnet to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.PING_SCAN_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.PING_SCAN_ALL

        cmd = ["sudo nmap -sP " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="Ping Scan", cmds=cmd,
                                       type=EmulationAttackerActionType.RECON,
                                       descr="A host discovery scan, it is quick because it only checks of hosts "
                                             "are up with Ping, without scanning the ports.",
                                       ips=ips, index=index,
                                       action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                       backdoor=False)

    @staticmethod
    def UDP_PORT_SCAN(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a UDP port scan

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.UDP_PORT_SCAN_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.UDP_PORT_SCAN_ALL

        cmd = ["sudo nmap -sU -p- " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="UDP Port Scan", cmds=cmd,
                                       type=EmulationAttackerActionType.RECON,
                                       descr="", index=index,
                                       ips=ips,
                                       action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                       backdoor=False)

    @staticmethod
    def TCP_CON_NON_STEALTH_SCAN(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a TCP CON (non-stealthy) scan

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.TCP_CON_NON_STEALTH_SCAN_HOST
        if ips is None:
            ips = []

        if index == -1:
            id = EmulationAttackerActionId.TCP_CON_NON_STEALTH_SCAN_ALL

        cmd = ["sudo nmap -sT -p- " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(
            id=id, name="TCP Connection (Non-Stealth) Scan", cmds=cmd,
            type=EmulationAttackerActionType.RECON, index=index,
            descr="A non-stealthy and fast TCP SYN scan to detect open TCP ports on the subnet",
            ips=ips, action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
            backdoor=False)

    @staticmethod
    def TCP_FIN_SCAN(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a TCP FIN scan

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.TCP_FIN_SCAN_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.TCP_FIN_SCAN_ALL

        cmd = ["sudo nmap -sF -p- " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(
            id=id, name="FIN Scan", cmds=cmd,
            type=EmulationAttackerActionType.RECON, index=index,
            descr="A special type of TCP port scan using FIN, can avoid IDS and firewalls that block SYN scans",
            ips=ips, action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
            backdoor=False)

    @staticmethod
    def TCP_NULL_SCAN(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a TCP Null scan

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.TCP_NULL_SCAN_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.TCP_NULL_SCAN_ALL

        cmd = ["sudo nmap -sN -p- " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(
            id=id, name="Null Scan", cmds=cmd, index=index, type=EmulationAttackerActionType.RECON,
            descr="A special type of TCP port scan using Null, can avoid IDS and firewalls that block SYN scans",
            ips=ips, action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING, backdoor=False)

    @staticmethod
    def TCP_XMAS_TREE_SCAN(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a TCP XMAS TREE scan

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.TCP_XMAS_TREE_SCAN_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.TCP_XMAS_TREE_SCAN_ALL

        cmd = ["sudo nmap -sX -p- " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="Xmas Tree Scan",
                                       cmds=cmd, type=EmulationAttackerActionType.RECON, index=index,
                                       descr="A special type of TCP port scan using XMas Tree, "
                                             "can avoid IDS and firewalls that block SYN scans",
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                       backdoor=False)

    @staticmethod
    def OS_DETECTION_SCAN(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a OS detection scan

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.OS_DETECTION_SCAN_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.OS_DETECTION_SCAN_ALL

        cmd = ["sudo nmap -O --osscan-guess --max-os-tries 1 " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="OS detection scan",
                                       cmds=cmd, type=EmulationAttackerActionType.RECON,
                                       descr="OS detection/guess scan", index=index,
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                       backdoor=False)

    @staticmethod
    def VULSCAN(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a vulnerability scan using the VULSCAN script

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.VULSCAN_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.VULSCAN_ALL

        cmd = ["sudo nmap -sV --script=vulscan/vulscan.nse " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="vulscan.nse vulnerability scanner",
                                       cmds=cmd, type=EmulationAttackerActionType.RECON, index=index,
                                       descr="Uses a vulcan.nse script to turn NMAP into a vulnerability scanner",
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                       backdoor=False)

    @staticmethod
    def NMAP_VULNERS(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a vulnerability scan using the Vulners script

        :param index: index of the machine to apply the action to
        :param ips: ip of the machine or subnet to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.NMAP_VULNERS_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.NMAP_VULNERS_ALL

        cmd = ["sudo nmap -sV --script vulners.nse " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="nmap_vulners vulnerability scanner",
                                       cmds=cmd, type=EmulationAttackerActionType.RECON, index=index,
                                       descr="Uses vulners.nse script to turn NMAP into a vulnerability scanner",
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                       backdoor=False)

    @staticmethod
    def TELNET_SAME_USER_PASS_DICTIONARY(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against telnet

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        telnet_args = constants.NMAP.TELNET_BRUTE_HOST
        id = EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL
            telnet_args = constants.NMAP.TELNET_BRUTE_SUBNET

        cmd = ["sudo nmap " + telnet_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(
            id=id, name="Telnet dictionary attack for username=pw",
            cmds=cmd, type=EmulationAttackerActionType.EXPLOIT, index=index,
            descr="A dictionary attack that tries common passwords and usernames "
                  "for Telnet where username=password",
            ips=ips, action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS,
            vulnerability=constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS,
            backdoor=False)

    @staticmethod
    def SSH_SAME_USER_PASS_DICTIONARY(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against ssh

        :param index: index of the machine to apply the action to
        :param ips: ip of the machine or subnet to apply the action to
        :return: the action
        """
        ssh_args = constants.NMAP.SSH_BRUTE_HOST
        id = EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL
            ssh_args = constants.NMAP.SSH_BRUTE_SUBNET

        cmd = ["sudo nmap " + ssh_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="SSH dictionary attack for username=pw",
                                       cmds=cmd, type=EmulationAttackerActionType.EXPLOIT, index=index,
                                       descr="A dictionary attack that tries common passwords and usernames "
                                             "for SSH where username=password",
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS,
                                       vulnerability=constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS,
                                       backdoor=False)

    @staticmethod
    def FTP_SAME_USER_PASS_DICTIONARY(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against ftp

        :param index: index of the machine to apply the action to
        :param ips: ip of the machine or subnet to apply the action to
        :return: the action
        """
        ftp_args = constants.NMAP.FTP_BRUTE_HOST
        id = EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL
            ftp_args = constants.NMAP.FTP_BRUTE_SUBNET

        cmd = ["sudo nmap " + ftp_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="FTP dictionary attack for username=pw",
                                       cmds=cmd, type=EmulationAttackerActionType.EXPLOIT,
                                       descr="A dictionary attack that tries common passwords and usernames "
                                             "for FTP where username=password", index=index,
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS,
                                       vulnerability=constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS,
                                       backdoor=False)

    @staticmethod
    def CASSANDRA_SAME_USER_PASS_DICTIONARY(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against cassandra

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        cassandra_args = constants.NMAP.CASSANDRA_BRUTE_HOST
        id = EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL
            cassandra_args = constants.NMAP.CASSANDRA_BRUTE_SUBNET

        cmd = ["sudo nmap " + cassandra_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="Cassandra dictionary attack for username=pw",
                                       cmds=cmd, type=EmulationAttackerActionType.EXPLOIT,
                                       descr="A dictionary attack that tries common passwords and usernames "
                                             "for Cassandra where username=password", index=index,
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS,
                                       vulnerability=constants.EXPLOIT_VULNERABILITES.CASSANDRA_DICTS_SAME_USER_PASS,
                                       backdoor=False)

    @staticmethod
    def IRC_SAME_USER_PASS_DICTIONARY(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against irc

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        irc_args = constants.NMAP.IRC_BRUTE_HOST
        id = EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL
            irc_args = constants.NMAP.IRC_BRUTE_SUBNET

        cmd = ["sudo nmap " + irc_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="IRC dictionary attack for username=pw",
                                       cmds=cmd, type=EmulationAttackerActionType.EXPLOIT,
                                       descr="A dictionary attack that tries common passwords and usernames "
                                             "for IRC where username=password", index=index,
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS,
                                       vulnerability=constants.EXPLOIT_VULNERABILITES.IRC_DICTS_SAME_USER_PASS,
                                       backdoor=False)

    @staticmethod
    def MONGO_SAME_USER_PASS_DICTIONARY(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against mongo

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        mongo_args = constants.NMAP.MONGO_BRUTE_HOST
        id = EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if index == -1:
            id = EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL
            mongo_args = constants.NMAP.MONGO_BRUTE_SUBNET

        cmd = ["sudo nmap " + mongo_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="MongoDB dictionary attack for username=pw",
                                       cmds=cmd, type=EmulationAttackerActionType.EXPLOIT, index=index,
                                       descr="A dictionary attack that tries common passwords and usernames "
                                             "for MongoDB where username=password",
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS,
                                       vulnerability=constants.EXPLOIT_VULNERABILITES.MONGO_DICTS_SAME_USER_PASS,
                                       backdoor=False)

    @staticmethod
    def MYSQL_SAME_USER_PASS_DICTIONARY(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against mysql

        :param index: index of the machine to apply the action to
        :param ips: ip of the machines or subnets to apply the action to
        :return: the action
        """
        mysql_args = constants.NMAP.MYSQL_BRUTE_HOST
        id = EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if index == -1:
            mysql_args = constants.NMAP.MYSQL_BRUTE_SUBNET
            id = EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL

        cmd = ["sudo nmap " + mysql_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="MySQL dictionary attack for username=pw",
                                       cmds=cmd, type=EmulationAttackerActionType.EXPLOIT, index=index,
                                       descr="A dictionary attack that tries common passwords and usernames "
                                             "for MySQL where username=password",
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS,
                                       vulnerability=constants.EXPLOIT_VULNERABILITES.MYSQL_DICTS_SAME_USER_PASS,
                                       backdoor=False)

    @staticmethod
    def SMTP_SAME_USER_PASS_DICTIONARY(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against smtp

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        smtp_args = constants.NMAP.SMTP_BRUTE_HOST
        id = EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if index == -1:
            smtp_args = constants.NMAP.SMTP_BRUTE_SUBNET
            id = EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL

        cmd = ["sudo nmap " + smtp_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="SMTP dictionary attack for username=pw",
                                       cmds=cmd, type=EmulationAttackerActionType.EXPLOIT, index=index,
                                       descr="A dictionary attack that tries common passwords and usernames "
                                             "for SMTP where username=password",
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS,
                                       vulnerability=constants.EXPLOIT_VULNERABILITES.SMTP_DICTS_SAME_USER_PASS,
                                       backdoor=False)

    @staticmethod
    def POSTGRES_SAME_USER_PASS_DICTIONARY(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a dictionary attack trying combinations with same user+pw against postgres

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        postgres_args = constants.NMAP.POSTGRES_BRUTE_HOST
        id = EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST
        if ips is None:
            ips = []
        if index == -1:
            postgres_args = constants.NMAP.POSTGRES_BRUTE_SUBNET
            id = EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL

        cmd = ["sudo nmap " + postgres_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="Postgres dictionary attack for username=pw",
                                       cmds=cmd, type=EmulationAttackerActionType.EXPLOIT, index=index,
                                       descr="A dictionary attack that tries common passwords and usernames "
                                             "for Postgres where username=password",
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS,
                                       vulnerability=constants.EXPLOIT_VULNERABILITES.POSTGRES_DICTS_SAME_USER_PASS,
                                       backdoor=False)

    @staticmethod
    def FIREWALK(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a firewalk scan to try to identify and bypass firewalls

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        firewalk_args = constants.NMAP.FIREWALK_HOST
        id = EmulationAttackerActionId.FIREWALK_HOST
        if ips is None:
            ips = []
        if index == -1:
            firewalk_args = constants.NMAP.FIREWALK_HOST
            id = EmulationAttackerActionId.FIREWALK_ALL

        cmd = ["sudo nmap " + firewalk_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="Firewalk scan",
                                       cmds=cmd, type=EmulationAttackerActionType.RECON, index=index,
                                       descr="Tries to discover firewall rules using an IP TTL expiration technique "
                                             "known as firewalking.",
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                       backdoor=False)

    @staticmethod
    def HTTP_ENUM(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a HTTP enumeration scan

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        http_enum_args = constants.NMAP.HTTP_ENUM
        id = EmulationAttackerActionId.HTTP_ENUM_HOST
        if ips is None:
            ips = []
        if index == -1:
            http_enum_args = constants.NMAP.HTTP_ENUM
            id = EmulationAttackerActionId.HTTP_ENUM_ALL

        cmd = ["sudo nmap " + http_enum_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="HTTP Enum",
                                       cmds=cmd, type=EmulationAttackerActionType.RECON, index=index,
                                       descr="Enumerates directories used by popular web applications and servers.",
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                       backdoor=False)

    @staticmethod
    def HTTP_GREP(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a HTTP grep scan

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        http_grep_args = constants.NMAP.HTTP_GREP
        id = EmulationAttackerActionId.HTTP_GREP_HOST

        if ips is None:
            ips = []
        if index == -1:
            http_grep_args = constants.NMAP.HTTP_GREP
            id = EmulationAttackerActionId.HTTP_GREP_ALL

        cmd = ["sudo nmap " + http_grep_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="HTTP Grep",
                                       cmds=cmd, type=EmulationAttackerActionType.RECON, index=index,
                                       descr="Spiders a website and attempts to match all pages and urls "
                                             "to find ips and emails.",
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                       backdoor=False)

    @staticmethod
    def FINGER(index: int, ips: Optional[List[str]] = None) -> EmulationAttackerAction:
        """
        Runs a fingerprint scan

        :param index: index of the machine to apply the action to
        :param ips: ips of the machines or subnets to apply the action to
        :return: the action
        """
        finger_args = constants.NMAP.FINGER
        id = EmulationAttackerActionId.FINGER_HOST

        if ips is None:
            ips = []
        if index == -1:
            finger_args = constants.NMAP.FINGER
            id = EmulationAttackerActionId.FINGER_ALL

        cmd = ["sudo nmap " + finger_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return EmulationAttackerAction(id=id, name="Finger",
                                       cmds=cmd, type=EmulationAttackerActionType.RECON, index=index,
                                       descr="Attempts to retrieve a list of usernames using the finger service.",
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                       backdoor=False)
