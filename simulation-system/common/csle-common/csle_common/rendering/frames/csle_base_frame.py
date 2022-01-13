import pyglet
from csle_common.dao.envs.base_csle_env import BaseCSLEEnv
from csle_common.dao.network.base_env_config import BaseCSLEEnvConfig
from csle_common.dao.network.attacker.base_attacker_agent_state import BaseAttackerAgentState


class CSLEBaseFrame(pyglet.window.Window):
    """
    Abstract class representing a game-frame of a csle environment
    """

    def __init__(self, height: int, width: int, caption: str, env_config: BaseCSLEEnvConfig,
                 init_state: BaseAttackerAgentState, env : BaseCSLEEnv):
        super(CSLEBaseFrame, self).__init__(height=height, width=width, caption=caption)
        self.env_config = env_config
        self.init_state = init_state
        self.env = env
