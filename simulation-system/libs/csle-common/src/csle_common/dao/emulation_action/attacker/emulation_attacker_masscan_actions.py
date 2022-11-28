from typing import List
import csle_common.constants.constants as constants
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerActionOutcome


class EmulationAttackerMasscanActions:
    """
    Class containing attacker Massscan actions in the emulation
    """

    @staticmethod
    def MASSCAN_HOST_SCAN(index: int, ips: List[str] = None, host_ip: str = "") -> EmulationAttackerAction:
        """
        Action for running a MASSCAN network scan

        :param index: the index of the action
        :param ips: ips of the machines or subnets to apply the action to
        :param host_ip: the host ip
        :return: The created action
        """
        id = EmulationAttackerActionId.MASSCAN_HOST_SCAN
        if ips is None:
            ips = []
        cmd = ["sudo masscan " + constants.MASSCAN.BASE_ARGS + " " + constants.MASSCAN.HOST_ARG + host_ip + " "]
        if index == -1:
            id = EmulationAttackerActionId.MASSCAN_ALL_SCAN

        return EmulationAttackerAction(id=id, name="Masscan port 0-1024", cmds=cmd,
                                       type=EmulationAttackerActionType.RECON,
                                       descr="Masscan port 0-1024",
                                       ips=ips, index=index,
                                       action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING)
