from typing import List
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerActionOutcome


class EmulationAttackerNetworkServiceActions:
    """
    Class that implements network-service actions for the attacker in the emulation
    """

    @staticmethod
    def SERVICE_LOGIN(index: int, ips: List[str] = None) -> EmulationAttackerAction:
        """
        Action for using known credentials to login to a server

        :param index: index of the machine to apply the action to
        :param ips: ip of the machine to apply the action to
        :return: the action
        """
        if ips is None:
            ips = []
        id = EmulationAttackerActionId.NETWORK_SERVICE_LOGIN
        cmd = []
        return EmulationAttackerAction(id=id, name="Network service login", cmds=cmd,
                                       type=EmulationAttackerActionType.POST_EXPLOIT,
                                       descr="Uses known credentials to login to network services on a server",
                                       index=index,
                                       ips=ips, action_outcome=EmulationAttackerActionOutcome.LOGIN)
