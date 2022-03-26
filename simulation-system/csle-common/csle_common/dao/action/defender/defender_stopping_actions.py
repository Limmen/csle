from csle_common.dao.action.defender.defender_action import DefenderAction
from csle_common.dao.action.defender.defender_action_type import DefenderActionType
from csle_common.dao.action.defender.defender_action_id import DefenderActionId
from csle_common.dao.action.defender.defender_action_outcome import DefenderActionOutcome


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

    @staticmethod
    def RESET_USERS(index: int) -> DefenderAction:
        """
        A non terminal stop action, the defender resets all user accounts, which means that password vulnerabilities
        are mitigated.

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = DefenderActionId.RESET_USERS
        cmd = []
        alt_cmd = []
        return DefenderAction(id=id, name="Reset Users", cmd=cmd,
                              type=DefenderActionType.ADD_DEFENSIVE_MECHANISM,
                              descr="A non terminal stop action the defender resets all user accounts, "
                                    "which means that password vulnerabilities are mitigated",
                              cost=0.0, index=index,
                              ip=None, subnet=False, action_outcome=DefenderActionOutcome.ADD_DEFENSIVE_MECHANISM,
                              alt_cmd=alt_cmd)

    @staticmethod
    def ENABLE_DPI(index: int) -> DefenderAction:
        """
        A non terminal stop action, the defender enables DPI by starting the IDS

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = DefenderActionId.ENABLE_DPI
        cmd = []
        alt_cmd = []
        return DefenderAction(id=id, name="Enable DPI", cmd=cmd,
                              type=DefenderActionType.ADD_DEFENSIVE_MECHANISM,
                              descr="A non terminal stop action, the defender enables DPI by starting the IDS",
                              cost=0.0, index=index,
                              ip=None, subnet=False, action_outcome=DefenderActionOutcome.ADD_DEFENSIVE_MECHANISM,
                              alt_cmd=alt_cmd)

    @staticmethod
    def BLACKLIST_IPS(index: int) -> DefenderAction:
        """
        A non terminal stop action, the defender blacklists all IPs that generate IDS alerts that exceed a threshold,
        the blacklist is implemented using the firewall.

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = DefenderActionId.BLACKLIST_IPS
        cmd = []
        alt_cmd = []
        return DefenderAction(id=id, name="Blacklist IPs", cmd=cmd,
                              type=DefenderActionType.ADD_DEFENSIVE_MECHANISM,
                              descr="A non terminal stop action, the defender blacklists all IPs that generate "
                                    "IDS alerts that exceed a threshold, the blacklist is implemented "
                                    "using the firewall.",
                              cost=0.0, index=index,
                              ip=None, subnet=False, action_outcome=DefenderActionOutcome.ADD_DEFENSIVE_MECHANISM,
                              alt_cmd=alt_cmd)