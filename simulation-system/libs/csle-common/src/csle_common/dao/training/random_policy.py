from typing import Union, List, Dict, Optional, Tuple
import random
import numpy as np
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.policy import Policy
from csle_common.dao.simulation_config.action import Action


class RandomPolicy(Policy):
    """
    Object representing a static policy
    """

    def __init__(self, player_type: PlayerType, actions: List[Action],
                 stage_policy_tensor: Optional[List[List[float]]]) -> None:
        """
        Initializes the policy

        :param actions: list of actions
        :param player_type: the player type
        :param stage_policy_tensor: the stage policy tensor
        """
        super(RandomPolicy, self).__init__(agent_type=AgentType.RANDOM, player_type=player_type)
        self.actions = actions
        self.stage_policy_tensor = stage_policy_tensor

    def action(self, o: Union[List[Union[int, float]], int, float]) -> Union[int, float]:
        """
        Selects the next action

        :param o: the input observation
        :return: the next action and its probability
        """
        action = random.choice(self.actions)
        return action.id

    def _defender_action(self, o: Union[List[Union[int, float]], int, float]) -> Tuple[Union[int, float], float]:
        """
        Selects the next defender action

        :param o: the input observation
        :return: the next action and its probability
        """
        action = random.choice(self.actions)
        return action.id, self.probability(o=o, a=action.id)

    def probability(self, o: Union[List[Union[int, float]], int, float], a: int) -> float:
        """
        Calculates the probability of taking a given action for a given observation

        :param o: the input observation
        :param a: the action
        :return: p(a|o)
        """
        return 1 / len(self.actions)

    @staticmethod
    def from_dict(d: Dict) -> "RandomPolicy":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        return RandomPolicy(actions=list(map(lambda x: Action.from_dict(x), d["actions"])),
                            stage_policy_tensor=d["stage_policy_tensor"], player_type=d["player_type"])

    def to_dict(self) -> Dict:
        """
        :return: A dict representation of the function
        """
        d = {}
        d["agent_type"] = self.agent_type
        d["player_type"] = self.player_type
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["stage_policy_tensor"] = self.stage_policy_tensor
        return d

    def stage_policy(self, o: Union[List[Union[int, float]], int, float]) -> List[List[float]]:
        """
        Gets the stage policy, i.e a |S|x|A| policy

        :param o: the latest observation
        :return: the |S|x|A| stage policy
        """
        return np.array(self.stage_policy_tensor)

    def __str__(self) -> str:
        """
        :return: a string representation of the policy
        """
        return f"agent_type: {self.agent_type}, player_type: {self.player_type}, " \
               f"actions: {list(map(lambda x: str(x), self.actions))}, stage_policy_tensor: {self.stage_policy_tensor}"

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

    def copy(self) -> "RandomPolicy":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())
