from typing import List, Dict, Any


class TransitionOperatorConfig:
    """
    DTO representing the transition operator definition of a simulation
    """

    def __init__(self, transition_tensor: List):
        """
        Initializes the DTO

        :param transition_tensor: the transition tensor of the simulation
        """
        self.transition_tensor = transition_tensor

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TransitionOperatorConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = TransitionOperatorConfig(
            transition_tensor=d["transition_tensor"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["transition_tensor"] = self.transition_tensor
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"transition tensor: {self.transition_tensor}"
