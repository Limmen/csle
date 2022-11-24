from typing import Dict, Any, List


class RewardFunctionConfig:
    """
    DTO containing the reward tensor of a simulation
    """

    def __init__(self, reward_tensor: List):
        """
        Initalizes the DTO

        :param reward_tensor: the reward tensor of the simulation
        """
        self.reward_tensor = reward_tensor

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RewardFunctionConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = RewardFunctionConfig(
            reward_tensor=d["reward_tensor"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation  of the object
        """
        d = {}
        d["reward_tensor"] = self.reward_tensor
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"reward_tensor:{self.reward_tensor}"
