from typing import Tuple
from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.env_state import EnvState
from csle_common.dao.network.env_config import CSLEEnvConfig
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.defender.defender_action import DefenderAction
from csle_defender.emulation.emulated_defender import EmulatedDefender
from csle_defender.simulation.simulated_defender import SimulatedDefender


class Defender:
    """
    Represents an automated defender agent
    """

    @staticmethod
    def defender_transition(s: EnvState, defender_action: DefenderAction, env_config: CSLEEnvConfig,
                            attacker_action : AttackerAction = None) \
            -> Tuple[EnvState, float, bool]:
        """
        Implements the transition operator of the MDP/Markov Game for defense actions,
        supporting both simulation and emulation mode
        (s, a) --> (s', r)

        :param s: the current state
        :param defender_action: the defender's action of the transition
        :param env_config: the environment config
        :param attacker_action: previous attacker action
        :return: s', r, done
        """
        if env_config.env_mode == EnvMode.SIMULATION:
            return SimulatedDefender.defender_transition(s=s, defender_action=defender_action, env_config=env_config,
                                                 attacker_action=attacker_action)
        elif env_config.env_mode == EnvMode.EMULATION or env_config.env_mode == EnvMode.GENERATED_SIMULATION:
            return EmulatedDefender.defender_transition(s=s, defender_action=defender_action,
                                                           attacker_action=attacker_action,
                                                           env_config=env_config)
        else:
            raise ValueError("Invalid environment mode")