from typing import Union, List, Dict, Optional
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
        Intializes the policy

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
        :return: the next action
        """
        action = random.choice(self.actions)
        return action.id

    @staticmethod
    def from_dict(d: Dict) -> "Policy":
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
