from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_type import ActionType
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.action.action import ActionOutcome

class NMAPActions:

    @staticmethod
    def TCP_SYN_STEALTH_SCAN(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        id = ActionId.TCP_SYN_STEALTH_SCAN_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.TCP_SYN_STEALTH_SCAN_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap -sS -p- " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="TCP SYN (Stealth) Scan", cmd=cmd,
                      type=ActionType.RECON,
                      descr="A stealthy and fast TCP SYN scan to detect open TCP ports on the subnet",
                      cost=0.1*cost_noise_multiplier, noise=0.01*cost_noise_multiplier,
                      ip=ip, subnet=subnet, index=index,
                      action_outcome=ActionOutcome.INFORMATION_GATHERING)

    @staticmethod
    def PING_SCAN(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        id = ActionId.PING_SCAN_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.PING_SCAN_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap -sP -p- " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="Ping Scan", cmd=cmd,
               type=ActionType.RECON,
               descr="A host discovery scan, it is quick because it only checks of hosts are up with Ping, without "
                     "scanning the ports.",
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
               ip=ip, subnet=subnet, index=index,
                      action_outcome=ActionOutcome.INFORMATION_GATHERING)

    @staticmethod
    def UDP_PORT_SCAN(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        id = ActionId.UDP_PORT_SCAN_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.UDP_PORT_SCAN_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap -sU -p- " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="UDP Port Scan", cmd=cmd,
               type=ActionType.RECON,
               descr="", index=index,
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
               ip=ip, subnet=subnet, action_outcome=ActionOutcome.INFORMATION_GATHERING)

    @staticmethod
    def TCP_CON_NON_STEALTH_SCAN(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        id = ActionId.TCP_CON_NON_STEALTH_SCAN_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap -sT -p- " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="TCP Connection (Non-Stealth) Scan", cmd=cmd,
               type=ActionType.RECON, index=index,
               descr="A non-stealthy and fast TCP SYN scan to detect open TCP ports on the subnet",
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
               ip=ip, subnet=subnet, action_outcome=ActionOutcome.INFORMATION_GATHERING)

    @staticmethod
    def TCP_FIN_SCAN(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        id = ActionId.TCP_FIN_SCAN_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.TCP_FIN_SCAN_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap -sF -p- " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="FIN Scan",
               cmd=cmd,
               type=ActionType.RECON, index=index,
               descr="A special type of TCP port scan using FIN, can avoid IDS and firewalls that block SYN scans",
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
               ip=ip, subnet=subnet, action_outcome=ActionOutcome.INFORMATION_GATHERING)

    @staticmethod
    def TCP_NULL_SCAN(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        id = ActionId.TCP_NULL_SCAN_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.TCP_NULL_SCAN_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap -sN -p- " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="Null Scan",
               cmd=cmd, index=index,
               type=ActionType.RECON,
               descr="A special type of TCP port scan using Null, can avoid IDS and firewalls that block SYN scans",
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
               ip=ip, subnet=subnet, action_outcome=ActionOutcome.INFORMATION_GATHERING)

    @staticmethod
    def TCP_XMAS_TREE_SCAN(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        id = ActionId.TCP_XMAS_TREE_SCAN_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.TCP_XMAS_TREE_SCAN_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap -sX -p- " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="Xmas Tree Scan",
               cmd=cmd, type=ActionType.RECON, index=index,
               descr="A special type of TCP port scan using XMas Tree, "
                     "can avoid IDS and firewalls that block SYN scans",
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
               ip=ip, subnet=subnet, action_outcome=ActionOutcome.INFORMATION_GATHERING)

    @staticmethod
    def OS_DETECTION_SCAN(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        id = ActionId.OS_DETECTION_SCAN_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.OS_DETECTION_SCAN_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap -O --osscan-guess --max-os-tries 1 " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="OS detection scan",
               cmd=cmd, type=ActionType.RECON,
               descr="OS detection/guess scan", index=index,
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
               ip=ip, subnet=subnet, action_outcome=ActionOutcome.INFORMATION_GATHERING)

    @staticmethod
    def VULSCAN(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        id = ActionId.VULSCAN_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.VULSCAN_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap -sV --script=vulscan/vulscan.nse " + constants.NMAP.SPEED_ARGS + " " + constants.NMAP.FILE_ARGS \
              + " " + file_name + ip]
        return Action(id=id, name="vulscan.nse vulnerability scanner",
               cmd=cmd, type=ActionType.RECON, index=index,
               descr="Uses a vulcan.nse script to turn NMAP into a vulnerability scanner",
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
               ip=ip, subnet=subnet, action_outcome=ActionOutcome.INFORMATION_GATHERING)

    @staticmethod
    def NMAP_VULNERS(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        id = ActionId.NMAP_VULNERS_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.NMAP_VULNERS_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap -sV --script vulners.nse " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="nmap_vulners vulnerability scanner",
               cmd=cmd, type=ActionType.RECON, index=index,
               descr="Uses vulners.nse script to turn NMAP into a vulnerability scanner",
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
               ip=ip, subnet=subnet, action_outcome=ActionOutcome.INFORMATION_GATHERING)

    @staticmethod
    def TELNET_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        telnet_args = constants.NMAP.TELNET_BRUTE_HOST
        id = ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET
            telnet_args = constants.NMAP.TELNET_BRUTE_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap " + telnet_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="Telnet dictionary attack for username=pw",
               cmd=cmd, type=ActionType.EXPLOIT, index=index,
               descr="A dictionary attack that tries common passwords and usernames "
                     "for Telnet where username=password",
                      cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                      ip=ip, subnet=subnet, action_outcome=ActionOutcome.SHELL_ACCESS,
                      vulnerability="telnet-weak-password")

    @staticmethod
    def SSH_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        ssh_args = constants.NMAP.SSH_BRUTE_HOST
        id = ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET
            ssh_args = constants.NMAP.SSH_BRUTE_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap " + ssh_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="SSH dictionary attack for username=pw",
               cmd=cmd, type=ActionType.EXPLOIT, index=index,
               descr="A dictionary attack that tries common passwords and usernames"
                      "for SSH where username=password",
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                      ip=ip, subnet=subnet, action_outcome=ActionOutcome.SHELL_ACCESS,
                      vulnerability="ssh-weak-password")

    @staticmethod
    def FTP_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        ftp_args = constants.NMAP.FTP_BRUTE_HOST
        id = ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET
            file_name = str(id.value) + ".xml "
            ftp_args = constants.NMAP.FTP_BRUTE_SUBNET

        cmd = ["sudo nmap " + ftp_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="FTP dictionary attack for username=pw",
               cmd=cmd, type=ActionType.EXPLOIT,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for FTP where username=password", index=index,
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                      ip=ip, subnet=subnet, action_outcome=ActionOutcome.SHELL_ACCESS,
                      vulnerability="ftp-weak-password")

    @staticmethod
    def CASSANDRA_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        cassandra_args = constants.NMAP.CASSANDRA_BRUTE_HOST
        id = ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST
        file_name = str(id.value) + "_" + ip + ".xml "

        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET
            cassandra_args = constants.NMAP.CASSANDRA_BRUTE_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap " + cassandra_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="Cassandra dictionary attack for username=pw",
               cmd=cmd, type=ActionType.EXPLOIT,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for Cassandra where username=password", index=index,
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                      ip=ip, subnet=subnet, action_outcome=ActionOutcome.SHELL_ACCESS,
                      vulnerability="cassandra-weak-password")

    @staticmethod
    def IRC_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        irc_args = constants.NMAP.IRC_BRUTE_HOST
        id = ActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET
            irc_args = constants.NMAP.IRC_BRUTE_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap " + irc_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="IRC dictionary attack for username=pw",
               cmd=cmd, type=ActionType.EXPLOIT,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for IRC where username=password", index=index,
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                      ip=ip, subnet=subnet, action_outcome=ActionOutcome.SHELL_ACCESS,
                      vulnerability="irc-weak-password")

    @staticmethod
    def MONGO_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        mongo_args = constants.NMAP.MONGO_BRUTE_HOST
        id = ActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST
        file_name = str(id.value) + "_" + ip + ".xml "

        if subnet:
            cost_noise_multiplier = 10
            mongo_args = constants.NMAP.MONGO_BRUTE_SUBNET
            id = ActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap " + mongo_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="MongoDB dictionary attack for username=pw",
               cmd=cmd, type=ActionType.EXPLOIT, index=index,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for MongoDB where username=password",
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                      ip=ip, subnet=subnet, action_outcome=ActionOutcome.SHELL_ACCESS,
                      vulnerability="mongo-weak-password")

    @staticmethod
    def MYSQL_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        mysql_args = constants.NMAP.MYSQL_BRUTE_HOST
        id = ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            mysql_args = constants.NMAP.MYSQL_BRUTE_SUBNET
            id = ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET
            file_name = str(id.value) + ".xml "
        cmd = ["sudo nmap " + mysql_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="MySQL dictionary attack for username=pw",
               cmd=cmd, type=ActionType.EXPLOIT, index=index,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for MySQL where username=password",
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                      ip=ip, subnet=subnet, action_outcome=ActionOutcome.SHELL_ACCESS,
                      vulnerability="mysql-weak-password")

    @staticmethod
    def SMTP_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        smtp_args = constants.NMAP.SMTP_BRUTE_HOST
        id = ActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            smtp_args = constants.NMAP.SMTP_BRUTE_SUBNET
            id = ActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap " + smtp_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="SMTP dictionary attack for username=pw",
               cmd=cmd, type=ActionType.EXPLOIT, index=index,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for SMTP where username=password",
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                      ip=ip, subnet=subnet, action_outcome=ActionOutcome.SHELL_ACCESS,
                      vulnerability="smtp-weak-password")

    @staticmethod
    def POSTGRES_SAME_USER_PASS_DICTIONARY(index:int, subnet=True, ip:str = "") -> Action:
        cost_noise_multiplier = 1
        postgres_args = constants.NMAP.POSTGRES_BRUTE_HOST
        id = ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            postgres_args = constants.NMAP.POSTGRES_BRUTE_SUBNET
            id = ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap " + postgres_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="Postgres dictionary attack for username=pw",
               cmd=cmd, type=ActionType.EXPLOIT, index=index,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for Postgres where username=password",
               cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                      ip=ip, subnet=subnet, action_outcome=ActionOutcome.SHELL_ACCESS,
                      vulnerability="postgres-weak-password")

    @staticmethod
    def FIREWALK(index: int, subnet=True, ip: str = "") -> Action:
        cost_noise_multiplier = 1
        firewalk_args = constants.NMAP.FIREWALK_HOST
        id = ActionId.FIREWALK_HOST
        file_name = str(id.value) + "_" + ip + ".xml "
        if subnet:
            cost_noise_multiplier = 10
            firewalk_args = constants.NMAP.FIREWALK_HOST
            id = ActionId.FIREWALK_SUBNET
            file_name = str(id.value) + ".xml "

        cmd = ["sudo nmap " + firewalk_args + " " + constants.NMAP.SPEED_ARGS + " "]
        return Action(id=id, name="Firewalk scan",
                      cmd=cmd, type=ActionType.RECON, index=index,
                      descr="Tries to discover firewall rules using an IP TTL expiration technique "
                            "known as firewalking.",
                      cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                      ip=ip, subnet=subnet, action_outcome=ActionOutcome.INFORMATION_GATHERING)