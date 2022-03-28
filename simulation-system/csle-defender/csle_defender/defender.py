from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_env_state import EmulationEnvState
from csle_common.dao.network.emulation_env_agent_config import EmulationEnvAgentConfig
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.defender.defender_action import DefenderAction
from csle_defender.emulation.emulated_defender import EmulatedDefender
from csle_defender.simulation.simulated_defender import SimulatedDefender


class Defender:
    """
    Represents an automated defender agent
    """

    @staticmethod
    def defender_transition(s: EmulationEnvState, defender_action: DefenderAction, env_config: EmulationEnvAgentConfig,
                            attacker_action : AttackerAction = None) -> EmulationEnvState:
        """
        Implements the transition operator of the MDP/Markov Game for defense actions,
        supporting both simulation and emulation mode
        (s, a) --> s'

        :param s: the current state
        :param defender_action: the defender's action of the transition
        :param env_config: the environment config
        :param attacker_action: previous attacker action
        :return: s'
        """
        if env_config.env_mode == EnvMode.SIMULATION:
            return SimulatedDefender.defender_transition(s=s, defender_action=defender_action, env_config=env_config,
                                                 attacker_action=attacker_action)
        elif env_config.env_mode == EnvMode.EMULATION:
            return EmulatedDefender.defender_transition(s=s, defender_action=defender_action,
                                                           attacker_action=attacker_action,
                                                           env_config=env_config)
        else:
            raise ValueError("Invalid environment mode")