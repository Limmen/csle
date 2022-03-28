from typing import List
import csle_common.constants.constants as constants
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.attacker.attacker_action_type import AttackerActionType
from csle_common.dao.action.attacker.attacker_action_id import AttackerActionId
from csle_common.dao.action.attacker.attacker_action import AttackerActionOutcome


class AttackerNIKTOActions:
    """
    Class implementing NIKTO scan actions for the attacker
    """

    @staticmethod
    def NIKTO_WEB_HOST_SCAN(index: int, ips: List[str] = None) -> AttackerAction:
        """
        Action for running a nikto web scan on a given host

        :param index: index of the machine to apply the action to
        :param ips: ip of the machine to apply the action to
        :return: the action
        """
        if ips is None:
            ips = []
        id = AttackerActionId.NIKTO_WEB_HOST_SCAN
        cmd = ["no | sudo nikto " + constants.NIKTO.BASE_ARGS]
        return AttackerAction(id=id, name="Nikto Web Scan", cmds=cmd,
                              type=AttackerActionType.RECON,
                              descr="Nikto Web Scan",
                              ips=ips, subnet=False, index=index,
                              action_outcome=AttackerActionOutcome.INFORMATION_GATHERING)
