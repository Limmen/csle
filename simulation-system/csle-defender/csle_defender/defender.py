from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.defender.defender_action import DefenderAction
from csle_defender.emulation.emulated_defender import EmulatedDefender
from csle_defender.simulation.simulated_defender import SimulatedDefender


class Defender:
    """
    Represents an automated defender agent
    """

    @staticmethod
    def defender_transition(s: EmulationEnvState, defender_action: DefenderAction,
                            emulation_env_config: EmulationEnvConfig,
                            attacker_action : AttackerAction = None, simulation: bool = False) -> EmulationEnvState:
        """
        Implements the transition operator of the MDP/Markov Game for defense actions,
        supporting both simulation and emulation mode
        (s, a) --> s'

        :param s: the current state
        :param defender_action: the defender's action of the transition
        :param emulation_env_config: the environment config
        :param attacker_action: previous attacker action
        :param simulation: boolean flag whether it is a simulated transition or not
        :return: s'
        """
        if simulation:
            return SimulatedDefender.defender_transition(s=s, defender_action=defender_action, emulation_env_config=emulation_env_config,
                                                         attacker_action=attacker_action)
        else:
            return EmulatedDefender.defender_transition(s=s, defender_action=defender_action,
                                                        attacker_action=attacker_action,
                                                        emulation_env_config=emulation_env_config)