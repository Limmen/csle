from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId

class ActionCosts:


    def __init__(self):
        self.costs = {}
        self.find_costs = {}
        self.service_costs = {}
        self.install_costs = {}
        self.pivot_scan_costs = {}

    def add_cost(self, action_id : AttackerActionId, ip: str, cost: float):
        key = (action_id, ip)
        self.costs[key] = cost

    def get_cost(self, action_id : AttackerActionId, ip: str):
        key = (action_id, ip)
        return self.costs[key]

    def exists(self, action_id: AttackerActionId, ip: str):
        key = (action_id, ip)
        return key in self.costs

    def find_add_cost(self, action_id: AttackerActionId, ip: str, cost: float, user: str, service: str):
        key = (action_id, ip, service, user)
        self.find_costs[key] = cost

    def find_get_cost(self, action_id: AttackerActionId, ip: str, user: str, service: str):
        key = (action_id, ip, service, user)
        return self.find_costs[key]

    def find_exists(self, action_id: AttackerActionId, ip: str, user: str, service: str):
        key = (action_id, ip, service, user)
        return key in self.find_costs

    def service_add_cost(self, action_id: AttackerActionId, ip: str, cost: float):
        key = (action_id, ip)
        self.costs[key] = cost

    def service_get_cost(self, action_id: AttackerActionId, ip: str):
        key = (action_id, ip)
        return self.costs[key]

    def service_exists(self, action_id: AttackerActionId, ip: str):
        key = (action_id, ip)
        return key in self.costs

    def install_add_cost(self, action_id: AttackerActionId, ip: str, cost: float, user: str):
        key = (action_id, ip, user)
        self.install_costs[key] = cost

    def install_get_cost(self, action_id: AttackerActionId, ip: str, user: str):
        key = (action_id, ip, user)
        return self.install_costs[key]

    def install_exists(self, action_id: AttackerActionId, ip: str, user: str):
        key = (action_id, ip, user)
        return key in self.install_costs

    def pivot_scan_add_cost(self, action_id: AttackerActionId, ip: str, cost: float, user: str, target_ip: str):
        key = (action_id, ip, user, target_ip)
        self.pivot_scan_costs[key] = cost

    def pivot_scan_get_cost(self, action_id: AttackerActionId, ip: str, user: str, target_ip: str):
        key = (action_id, ip, user, target_ip)
        return self.pivot_scan_costs[key]

    def pivot_scan_exists(self, action_id: AttackerActionId, ip: str, user: str, target_ip: str):
        key = (action_id, ip, user, target_ip)
        return key in self.pivot_scan_costs
