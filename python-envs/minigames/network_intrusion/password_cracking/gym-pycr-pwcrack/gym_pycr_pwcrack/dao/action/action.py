from gym_pycr_pwcrack.dao.action.action_type import ActionType
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.action.action_outcome import ActionOutcome

class Action:

    def __init__(self, id : ActionId, name :str, cmd : str, type: ActionType, descr: str, cost: float, noise : int,
                 ip :str, subnet : bool = False, action_outcome: ActionOutcome = ActionOutcome.INFORMATION_GATHERING,
                 vulnerability: str = None):
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

    def __str__(self):
        return "id:{},name:{},ip:{},subnet:{}".format(self.id, self.name, self.ip, self.subnet)