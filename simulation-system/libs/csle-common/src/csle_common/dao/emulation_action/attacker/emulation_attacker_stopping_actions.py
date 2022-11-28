from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerActionOutcome


class EmulationAttackerStoppingActions:
    """
    Class implementing stopping actions for the attacker in the emulation
    """

    @staticmethod
    def STOP(index: int) -> EmulationAttackerAction:
        """
        Reports a detected intrusion and stops

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.STOP
        cmd = []
        alt_cmd = []
        return EmulationAttackerAction(id=id, name="Abort Intrusion", cmds=cmd,
                                       type=EmulationAttackerActionType.STOP,
                                       descr="Aborts an ongoing intrusion",
                                       index=index,
                                       ips=[], action_outcome=EmulationAttackerActionOutcome.GAME_END, alt_cmds=alt_cmd)

    @staticmethod
    def CONTINUE(index: int) -> EmulationAttackerAction:
        """
        A "continue" action, the attacker chooses to not make any action

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.CONTINUE
        cmd = []
        alt_cmd = []
        return EmulationAttackerAction(id=id, name="Continue", cmds=cmd,
                                       type=EmulationAttackerActionType.CONTINUE,
                                       descr="A 'continue' action, the attacker chooses to not make any action",
                                       index=index,
                                       ips=[], action_outcome=EmulationAttackerActionOutcome.CONTINUE, alt_cmds=alt_cmd)
