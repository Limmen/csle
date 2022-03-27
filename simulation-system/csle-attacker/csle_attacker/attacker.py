from typing import Tuple
from csle_common.dao.network.env_state import EnvState
from csle_common.dao.network.env_config import CSLEEnvConfig
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.network.env_mode import EnvMode
from csle_attacker.emulation.emulated_attacker import EmulatedAttacker
from csle_attacker.simulation.simulated_attacker import SimulatedAttacker


class Attacker:
    """
    Represents an automated attacker agent
    """

    @staticmethod
    def attacker_transition(s : EnvState, attacker_action : AttackerAction) -> \
            Tuple[EnvState, float, bool]:
        """
        Implements an attacker transition of the MDP/Markov Game:

        (s, a) --> (s', r)
        """
        if s.env_config.env_mode == EnvMode.SIMULATION:
            return SimulatedAttacker.attacker_transition(s=s, attacker_action=attacker_action, env_config=s.env_config)
        elif s.env_config.env_mode == EnvMode.EMULATION or s.env_config.env_mode == EnvMode.GENERATED_SIMULATION:
            return EmulatedAttacker.attacker_transition(s=s, attacker_action=attacker_action, env_config=s.env_config)
        else:
            raise ValueError("Invalid environment mode")