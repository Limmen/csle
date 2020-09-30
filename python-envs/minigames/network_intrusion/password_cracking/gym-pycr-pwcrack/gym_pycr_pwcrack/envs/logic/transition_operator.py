from typing import Union
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.network.env_mode import EnvMode
from gym_pycr_pwcrack.envs.logic.cluster.cluster_middleware import ClusterMiddleware
from gym_pycr_pwcrack.envs.logic.simulation.simulator import Simulator
from gym_pycr_pwcrack.dao.action.action import Action

class TransitionOperator:

    @staticmethod
    def transition(s : EnvState, a : Action, env_config : EnvConfig) -> Union[EnvState, int, bool]:
        if env_config.env_mode == EnvMode.SIMULATION:
            return Simulator.transition(s=s,a=a,env_config=env_config)
        elif env_config.env_mode == EnvMode.CLUSTER:
            return ClusterMiddleware.transition(s=s, a=a, env_config=env_config)
            # try:
            #     return ClusterMiddleware.transition(s=s,a=a,env_config=env_config)
            # except Exception as e:
            #     print("Could not execute action on the Cluster, using simulation instead. \n Error:{}".format(str(e)))
            #     return Simulator.transition(s=s, a=a, env_config=env_config)

        else:
            raise ValueError("Invalid environment mode")