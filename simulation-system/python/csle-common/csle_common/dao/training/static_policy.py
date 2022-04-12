from typing import Callable, Union, List, Dict
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.policy import Policy


class StaticPolicy(Policy):
    """
    Object representing a static policy
    """

    def __init__(self, action_selection_function: Callable) -> None:
        super(StaticPolicy, self).__init__(agent_type=AgentType.STATIC)
        self.action_selection_function = action_selection_function

    def action(self, o: Union[List[Union[int, float]], int, float]) -> Union[int, float]:
        """
        Selects the next action

        :param o: the input observation
        :return: the next action
        """
        return self.action_selection_function(o)

    def from_dict(d: Dict) -> "Policy":
        return None

    def to_dict(self) -> Dict:
        d = {}
        d["agent_type"] = self.agent_type
        return d

    def __str__(self):
        """
        :return: a string representation of the policy
        """
        return f"agent_type: {self.agent_type}"
