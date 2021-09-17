import pyglet
from pycr_common.dao.envs.base_pycr_env import BasePyCREnv
from pycr_common.dao.network.base_env_config import BaseEnvConfig
from pycr_common.dao.network.attacker.base_attacker_agent_state import BaseAttackerAgentState


class PyCRBaseFrame(pyglet.window.Window):
    """
    Abstract class representing a game-frame of a PyCR environment
    """

    def __init__(self, height: int, width: int, caption: str, env_config: BaseEnvConfig,
                 init_state: BaseAttackerAgentState, env : BasePyCREnv):
        super(PyCRBaseFrame, self).__init__(height=height, width=width, caption=caption)
        self.env_config = env_config
        self.init_state = init_state
        self.env = env
