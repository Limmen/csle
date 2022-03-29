from csle_common.dao.network.emulation_env_state import EmulationEnvState
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.network.env_mode import EnvMode
from csle_attacker.emulation.emulated_attacker import EmulatedAttacker
from csle_attacker.simulation.simulated_attacker import SimulatedAttacker


class Attacker:
    """
    Represents an automated attacker agent
    """

    @staticmethod
    def attacker_transition(s : EmulationEnvState, attacker_action : AttackerAction) -> EmulationEnvState:
        """
        Implements an attacker transition of the MDP/Markov Game:

        (s, a) --> s'
        """
        if s.emulation_env_config.env_mode == EnvMode.SIMULATION:
            return SimulatedAttacker.attacker_transition(s=s, attacker_action=attacker_action, env_config=s.emulation_env_config)
        elif s.emulation_env_config.env_mode == EnvMode.EMULATION:
            return EmulatedAttacker.attacker_transition(s=s, attacker_action=attacker_action, emulation_env_agent_config=s.emulation_env_config)
        else:
            raise ValueError("Invalid environment mode")