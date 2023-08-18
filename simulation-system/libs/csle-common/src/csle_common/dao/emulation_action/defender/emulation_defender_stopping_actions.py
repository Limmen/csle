from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import EmulationDefenderActionOutcome
from typing import List


class EmulationDefenderStoppingActions:
    """
    Class implementing stopping actions for the defender
    """

    @staticmethod
    def STOP(index: int) -> EmulationDefenderAction:
        """
        Reports a detected intrusion and stops

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationDefenderActionId.STOP
        cmd: List[str] = []
        alt_cmd: List[str] = []
        return EmulationDefenderAction(id=id, name="Report Intrusion", cmds=cmd,
                                       type=EmulationDefenderActionType.STOP,
                                       descr="Reports an ongoing intrusion to the infrastructure and stops",
                                       index=index,
                                       ips=[], action_outcome=EmulationDefenderActionOutcome.GAME_END, alt_cmds=alt_cmd)

    @staticmethod
    def CONTINUE(index: int) -> EmulationDefenderAction:
        """
        A "continue" action, the defender chooses to not make any action

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationDefenderActionId.CONTINUE
        cmd: List[str] = []
        alt_cmd: List[str] = []
        return EmulationDefenderAction(
            id=id, name="Continue", cmds=cmd, type=EmulationDefenderActionType.CONTINUE,
            descr="A 'continue' action, the defender chooses to not make any action", index=index, ips=[],
            action_outcome=EmulationDefenderActionOutcome.CONTINUE, alt_cmds=alt_cmd)

    @staticmethod
    def RESET_USERS(index: int) -> EmulationDefenderAction:
        """
        A non terminal stop action, the defender resets all user accounts, which means that password vulnerabilities
        are mitigated.

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationDefenderActionId.RESET_USERS
        cmd: List[str] = []
        alt_cmd: List[str] = []
        return EmulationDefenderAction(
            id=id, name="Reset Users", cmds=cmd, type=EmulationDefenderActionType.ADD_DEFENSIVE_MECHANISM,
            descr="A non terminal stop action the defender resets all user accounts, which means that "
                  "password vulnerabilities are mitigated", index=index, ips=[],
            action_outcome=EmulationDefenderActionOutcome.ADD_DEFENSIVE_MECHANISM, alt_cmds=alt_cmd)

    @staticmethod
    def ENABLE_DPI(index: int) -> EmulationDefenderAction:
        """
        A non terminal stop action, the defender enables DPI by starting the IDS

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationDefenderActionId.ENABLE_DPI
        cmd: List[str] = []
        alt_cmd: List[str] = []
        return EmulationDefenderAction(id=id, name="Enable DPI", cmds=cmd,
                                       type=EmulationDefenderActionType.ADD_DEFENSIVE_MECHANISM,
                                       descr="A non terminal stop action, the defender enables DPI by starting the IDS",
                                       index=index,
                                       ips=[], action_outcome=EmulationDefenderActionOutcome.ADD_DEFENSIVE_MECHANISM,
                                       alt_cmds=alt_cmd)

    @staticmethod
    def BLACKLIST_IPS(index: int) -> EmulationDefenderAction:
        """
        A non terminal stop action, the defender blacklists all IPs that generate IDS alerts that exceed a threshold,
        the blacklist is implemented using the firewall.

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationDefenderActionId.BLACKLIST_IPS
        cmd: List[str] = []
        alt_cmd: List[str] = []
        return EmulationDefenderAction(
            id=id, name="Blacklist IPs", cmds=cmd,
            type=EmulationDefenderActionType.ADD_DEFENSIVE_MECHANISM,
            descr="A non terminal stop action, the defender blacklists all IPs that generate "
                  "IDS alerts that exceed a threshold, the blacklist is implemented using the firewall.",
            index=index, ips=[], action_outcome=EmulationDefenderActionOutcome.ADD_DEFENSIVE_MECHANISM,
            alt_cmds=alt_cmd)
