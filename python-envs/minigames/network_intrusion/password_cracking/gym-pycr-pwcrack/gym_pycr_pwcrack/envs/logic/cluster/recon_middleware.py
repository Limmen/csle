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
        cache_result = None
        if env_config.use_nmap_cache:
            cache_result = ClusterUtil.check_nmap_action_cache(a=a, env_config=env_config)
        if cache_result is None:
            ClusterUtil.execute_cmd(a=a, env_config=env_config)
            cache_result = str(a.id.value) + "_" + a.ip + ".xml"
            if a.subnet:
                cache_result = str(a.id.value) + ".xml"

        for i in range(env_config.num_retries):
            try:
                xml_data = ClusterUtil.parse_nmap_scan(file_name=cache_result, env_config=env_config)
                break
            except Exception as e:
                ClusterUtil.delete_cache_file(file_name=cache_result, env_config=env_config)
                ClusterUtil.execute_cmd(a=a, env_config=env_config)
                time.sleep(env_config.retry_timeout)
                xml_data = ClusterUtil.parse_nmap_scan(file_name=cache_result, env_config=env_config)
                break

        scan_result = ClusterUtil.parse_nmap_scan_xml(xml_data)
        s_prime, reward = ClusterUtil.merge_scan_result_with_state(scan_result=scan_result, s=s, a=a)
        return s_prime, reward, False