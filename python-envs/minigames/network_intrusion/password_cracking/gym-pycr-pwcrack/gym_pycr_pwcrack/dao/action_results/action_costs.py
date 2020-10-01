from gym_pycr_pwcrack.dao.action.action_id import ActionId

class ActionCosts:


    def __init__(self):
        self.costs = {}


    def add_cost(self, action_id : ActionId, ip: str, cost: float):
        key = (action_id, ip)
        self.costs[key] = cost


    def get_cost(self, action_id : ActionId, ip: str):
        key = (action_id, ip)
        return self.costs[key]