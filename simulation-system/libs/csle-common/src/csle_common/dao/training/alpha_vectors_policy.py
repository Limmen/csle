from typing import Union, List, Dict, Any
import numpy as np
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.policy import Policy
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.state import State
from csle_common.dao.training.policy_type import PolicyType


class AlphaVectorsPolicy(Policy):
    """
    Object representing a policy based on alpha vectors for a POMDP (Sondik 1971)
    """

    def __init__(self, player_type: PlayerType, actions: List[Action], alpha_vectors: List[Any],
                 transition_tensor: List[Any], reward_tensor: List[Any], states: List[State],
                 agent_type: AgentType, simulation_name: str, avg_R: float) -> None:
        """
        Initializes the policy

        :param actions: list of actions
        :param states: list of states
        :param player_type: the player type
        :param alpha_vectors: the lookup table that defines the policy
        :param value_function: the value function (optional)
        :param simulation_name: the name of the simulation
        :param avg_R: average reward obtained with the policy
        :param transition_tensor: the transition tensor of the POMDP
        :param reward_tensor: the reward tensor of the POMDP
        """
        super(AlphaVectorsPolicy, self).__init__(agent_type=agent_type, player_type=player_type)
        self.actions = actions
        self.alpha_vectors = alpha_vectors
        self.simulation_name = simulation_name
        self.id = -1
        self.avg_R = avg_R
        self.transition_tensor = transition_tensor
        self.reward_tensor = reward_tensor
        self.states = states
        self.policy_type = PolicyType.ALPHA_VECTORS

    def action(self, o: List[Union[int, float]]) -> int:
        """
        Selects the next action

        :param o: the belief
        :return: the next action and its probability
        """
        b = o
        max_a_v = -np.inf
        for a in self.actions:
            v_a = 0
            for s in self.states:
                for s_prime in self.states:
                    transition_prob = (b[s.id] * self.reward_tensor[a.id][s.id] *
                                       self.transition_tensor[a.id][s.id][s_prime.id])
                    max_alpha_v = -np.inf
                    for alpha in self.alpha_vectors:
                        v = np.dot(np.array(alpha), np.array(b[0:len(alpha)]))
                        if v > max_alpha_v:
                            max_alpha_v = v
                    v_a += max_alpha_v * transition_prob
            if v_a > max_a_v:
                max_a_v = v_a
                max_a = a
        try:
            return max_a.id
        except Exception:
            return 0

    def probability(self, o: List[Union[int, float]], a: int) -> float:
        """
        Calculates the probability of taking a given action for a given observation

        :param o: the input observation
        :param a: the action
        :return: p(a|o)
        """
        return a == self.action(o=o)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AlphaVectorsPolicy":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        dto = AlphaVectorsPolicy(actions=list(map(lambda x: Action.from_dict(x), d["actions"])),
                                 player_type=d["player_type"], agent_type=d["agent_type"],
                                 alpha_vectors=d["alpha_vectors"],
                                 simulation_name=d["simulation_name"], avg_R=d["avg_R"],
                                 transition_tensor=d["transition_tensor"], reward_tensor=d["reward_tensor"],
                                 states=list(map(lambda x: State.from_dict(x), d["states"])))
        if "id" in d:
            dto.id = d["id"]
        return dto

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: A dict representation of the function
        """
        d: Dict[str, Any] = {}
        d["agent_type"] = self.agent_type
        d["player_type"] = self.player_type
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["alpha_vectors"] = self.alpha_vectors
        d["simulation_name"] = self.simulation_name
        d["id"] = self.id
        d["avg_R"] = self.avg_R
        d["transition_tensor"] = self.transition_tensor
        d["states"] = list(map(lambda x: x.to_dict(), self.states))
        d["reward_tensor"] = self.reward_tensor
        d["policy_type"] = self.policy_type
        return d

    def stage_policy(self, o: Union[List[Union[int, float]], int, float]) -> List[List[float]]:
        """
        Gets the stage policy, i.e a |S|x|A| policy

        :param o: the latest observation
        :return: the |S|x|A| stage policy
        """
        return self.alpha_vectors

    def __str__(self) -> str:
        """
        :return: a string representation of the policy
        """
        return f"agent_type: {self.agent_type}, player_type: {self.player_type}, " \
               f"actions: {list(map(lambda x: str(x), self.actions))}, alpha_vectors: {self.alpha_vectors}, " \
               f"simulation_name: {self.simulation_name}, id: {self.id}, avg_R: {self.avg_R}," \
               f"transition_tensor: {self.transition_tensor}, states: {self.states}, " \
               f"reward_tensor: {self.reward_tensor}, policy_type: {self.policy_type}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "AlphaVectorsPolicy":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return AlphaVectorsPolicy.from_dict(json.loads(json_str))

    def copy(self) -> "AlphaVectorsPolicy":
        """
        :return: a copy of the DTO
        """
        return AlphaVectorsPolicy.from_dict(self.to_dict())
