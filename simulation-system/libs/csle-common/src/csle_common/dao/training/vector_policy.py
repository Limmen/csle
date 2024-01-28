from typing import Union, List, Dict, Any
import numpy as np
from numpy.typing import NDArray
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.policy_type import PolicyType


class VectorPolicy(Policy):
    """
    Object representing a tabular policy
    """

    def __init__(self, player_type: PlayerType, actions: List[int], policy_vector: List[float],
                 agent_type: AgentType, simulation_name: str, avg_R: float) -> None:
        """
        Initializes the policy

        :param actions: list of actions
        :param player_type: the player type
        :param policy_vector: the policy vector
        :param simulation_name: the name of the simulation
        :param avg_R: average reward obtained with the policy
        """
        super(VectorPolicy, self).__init__(agent_type=agent_type, player_type=player_type)
        self.actions = actions
        self.policy_vector = policy_vector
        self.simulation_name = simulation_name
        self.id = -1
        self.avg_R = avg_R
        self.policy_type = PolicyType.VECTOR

    def action(self, o: Union[List[Union[int, float]], int, float], deterministic: bool = True) \
            -> Union[int, List[int], float, NDArray[Any]]:
        """
        Selects the next action

        :param o: the input observation
        :param deterministic: boolean flag indicating whether the action selection should be deterministic
        :return: the next action and its probability
        """
        return float(np.random.choice(np.arange(0, len(self.policy_vector)), p=self.policy_vector))

    def probability(self, o: Union[List[Union[int, float]], int, float], a: int) -> float:
        """
        Calculates the probability of taking a given action for a given observation

        :param o: the input observation
        :param a: the action
        :return: p(a|o)
        """
        return self.policy_vector[a]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "VectorPolicy":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        dto = VectorPolicy(actions=d["actions"],
                           player_type=d["player_type"], agent_type=d["agent_type"],
                           policy_vector=d["policy_vector"],
                           simulation_name=d["simulation_name"], avg_R=d["avg_R"])
        if "id" in d:
            dto.id = d["id"]
        return dto

    def to_dict(self) -> Dict[str, Any]:
        """
        Gets a dict representation of the object

        :return: A dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["agent_type"] = self.agent_type
        d["player_type"] = self.player_type
        d["actions"] = self.actions
        d["policy_vector"] = self.policy_vector
        d["simulation_name"] = self.simulation_name
        d["id"] = self.id
        d["avg_R"] = self.avg_R
        d["policy_type"] = self.policy_type
        return d

    def stage_policy(self, o: Union[List[Union[int, float]], int, float]) -> List[float]:
        """
        Gets the stage policy, i.e a |S|x|A| policy

        :param o: the latest observation
        :return: the |S|x|A| stage policy
        """
        return self.policy_vector

    def __str__(self) -> str:
        """
        :return: a string representation of the policy
        """
        return f"agent_type: {self.agent_type}, player_type: {self.player_type}, " \
               f"actions: {list(map(lambda x: str(x), self.actions))}, policy_vector: {self.policy_vector}, " \
               f"simulation_name: {self.simulation_name}, id: {self.id}, " \
               f"avg_R: {self.avg_R}, type: {self.policy_type}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "VectorPolicy":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return VectorPolicy.from_dict(json.loads(json_str))

    def copy(self) -> "VectorPolicy":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())
