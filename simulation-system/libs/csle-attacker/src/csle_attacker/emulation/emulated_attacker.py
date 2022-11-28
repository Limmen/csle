from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_attacker.emulation.recon_middleware import ReconMiddleware
from csle_attacker.emulation.exploit_middleware import ExploitMiddleware
from csle_attacker.emulation.attacker_stopping_middleware import AttackerStoppingMiddleware
from csle_attacker.emulation.post_exploit_middleware import PostExploitMiddleware
from csle_common.util.env_dynamics_util import EnvDynamicsUtil
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction


class EmulatedAttacker:
    """
    Represents an emulated attacker agent
    """

    @staticmethod
    def attacker_transition(s: EmulationEnvState, attacker_action: EmulationAttackerAction) -> EmulationEnvState:
        """
        Implements the transition operator T: (s,a) -> s'

        :param s: the current state
        :param attacker_action: the attacker action
        :param emulation_env_config: the emulation environment configuration
        :return: s'
        """
        if attacker_action.type == EmulationAttackerActionType.RECON:
            EnvDynamicsUtil.cache_attacker_action(a=attacker_action, s=s)
            return EmulatedAttacker.attacker_recon_action(s=s, a=attacker_action)
        elif attacker_action.type == EmulationAttackerActionType.EXPLOIT \
                or attacker_action.type == EmulationAttackerActionType.PRIVILEGE_ESCALATION:
            if attacker_action.index == -1:
                EnvDynamicsUtil.cache_attacker_action(a=attacker_action, s=s)
            return EmulatedAttacker.attacker_exploit_action(s=s, a=attacker_action)
        elif attacker_action.type == EmulationAttackerActionType.POST_EXPLOIT:
            return EmulatedAttacker.attacker_post_exploit_action(s=s, a=attacker_action)
        elif attacker_action.type == EmulationAttackerActionType.STOP \
                or attacker_action.type == EmulationAttackerActionType.CONTINUE:
            return EmulatedAttacker.attacker_stopping_action(s=s, a=attacker_action)
        else:
            raise ValueError("Action type not recognized")

    @staticmethod
    def attacker_recon_action(s: EmulationEnvState, a: EmulationAttackerAction) \
            -> EmulationEnvState:
        """
        Implements the transition of a reconnaissance action

        :param s: the current state
        :param a: the action
        :return: s'
        """
        if a.id == EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST \
                or a.id == EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_ALL:
            return ReconMiddleware.execute_tcp_syn_stealth_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.PING_SCAN_HOST or a.id == EmulationAttackerActionId.PING_SCAN_ALL:
            return ReconMiddleware.execute_ping_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.UDP_PORT_SCAN_HOST \
                or a.id == EmulationAttackerActionId.UDP_PORT_SCAN_ALL:
            return ReconMiddleware.execute_udp_port_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.TCP_CON_NON_STEALTH_SCAN_HOST \
                or a.id == EmulationAttackerActionId.TCP_CON_NON_STEALTH_SCAN_ALL:
            return ReconMiddleware.execute_tcp_con_stealth_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.TCP_FIN_SCAN_HOST or a.id == EmulationAttackerActionId.TCP_FIN_SCAN_ALL:
            return ReconMiddleware.execute_tcp_fin_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.TCP_NULL_SCAN_HOST \
                or a.id == EmulationAttackerActionId.TCP_NULL_SCAN_ALL:
            return ReconMiddleware.execute_tcp_null_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.TCP_XMAS_TREE_SCAN_HOST \
                or a.id == EmulationAttackerActionId.TCP_XMAS_TREE_SCAN_ALL:
            return ReconMiddleware.execute_tcp_xmas_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.OS_DETECTION_SCAN_HOST \
                or a.id == EmulationAttackerActionId.OS_DETECTION_SCAN_ALL:
            return ReconMiddleware.execute_os_detection_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.VULSCAN_HOST \
                or a.id == EmulationAttackerActionId.VULSCAN_ALL:
            return ReconMiddleware.execute_vulscan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.NMAP_VULNERS_HOST  \
                or a.id == EmulationAttackerActionId.NMAP_VULNERS_ALL:
            return ReconMiddleware.execute_nmap_vulners(s=s, a=a)
        elif a.id == EmulationAttackerActionId.NIKTO_WEB_HOST_SCAN:
            return ReconMiddleware.execute_nikto_web_host_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.MASSCAN_HOST_SCAN or a.id == EmulationAttackerActionId.MASSCAN_ALL_SCAN:
            return ReconMiddleware.execute_masscan_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.FIREWALK_HOST \
                or a.id == EmulationAttackerActionId.FIREWALK_ALL:
            return ReconMiddleware.execute_firewalk_scan(s=s, a=a)
        elif a.id == EmulationAttackerActionId.HTTP_ENUM_HOST  \
                or a.id == EmulationAttackerActionId.HTTP_ENUM_ALL:
            return ReconMiddleware.execute_http_enum(s=s, a=a)
        elif a.id == EmulationAttackerActionId.HTTP_GREP_HOST \
                or a.id == EmulationAttackerActionId.HTTP_GREP_ALL:
            return ReconMiddleware.execute_http_grep(s=s, a=a)
        elif a.id == EmulationAttackerActionId.FINGER_HOST \
                or a.id == EmulationAttackerActionId.FINGER_ALL:
            return ReconMiddleware.execute_finger(s=s, a=a)
        else:
            raise ValueError("Recon action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def attacker_exploit_action(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Implements transition of an exploit action

        :param s: the current state
        :param a: the action
        :return: s'
        """
        if a.id == EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_telnet_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_ssh_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_ftp_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_cassandra_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_irc_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_mongo_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_mysql_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_smtp_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_postgres_same_user_dictionary(s=s, a=a)
        elif a.id == EmulationAttackerActionId.SAMBACRY_EXPLOIT:
            return ExploitMiddleware.execute_sambacry(s=s, a=a)
        elif a.id == EmulationAttackerActionId.SHELLSHOCK_EXPLOIT:
            return ExploitMiddleware.execute_shellshock(s=s, a=a)
        elif a.id == EmulationAttackerActionId.DVWA_SQL_INJECTION:
            return ExploitMiddleware.execute_dvwa_sql_injection(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CVE_2015_3306_EXPLOIT:
            return ExploitMiddleware.execute_cve_2015_3306_exploit(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CVE_2015_1427_EXPLOIT:
            return ExploitMiddleware.execute_cve_2015_1427_exploit(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CVE_2016_10033_EXPLOIT:
            return ExploitMiddleware.execute_cve_2016_10033_exploit(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CVE_2010_0426_PRIV_ESC:
            return ExploitMiddleware.execute_cve_2010_0426_exploit(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CVE_2015_5602_PRIV_ESC:
            return ExploitMiddleware.execute_cve_2015_5602_exploit(s=s, a=a)
        else:
            raise ValueError("Exploit action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def attacker_post_exploit_action(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Implements the transition of a post-exploit action

        :param s: the current state
        :param a: the action
        :return: s'
        """
        if a.id == EmulationAttackerActionId.NETWORK_SERVICE_LOGIN:
            return PostExploitMiddleware.execute_service_login(s=s, a=a)
        if a.id == EmulationAttackerActionId.FIND_FLAG:
            return PostExploitMiddleware.execute_bash_find_flag(s=s, a=a)
        if a.id == EmulationAttackerActionId.INSTALL_TOOLS:
            return PostExploitMiddleware.execute_install_tools(s=s, a=a)
        if a.id == EmulationAttackerActionId.SSH_BACKDOOR:
            return PostExploitMiddleware.execute_ssh_backdoor(s=s, a=a)
        else:
            raise ValueError("Post-expoit action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def attacker_stopping_action(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Implements transition of a stopping action of the attacker

        :param s: the current state
        :param a: the action
        :return: s'
        """
        if a.id == EmulationAttackerActionId.STOP:
            return AttackerStoppingMiddleware.stop_intrusion(s=s, a=a)
        elif a.id == EmulationAttackerActionId.CONTINUE:
            return AttackerStoppingMiddleware.continue_intrusion(s=s, a=a)
        else:
            raise ValueError("Stopping action id:{},name:{} not recognized".format(a.id, a.name))
