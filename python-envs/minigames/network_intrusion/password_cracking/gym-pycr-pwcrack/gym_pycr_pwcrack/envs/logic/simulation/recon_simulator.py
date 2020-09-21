from typing import Union
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.envs.logic.simulation.simulator_util import SimulatorUtil

class ReconSimulator:
    """
    Class that implements functionality for simulating reconnissance actions
    """

    @staticmethod
    def simulate_tcp_syn_stealth_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a TCP SYN Stealth Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward = SimulatorUtil.simulate_port_scan_helper(s=s, a=a, env_config=env_config,
                                                          miss_p=env_config.syn_stealth_scan_miss_p,
                                                          protocol=TransportProtocol.TCP)
        return s_prime, reward, False

    @staticmethod
    def simulate_ping_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a Ping Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward = SimulatorUtil.simulate_host_scan_helper(s=s, a=a, env_config=env_config,
                                                          miss_p=env_config.ping_scan_miss_p,
                                                          os=False)
        return s_prime, reward, False

    @staticmethod
    def simulate_udp_port_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a UDP port scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward = SimulatorUtil.simulate_port_scan_helper(s=s, a=a, env_config=env_config,
                                                          miss_p=env_config.udp_port_scan_miss_p,
                                                          protocol=TransportProtocol.UDP)
        return s_prime, reward, False

    @staticmethod
    def simulate_con_non_stealth_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a TCP CON Scan (non-stealth) action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward = SimulatorUtil.simulate_port_scan_helper(s=s, a=a, env_config=env_config,
                                                          miss_p=env_config.syn_stealth_scan_miss_p,
                                                          protocol=TransportProtocol.TCP)
        return s_prime, reward, False

    @staticmethod
    def simulate_fin_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a TCP FIN Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward = SimulatorUtil.simulate_port_scan_helper(s=s, a=a, env_config=env_config,
                                                          miss_p=env_config.syn_stealth_scan_miss_p,
                                                          protocol=TransportProtocol.TCP)
        return s_prime, reward, False

    @staticmethod
    def simulate_tcp_null_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a TCP NULL Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward = SimulatorUtil.simulate_port_scan_helper(s=s, a=a, env_config=env_config,
                                                          miss_p=env_config.syn_stealth_scan_miss_p,
                                                          protocol=TransportProtocol.TCP)
        return s_prime, reward, False

    @staticmethod
    def simulate_tcp_xmas_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a TCP XMAS Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward = SimulatorUtil.simulate_port_scan_helper(s=s, a=a, env_config=env_config,
                                                          miss_p=env_config.syn_stealth_scan_miss_p,
                                                          protocol=TransportProtocol.TCP)
        return s_prime, reward, False

    @staticmethod
    def simulate_os_detection_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs an OS Detection scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward = SimulatorUtil.simulate_host_scan_helper(s=s, a=a, env_config=env_config,
                                                          miss_p=env_config.os_scan_miss_p, os=True)
        return s_prime, reward, False

    @staticmethod
    def simulate_vulscan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a nmap vulnerability scan using "vulscan" action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_nmap_vulners(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a nmap vulnerability scan using "vulners" action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_telnet_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[
        EnvState, int, bool]:
        """
        Performs a telnet dictionary attack constrainted to username-password combinations where username==password

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_ssh_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a ssh dictionary attack constrainted to username-password combinations where username==password

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_ftp_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a ftp dictionary attack constrainted to username-password combinations where username==password

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_cassandra_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[
        EnvState, int, bool]:
        """
        Performs a cassandra dictionary attack constrainted to username-password combinations where username==password

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_irc_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a IRC dictionary attack constrainted to username-password combinations where username==password

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_mongo_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[
        EnvState, int, bool]:
        """
        Performs a mongodb dictionary attack constrainted to username-password combinations where username==password

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_mysql_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[
        EnvState, int, bool]:
        """
        Performs a mysql dictionary attack constrainted to username-password combinations where username==password

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_smtp_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        """
        Performs a SMTP dictionary attack constrainted to username-password combinations where username==password

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_postgres_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[
        EnvState, int, bool]:
        """
        Performs a postgres dictionary attack constrainted to username-password combinations where username==password

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False