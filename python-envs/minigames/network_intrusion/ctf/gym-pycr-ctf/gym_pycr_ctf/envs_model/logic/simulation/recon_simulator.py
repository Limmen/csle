from typing import Tuple
from pycr_common.dao.network.transport_protocol import TransportProtocol
from pycr_common.envs_model.logic.simulation.util.simulator_util import SimulatorUtil
from pycr_common.envs_model.logic.simulation.util.recon_simulator_util import ReconSimulatorUtil
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction


class ReconSimulator:
    """
    Class that implements functionality for simulating reconnaissance actions
    """

    @staticmethod
    def simulate_tcp_syn_stealth_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a TCP SYN Stealth Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward, done = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, env_config=env_config,
                                                                       miss_p=env_config.syn_stealth_scan_miss_p,
                                                                       protocol=TransportProtocol.TCP)
        if not done:
            done, d_reward = SimulatorUtil.simulate_detection(a=a, env_config=env_config)
            if done:
                reward = d_reward
            s_prime.attacker_obs_state.detected = done
        return s_prime, reward, done

    @staticmethod
    def simulate_ping_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a Ping Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward, done = ReconSimulatorUtil.simulate_host_scan_helper(s=s, a=a, env_config=env_config,
                                                          miss_p=env_config.ping_scan_miss_p,
                                                          os=False)
        if not done:
            done, d_reward = SimulatorUtil.simulate_detection(a=a, env_config=env_config)
            if done:
                reward = d_reward
            s_prime.attacker_obs_state.detected = done
        return s_prime, reward, done

    @staticmethod
    def simulate_udp_port_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a UDP port scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward, done = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, env_config=env_config,
                                                                       miss_p=env_config.udp_port_scan_miss_p,
                                                                       protocol=TransportProtocol.UDP)
        if not done:
            done, d_reward = SimulatorUtil.simulate_detection(a=a, env_config=env_config)
            if done:
                reward = d_reward
            s_prime.attacker_obs_state.detected = done
        return s_prime, reward, done

    @staticmethod
    def simulate_con_non_stealth_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a TCP CON Scan (non-stealth) action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward, done = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, env_config=env_config,
                                                                       miss_p=env_config.syn_stealth_scan_miss_p,
                                                                       protocol=TransportProtocol.TCP)
        if not done:
            done, d_reward = SimulatorUtil.simulate_detection(a=a, env_config=env_config)
            if done:
                reward = d_reward
            s_prime.attacker_obs_state.detected = done
        return s_prime, reward, done

    @staticmethod
    def simulate_fin_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a TCP FIN Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward, done = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, env_config=env_config,
                                                                       miss_p=env_config.syn_stealth_scan_miss_p,
                                                                       protocol=TransportProtocol.TCP)
        if not done:
            done, d_reward = SimulatorUtil.simulate_detection(a=a, env_config=env_config)
            if done:
                reward = d_reward
            s_prime.attacker_obs_state.detected = done
        return s_prime, reward, done

    @staticmethod
    def simulate_tcp_null_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a TCP NULL Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward, done = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, env_config=env_config,
                                                                       miss_p=env_config.syn_stealth_scan_miss_p,
                                                                       protocol=TransportProtocol.TCP)
        if not done:
            done, d_reward = SimulatorUtil.simulate_detection(a=a, env_config=env_config)
            if done:
                reward = d_reward
            s_prime.attacker_obs_state.detected = done
        return s_prime, reward, done

    @staticmethod
    def simulate_tcp_xmas_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a TCP XMAS Scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward, done = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, env_config=env_config,
                                                                       miss_p=env_config.syn_stealth_scan_miss_p,
                                                                       protocol=TransportProtocol.TCP)
        if not done:
            done, d_reward = SimulatorUtil.simulate_detection(a=a, env_config=env_config)
            if done:
                reward = d_reward
            s_prime.attacker_obs_state.detected = done
        return s_prime, reward, done

    @staticmethod
    def simulate_os_detection_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs an OS Detection scan action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward, done = ReconSimulatorUtil.simulate_host_scan_helper(s=s, a=a, env_config=env_config,
                                                          miss_p=env_config.os_scan_miss_p, os=True)
        if not done:
            done, d_reward = SimulatorUtil.simulate_detection(a=a, env_config=env_config)
            if done:
                reward = d_reward
            s_prime.attacker_obs_state.detected = done
        return s_prime, reward, done

    @staticmethod
    def simulate_vulscan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a nmap vulnerability scan using "vulscan" action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward, done = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, env_config=env_config,
                                                                       miss_p=env_config.vulscan_miss_p,
                                                                       protocol=TransportProtocol.TCP,
                                                                       vuln_scan=True)
        if not done:
            done, d_reward = SimulatorUtil.simulate_detection(a=a, env_config=env_config)
            if done:
                reward = d_reward
            s_prime.attacker_obs_state.detected = done
        return s_prime, reward, done

    @staticmethod
    def simulate_nmap_vulners(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Performs a nmap vulnerability scan using "vulners" action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward, done = ReconSimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, env_config=env_config,
                                                                       miss_p=env_config.vulners_miss_p,
                                                                       protocol=TransportProtocol.TCP,
                                                                       vuln_scan=True)
        if not done:
            done, d_reward = SimulatorUtil.simulate_detection(a=a, env_config=env_config)
            if done:
                reward = d_reward
            s_prime.attacker_obs_state.detected = done
        return s_prime, reward, done

    @staticmethod
    def simulate_nikto_web_host_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Simulates a Nikto web host scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_masscan_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Simulates a masscan host scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_firewalk_scan(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Simulates a firewalk scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_http_enum(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Simulates a http enum scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_http_grep(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Simulates a http grep scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False

    @staticmethod
    def simulate_finger(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Simulates a finger scan

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return s, 0, False