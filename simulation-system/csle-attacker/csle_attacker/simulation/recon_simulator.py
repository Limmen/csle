from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_attacker.simulation.util.recon_simulator_util import ReconSimulatorUtil
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction


class ReconSimulator:
    """
    Class that implements functionality for simulating reconnaissance actions
    """

    @staticmethod
    def simulate_tcp_syn_stealth_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a TCP SYN Stealth Scan action

        :param s: the current state
        :param a: the action to take
        :param emulation_env_config: the environment configuration
        :return: s_prime
        """
        s_prime = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, protocol=TransportProtocol.TCP)
        return s_prime

    @staticmethod
    def simulate_ping_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a Ping Scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        s_prime = ReconSimulatorUtil.simulate_host_scan_helper(s=s, a=a, os=False)
        return s_prime

    @staticmethod
    def simulate_udp_port_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a UDP port scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        s_prime = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, protocol=TransportProtocol.UDP)
        return s_prime

    @staticmethod
    def simulate_con_non_stealth_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a TCP CON Scan (non-stealth) action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        s_prime = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, protocol=TransportProtocol.TCP)
        return s_prime

    @staticmethod
    def simulate_fin_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a TCP FIN Scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        s_prime = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, protocol=TransportProtocol.TCP)
        return s_prime

    @staticmethod
    def simulate_tcp_null_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a TCP NULL Scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        s_prime = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, protocol=TransportProtocol.TCP)
        return s_prime

    @staticmethod
    def simulate_tcp_xmas_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a TCP XMAS Scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        s_prime = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, protocol=TransportProtocol.TCP)
        return s_prime

    @staticmethod
    def simulate_os_detection_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs an OS Detection scan action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        s_prime = ReconSimulatorUtil.simulate_host_scan_helper(s=s, a=a, os=True)
        return s_prime

    @staticmethod
    def simulate_vulscan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a nmap vulnerability scan using "vulscan" action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        s_prime, reward, done = ReconSimulatorUtil.simulate_port_vuln_scan_helper(
            s=s, a=a, protocol=TransportProtocol.TCP, vuln_scan=True)
        return s_prime

    @staticmethod
    def simulate_nmap_vulners(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Performs a nmap vulnerability scan using "vulners" action

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        s_prime = ReconSimulatorUtil.simulate_port_vuln_scan_helper(
            s=s, a=a, protocol=TransportProtocol.TCP, vuln_scan=True)
        return s_prime

    @staticmethod
    def simulate_nikto_web_host_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Simulates a Nikto web host scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime, reward, done
        """
        return s

    @staticmethod
    def simulate_masscan_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Simulates a masscan host scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return s

    @staticmethod
    def simulate_firewalk_scan(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Simulates a firewalk scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return s

    @staticmethod
    def simulate_http_enum(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Simulates a http enum scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return s

    @staticmethod
    def simulate_http_grep(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Simulates a http grep scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return s

    @staticmethod
    def simulate_finger(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Simulates a finger scan

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        return s