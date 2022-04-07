from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_attacker.simulation.recon_simulator import ReconSimulator
from csle_attacker.simulation.exploit_simulator import ExploitSimulator
from csle_attacker.simulation.post_exploit_simulator import PostExploitSimulator
from csle_common.util.env_dynamics_util import EnvDynamicsUtil
from csle_attacker.simulation.attacker_stopping_simulator import AttackerStoppingSimulator
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction


class SimulatedAttacker:
    """
    Represents a simulated attacker agent
    """

    @staticmethod
    def attacker_transition(s: EmulationEnvState, attacker_action: EmulationAttackerAction) -> EmulationEnvState:
        """
        Simulates a state transition in the MDP or Markov Game

        :param s: the current state
        :param attacker_action: the action to take
        :return: s_prime
        """
        if attacker_action.type == EmulationAttackerActionType.RECON:
            EnvDynamicsUtil.cache_attacker_action(a=attacker_action, s=s)
            return SimulatedAttacker.attacker_recon_action(s=s, a=attacker_action)
        elif attacker_action.type == EmulationAttackerActionType.EXPLOIT \
                or attacker_action.type == EmulationAttackerActionType.PRIVILEGE_ESCALATION:
            if attacker_action.index == -1:
                EnvDynamicsUtil.cache_attacker_action(a=attacker_action, s=s)
            return SimulatedAttacker.attacker_exploit_action(s=s, a=attacker_action)
        elif attacker_action.type == EmulationAttackerActionType.POST_EXPLOIT:
            return SimulatedAttacker.attacker_post_exploit_action(s=s, a=attacker_action)
        elif attacker_action.type == EmulationAttackerActionType.STOP \
                or attacker_action.type == EmulationAttackerActionType.CONTINUE:
            return SimulatedAttacker.attacker_stopping_action(s=s, a=attacker_action)
        else:
            raise ValueError("Action type:{} not recognized".format(attacker_action.type))


    @staticmethod
    def attacker_recon_action(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a reconnaissance action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        if a.id == EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST \
                or a.id == EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_ALL:
            return ReconSimulator.simulate_tcp_syn_stealth_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.PING_SCAN_HOST or a.id == EmulationAttackerActionId.PING_SCAN_ALL:
            return ReconSimulator.simulate_ping_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.UDP_PORT_SCAN_HOST \
                or a.id == EmulationAttackerActionId.UDP_PORT_SCAN_ALL:
            return ReconSimulator.simulate_udp_port_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.TCP_CON_NON_STEALTH_SCAN_HOST \
                or a.id == EmulationAttackerActionId.TCP_CON_NON_STEALTH_SCAN_ALL:
            return ReconSimulator.simulate_con_non_stealth_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.TCP_FIN_SCAN_HOST \
                or a.id == EmulationAttackerActionId.TCP_FIN_SCAN_ALL:
            return ReconSimulator.simulate_fin_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.TCP_NULL_SCAN_HOST \
                or a.id == EmulationAttackerActionId.TCP_NULL_SCAN_ALL:
            return ReconSimulator.simulate_tcp_null_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.TCP_XMAS_TREE_SCAN_HOST \
                or a.id == EmulationAttackerActionId.TCP_XMAS_TREE_SCAN_ALL:
            return ReconSimulator.simulate_tcp_xmas_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.OS_DETECTION_SCAN_HOST \
                or a.id == EmulationAttackerActionId.OS_DETECTION_SCAN_ALL:
            return ReconSimulator.simulate_os_detection_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.VULSCAN_HOST \
                or a.id == EmulationAttackerActionId.VULSCAN_ALL:
            return ReconSimulator.simulate_vulscan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.NMAP_VULNERS_HOST \
                or a.id == EmulationAttackerActionId.NMAP_VULNERS_ALL:
            return ReconSimulator.simulate_nmap_vulners(s=s, a=a)
        elif a.id == EmulationAttackerActionId.NIKTO_WEB_HOST_SCAN:
            return ReconSimulator.simulate_nikto_web_host_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.MASSCAN_HOST_SCAN or a.id == EmulationAttackerActionId.MASSCAN_ALL_SCAN:
            return ReconSimulator.simulate_masscan_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.FIREWALK_HOST or a.id == EmulationAttackerActionId.FIREWALK_ALL \
                or a.id == EmulationAttackerActionId.FIREWALK_ALL:
            return ReconSimulator.simulate_firewalk_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.HTTP_ENUM_HOST or a.id == EmulationAttackerActionId.HTTP_ENUM_ALL \
                or a.id == EmulationAttackerActionId.HTTP_ENUM_ALL:
            return ReconSimulator.simulate_http_enum(s=s, a=a)
        elif a.id == EmulationAttackerActionId.HTTP_GREP_HOST or a.id == EmulationAttackerActionId.HTTP_GREP_ALL \
                or a.id == EmulationAttackerActionId.HTTP_GREP_ALL:
            return ReconSimulator.simulate_http_grep(s=s, a=a)
        elif a.id == EmulationAttackerActionId.FINGER_HOST or a.id == EmulationAttackerActionId.FINGER_ALL \
                or a.id == EmulationAttackerActionId.FINGER_ALL:
            return ReconSimulator.simulate_finger(s=s, a=a)
        else:
            raise ValueError("Recon action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def attacker_exploit_action(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs an exploit action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        if a.id == EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_telnet_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_ssh_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_ftp_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_cassandra_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_irc_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_mongo_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_mysql_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_smtp_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_postgres_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.SAMBACRY_EXPLOIT:
            return ExploitSimulator.simulate_sambacry_exploit(s=s, a=a)
        elif a.id == EmulationAttackerActionId.SHELLSHOCK_EXPLOIT:
            return ExploitSimulator.simulate_shellshock_exploit(s=s, a=a)
        elif a.id == EmulationAttackerActionId.DVWA_SQL_INJECTION:
            return ExploitSimulator.simulate_sql_injection_exploit(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CVE_2015_3306_EXPLOIT:
            return ExploitSimulator.simulate_cve_2015_3306_exploit(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CVE_2015_1427_EXPLOIT:
            return ExploitSimulator.simulate_cve_2015_1427_exploit(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CVE_2016_10033_EXPLOIT:
            return ExploitSimulator.simulate_cve_2016_10033_exploit(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CVE_2010_0426_PRIV_ESC:
            return ExploitSimulator.simulate_cve_2010_0426_exploit(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CVE_2015_5602_PRIV_ESC:
            return ExploitSimulator.simulate_cve_2015_5602_exploit(s=s, a=a)
        else:
            raise ValueError("Exploit action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def attacker_post_exploit_action(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Simulates a post-exploit action

        :param s: the current state
        :param a: the action
        :return: s'
        """
        if a.id == EmulationAttackerActionId.NETWORK_SERVICE_LOGIN:
            s_1, r_1, _ = PostExploitSimulator.simulate_ssh_login(s=s, a=a)
            s_2, r_2, _ = PostExploitSimulator.simulate_ftp_login(s=s_1, a=a)
            s_3, r_3, done = PostExploitSimulator.simulate_telnet_login(s=s_2, a=a)
            return s_3
        if a.id == EmulationAttackerActionId.FIND_FLAG:
            return PostExploitSimulator.simulate_bash_find_flag(s=s, a=a)
        if a.id == EmulationAttackerActionId.INSTALL_TOOLS:
            return PostExploitSimulator.execute_install_tools(s=s, a=a)
        if a.id == EmulationAttackerActionId.SSH_BACKDOOR:
            return PostExploitSimulator.execute_ssh_backdoor(s=s, a=a)
        else:
            raise ValueError("Post-expoit action id:{},name:{} not recognized".format(a.id, a.name))


    @staticmethod
    def attacker_stopping_action(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Implements transition of a stopping action of the attacker

        :param s: the current state
        :param a: the action
        :return: s', r, done
        """
        if a.id == EmulationAttackerActionId.STOP:
            return AttackerStoppingSimulator.stop_intrusion(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CONTINUE:
            return AttackerStoppingSimulator.continue_intrusion(s=s, a=a)
        else:
            raise ValueError("Stopping action id:{},name:{} not recognized".format(a.id, a.name))