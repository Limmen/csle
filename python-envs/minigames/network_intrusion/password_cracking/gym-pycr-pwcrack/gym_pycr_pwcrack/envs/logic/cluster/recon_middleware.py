from typing import Union
import time
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.envs.logic.cluster.cluster_util import ClusterUtil

class ReconMiddleware:
    """
    Class that implements functionality for executing reconnaissance actions on the cluster
    """

    @staticmethod
    def execute_tcp_syn_stealth_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a TCP SYN Stealth Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return ClusterUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_ping_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a Ping Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return ClusterUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_udp_port_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a UDP Port Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return ClusterUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_tcp_con_stealth_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a TCP CON Stealth scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return ClusterUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_tcp_fin_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a TCP FIN scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return ClusterUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_tcp_null_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a TCP Null scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return ClusterUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_tcp_xmas_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a TCP Xmas scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return ClusterUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)