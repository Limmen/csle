from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_defender.emulation.emulated_defender import EmulatedDefender


class Defender:
    """
    Represents an automated defender agent
    """

    @staticmethod
    def defender_transition(s: EmulationEnvState, defender_action: EmulationDefenderAction,
                            attacker_action: EmulationAttackerAction = None) -> EmulationEnvState:
        """
        Implements the transition operator of the MDP/Markov Game for defense actions,
        supporting both simulation and emulation mode
        (s, a) --> s'

        :param s: the current state
        :param defender_action: the defender's action of the transition
        :param attacker_action: previous attacker action
        :return: s'
        """
        return EmulatedDefender.defender_transition(s=s, defender_action=defender_action,
                                                    attacker_action=attacker_action)
