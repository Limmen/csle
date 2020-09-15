from typing import Union
from gym_pycr_pwcrack.dao.env_state import EnvState
from gym_pycr_pwcrack.dao.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action import Action

class Simulator:

    def __init__(self):
        pass

    @staticmethod
    def transition(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        action = env_config.action_conf.action_lookup_d[a]
        return s, 0, False