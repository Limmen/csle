from typing import Union, List, Dict, Optional, Tuple, Any
import random
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.policy import Policy
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.policy_type import PolicyType


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
        self.policy_type = PolicyType.RANDOM

    def action(self, o: Union[List[Union[int, float]], int, float], deterministic: bool = True) -> int:
        """
        Selects the next action

        :param o: the input observation
        :param deterministic: boolean flag indicating whether the action selection should be deterministic
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
    def from_dict(d: Dict[str, Any]) -> "RandomPolicy":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        return RandomPolicy(actions=list(map(lambda x: Action.from_dict(x), d["actions"])),
                            stage_policy_tensor=d["stage_policy_tensor"], player_type=d["player_type"])

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: A dict representation of the function
        """
        d: Dict[str, Any] = {}
        d["agent_type"] = self.agent_type
        d["player_type"] = self.player_type
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["stage_policy_tensor"] = self.stage_policy_tensor
        d["policy_type"] = self.policy_type
        return d

    def stage_policy(self, o: Any) -> Union[List[List[float]], List[float]]:
        """
        Gets the stage policy, i.e a |S|x|A| policy

        :param o: the latest observation
        :return: the |S|x|A| stage policy
        """
        if self.stage_policy_tensor is None:
            raise ValueError("Stage policy is None")
        return self.stage_policy_tensor

    def __str__(self) -> str:
        """
        :return: a string representation of the policy
        """
        return f"agent_type: {self.agent_type}, player_type: {self.player_type}, " \
               f"actions: {list(map(lambda x: str(x), self.actions))}, " \
               f"stage_policy_tensor: {self.stage_policy_tensor}, policy_type: {self.policy_type}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "RandomPolicy":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return RandomPolicy.from_dict(json.loads(json_str))

    def copy(self) -> "RandomPolicy":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())
