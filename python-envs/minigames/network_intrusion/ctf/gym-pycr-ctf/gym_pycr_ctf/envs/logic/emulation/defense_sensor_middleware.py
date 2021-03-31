from typing import Tuple
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.envs.logic.emulation.util.nmap_util import NmapUtil

class DefenseSensorMiddleware:
    """
    Class that implements functionality for sensing the state of the emulation enviroment from a system operator's
    (defender's) perspective.
    """

    @staticmethod
    def get_observation(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Extract the latest defender-observation from the emulation and combines it with the current belief state

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward, done = NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)
        return s_prime, reward, done

