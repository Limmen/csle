from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_attacker.emulation.util.nmap_util import NmapUtil
from csle_attacker.emulation.util.nikto_util import NiktoUtil


class ReconMiddleware:
    """
    Class that implements functionality for executing reconnaissance actions on the emulation
    """

    @staticmethod
    def execute_tcp_syn_stealth_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a TCP SYN Stealth Scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a)

    @staticmethod
    def execute_ping_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a Ping Scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a)

    @staticmethod
    def execute_udp_port_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a UDP Port Scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a)

    @staticmethod
    def execute_tcp_con_stealth_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a TCP CON Stealth scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a)

    @staticmethod
    def execute_tcp_fin_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a TCP FIN scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a)

    @staticmethod
    def execute_tcp_null_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a TCP Null scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a)

    @staticmethod
    def execute_tcp_xmas_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a TCP Xmas scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a)

    @staticmethod
    def execute_os_detection_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a OS detection scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a)

    @staticmethod
    def execute_vulscan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a vulscan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a)

    @staticmethod
    def execute_nmap_vulners(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a nmap_vulners scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a)

    @staticmethod
    def execute_nikto_web_host_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a nikto web host scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NiktoUtil.nikto_scan_action_helper(s=s, a=a)

    @staticmethod
    def execute_masscan_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a masscan scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, masscan=True)

    @staticmethod
    def execute_firewalk_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a firewalk scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, masscan=True)

    @staticmethod
    def execute_http_enum(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a http enum scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, masscan=True)

    @staticmethod
    def execute_http_grep(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a http grep scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, masscan=True)

    @staticmethod
    def execute_finger(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a finger scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return NmapUtil.nmap_scan_action_helper(s=s, a=a, masscan=True)
