from typing import List
import numpy as np
import math


class IntrusionResponseCmdpUtil:
    """
    Class with utility functions for the intrusion-response CMDP
    """

    @staticmethod
    def state_space(s_max) -> List[int]:
        """
        Gets the state space of the CMDP

        :return: a list with the states
        """
        return list(range(s_max + 1))

    @staticmethod
    def action_space() -> List[int]:
        """
        Gets the action space of the CMDP

        :return: a list with the actions
        """
        return [0, 1]

    @staticmethod
    def cost_function(s: int, negate: bool = False) -> float:
        """
        Cost function of the CMDP

        :param negate: boolean flag, if true then return negated version of the cost (the reward)
        :param s: the state
        :return: the cost
        """
        if negate:
            return float(-s)
        else:
            return float(s)

    @staticmethod
    def cost_tensor(states: List[int], negate: bool = False) -> List[float]:
        """
        Creates a |S| tensor with the costs (or rewards) of the CMDP

        :param states: the list of states
        :param negate: a boolean flag indicating whether the cost should be negated as a reward or not
        :return: A tensor with the costs (or rewards)
        """
        cost_tensor = []
        for s in states:
            cost_tensor.append(IntrusionResponseCmdpUtil.cost_function(s=s, negate=negate))
        return cost_tensor

    @staticmethod
    def constraint_cost_function(s: int, f: int) -> float:
        """
        Constraint cost function of the CMDP

        :param s: the state
        :param f: the tolerance threshold
        :return: the cost
        """
        constraint_cost = 0.0
        if s >= f + 1:
            constraint_cost = 1.0
        return constraint_cost

    @staticmethod
    def constraint_cost_tensor(states: List[int], f: int) -> List[float]:
        """
        Creates a |S| tensor with the constraint costs of the CMDP

        :param states: the list of states
        :param f: the tolerance threshold
        :return: A tensor with the costs (or rewards)
        """
        constraint_cost_tensor = []
        for s in states:
            constraint_cost_tensor.append(IntrusionResponseCmdpUtil.constraint_cost_function(s=s, f=f))
        return constraint_cost_tensor

    @staticmethod
    def delta_function(s: int, p_a: float, p_c: float, p_u: float, delta: int, s_max: int) -> float:
        """
        The delta function that gives the probability of the change in the number of healthy nodes

        :param s: the current state
        :param p_a: the intrusion probability
        :param p_c: the crash probability
        :param p_u: the recovery probability
        :param delta: the delta value
        :param s_max: the maximum number of nodes
        :return:
        """
        prob = 0.0
        for failures in range(0, s_max + 1):
            for recoveries in range(0, s_max + 1):
                if (recoveries - failures) == delta and (s + delta) <= s_max and (s + delta) >= 0:
                    non_recoveries = s - recoveries
                    non_failures = s - failures
                    prob += (math.pow(p_u, recoveries) * math.pow(1 - p_u, non_recoveries) *
                             math.pow(p_a + p_c, failures) * math.pow(1 - p_a - p_c, non_failures))
        return prob

    @staticmethod
    def transition_function(s: int, s_prime: int, a: int, p_a: float, p_c: float, p_u: float, s_max: int) -> float:
        """
        The transition function of the CMDP

        :param s: the state
        :param s_prime: the next state
        :param a: the action
        :param p_a: the intrusion probability
        :param p_c: the crash probability
        :param p_u: the recovery probability
        :param s_max: the maximum state
        :return: P(s_prime | s, a)
        """
        delta = s_prime - a - s
        delta_prob = IntrusionResponseCmdpUtil.delta_function(s=s, p_a=p_a, p_c=p_c, p_u=p_u, delta=delta, s_max=s_max)
        return delta_prob

    @staticmethod
    def transition_tensor(states: List[int], actions: List[int], p_a: float, p_c: float, p_u: float, s_max: int) \
            -> List[List[List[float]]]:
        """
        Creates a |A|x|S|x|S| tensor with the transition probabilities of the CMDP

        :param states: the list of states
        :param actions: the list of actions
        :param p_a: the intrusion probability
        :param p_c: the failure probability
        :param p_u: the upgrade probability
        :return: the transition tensor
        """
        transition_tensor = []
        for a in actions:
            a_transitions = []
            for s in states:
                s_a_transitions = []
                normalizing_constant = 0.0
                for delta in range(-s_max, s_max + 1):
                    normalizing_constant += IntrusionResponseCmdpUtil.delta_function(s=s, p_a=p_a, p_c=p_c, p_u=p_u,
                                                                                     delta=delta, s_max=s_max)
                for s_prime in states:
                    s_a_transitions.append(IntrusionResponseCmdpUtil.transition_function(
                        s=s, s_prime=s_prime, a=a, p_a=p_a, p_c=p_c, p_u=p_u, s_max=s_max))
                normalizing_constant = sum(s_a_transitions)
                s_a_transitions = list(np.array(s_a_transitions) * (1 / normalizing_constant))
                if not round(sum(s_a_transitions), 2) == 1:
                    print(f"{sum(s_a_transitions)}, s:{s}, a:{a}, normalizing constant: {normalizing_constant}, "
                          f"s_a_transitions: {s_a_transitions}")
                a_transitions.append(s_a_transitions)
            transition_tensor.append(a_transitions)
        return transition_tensor
