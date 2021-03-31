from typing import Tuple
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.envs.logic.emulation.emulation_middleware import EmulationMiddleware
from gym_pycr_ctf.envs.logic.simulation.simulator import Simulator
from gym_pycr_ctf.dao.action.action import Action

class TransitionOperator:
    """
    Implements the transition operator of the MDP/Markov Game:

    (s, a) --> (s', r)
    """

    @staticmethod
    def transition(s : EnvState, a : Action, env_config : EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Implements the transition operator of the MDP/Markov Game, supporting both simulation and emulation mode
        (s, a) --> (s', r)

        :param s: the current state
        :param a: the action of the transition
        :param env_config: the environment config
        :return: s', r, done
        """
        if env_config.env_mode == EnvMode.SIMULATION:
            return Simulator.transition(s=s,a=a,env_config=env_config)
        elif env_config.env_mode == EnvMode.emulation or env_config.env_mode == EnvMode.GENERATED_SIMULATION:
            return EmulationMiddleware.transition(s=s, a=a, env_config=env_config)
            # try:
            #     return emulationMiddleware.transition(s=s,a=a,env_config=env_config)
            # except Exception as e:
            #     print("Could not execute action on the emulation, using simulation instead. \n Error:{}".format(str(e)))
            #     return Simulator.transition(s=s, a=a, env_config=env_config)

        else:
            raise ValueError("Invalid environment mode")