from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_defender.simulation.defender_stopping_simulator import DefenderStoppingSimulator


class SimulatedDefender:
    """
    Represents a simulated defender agent
    """

    @staticmethod
    def defender_transition(s: EmulationEnvState, defender_action: EmulationDefenderAction,
                            attacker_action : EmulationAttackerAction = None) -> EmulationEnvState:
        """
        Implements the transition operator T: (s,a) -> (s',r)

        :param s: the current state
        :param defender_action: the defender action
        :param attacker_action: previous attacker action
        :return: s'
        """
        if defender_action.type == EmulationDefenderActionType.STOP or defender_action.type == EmulationDefenderActionType.CONTINUE:
            return SimulatedDefender.defender_stopping_action(s=s, defender_action=defender_action,
                                                              attacker_action=attacker_action)
        else:
            raise ValueError("Action type not recognized")


    @staticmethod
    def defender_stopping_action(s: EmulationEnvState, defender_action: EmulationDefenderAction,
                                 attacker_action: EmulationAttackerAction) -> EmulationEnvState:
        """
        Implements transition of a stopping action of the defender

        :param s: the current state
        :param defender_action: the defender's action
        :param attacker_action: previous attacker action
        :return: s'
        """
        if defender_action.id == EmulationDefenderActionId.STOP:
            return DefenderStoppingSimulator.stop_monitor(s=s, defender_action=defender_action,
                                                          attacker_action=attacker_action)
        elif defender_action.id == EmulationDefenderActionId.CONTINUE:
            return DefenderStoppingSimulator.continue_monitor(s=s, attacker_action=attacker_action,
                                                              defender_action=defender_action)
        else:
            raise ValueError("Stopping action id:{},name:{} not recognized".format(
                defender_action.id, defender_action.name))
