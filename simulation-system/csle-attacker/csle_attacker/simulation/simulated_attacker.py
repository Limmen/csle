from typing import Tuple
from csle_common.dao.network.env_state import EnvState
from csle_common.dao.network.env_config import CSLEEnvConfig
from csle_common.dao.action.attacker.attacker_action_type import AttackerActionType
from csle_common.dao.action.attacker.attacker_action_id import AttackerActionId
from csle_attacker.simulation.recon_simulator import ReconSimulator
from csle_attacker.simulation.exploit_simulator import ExploitSimulator
from csle_attacker.simulation.post_exploit_simulator import PostExploitSimulator
from gym_csle_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
from csle_attacker.simulation.attacker_stopping_simulator import AttackerStoppingSimulator
from csle_common.dao.action.attacker.attacker_action import AttackerAction


class SimulatedAttacker:
    """
    Represents a simulated attacker agent
    """

    @staticmethod
    def attacker_transition(s: EnvState, attacker_action: AttackerAction, env_config: CSLEEnvConfig) \
            -> Tuple[EnvState, float, bool]:
        """
        Simulates a state transition in the MDP or Markov Game

        :param s: the current state
        :param attacker_action: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        if attacker_action.type == AttackerActionType.RECON:
            EnvDynamicsUtil.cache_action(env_config=env_config, a=attacker_action, s=s)
            return SimulatedAttacker.attacker_recon_action(s=s, a=attacker_action, env_config=env_config)
        elif attacker_action.type == AttackerActionType.EXPLOIT \
                or attacker_action.type == AttackerActionType.PRIVILEGE_ESCALATION:
            if attacker_action.subnet:
                EnvDynamicsUtil.cache_action(env_config=env_config, a=attacker_action, s=s)
            return SimulatedAttacker.attacker_exploit_action(s=s, a=attacker_action, env_config=env_config)
        elif attacker_action.type == AttackerActionType.POST_EXPLOIT:
            return SimulatedAttacker.attacker_post_exploit_action(s=s, a=attacker_action, env_config=env_config)
        elif attacker_action.type == AttackerActionType.STOP or attacker_action.type == AttackerActionType.CONTINUE:
            return SimulatedAttacker.attacker_stopping_action(s=s, a=attacker_action, env_config=env_config)
        else:
            raise ValueError("Action type:{} not recognized".format(attacker_action.type))


    @staticmethod
    def attacker_recon_action(s: EnvState, a: AttackerAction, env_config: CSLEEnvConfig) \
            -> Tuple[EnvState, float, bool]:
        """
        Performs a reconnaissance action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        if a.id == AttackerActionId.TCP_SYN_STEALTH_SCAN_SUBNET \
                or a.id == AttackerActionId.TCP_SYN_STEALTH_SCAN_HOST \
                or a.id == AttackerActionId.TCP_SYN_STEALTH_SCAN_ALL:
            return ReconSimulator.simulate_tcp_syn_stealth_scan(s=s,a=a,env_config=env_config)
        elif a.id == AttackerActionId.PING_SCAN_SUBNET or a.id == AttackerActionId.PING_SCAN_HOST \
                or a.id == AttackerActionId.PING_SCAN_ALL:
            return ReconSimulator.simulate_ping_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.UDP_PORT_SCAN_SUBNET or a.id == AttackerActionId.UDP_PORT_SCAN_HOST \
                or a.id == AttackerActionId.UDP_PORT_SCAN_ALL:
            return ReconSimulator.simulate_udp_port_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET \
                or a.id == AttackerActionId.TCP_CON_NON_STEALTH_SCAN_HOST \
                or a.id == AttackerActionId.TCP_CON_NON_STEALTH_SCAN_ALL:
            return ReconSimulator.simulate_con_non_stealth_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.TCP_FIN_SCAN_SUBNET or a.id == AttackerActionId.TCP_FIN_SCAN_HOST \
                or a.id == AttackerActionId.TCP_FIN_SCAN_ALL:
            return ReconSimulator.simulate_fin_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.TCP_NULL_SCAN_SUBNET or a.id == AttackerActionId.TCP_NULL_SCAN_HOST \
                or a.id == AttackerActionId.TCP_NULL_SCAN_ALL:
            return ReconSimulator.simulate_tcp_null_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.TCP_XMAS_TREE_SCAN_HOST or a.id == AttackerActionId.TCP_XMAS_TREE_SCAN_SUBNET \
                or a.id == AttackerActionId.TCP_XMAS_TREE_SCAN_ALL:
            return ReconSimulator.simulate_tcp_xmas_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.OS_DETECTION_SCAN_HOST or a.id == AttackerActionId.OS_DETECTION_SCAN_SUBNET \
                or a.id == AttackerActionId.OS_DETECTION_SCAN_ALL:
            return ReconSimulator.simulate_os_detection_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.VULSCAN_HOST or a.id == AttackerActionId.VULSCAN_SUBNET \
                or a.id == AttackerActionId.VULSCAN_ALL:
            return ReconSimulator.simulate_vulscan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.NMAP_VULNERS_HOST or a.id == AttackerActionId.NMAP_VULNERS_SUBNET \
                or a.id == AttackerActionId.NMAP_VULNERS_ALL:
            return ReconSimulator.simulate_nmap_vulners(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.NIKTO_WEB_HOST_SCAN:
            return ReconSimulator.simulate_nikto_web_host_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.MASSCAN_HOST_SCAN or a.id == AttackerActionId.MASSCAN_SUBNET_SCAN:
            return ReconSimulator.simulate_masscan_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.FIREWALK_HOST or a.id == AttackerActionId.FIREWALK_SUBNET \
                or a.id == AttackerActionId.FIREWALK_ALL:
            return ReconSimulator.simulate_firewalk_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.HTTP_ENUM_HOST or a.id == AttackerActionId.HTTP_ENUM_SUBNET \
                or a.id == AttackerActionId.HTTP_ENUM_ALL:
            return ReconSimulator.simulate_http_enum(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.HTTP_GREP_HOST or a.id == AttackerActionId.HTTP_GREP_SUBNET \
                or a.id == AttackerActionId.HTTP_GREP_ALL:
            return ReconSimulator.simulate_http_grep(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.FINGER_HOST or a.id == AttackerActionId.FINGER_SUBNET \
                or a.id == AttackerActionId.FINGER_ALL:
            return ReconSimulator.simulate_finger(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Recon action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def attacker_exploit_action(s: EnvState, a: AttackerAction, env_config: CSLEEnvConfig) \
            -> Tuple[EnvState, float, bool]:
        """
        Performs an exploit action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        if a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_telnet_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_ssh_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_ftp_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_cassandra_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_irc_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_mongo_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_mysql_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_smtp_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_postgres_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.SAMBACRY_EXPLOIT:
            return ExploitSimulator.simulate_sambacry_exploit(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.SHELLSHOCK_EXPLOIT:
            return ExploitSimulator.simulate_shellshock_exploit(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.DVWA_SQL_INJECTION:
            return ExploitSimulator.simulate_sql_injection_exploit(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CVE_2015_3306_EXPLOIT:
            return ExploitSimulator.simulate_cve_2015_3306_exploit(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CVE_2015_1427_EXPLOIT:
            return ExploitSimulator.simulate_cve_2015_1427_exploit(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CVE_2016_10033_EXPLOIT:
            return ExploitSimulator.simulate_cve_2016_10033_exploit(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CVE_2010_0426_PRIV_ESC:
            return ExploitSimulator.simulate_cve_2010_0426_exploit(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CVE_2015_5602_PRIV_ESC:
            return ExploitSimulator.simulate_cve_2015_5602_exploit(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Exploit action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def attacker_post_exploit_action(s: EnvState, a: AttackerAction, env_config: CSLEEnvConfig) \
            -> Tuple[EnvState, float, bool]:
        """
        Simulates a post-exploit action

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == AttackerActionId.NETWORK_SERVICE_LOGIN:
            s_1, r_1, _ = PostExploitSimulator.simulate_ssh_login(s=s, a=a, env_config=env_config)
            s_2, r_2, _ = PostExploitSimulator.simulate_ftp_login(s=s_1, a=a, env_config=env_config)
            s_3, r_3, done = PostExploitSimulator.simulate_telnet_login(s=s_2, a=a, env_config=env_config)
            rewards = list(filter(lambda x: x >= 0, [r_1, r_2, r_3]))
            if len(rewards) > 0:
                reward = sum(rewards)
            else:
                reward = r_3
            return s_3, reward, done
        if a.id == AttackerActionId.FIND_FLAG:
            return PostExploitSimulator.simulate_bash_find_flag(s=s, a=a, env_config=env_config)
        if a.id == AttackerActionId.INSTALL_TOOLS:
            return PostExploitSimulator.execute_install_tools(s=s, a=a, env_config=env_config)
        if a.id == AttackerActionId.SSH_BACKDOOR:
            return PostExploitSimulator.execute_ssh_backdoor(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Post-expoit action id:{},name:{} not recognized".format(a.id, a.name))


    @staticmethod
    def attacker_stopping_action(s: EnvState, a: AttackerAction, env_config: CSLEEnvConfig) \
            -> Tuple[EnvState, float, bool]:
        """
        Implements transition of a stopping action of the attacker

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == AttackerActionId.STOP:
            return AttackerStoppingSimulator.stop_intrusion(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CONTINUE:
            return AttackerStoppingSimulator.continue_intrusion(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Stopping action id:{},name:{} not recognized".format(a.id, a.name))