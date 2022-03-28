from typing import List
from csle_common.dao.action.attacker.attacker_action_type import AttackerActionType
from csle_common.dao.action.attacker.attacker_action_id import AttackerActionId
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.attacker.attacker_action import AttackerActionOutcome


class AttackerNetworkServiceActions:
    """
    Class that implements network-service actions for the attacker
    """

    @staticmethod
    def SERVICE_LOGIN(index: int, ips: List[str] = None) -> AttackerAction:
        """
        Action for using known credentials to login to a server

        :param index: index of the machine to apply the action to
        :param ips: ip of the machine to apply the action to
        :return: the action
        """
        if ips is None:
            ips = []
        id = AttackerActionId.NETWORK_SERVICE_LOGIN
        cmd = []
        return AttackerAction(id=id, name="Network service login", cmds=cmd,
                              type=AttackerActionType.POST_EXPLOIT,
                              descr="Uses known credentials to login to network services on a server",
                              index=index,
                              ips=ips, subnet=False, action_outcome=AttackerActionOutcome.LOGIN)