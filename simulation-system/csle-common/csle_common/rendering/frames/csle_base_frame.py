import pyglet
from csle_common.dao.envs.base_env import BaseEnv
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig


class CSLEBaseFrame(pyglet.window.Window):
    """
    Abstract class representing a game-frame of a csle environment
    """

    def __init__(self, height: int, width: int, caption: str, emulation_env_config: EmulationEnvConfig,
                 env : BaseEnv):
        super(CSLEBaseFrame, self).__init__(height=height, width=width, caption=caption)
        self.emulation_env_config = emulation_env_config
        self.init_state = None
        self.env = env
