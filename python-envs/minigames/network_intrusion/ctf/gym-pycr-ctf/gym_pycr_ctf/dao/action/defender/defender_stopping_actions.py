from gym_pycr_ctf.dao.action.defender.defender_action import DefenderAction
from gym_pycr_ctf.dao.action.defender.defender_action_type import DefenderActionType
from gym_pycr_ctf.dao.action.defender.defender_action_id import DefenderActionId
from gym_pycr_ctf.dao.action.defender.defender_action_outcome import DefenderActionOutcome


class DefenderStoppingActions:
    """
    Class implementing stopping actions for the defender
    """

    @staticmethod
    def STOP(index : int) -> DefenderAction:
        """
        Reports a detected intrusion and stops

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = DefenderActionId.STOP
        cmd = []
        alt_cmd = []
        return DefenderAction(id=id, name="Report Intrusion", cmd=cmd,
                              type=DefenderActionType.STOP,
                              descr="Reports an ongoing intrusion to the infrastructure and stops",
                              cost=0.0, index=index,
                              ip=None, subnet=False, action_outcome=DefenderActionOutcome.GAME_END, alt_cmd=alt_cmd)

    @staticmethod
    def CONTINUE(index: int) -> DefenderAction:
        """
        A "continue" action, the defender chooses to not make any action

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = DefenderActionId.CONTINUE
        cmd = []
        alt_cmd = []
        return DefenderAction(id=id, name="Continue", cmd=cmd,
                              type=DefenderActionType.CONTINUE,
                              descr="A 'continue' action, the defender chooses to not make any action",
                              cost=0.0, index=index,
                              ip=None, subnet=False, action_outcome=DefenderActionOutcome.CONTINUE, alt_cmd=alt_cmd)