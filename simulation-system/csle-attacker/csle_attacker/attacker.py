from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_attacker.emulation.emulated_attacker import EmulatedAttacker
from csle_attacker.simulation.simulated_attacker import SimulatedAttacker


class Attacker:
    """
    Represents an automated attacker agent
    """

    @staticmethod
    def attacker_transition(s : EmulationEnvState, attacker_action : AttackerAction, simulation : bool = False) \
            -> EmulationEnvState:
        """
        Implements an attacker transition of the MDP/Markov Game:
        (s, a) --> s'

        :param s: the current environment state in the emulation
        :param attacker_action: the attacker action
        :param simulation: boolean flag if it is a simulated transition or an actual transition in the emulation
        :return: s' (EmulationEnvState)
        """
        if simulation:
            return SimulatedAttacker.attacker_transition(s=s, attacker_action=attacker_action,
                                                         emulation_env_config=s.emulation_env_config)
        else:
            return EmulatedAttacker.attacker_transition(s=s, attacker_action=attacker_action,
                                                        emulation_env_config=s.emulation_env_config)