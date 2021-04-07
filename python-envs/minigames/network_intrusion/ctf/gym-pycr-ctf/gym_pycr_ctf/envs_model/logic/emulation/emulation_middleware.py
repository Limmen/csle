from typing import Tuple
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.dao.action.defender.defender_action import DefenderAction
from gym_pycr_ctf.dao.action.attacker.attacker_action_type import AttackerActionType
from gym_pycr_ctf.dao.action.defender.defender_action_type import DefenderActionType
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_pycr_ctf.envs_model.logic.emulation.recon_middleware import ReconMiddleware
from gym_pycr_ctf.envs_model.logic.emulation.exploit_middleware import ExploitMiddleware
from gym_pycr_ctf.envs_model.logic.emulation.post_exploit_middleware import PostExploitMiddleware
from gym_pycr_ctf.envs_model.logic.emulation.defender_stopping_middleware import DefenderStoppingMiddleware
from gym_pycr_ctf.envs_model.logic.emulation.attacker_stopping_middleware import AttackerStoppingMiddleware
from gym_pycr_ctf.dao.action.defender.defender_action_id import DefenderActionId
from gym_pycr_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
from gym_pycr_ctf.envs_model.logic.emulation.defender_update_state_middleware import DefenderUpdateStateMiddleware

class EmulationMiddleware:
    """
    Class that provides a middleware between the OpenAI Gym Env and the Emulation
    """

    @staticmethod
    def attacker_transition(s: EnvState, attacker_action: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Implements the transition operator T: (s,a) -> (s',r)

        :param s: the current state
        :param attacker_action: the attacker action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if attacker_action.type == AttackerActionType.RECON:
            EnvDynamicsUtil.cache_action(env_config=env_config, a=attacker_action, s=s)
            return EmulationMiddleware.attacker_recon_action(s=s, a=attacker_action, env_config=env_config)
        elif attacker_action.type == AttackerActionType.EXPLOIT or attacker_action.type == AttackerActionType.PRIVILEGE_ESCALATION:
            if attacker_action.subnet:
                EnvDynamicsUtil.cache_action(env_config=env_config, a=attacker_action, s=s)
            return EmulationMiddleware.attacker_exploit_action(s=s, a=attacker_action, env_config=env_config)
        elif attacker_action.type == AttackerActionType.POST_EXPLOIT:
            return EmulationMiddleware.attacker_post_exploit_action(s=s, a=attacker_action, env_config=env_config)
        elif attacker_action.type == AttackerActionType.STOP or attacker_action.type == AttackerActionType.CONTINUE:
            return EmulationMiddleware.attacker_stopping_action(s=s, a=attacker_action, env_config=env_config)
        else:
            raise ValueError("Action type not recognized")

    @staticmethod
    def defender_transition(s: EnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                            env_config: EnvConfig) -> Tuple[
        EnvState, int, bool]:
        """
        Implements the transition operator T: (s,a) -> (s',r)

        :param s: the current state
        :param defender_action: the defender action
        :param attacker_action: the previous action of the attacker
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if defender_action.type == DefenderActionType.STOP or defender_action.type == DefenderActionType.CONTINUE:
            return EmulationMiddleware.defender_stopping_action(s=s, defender_action=defender_action,
                                                                attacker_action=attacker_action,
                                                                env_config=env_config)
        if defender_action.type == DefenderActionType.STATE_UPDATE:
            return EmulationMiddleware.defender_update_state_action(s=s, a=defender_action, env_config=env_config)
        else:
            raise ValueError("Action type not recognized")

    @staticmethod
    def attacker_recon_action(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Implements the transition of a reconnaissance action

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == AttackerActionId.TCP_SYN_STEALTH_SCAN_SUBNET or a.id == AttackerActionId.TCP_SYN_STEALTH_SCAN_HOST \
                or a.id == AttackerActionId.TCP_SYN_STEALTH_SCAN_ALL:
            return ReconMiddleware.execute_tcp_syn_stealth_scan(s=s,a=a,env_config=env_config)
        elif a.id == AttackerActionId.PING_SCAN_SUBNET or a.id == AttackerActionId.PING_SCAN_HOST or a.id == AttackerActionId.PING_SCAN_ALL:
            return ReconMiddleware.execute_ping_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.UDP_PORT_SCAN_SUBNET or a.id == AttackerActionId.UDP_PORT_SCAN_HOST \
                or a.id == AttackerActionId.UDP_PORT_SCAN_ALL:
            return ReconMiddleware.execute_udp_port_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET or a.id == AttackerActionId.TCP_CON_NON_STEALTH_SCAN_HOST \
                or a.id == AttackerActionId.TCP_CON_NON_STEALTH_SCAN_ALL:
            return ReconMiddleware.execute_tcp_con_stealth_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.TCP_FIN_SCAN_SUBNET or a.id == AttackerActionId.TCP_FIN_SCAN_HOST \
                or a.id == AttackerActionId.TCP_FIN_SCAN_ALL:
            return ReconMiddleware.execute_tcp_fin_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.TCP_NULL_SCAN_SUBNET or a.id == AttackerActionId.TCP_NULL_SCAN_HOST \
                or a.id == AttackerActionId.TCP_NULL_SCAN_ALL:
            return ReconMiddleware.execute_tcp_null_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.TCP_XMAS_TREE_SCAN_HOST or a.id == AttackerActionId.TCP_XMAS_TREE_SCAN_SUBNET \
                or a.id == AttackerActionId.TCP_XMAS_TREE_SCAN_ALL:
            return ReconMiddleware.execute_tcp_xmas_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.OS_DETECTION_SCAN_HOST or a.id == AttackerActionId.OS_DETECTION_SCAN_SUBNET \
                or a.id == AttackerActionId.OS_DETECTION_SCAN_ALL:
            return ReconMiddleware.execute_os_detection_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.VULSCAN_HOST or a.id == AttackerActionId.VULSCAN_SUBNET or a.id == AttackerActionId.VULSCAN_ALL:
            return ReconMiddleware.execute_vulscan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.NMAP_VULNERS_HOST or a.id == AttackerActionId.NMAP_VULNERS_SUBNET \
                or a.id == AttackerActionId.NMAP_VULNERS_ALL:
            return ReconMiddleware.execute_nmap_vulners(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.NIKTO_WEB_HOST_SCAN:
            return ReconMiddleware.execute_nikto_web_host_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.MASSCAN_HOST_SCAN or a.id == AttackerActionId.MASSCAN_SUBNET_SCAN:
            return ReconMiddleware.execute_masscan_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.FIREWALK_HOST or a.id == AttackerActionId.FIREWALK_SUBNET or a.id == AttackerActionId.FIREWALK_ALL:
            return ReconMiddleware.execute_firewalk_scan(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.HTTP_ENUM_HOST or a.id == AttackerActionId.HTTP_ENUM_SUBNET or a.id == AttackerActionId.HTTP_ENUM_ALL:
            return ReconMiddleware.execute_http_enum(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.HTTP_GREP_HOST or a.id == AttackerActionId.HTTP_GREP_SUBNET or a.id == AttackerActionId.HTTP_GREP_ALL:
            return ReconMiddleware.execute_http_grep(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.FINGER_HOST or a.id == AttackerActionId.FINGER_SUBNET or a.id == AttackerActionId.FINGER_ALL:
            return ReconMiddleware.execute_finger(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Recon action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def attacker_exploit_action(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Implements transition of an exploit action

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST or a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_telnet_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST or a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_ssh_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST or a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_ftp_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST or a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_cassandra_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST or a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_irc_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST or a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_mongo_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST or a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_mysql_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST or a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_smtp_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST or a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_postgres_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.SAMBACRY_EXPLOIT:
            return ExploitMiddleware.execute_sambacry(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.SHELLSHOCK_EXPLOIT:
            return ExploitMiddleware.execute_shellshock(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.DVWA_SQL_INJECTION:
            return ExploitMiddleware.execute_dvwa_sql_injection(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CVE_2015_3306_EXPLOIT:
            return ExploitMiddleware.execute_cve_2015_3306_exploit(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CVE_2015_1427_EXPLOIT:
            return ExploitMiddleware.execute_cve_2015_1427_exploit(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CVE_2016_10033_EXPLOIT:
            return ExploitMiddleware.execute_cve_2016_10033_exploit(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CVE_2010_0426_PRIV_ESC:
            return ExploitMiddleware.execute_cve_2010_0426_exploit(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CVE_2015_5602_PRIV_ESC:
            return ExploitMiddleware.execute_cve_2015_5602_exploit(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Exploit action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def attacker_post_exploit_action(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Implements the transition of a post-exploit action

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == AttackerActionId.NETWORK_SERVICE_LOGIN:
            return PostExploitMiddleware.execute_service_login(s=s, a=a, env_config=env_config)
        if a.id == AttackerActionId.FIND_FLAG:
            # Temporary
            s_prime = s
            s_prime.all_flags = True
            s_prime.attacker_obs_state.all_flags = True
            s_prime.attacker_obs_state.catched_flags = 3
            return s_prime, env_config.attacker_all_flags_reward, True
            #return PostExploitMiddleware.execute_bash_find_flag(s=s, a=a, env_config=env_config)
        if a.id == AttackerActionId.INSTALL_TOOLS:
            return PostExploitMiddleware.execute_install_tools(s=s, a=a, env_config=env_config)
        if a.id == AttackerActionId.SSH_BACKDOOR:
            return PostExploitMiddleware.execute_ssh_backdoor(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Post-expoit action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def defender_stopping_action(s: EnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                                 env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Implements transition of a stopping action of the defender

        :param s: the current state
        :param defender_action: the defender's action
        :param attacker_action: the previous action of the attacker
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if defender_action.id == DefenderActionId.STOP:
            return DefenderStoppingMiddleware.stop_monitor(s=s, defender_action=defender_action,
                                                           attacker_action=attacker_action,
                                                           env_config=env_config)
        elif defender_action.id == DefenderActionId.CONTINUE:
            return DefenderStoppingMiddleware.continue_monitor(s=s, defender_action=defender_action,
                                                               attacker_action=attacker_action,
                                                               env_config=env_config)
        else:
            raise ValueError("Stopping action id:{},name:{} not recognized".format(defender_action.id, defender_action.name))

    @staticmethod
    def attacker_stopping_action(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Implements transition of a stopping action of the attacker

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == AttackerActionId.STOP:
            return AttackerStoppingMiddleware.stop_intrusion(s=s, a=a, env_config=env_config)
        elif a.id == AttackerActionId.CONTINUE:
            return AttackerStoppingMiddleware.continue_intrusion(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Stopping action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def defender_update_state_action(s: EnvState, a: DefenderAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Implements transition of state update for the defender

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == DefenderActionId.UPDATE_STATE:
            return DefenderUpdateStateMiddleware.update_belief_state(s=s, a=a, env_config=env_config)
        elif a.id == DefenderActionId.INITIALIZE_STATE:
            return DefenderUpdateStateMiddleware.initialize_state(s=s, a=a, env_config=env_config)
        elif a.id == DefenderActionId.RESET_STATE:
            return DefenderUpdateStateMiddleware.reset_state(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("State update action id:{},name:{} not recognized".format(a.id, a.name))