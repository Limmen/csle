from enum import Enum


class ActionCosts:
    """
    Object for storing costs of actions
    """

    def __init__(self):
        """
        Initializes the object
        """
        self.costs = {}
        self.find_costs = {}
        self.service_costs = {}
        self.install_costs = {}
        self.pivot_scan_costs = {}

    def add_cost(self, action_id : Enum, ip: str, cost: float) -> None:
        """
        Adds a cost for a given action id and ip

        :param action_id: the action id
        :param ip: the ip
        :param cost: the cost to add
        :return: None
        """
        key = (action_id, ip)
        self.costs[key] = cost

    def get_cost(self, action_id : Enum, ip: str) -> int:
        """
        Get the cost of a given action and ip

        :param action_id: the action id
        :param ip: the ip
        :return: the number of costs for the current action id and ip
        """
        key = (action_id, ip)
        return self.costs[key]

    def exists(self, action_id: Enum, ip: str) -> bool:
        """
        Checks if there is a cost stored for the given action id and ip

        :param action_id: the action id
        :param ip: the ip
        :return: true or false
        """
        key = (action_id, ip)
        return key in self.costs

    def find_add_cost(self, action_id: Enum, ip: str, cost: float, user: str, service: str) -> None:
        """
        Adds a cost for a given user service and action id

        :param action_id: the action id
        :param ip: the ip
        :param cost: the cost to add
        :param user: the user
        :param service: the service
        :return: None
        """
        key = (action_id, ip, service, user)
        self.find_costs[key] = cost

    def find_get_cost(self, action_id: Enum, ip: str, user: str, service: str) -> float:
        """
        Gets the cost stored for a given action, ip, user and service

        :param action_id: the action id
        :param ip: the ip
        :param user: the user
        :param service: the service
        :return: the cost
        """
        key = (action_id, ip, service, user)
        return self.find_costs[key]

    def find_exists(self, action_id: Enum, ip: str, user: str, service: str) -> bool:
        """
        Checks if there is a cost stored for the given action, ip, user, and service

        :param action_id: the action id
        :param ip: the ip
        :param user: the user
        :param service: the service
        :return: true or false
        """
        key = (action_id, ip, service, user)
        return key in self.find_costs

    def service_add_cost(self, action_id: Enum, ip: str, cost: float) -> None:
        """
        Adds a cost for a given action id and ip

        :param action_id: the action id
        :param ip: the ip
        :param cost: the cost to add
        :return: None
        """
        key = (action_id, ip)
        self.costs[key] = cost

    def service_get_cost(self, action_id: Enum, ip: str) -> float:
        """
        Gets the cost for a given action id

        :param action_id: the action id
        :param ip: the ip
        :return: the stored cost

        """
        key = (action_id, ip)
        return self.costs[key]

    def service_exists(self, action_id: Enum, ip: str) -> bool:
        """
        Checks if there exists a cost stored for a given action id and ip

        :param action_id: the action id
        :param ip: the ip
        :return: True or False
        """
        key = (action_id, ip)
        return key in self.costs

    def install_add_cost(self, action_id: Enum, ip: str, cost: float, user: str) -> None:
        """
        Adds a cost for a given action id, user and ip

        :param action_id: the action id
        :param ip: the ip
        :param cost: the cost
        :param user: the user
        :return: None
        """
        key = (action_id, ip, user)
        self.install_costs[key] = cost

    def install_get_cost(self, action_id: Enum, ip: str, user: str) -> float:
        """
        Gets the cost of an install action for a given action id and ip

        :param action_id: the action id
        :param ip: the ip
        :param user: the user
        :return: the cost
        """
        key = (action_id, ip, user)
        return self.install_costs[key]

    def install_exists(self, action_id: Enum, ip: str, user: str) -> bool:
        """
        Checks if there exists a cost stored for a given install action id and ip

        :param action_id: the action id
        :param ip: the ip
        :param user: the user
        :return: True or False
        """
        key = (action_id, ip, user)
        return key in self.install_costs

    def pivot_scan_add_cost(self, action_id: Enum, ip: str, cost: float,
                            user: str, target_ip: str) -> None:
        """
        Adds a cost for a given pivot scan action id, ip, user, and target ip

        :param action_id: the action id
        :param ip: the ip
        :param cost: the cost to add
        :param user: the user
        :param target_ip: the target ip
        :return: None
        """
        key = (action_id, ip, user, target_ip)
        self.pivot_scan_costs[key] = cost

    def pivot_scan_get_cost(self, action_id: Enum, ip: str, user: str, target_ip: str) -> float:
        """
        Gets the cost of a given pivot scan action, ip, user, and target ip

        :param action_id: the id of the actin
        :param ip: the ip
        :param user: the user
        :param target_ip: the target ip
        :return: the cost
        """
        key = (action_id, ip, user, target_ip)
        return self.pivot_scan_costs[key]

    def pivot_scan_exists(self, action_id: Enum, ip: str, user: str, target_ip: str) -> bool:
        """
        Checks if there exists a cost stored for a given pivot scan action id, ip, user, and target ip

        :param action_id: the action id
        :param ip: the ip
        :param user: the user
        :param target_ip: the target ip
        :return: True or False
        """
        key = (action_id, ip, user, target_ip)
        return key in self.pivot_scan_costs
