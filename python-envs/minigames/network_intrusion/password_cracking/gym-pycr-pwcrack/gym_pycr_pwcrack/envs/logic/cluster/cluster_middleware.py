from typing import Union
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_type import ActionType
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.envs.logic.cluster.recon_middleware import ReconMiddleware
from gym_pycr_pwcrack.envs.logic.cluster.exploit_middleware import ExploitMiddleware

class ClusterMiddleware:
    """
    Class that provides a middleware between the OpenAI Gym Env and the Cluster
    """

    @staticmethod
    def transition(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Implements the transition operator T: (s,a) -> (s',r)

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.type == ActionType.RECON:
            return ClusterMiddleware.recon_action(s=s,a=a,env_config=env_config)
        elif a.type == ActionType.EXPLOIT:
            return ClusterMiddleware.exploit_action(s=s, a=a, env_config=env_config)
        elif a.type == ActionType.POST_EXPLOIT:
            return ClusterMiddleware.post_exploit_action(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Action type not recognized")

    @staticmethod
    def recon_action(s: EnvState, a: Action, env_config: EnvConfig):
        """
        Implements the transition of a reconnaissance action

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == ActionId.TCP_SYN_STEALTH_SCAN_SUBNET or a.id == ActionId.TCP_SYN_STEALTH_SCAN_HOST:
            return ReconMiddleware.execute_tcp_syn_stealth_scan(s=s,a=a,env_config=env_config)
        elif a.id == ActionId.PING_SCAN_SUBNET or a.id == ActionId.PING_SCAN_HOST:
            return ReconMiddleware.execute_ping_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.UDP_PORT_SCAN_SUBNET or a.id == ActionId.UDP_PORT_SCAN_HOST:
            return ReconMiddleware.execute_udp_port_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET or a.id == ActionId.TCP_CON_NON_STEALTH_SCAN_HOST:
            return ReconMiddleware.execute_tcp_con_stealth_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_FIN_SCAN_SUBNET or a.id == ActionId.TCP_FIN_SCAN_HOST:
            return ReconMiddleware.execute_tcp_fin_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_NULL_SCAN_SUBNET or a.id == ActionId.TCP_NULL_SCAN_HOST:
            return ReconMiddleware.execute_tcp_null_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_XMAS_TREE_SCAN_HOST or a.id == ActionId.TCP_XMAS_TREE_SCAN_SUBNET:
            return ReconMiddleware.execute_tcp_xmas_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.OS_DETECTION_SCAN_HOST or a.id == ActionId.OS_DETECTION_SCAN_SUBNET:
            return ReconMiddleware.execute_os_detection_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.VULSCAN_HOST or a.id == ActionId.VULSCAN_SUBNET:
            return ReconMiddleware.execute_vulscan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.NMAP_VULNERS_HOST or a.id == ActionId.NMAP_VULNERS_SUBNET:
            return ReconMiddleware.execute_nmap_vulners(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Recon action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def exploit_action(s: EnvState, a: Action, env_config: EnvConfig):
        """
        Implements transition of an exploit action

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET:
            return ExploitMiddleware.simulate_telnet_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET:
            return ExploitMiddleware.simulate_ssh_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET:
            return ExploitMiddleware.simulate_ftp_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET:
            return ExploitMiddleware.simulate_cassandra_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET:
            return ExploitMiddleware.simulate_irc_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET:
            return ExploitMiddleware.simulate_mongo_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET:
            return ExploitMiddleware.simulate_mysql_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET:
            return ExploitMiddleware.simulate_smtp_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET:
            return ExploitMiddleware.simulate_postgres_same_user_dictionary(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Exploit action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def post_exploit_action(s: EnvState, a: Action, env_config: EnvConfig):
        """
        Implements the transition of a post-exploit action

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        raise NotImplemented