from typing import Tuple
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.action import Action
from gym_pycr_ctf.envs.logic.emulation.util.emulation_util import EmulationUtil
from gym_pycr_ctf.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_ctf.envs.logic.common.env_dynamics_util import EnvDynamicsUtil
from gym_pycr_ctf.dao.network.credential import Credential
from gym_pycr_ctf.dao.network.transport_protocol import TransportProtocol
from gym_pycr_ctf.dao.network.vulnerability import Vulnerability
import gym_pycr_ctf.constants.constants as constants
from gym_pycr_ctf.envs.logic.emulation.util.nmap_util import NmapUtil
from gym_pycr_ctf.envs.logic.emulation.util.exploit_util import ExploitUtil
from gym_pycr_ctf.envs.logic.emulation.util.connection_util import ConnectionUtil

class DefenseSensorMiddleware:
    """
    Class that implements functionality for sensing the state of the emulation enviroment from a system operator's
    (defender's) perspective.
    """

    @staticmethod
    def get_observation(s: EnvState, a: Action, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a Telnet Dictionary Password Attack action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime, reward, done = NmapUtil.nmap_scan_action_helper(s=s, a=a, env_config=env_config)
        return s_prime, reward, done

