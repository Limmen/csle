from typing import List
import csle_common.constants.constants as constants
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerActionOutcome


class EmulationAttackerNIKTOActions:
    """
    Class implementing NIKTO scan actions for the attacker in the emulation
    """

    @staticmethod
    def NIKTO_WEB_HOST_SCAN(index: int, ips: List[str] = None) -> EmulationAttackerAction:
        """
        Action for running a nikto web scan on a given host

        :param index: index of the machine to apply the action to
        :param ips: ip of the machine to apply the action to
        :return: the action
        """
        if ips is None:
            ips = []
        id = EmulationAttackerActionId.NIKTO_WEB_HOST_SCAN
        cmd = ["no | sudo nikto " + constants.NIKTO.BASE_ARGS]
        return EmulationAttackerAction(id=id, name="Nikto Web Scan", cmds=cmd,
                                       type=EmulationAttackerActionType.RECON,
                                       descr="Nikto Web Scan",
                                       ips=ips, index=index,
                                       action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING)
