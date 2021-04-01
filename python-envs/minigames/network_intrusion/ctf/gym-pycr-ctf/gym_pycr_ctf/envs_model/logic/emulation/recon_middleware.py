from typing import Tuple
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.envs_model.logic.emulation.util.attacker.nmap_util import NmapUtil
from gym_pycr_ctf.envs_model.logic.emulation.util.attacker.nikto_util import NiktoUtil

class ReconMiddleware:
    """
    Class that implements functionality for executing reconnaissance actions on the emulation
    """

    @staticmethod
    def execute_tcp_syn_stealth_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a TCP SYN Stealth Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_ping_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a Ping Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_udp_port_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a UDP Port Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_tcp_con_stealth_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a TCP CON Stealth scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_tcp_fin_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a TCP FIN scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_tcp_null_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a TCP Null scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_tcp_xmas_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a TCP Xmas scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_os_detection_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a OS detection scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_vulscan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a vulscan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)


    @staticmethod
    def execute_nmap_vulners(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a nmap_vulners scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_nikto_web_host_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a nikto web host scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NiktoUtil.nikto_scan_action_helper(s=s, a=a, env_config=env_config)

    @staticmethod
    def execute_masscan_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a masscan scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config, masscan=True)

    @staticmethod
    def execute_firewalk_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a firewalk scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config, masscan=True)

    @staticmethod
    def execute_http_enum(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a http enum scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config, masscan=True)

    @staticmethod
    def execute_http_grep(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a http grep scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config, masscan=True)

    @staticmethod
    def execute_finger(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a finger scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config, masscan=True)