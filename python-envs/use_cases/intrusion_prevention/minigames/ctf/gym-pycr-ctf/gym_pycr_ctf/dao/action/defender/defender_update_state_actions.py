from gym_pycr_ctf.dao.action.defender.defender_action import DefenderAction
from gym_pycr_ctf.dao.action.defender.defender_action_type import DefenderActionType
from gym_pycr_ctf.dao.action.defender.defender_action_id import DefenderActionId
from gym_pycr_ctf.dao.action.defender.defender_action_outcome import DefenderActionOutcome


class DefenderUpdateStateActions:
    """
    Class implementing actions for updating the defender's state
    """

    @staticmethod
    def UPDATE_STATE(index : int) -> DefenderAction:
        """
        Updates the defender's state

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = DefenderActionId.UPDATE_STATE
        cmd = []
        alt_cmd = []
        return DefenderAction(id=id, name="Update the defender's state", cmd=cmd,
                              type=DefenderActionType.STATE_UPDATE,
                              descr="Update's the defenders state",
                              cost=0.0, index=index,
                              ip=None, subnet=False, action_outcome=DefenderActionOutcome.STATE_UPDATE,
                              alt_cmd=alt_cmd)

    @staticmethod
    def INITIALIZE_STATE(index: int) -> DefenderAction:
        """
        Initializes the defender's state

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = DefenderActionId.INITIALIZE_STATE
        cmd = []
        alt_cmd = []
        return DefenderAction(id=id, name="Initializes the defender's state", cmd=cmd,
                              type=DefenderActionType.STATE_UPDATE,
                              descr="Initializes's the defenders state",
                              cost=0.0, index=index,
                              ip=None, subnet=False, action_outcome=DefenderActionOutcome.STATE_UPDATE,
                              alt_cmd=alt_cmd)

    @staticmethod
    def RESET_STATE(index: int) -> DefenderAction:
        """
        Resets the defender's state

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = DefenderActionId.RESET_STATE
        cmd = []
        alt_cmd = []
        return DefenderAction(id=id, name="Resets the defender's state", cmd=cmd,
                              type=DefenderActionType.STATE_UPDATE,
                              descr="Resets's the defenders state",
                              cost=0.0, index=index,
                              ip=None, subnet=False, action_outcome=DefenderActionOutcome.STATE_UPDATE,
                              alt_cmd=alt_cmd)