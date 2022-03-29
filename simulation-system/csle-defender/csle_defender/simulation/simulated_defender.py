from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.defender.defender_action import DefenderAction
from csle_common.dao.action.defender.defender_action_type import DefenderActionType
from csle_common.dao.action.defender.defender_action_id import DefenderActionId
from csle_defender.simulation.defender_stopping_simulator import DefenderStoppingSimulator


class SimulatedDefender:
    """
    Represents a simulated defender agent
    """

    @staticmethod
    def defender_transition(s: EmulationEnvState, defender_action: DefenderAction, emulation_env_config: EmulationEnvConfig,
                            attacker_action : AttackerAction = None) -> EmulationEnvState:
        """
        Implements the transition operator T: (s,a) -> (s',r)

        :param s: the current state
        :param defender_action: the defender action
        :param emulation_env_config: the emulation environment configuration
        :param attacker_action: previous attacker action
        :return: s'
        """
        if defender_action.type == DefenderActionType.STOP or defender_action.type == DefenderActionType.CONTINUE:
            return SimulatedDefender.defender_stopping_action(s=s, defender_action=defender_action,
                                                              attacker_action=attacker_action,
                                                              emulation_env_config=emulation_env_config)
        else:
            raise ValueError("Action type not recognized")


    @staticmethod
    def defender_stopping_action(s: EmulationEnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                                 emulation_env_config: EmulationEnvConfig) -> EmulationEnvState:
        """
        Implements transition of a stopping action of the defender

        :param s: the current state
        :param defender_action: the defender's action
        :param attacker_action: previous attacker action
        :param emulation_env_config: the environment configuration
        :return: s'
        """
        if defender_action.id == DefenderActionId.STOP:
            return DefenderStoppingSimulator.stop_monitor(s=s, defender_action=defender_action,
                                                          attacker_action=attacker_action,
                                                          emulation_env_config=emulation_env_config)
        elif defender_action.id == DefenderActionId.CONTINUE:
            return DefenderStoppingSimulator.continue_monitor(s=s, attacker_action=attacker_action,
                                                              defender_action=defender_action, emulation_env_config=emulation_env_config)
        else:
            raise ValueError("Stopping action id:{},name:{} not recognized".format(
                defender_action.id, defender_action.name))
