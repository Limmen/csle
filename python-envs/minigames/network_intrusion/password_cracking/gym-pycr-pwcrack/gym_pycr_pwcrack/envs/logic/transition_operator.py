from typing import Union
from gym_pycr_pwcrack.dao.env_state import EnvState
from gym_pycr_pwcrack.dao.env_config import EnvConfig
from gym_pycr_pwcrack.dao.env_mode import EnvMode
from gym_pycr_pwcrack.envs.logic.cluster_middleware import ClusterMiddleware
from gym_pycr_pwcrack.envs.logic.simulator import Simulator
from gym_pycr_pwcrack.dao.action import Action

class TransitionOperator:

    @staticmethod
    def transition(s : EnvState, a : Action, env_config : EnvConfig) -> Union[EnvState, int, bool]:
        if env_config.env_mode == EnvMode.SIMULATION:
            return Simulator.transition(s=s,a=a,env_config=env_config)
        elif env_config.env_mode == EnvMode.CLUSTER:
            return ClusterMiddleware.transition(s=s,a=a,env_config=env_config)
        else:
            raise ValueError("Invalid environment mode")