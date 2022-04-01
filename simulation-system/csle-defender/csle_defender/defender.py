from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_defender.emulation.emulated_defender import EmulatedDefender
from csle_defender.simulation.simulated_defender import SimulatedDefender


class Defender:
    """
    Represents an automated defender agent
    """

    @staticmethod
    def defender_transition(s: EmulationEnvState, defender_action: EmulationDefenderAction,
                            attacker_action : EmulationAttackerAction = None, simulation: bool = False) \
            -> EmulationEnvState:
        """
        Implements the transition operator of the MDP/Markov Game for defense actions,
        supporting both simulation and emulation mode
        (s, a) --> s'

        :param s: the current state
        :param defender_action: the defender's action of the transition
        :param attacker_action: previous attacker action
        :param simulation: boolean flag whether it is a simulated transition or not
        :return: s'
        """
        if simulation:
            return SimulatedDefender.defender_transition(s=s, defender_action=defender_action,
                                                         attacker_action=attacker_action)
        else:
            return EmulatedDefender.defender_transition(s=s, defender_action=defender_action,
                                                        attacker_action=attacker_action)


    @staticmethod
    def update_defender_state(s: EmulationEnvState) -> EmulationEnvState:
        """
        Updates the defender's state by measuring metrics from the emulatio

        :param s: the current state
        :return: the updated state
        """
        return EmulatedDefender.update_state(s)