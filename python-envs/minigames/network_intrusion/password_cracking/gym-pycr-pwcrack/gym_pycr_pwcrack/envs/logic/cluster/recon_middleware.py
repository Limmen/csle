from typing import Union
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action.action import Action

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
        print("executing cmd:{}".format(a.cmd))
        stdin, stdout, stderr = env_config.cluster_config.agent_conn.exec_command(a.cmd[0])
        for line in stdout:
            print(line.strip('\n'))
        # s_prime, reward = SimulatorUtil.simulate_port_vuln_scan_helper(s=s, a=a, env_config=env_config,
        #                                                                miss_p=env_config.syn_stealth_scan_miss_p,
        #                                                                protocol=TransportProtocol.TCP)
        # done = SimulatorUtil.simulate_detection(a=a, env_config=env_config)
        # s_prime.obs_state.detected = done
        # return s_prime, reward, done
        return s, 0, False