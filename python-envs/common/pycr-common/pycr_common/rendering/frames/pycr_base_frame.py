from abc import ABC
import pyglet
from pycr_common.dao.network.base_env_config import BaseEnvConfig
from pycr_common.dao.network.attacker.base_attacker_agent_state import BaseAttackerAgentState


class PyCRBaseFrame(ABC, pyglet.window.Window):

    def __init__(self, height: int, width: int, caption: str, env_config: BaseEnvConfig,
                 init_state: BaseAttackerAgentState):
        super(PyCRBaseFrame, self).__init__(height=height, width=width, caption=caption)
        self.env_config = env_config
        self.init_state = init_state
