from typing import List
from gym_pycr_pwcrack.dao.action.action_type import ActionType
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.action.action_outcome import ActionOutcome
import gym_pycr_pwcrack.constants.constants as constants

class Action:

    def __init__(self, id : ActionId, name :str, cmd : List[str], type: ActionType, descr: str, cost: float,
                 noise : float, ip :str, index: int, subnet : bool = False,
                 action_outcome: ActionOutcome = ActionOutcome.INFORMATION_GATHERING,
                 vulnerability: str = None, alt_cmd = List[str]):
        self.id = id
        self.name = name
        self.cmd = cmd
        self.type = type
        self.descr = descr
        self.cost = cost
        self.noise = noise
        self.ip = ip
        self.subnet = subnet
        self.action_outcome = action_outcome
        self.vulnerability = vulnerability
        self.alt_cmd = alt_cmd
        self.index = index

    def __str__(self):
        return "id:{},name:{},ip:{},subnet:{},index:{}".format(self.id, self.name, self.ip, self.subnet,self.index)

    def nmap_cmd(self, machine_ip : str = None):
        file_name = str(self.id.value) + "_" + str(self.index) + "_" + self.ip
        if self.subnet:
            file_name = str(self.id.value) + "_" + str(self.index)
        if machine_ip is not None:
            file_name = file_name + "_" + machine_ip
        file_name = file_name + ".xml "
        return self.cmd[0] + constants.NMAP.FILE_ARGS + " " + file_name + self.ip

    def nikto_cmd(self):
        file_name = str(self.id.value) + "_" + str(self.index) + "_" + self.ip + ".xml "
        return self.cmd[0] + constants.NIKTO.HOST_ARG + self.ip + " " + constants.NIKTO.OUTPUT_ARG + file_name

    def masscan_cmd(self):
        file_name = str(self.id.value) + "_" + str(self.index) + "_" + self.ip + ".xml "
        if self.subnet:
            file_name = str(self.id.value) + "_" + str(self.index) + ".xml "
        return self.cmd[0] + constants.MASSCAN.OUTPUT_ARG + " " + file_name + self.ip