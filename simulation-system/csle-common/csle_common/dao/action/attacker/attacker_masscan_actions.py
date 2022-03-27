from typing import List
import csle_common.constants.constants as constants
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.attacker.attacker_action_type import AttackerActionType
from csle_common.dao.action.attacker.attacker_action_id import AttackerActionId
from csle_common.dao.action.attacker.attacker_action import AttackerActionOutcome


class AttackerMasscanActions:
    """
    Class containing attacker Massscan actions
    """

    @staticmethod
    def MASSCAN_HOST_SCAN(index: int, subnet=True, ips: List[str] = None, host_ip : str = "") -> AttackerAction:
        """
        Action for running a MASSCAN network scan

        :param index: the index of the action
        :param subnet: if true, apply action to entire subnet
        :param ips: ips of the machines or subnets to apply the action to
        :param host_ip: the host ip
        :return: The created action
        """
        cost_noise_multiplier = 1
        id = AttackerActionId.MASSCAN_HOST_SCAN
        file_name = str(id.value) + "_" + "_".join(ips) + ".xml "
        cmd = ["sudo masscan " + constants.MASSCAN.BASE_ARGS + " " + constants.MASSCAN.HOST_ARG + host_ip + " "]
        if subnet:
            cost_noise_multiplier = 10
            id = AttackerActionId.MASSCAN_SUBNET_SCAN
            file_name = str(id.value) + ".xml "

        return AttackerAction(id=id, name="Masscan port 0-1024", cmd=cmd,
                              type=AttackerActionType.RECON,
                              descr="Masscan port 0-1024",
                              cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                              ips=ips, subnet=subnet, index=index,
                              action_outcome=AttackerActionOutcome.INFORMATION_GATHERING)
