from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_type import ActionType
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.action.action import ActionOutcome

class SSHActions:

    @staticmethod
    def SSH_LOGIN(ip: str) -> Action:
        id = ActionId.SSH_LOGIN
        cmd = "sshpass -p " + constants.AUXILLARY.PW_PLACEHOLDER + " ssh " + "-o StrictHostKeyChecking=no " \
              + constants.AUXILLARY.USER_PLACEHOLDER + "@" + ip
        return Action(id=id, name="SSH Login", cmd=cmd,
                      type=ActionType.POST_EXPLOIT,
                      descr="Uses kown credentials to login with SSH on a server",
                      cost=0.1, noise=0.1,
                      ip=ip, subnet=False, action_outcome=ActionOutcome.LOGIN)