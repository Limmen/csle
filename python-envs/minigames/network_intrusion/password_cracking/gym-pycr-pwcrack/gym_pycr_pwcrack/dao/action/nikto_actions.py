from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_type import ActionType
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.action.action import ActionOutcome

class NIKTOActions:

    @staticmethod
    def NIKTO_WEB_HOST_SCAN(index: int, ip: str = "") -> Action:
        cost_noise_multiplier = 1
        id = ActionId.NIKTO_WEB_HOST_SCAN
        file_name = str(id.value) + "_" + ip + ".xml "
        cmd = ["no | sudo nikto " + constants.NIKTO.BASE_ARGS]
        return Action(id=id, name="Nikto Web Scan", cmd=cmd,
                      type=ActionType.RECON,
                      descr="Nikto Web Scan",
                      cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                      ip=ip, subnet=False, index=index,
                      action_outcome=ActionOutcome.INFORMATION_GATHERING)
