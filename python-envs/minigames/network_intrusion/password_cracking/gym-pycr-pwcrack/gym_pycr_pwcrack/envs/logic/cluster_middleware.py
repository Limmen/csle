from typing import Union
from gym_pycr_pwcrack.dao.env_state import EnvState
from gym_pycr_pwcrack.dao.env_config import EnvConfig

class ClusterMiddleware:

    def __init__(self):
        pass

    @staticmethod
    def transition(s: EnvState, a: int, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False