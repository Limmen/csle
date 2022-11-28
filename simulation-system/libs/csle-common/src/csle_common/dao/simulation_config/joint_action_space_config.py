from typing import List, Dict, Any
from csle_common.dao.simulation_config.action_space_config import ActionSpaceConfig


class JointActionSpaceConfig:
    """
    DTO representing the joint action space of a simulation environment
    """

    def __init__(self, action_spaces: List[ActionSpaceConfig]):
        """
        Initializes the DTO

        :param action_spaces: the list of action spaces for each player
        """
        self.action_spaces = action_spaces

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "JointActionSpaceConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = JointActionSpaceConfig(
            action_spaces=list(map(lambda x: ActionSpaceConfig.from_dict(x), d["action_spaces"]))
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["action_spaces"] = list(map(lambda x: x.to_dict(), self.action_spaces))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"action_spaces: {list(map(lambda x: str(x), self.action_spaces))}"
