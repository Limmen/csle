from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.attacker.attacker_action_type import AttackerActionType
from csle_common.dao.action.attacker.attacker_action_id import AttackerActionId
from csle_common.dao.action.attacker.attacker_action import AttackerActionOutcome


class AttackerStoppingActions:
    """
    Class implementing stopping actions for the attacker
    """

    @staticmethod
    def STOP(index : int) -> AttackerAction:
        """
        Reports a detected intrusion and stops

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.STOP
        cmd = []
        alt_cmd = []
        return AttackerAction(id=id, name="Abort Intrusion", cmd=cmd,
                              type=AttackerActionType.STOP,
                              descr="Aborts an ongoing intrusion",
                              cost=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.GAME_END, alt_cmd=alt_cmd,
                              noise=0)

    @staticmethod
    def CONTINUE(index: int) -> AttackerAction:
        """
        A "continue" action, the attacker chooses to not make any action

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.CONTINUE
        cmd = []
        alt_cmd = []
        return AttackerAction(id=id, name="Continue", cmd=cmd,
                              type=AttackerActionType.CONTINUE,
                              descr="A 'continue' action, the attacker chooses to not make any action",
                              cost=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.CONTINUE, alt_cmd=alt_cmd,
                              noise=0)