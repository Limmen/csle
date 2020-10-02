from gym_pycr_pwcrack.dao.action.action_id import ActionId

class ActionCosts:


    def __init__(self):
        self.costs = {}
        self.find_costs = {}


    def add_cost(self, action_id : ActionId, ip: str, cost: float):
        key = (action_id, ip)
        self.costs[key] = cost


    def get_cost(self, action_id : ActionId, ip: str):
        key = (action_id, ip)
        return self.costs[key]

    def exists(self, action_id: ActionId, ip: str):
        key = (action_id, ip)
        return key in self.costs

    def find_add_cost(self, action_id: ActionId, ip: str, cost: float, user: str, service: str):
        key = (action_id, ip, service, user)
        self.find_costs[key] = cost

    def find_get_cost(self, action_id: ActionId, ip: str, user: str, service: str):
        key = (action_id, ip, service, user)
        return self.find_costs[key]

    def find_exists(self, action_id: ActionId, ip: str, user: str, service: str):
        key = (action_id, ip, service, user)
        return key in self.find_costs
