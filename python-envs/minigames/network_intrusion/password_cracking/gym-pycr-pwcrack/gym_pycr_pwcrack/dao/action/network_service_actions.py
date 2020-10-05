from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_type import ActionType
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.action.action import ActionOutcome

class NetworkServiceActions:

    @staticmethod
    def SERVICE_LOGIN(index: int, ip: str = "") -> Action:
        id = ActionId.NETWORK_SERVICE_LOGIN
        cmd = []
        return Action(id=id, name="Network service login", cmd=cmd,
                      type=ActionType.POST_EXPLOIT,
                      descr="Uses kown credentials to login to network services on a server",
                      cost=0.01, noise=0.01, index=index,
                      ip=ip, subnet=False, action_outcome=ActionOutcome.LOGIN)