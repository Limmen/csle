from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.dao.action.attacker.attacker_action_type import AttackerActionType
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerActionOutcome


class AttackerNetworkServiceActions:
    """
    Class that implements network-service actions for the attacker
    """

    @staticmethod
    def SERVICE_LOGIN(index: int, ip: str = "") -> AttackerAction:
        """
        Action for using known credentials to login to a server

        :param index: index of the machine to apply the action to
        :param ip: ip of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.NETWORK_SERVICE_LOGIN
        cmd = []
        return AttackerAction(id=id, name="Network service login", cmd=cmd,
                              type=AttackerActionType.POST_EXPLOIT,
                              descr="Uses known credentials to login to network services on a server",
                              cost=0.01, noise=0.01, index=index,
                              ip=ip, subnet=False, action_outcome=AttackerActionOutcome.LOGIN)