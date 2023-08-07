from typing import List, Dict, Any
from csle_base.json_serializable import JSONSerializable


class TransitionOperatorConfig(JSONSerializable):
    """
    DTO representing the transition operator definition of a simulation
    """

    def __init__(self, transition_tensor: List[Any]):
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
        Converts the object to a dict representation

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

    @staticmethod
    def from_json_file(json_file_path: str) -> "TransitionOperatorConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return TransitionOperatorConfig.from_dict(json.loads(json_str))
