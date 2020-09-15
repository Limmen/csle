from gym_pycr_pwcrack.dao.action_type import ActionType

class Action:

    def __init__(self, id : int, name :str, cmd : str, type: ActionType, descr: str, cost: float, noise : int):
        self.id = id
        self.name = name
        self.cmd = cmd
        self.type = type
        self.descr = descr
        self.cost = cost
        self.noise = noise