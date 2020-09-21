from typing import Union
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_type import ActionType

class ClusterMiddleware:

    def __init__(self):
        pass

    @staticmethod
    def transition(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        if a.type == ActionType.RECON:
            return ClusterMiddleware.recon_action(s=s,a=a,env_config=env_config)
        elif a.type == ActionType.EXPLOIT:
            return ClusterMiddleware.exploit_action(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Action type not recognized")

    @staticmethod
    def recon_action(s: EnvState, a: Action, env_config: EnvConfig):
        pass

    @staticmethod
    def exploit_action(s: EnvState, a: Action, env_config: EnvConfig):
        pass