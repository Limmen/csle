from typing import List
import gym
from gym_pycr_pwcrack.dao.action import Action
from gym_pycr_pwcrack.dao.action_type import ActionType
import gym_pycr_pwcrack.constants.constants as constants

class ActionConfig:

    def __init__(self, actions: List[Action]):
        self.actions = actions
        self.num_actions = len(self.actions)
        self.action_space = gym.spaces.Discrete(self.num_actions)
        self.action_lookup_d = {}
        for action in actions:
            self.action_lookup_d[action.id] = action


class NMAPActions:

    @staticmethod
    def TCP_SYN_STEALTH_SCAN(ip, subnet=True):
        cost_noise_multiplier = 1
        if subnet:
            cost_noise_multiplier = 10
        return Action(id=1, name="TCP SYN (Stealth) Scan", cmd="nmap -sS " + constants.NMAP.SPEED_ARGS + " "
                                                               + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
                                                               + ip,
                      type=ActionType.RECON,
                      descr="A stealthy and fast TCP SYN scan to detect open TCP ports on the subnet",
                      cost=1.6*cost_noise_multiplier, noise=2*cost_noise_multiplier)

    @staticmethod
    def PING_SCAN(ip, subnet=True):
        cost_noise_multiplier = 1
        if subnet:
            cost_noise_multiplier = 10
        Action(id=2, name="Ping Scan", cmd="nmap -sP " + constants.NMAP.SPEED_ARGS + " " +
                                           + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
                                           + ip,
               type=ActionType.RECON,
               descr="A host discovery scan, it is quick because it only checks of hosts are up with Ping, without "
                     "scanning the ports.",
               cost=1*cost_noise_multiplier, noise=1*cost_noise_multiplier)

    @staticmethod
    def UDP_PORT_SCAN(ip, subnet=True):
        cost_noise_multiplier = 1
        if subnet:
            cost_noise_multiplier = 10
        Action(id=3, name="UDP Port Scan", cmd="nmap -sU " + constants.NMAP.SPEED_ARGS + " " +
                                               + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
                                               + ip,
               type=ActionType.RECON,
               descr="",
               cost=2*cost_noise_multiplier, noise=3*cost_noise_multiplier),

    @staticmethod
    def TCP_CON_NON_STEALTH_SCAN(ip, subnet=True):
        cost_noise_multiplier = 1
        if subnet:
            cost_noise_multiplier = 10
        Action(id=4, name="TCP Connection (Non-Stealth) Scan", cmd="nmap -sT " + constants.NMAP.SPEED_ARGS + " " +
                                                                   + constants.NMAP.FILE_ARGS + " " + str(
            id) + ".xml" + " "
                                                                   + ip,
               type=ActionType.RECON,
               descr="A non-stealthy and fast TCP SYN scan to detect open TCP ports on the subnet",
               cost=1.6*cost_noise_multiplier, noise=2*cost_noise_multiplier)

    @staticmethod
    def TCP_FIN_SCAN(ip, subnet=True):
        cost_noise_multiplier = 1
        if subnet:
            cost_noise_multiplier = 10
        Action(id=5, name="FIN Scan",
               cmd="nmap -sF " + constants.NMAP.SPEED_ARGS + " " +
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
                   + ip,
               type=ActionType.RECON,
               descr="A special type of TCP port scan using FIN, can avoid IDS and firewalls that block SYN scans",
               cost=2*cost_noise_multiplier, noise=3*cost_noise_multiplier)

    @staticmethod
    def TCP_NULL_SCAN(ip, subnet=True):
        cost_noise_multiplier = 1
        if subnet:
            cost_noise_multiplier = 10
        Action(id=6, name="Null Scan",
               cmd="nmap -sN " + constants.NMAP.SPEED_ARGS + " " +
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
                   + ip,
               type=ActionType.RECON,
               descr="A special type of TCP port scan using Null, can avoid IDS and firewalls that block SYN scans",
               cost=2*cost_noise_multiplier, noise=3*cost_noise_multiplier)

    @staticmethod
    def TCP_XMAS_TREE_SCAN(ip, subnet=True):
        cost_noise_multiplier = 1
        if subnet:
            cost_noise_multiplier = 10
        Action(id=7, name="Xmas Tree Scan",
               cmd="nmap -sX " + constants.NMAP.SPEED_ARGS + " " +
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
                   + ip,
               type=ActionType.RECON,
               descr="A special type of TCP port scan using XMas Tree, "
                     "can avoid IDS and firewalls that block SYN scans",
               cost=2*cost_noise_multiplier, noise=3*cost_noise_multiplier)

    @staticmethod
    def OS_DETECTION_SCAN(ip, subnet=True):
        cost_noise_multiplier = 1
        if subnet:
            cost_noise_multiplier = 10
        Action(id=8, name="OS detection scan",
               cmd="nmap -O --osscan-guess --max-os-tries 1 " + constants.NMAP.SPEED_ARGS + " " +
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
                   + ip,
               type=ActionType.RECON,
               descr="OS detection/guess scan",
               cost=4*cost_noise_multiplier, noise=4*cost_noise_multiplier)

    @staticmethod
    def VULSCAN(ip, subnet=True):
        cost_noise_multiplier = 1
        if subnet:
            cost_noise_multiplier = 10
        Action(id=9, name="vulscan.nse vulnerability scanner",
               cmd="nmap -sV --script=vulscan/vulscan.nse " + constants.NMAP.SPEED_ARGS + " " +
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
                   + ip,
               type=ActionType.RECON,
               descr="Uses a vulcan.nse script to turn NMAP into a vulnerability scanner",
               cost=173*cost_noise_multiplier, noise=5*cost_noise_multiplier)

    @staticmethod
    def NMAP_VULNERS(ip, subnet=True):
        cost_noise_multiplier = 1
        if subnet:
            cost_noise_multiplier = 10
        Action(id=10, name="nmap_vulners vulnerability scanner",
               cmd="nmap -sV --script " + constants.NMAP.SPEED_ARGS + " " +
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
                   + ip,
               type=ActionType.RECON,
               descr="Uses vulners.nse script to turn NMAP into a vulnerability scanner",
               cost=170*cost_noise_multiplier, noise=5*cost_noise_multiplier)

    @staticmethod
    def TELNET_SAME_USER_PASS_DICTIONARY(ip, subnet=True):
        cost_noise_multiplier = 1
        telnet_args = constants.NMAP.TELNET_BRUTE_HOST
        if subnet:
            cost_noise_multiplier = 10
            telnet_args = constants.NMAP.TELNET_BRUTE_SUBNET
        Action(id=11, name="Telnet dictionary attack for username=pw",
               cmd="nmap " + telnet_args + " " + constants.NMAP.SPEED_ARGS + " "
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
                   + ip,
               type=ActionType.RECON,
               descr="A dictionary attack that tries common passwords and usernames "
                     "for Telnet where username=password",
               cost=49*cost_noise_multiplier, noise=6*cost_noise_multiplier)

    @staticmethod
    def SSH_SAME_USER_PASS_DICTIONARY(ip, subnet=True):
        cost_noise_multiplier = 1
        ssh_args = constants.NMAP.SSH_BRUTE_HOST
        if subnet:
            cost_noise_multiplier = 10
            ssh_args = constants.NMAP.SSH_BRUTE_SUBNET
        Action(id=12, name="SSH dictionary attack for username=pw",
               cmd="nmap " + ssh_args + " " + constants.NMAP.SPEED_ARGS + " "
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
                   + ip,
               type=ActionType.RECON,
               descr="A dictionary attack that tries common passwords and usernames"
                      "for SSH where username=password",
               cost=49 * cost_noise_multiplier, noise=6 * cost_noise_multiplier)

    @staticmethod
    def FTP_SAME_USER_PASS_DICTIONARY(ip, subnet=True):
        cost_noise_multiplier = 1
        ftp_args = constants.NMAP.FTP_BRUTE_HOST
        if subnet:
            cost_noise_multiplier = 10
            ftp_args = constants.NMAP.FTP_BRUTE_SUBNET
        Action(id=13, name="FTP dictionary attack for username=pw",
               cmd="nmap " + ftp_args + " " + constants.NMAP.SPEED_ARGS + " "
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
                   + ip,
               type=ActionType.RECON,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for FTP where username=password",
               cost=49 * cost_noise_multiplier, noise=6 * cost_noise_multiplier)

    @staticmethod
    def CASSANDRA_SAME_USER_PASS_DICTIONARY(ip, subnet=True):
        cost_noise_multiplier = 1
        cassandra_args = constants.NMAP.CASSANDRA_BRUTE_HOST
        if subnet:
            cost_noise_multiplier = 10
            cassandra_args = constants.NMAP.CASSANDRA_BRUTE_SUBNET
        Action(id=14, name="Cassandra dictionary attack for username=pw",
               cmd="nmap " + cassandra_args + " " + constants.NMAP.SPEED_ARGS + " "
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " " + ip,
               type=ActionType.RECON,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for Cassandra where username=password",
               cost=49 * cost_noise_multiplier, noise=6 * cost_noise_multiplier)

    @staticmethod
    def IRC_SAME_USER_PASS_DICTIONARY(ip, subnet=True):
        cost_noise_multiplier = 1
        irc_args = constants.NMAP.IRC_BRUTE_HOST
        if subnet:
            cost_noise_multiplier = 10
            irc_args = constants.NMAP.IRC_BRUTE_SUBNET
        Action(id=15, name="IRC dictionary attack for username=pw",
               cmd="nmap " + irc_args + " " + constants.NMAP.SPEED_ARGS + " "
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " " + ip,
               type=ActionType.RECON,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for IRC where username=password",
               cost=49 * cost_noise_multiplier, noise=6 * cost_noise_multiplier)

    @staticmethod
    def MONGO_SAME_USER_PASS_DICTIONARY(ip, subnet=True):
        cost_noise_multiplier = 1
        mongo_args = constants.NMAP.MONGO_BRUTE_HOST
        if subnet:
            cost_noise_multiplier = 10
            mongo_args = constants.NMAP.MONGO_BRUTE_SUBNET
        Action(id=16, name="MongoDB dictionary attack for username=pw",
               cmd="nmap " + mongo_args + " " + constants.NMAP.SPEED_ARGS + " "
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " " + ip,
               type=ActionType.RECON,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for MongoDB where username=password",
               cost=49 * cost_noise_multiplier, noise=6 * cost_noise_multiplier)

    @staticmethod
    def MYSQL_SAME_USER_PASS_DICTIONARY(ip, subnet=True):
        cost_noise_multiplier = 1
        mysql_args = constants.NMAP.MYSQL_BRUTE_HOST
        if subnet:
            cost_noise_multiplier = 10
            mysql_args = constants.NMAP.MYSQL_BRUTE_SUBNET
        Action(id=17, name="MySQL dictionary attack for username=pw",
               cmd="nmap " + mysql_args + " " + constants.NMAP.SPEED_ARGS + " "
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " " + ip,
               type=ActionType.RECON,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for MySQL where username=password",
               cost=49 * cost_noise_multiplier, noise=6 * cost_noise_multiplier)

    @staticmethod
    def SMTP_SAME_USER_PASS_DICTIONARY(ip, subnet=True):
        cost_noise_multiplier = 1
        smtp_args = constants.NMAP.SMTP_BRUTE_HOST
        if subnet:
            cost_noise_multiplier = 10
            smtp_args = constants.NMAP.SMTP_BRUTE_SUBNET
        Action(id=18, name="SMTP dictionary attack for username=pw",
               cmd="nmap " + smtp_args + " " + constants.NMAP.SPEED_ARGS + " "
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " " + ip,
               type=ActionType.RECON,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for SMTP where username=password",
               cost=49 * cost_noise_multiplier, noise=6 * cost_noise_multiplier)

    @staticmethod
    def POSTGRES_SAME_USER_PASS_DICTIONARY(ip, subnet=True):
        cost_noise_multiplier = 1
        postgres_args = constants.NMAP.POSTGRES_BRUTE_HOST
        if subnet:
            cost_noise_multiplier = 10
            postgres_args = constants.NMAP.POSTGRES_BRUTE_SUBNET
        Action(id=19, name="Postgres dictionary attack for username=pw",
               cmd="nmap " + postgres_args + " " + constants.NMAP.SPEED_ARGS + " "
                   + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " " + ip,
               type=ActionType.RECON,
               descr="A dictionary attack that tries common passwords and usernames"
                     "for Postgres where username=password",
               cost=49 * cost_noise_multiplier, noise=6 * cost_noise_multiplier)


# class HYDRAActions:
#     @staticmethod
#     def TELNET_SAME_USER_PASS_DICTIONARY(ip):
#         return Action(id=11, name="Telnet dictionary attack for username=pw ",
#                       cmd="hydra -L " + constants.SECLISTS.TOP_USERNAMES_SHORTLIST + " -P "
#                           + constants.SECLISTS.TOP_USERNAMES_SHORTLIST
#                           + " 172.18.1.3 telnet -V -f" + constants.NMAP.FILE_ARGS + " " + str(id) + ".xml" + " "
#                           + ip,
#                       type=ActionType.RECON,
#                       descr="A dictionary attack that tries common passwords and usernames "
#                             "for Telnet where username=password",
#                       cost=1.6, noise=2)