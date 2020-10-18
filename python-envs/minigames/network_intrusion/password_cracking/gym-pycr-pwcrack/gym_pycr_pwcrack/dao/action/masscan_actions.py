from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_type import ActionType
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.action.action import ActionOutcome

class MasscanActions:

    @staticmethod
    def MASSCAN_HOST_SCAN(index: int, subnet=True, ip: str = "", host_ip : str = "") -> Action:
        cost_noise_multiplier = 1
        id = ActionId.MASSCAN_HOST_SCAN
        file_name = str(id.value) + "_" + ip + ".xml "
        cmd = ["sudo masscan " + constants.MASSCAN.BASE_ARGS + " " + constants.MASSCAN.HOST_ARG + host_ip + " "]
        if subnet:
            cost_noise_multiplier = 10
            id = ActionId.MASSCAN_SUBNET_SCAN
            file_name = str(id.value) + ".xml "

        return Action(id=id, name="Masscan port 0-1024", cmd=cmd,
                      type=ActionType.RECON,
                      descr="Masscan port 0-1024",
                      cost=0.1 * cost_noise_multiplier, noise=0.01 * cost_noise_multiplier,
                      ip=ip, subnet=subnet, index=index,
                      action_outcome=ActionOutcome.INFORMATION_GATHERING)
