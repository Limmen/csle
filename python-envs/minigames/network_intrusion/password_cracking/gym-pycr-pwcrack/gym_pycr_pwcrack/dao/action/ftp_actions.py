from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_type import ActionType
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.action.action import ActionOutcome

class FTPActions:

    @staticmethod
    def FTP_LOGIN(ip: str) -> Action:
        id = ActionId.FTP_LOGIN
        cmd = ["lftp ftp://" + constants.AUXILLARY.USER_PLACEHOLDER + ":" + constants.AUXILLARY.PW_PLACEHOLDER + "@" + ip]
        return Action(id=id, name="FTP Login", cmd=cmd,
                      type=ActionType.POST_EXPLOIT,
                      descr="Uses known credentials to login with FTP on a server",
                      cost=0.01, noise=0.01,
                      ip=ip, subnet=False, action_outcome=ActionOutcome.LOGIN)