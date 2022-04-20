from typing import List, Dict, Tuple, Union
import math
import random
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.action import Action


class TSPSAPolicy(Policy):
    """
    A multi-threshold policy learned with T-SPSA
    """

    def __init__(self, theta, simulation_name: str, L: int, states : List[State], player_type: PlayerType,
                 actions: List[Action]):
        """
        Initializes the policy

        :param theta: the threshold vector
        :param simulation_name: the simulation name
        :param attacker: whether it is an attacker or not
        :param L: the number of stop actions
        :param states: list of states (required for computing stage policies)
        :param actions: list of actions
        """
        super(TSPSAPolicy, self).__init__(agent_type=AgentType.T_SPSA, player_type=player_type)
        self.theta = theta
        self.id = -1
        self.simulation_name = simulation_name
        self.L = L
        self.states = states
        self.actions = actions

    def action(self, o: List[float]) -> int:
        """
        Multi-threshold stopping policy

        :param o: the current observation
        :return: the selected action
        """
        if not self.player_type == PlayerType.ATTACKER:
            return self._defender_action(o=o)
        else:
            self._attacker_action(o=o)

    def _attacker_action(self, o) -> int:
        """
        Multi-threshold stopping policy of the attacker

        :param o: the input observation
        :return: the selected action (int)
        """
        s = o[2]
        b1 = o[1]
        l = int(o[0])
        theta_val = self.theta[s*self.L + l-1]
        threshold = TSPSAPolicy.sigmoid(theta_val)
        a = 0
        if b1 >= threshold:
            a, _ = TSPSAPolicy.smooth_threshold_action_selection(threshold=threshold, b1=b1)
        return a

    def stage_policy(self, o: Union[List[Union[int, float]], int, float]) -> List[List[float]]:
        """
        Gets the stage policy, i.e a |S|x|A| policy

        :param o: the latest observation
        :return: the |S|x|A| stage policy
        """
        b1 = o[1]
        l = int(o[0])
        threshold = TSPSAPolicy.sigmoid(self.theta[l-1])
        if not self.player_type == PlayerType.ATTACKER:
            stage_policy = []
            for _ in self.states:
                stopping_probability = TSPSAPolicy.stopping_probability(b1=b1, threshold=threshold)
                stage_policy.append([1-stopping_probability, stopping_probability])
            return stage_policy
        else:
            stage_policy = []
            for s in self.states:
                if s.state_type != StateType.TERMINAL:
                    theta_val = self.theta[s.id*self.L + l-1]
                    threshold = TSPSAPolicy.sigmoid(theta_val)
                    stopping_probability = TSPSAPolicy.stopping_probability(b1=b1, threshold=threshold)
                    stage_policy.append([1-stopping_probability, stopping_probability])
                else:
                    stage_policy.append([0.5, 0.5])
            return stage_policy

    def _defender_action(self, o) -> int:
        """
        Multi-threshold stopping policy of the defender

        :param o: the input observation
        :return: the selected action (int)
        """
        b1 = o[1]
        l = int(o[0])
        threshold = TSPSAPolicy.sigmoid(self.theta[l-1])
        a = 0
        if b1 >= threshold:
            a, _ = TSPSAPolicy.smooth_threshold_action_selection(threshold=threshold, b1=b1)
        return a

    @staticmethod
    def sigmoid(x) -> float:
        """
        The sigmoid function

        :param x:
        :return: sigmoid(x)
        """
        return 1/(1 + math.exp(-x))

    @staticmethod
    def smooth_threshold_action_selection(threshold: float, b1: float) -> Tuple[int, float]:
        """
        Selects the next action according to a smooth threshold function on the belief

        :param threshold: the threshold
        :param b1: the belief
        :return: the selected action and the probability
        """
        prob = TSPSAPolicy.stopping_probability(b1=b1, threshold=threshold)
        if random.uniform(0,1) >= prob:
            return 0, 1-prob
        else:
            return 1, prob

    @staticmethod
    def stopping_probability(b1, threshold) -> float:
        """
        Returns the probability of stopping given a belief and a threshold

        :param b1: the belief
        :param threshold: the threhsold
        :return: the stopping probability
        """
        if (threshold*(1-b1)) > 0 and (b1*(1-threshold))/(threshold*(1-b1)) > 0:
            return math.pow(1 + math.pow(((b1*(1-threshold))/(threshold*(1-b1))), -20), -1)
        else:
            return 0

    def to_dict(self) -> Dict[str, List[float]]:
        """
        :return: a dict representation of the policy
        """
        d = {}
        d["theta"] = self.theta
        d["id"] = self.id
        d["simulation_name"] = self.simulation_name
        d["thresholds"] = self.thresholds()
        d["states"] = list(map(lambda x: x.to_dict(), self.states))
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["player_type"] = self.player_type
        d["agent_type"] = self.agent_type
        d["L"] = self.L
        return d

    @staticmethod
    def from_dict(d: Dict) -> "TSPSAPolicy":
        """
        Converst a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = TSPSAPolicy(theta=d["theta"], simulation_name=d["simulation_name"], L=d["L"],
                          states=list(map(lambda x: State.from_dict(x), d["states"])), player_type=d["player_type"],
                          actions=list(map(lambda x: Action.from_dict(x), d["actions"])))
        obj.id = d["id"]
        return obj

    def thresholds(self) -> List[float]:
        """
        :return: the thresholds
        """
        return list(map(lambda x: round(TSPSAPolicy.sigmoid(x),3), self.theta))

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"theta: {self.theta}, id: {self.id}, simulation_name: {self.simulation_name}, " \
               f"thresholds: {self.thresholds()}, player_type: {self.player_type}, " \
               f"L:{self.L}, states: {self.states}, agent_type: {self.agent_type}, actions: {self.actions}"

