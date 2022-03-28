import pyglet
from csle_common.dao.envs.base_env import BaseEnv
from csle_common.dao.network.emulation_env_agent_config import EmulationEnvAgentConfig


class CSLEBaseFrame(pyglet.window.Window):
    """
    Abstract class representing a game-frame of a csle environment
    """

    def __init__(self, height: int, width: int, caption: str, env_config: EmulationEnvAgentConfig,
                 env : BaseEnv):
        super(CSLEBaseFrame, self).__init__(height=height, width=width, caption=caption)
        self.env_config = env_config
        self.init_state = None
        self.env = env
