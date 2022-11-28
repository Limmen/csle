from typing import Union, List, Dict
import numpy as np
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.policy import Policy


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

    def action(self, o: Union[List[Union[int, float]], int, float]) -> Union[int, float]:
        """
        Selects the next action

        :param o: the input observation
        :return: the next action and its probability
        """
        return np.random.choice(np.arange(0, len(self.policy_vector)), p=self.policy_vector)

    def probability(self, o: Union[List[Union[int, float]], int, float], a: int) -> float:
        """
        Calculates the probability of taking a given action for a given observation

        :param o: the input observation
        :param a: the action
        :return: p(a|o)
        """
        return self.policy_vector[a]

    @staticmethod
    def from_dict(d: Dict) -> "VectorPolicy":
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

    def to_dict(self) -> Dict:
        """
        :return: A dict representation of the function
        """
        d = {}
        d["agent_type"] = self.agent_type
        d["player_type"] = self.player_type
        d["actions"] = self.actions
        d["policy_vector"] = self.policy_vector
        d["simulation_name"] = self.simulation_name
        d["id"] = self.id
        d["avg_R"] = self.avg_R
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
               f"avg_R: {self.avg_R}"

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    def copy(self) -> "VectorPolicy":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())
