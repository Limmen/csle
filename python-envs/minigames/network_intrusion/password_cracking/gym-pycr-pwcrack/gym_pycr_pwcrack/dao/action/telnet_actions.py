from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_type import ActionType
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.action.action import ActionOutcome

class TelnetActions:

    @staticmethod
    def Telnet_LOGIN(ip: str) -> Action:
        id = ActionId.TELNET_LOGIN
        cmd = ["telnet " + ip + " -l " + constants.AUXILLARY.USER_PLACEHOLDER, constants.AUXILLARY.PW_PLACEHOLDER]
        return Action(id=id, name="Telnet Login", cmd=cmd,
                      type=ActionType.POST_EXPLOIT,
                      descr="Uses known credentials to login with telnet on a server",
                      cost=0.1, noise=0.1,
                      ip=ip, subnet=False, action_outcome=ActionOutcome.LOGIN)