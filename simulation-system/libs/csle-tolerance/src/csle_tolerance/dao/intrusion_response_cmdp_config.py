from typing import List


class IntrusionResponseCmdpConfig:
    """
    Configuration of the intrusion response CMDP
    """

    def __init__(self, p_a: float, p_c: float, p_u: float, s_max: int, transition_tensor: List[List[List[float]]],
                 cost_tensor: List[float], negate_costs: bool, seed: int, states: List[int], actions: List[int],
                 initial_state: int, constraint_cost_tensor: List[float], f: int, epsilon_a: float):
        """
        Initializes the DTO

        :param p_a: the intrusion probability
        :param p_c: the crash probability
        :param p_u: the recovery probability
        :param s_max: the maximum node of nodes
        :param transition_tensor: the transition tensor
        :param cost_tensor: the cost tensor
        :param constraint_cost_tensor: the constraint cost tensor
        :param negate_costs: boolean flag indicating whether costs should be negated or not
        :param seed: the random seed
        :param states: the list of states
        :param actions: the list of actions
        :param initial_state: the initial state of the CMDP
        :param cost_tensor: the constraint cost tensor
        :param f: the tolerance threshold
        :param epsilon_a: the expected availability threshold
        """
        self.p_a = p_a
        self.p_c = p_c
        self.p_u = p_u
        self.s_max = s_max
        self.transition_tensor = transition_tensor
        self.cost_tensor = cost_tensor
        self.negate_costs = negate_costs
        self.seed = seed
        self.states = states
        self.actions = actions
        self.initial_state = initial_state
        self.constraint_cost_tensor = constraint_cost_tensor
        self.f = f
        self.epsilon_a = epsilon_a

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return (f"p_a: {self.p_a}, p_c: {self.p_c}, p_u: {self.p_u}, s_max: {self.s_max}, "
                f"transition_tensor: {self.transition_tensor}, cost_tensor: {self.cost_tensor}, seed: {self.seed}, "
                f"negate_costs: {self.negate_costs}, states: {self.states}, actions: {self.actions}, "
                f"initial state: {self.initial_state}, constraint_cost_tensor: {self.constraint_cost_tensor}, "
                f"f: {self.f}, epsilon_a: {self.epsilon_a}")
