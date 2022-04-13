from typing import Callable, Union, List, Dict
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.policy import Policy


class StaticPolicy(Policy):
    """
    Object representing a static policy
    """

    def __init__(self, action_selection_function: Callable, player_type: PlayerType) -> None:
        """
        Intializes the policy

        :param action_selection_function: the policy function
        :param player_type: the player type
        """
        super(StaticPolicy, self).__init__(agent_type=AgentType.STATIC, player_type=player_type)
        self.action_selection_function = action_selection_function

    def action(self, o: Union[List[Union[int, float]], int, float]) -> Union[int, float]:
        """
        Selects the next action

        :param o: the input observation
        :return: the next action
        """
        return self.action_selection_function(o)

    def from_dict(d: Dict) -> "Policy":
        raise ValueError("Conversion from dict to policy is not supported for static policies")

    def to_dict(self) -> Dict:
        """
        :return: A dict representation of the function
        """
        d = {}
        d["agent_type"] = self.agent_type
        return d

    def stage_policy(self, o: Union[List[Union[int, float]], int, float]) -> List[List[float]]:
        """
        Gets the stage policy, i.e a |S|x|A| policy

        :param o: the latest observation
        :return: the |S|x|A| stage policy
        """
        return self.action_selection_function(o)

    def __str__(self):
        """
        :return: a string representation of the policy
        """
        return f"agent_type: {self.agent_type}"
