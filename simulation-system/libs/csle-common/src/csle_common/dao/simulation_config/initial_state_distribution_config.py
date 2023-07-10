from typing import List, Dict, Any
from csle_base.json_serializable import JSONSerializable


class InitialStateDistributionConfig(JSONSerializable):
    """
    DTO class representing the configuration of the initial state distribution of a simulation
    """

    def __init__(self, initial_state_distribution: List[float]):
        """
        Initializes the DTO

        :param initial_state_distribution: the initial state distribution
        """
        assert round(sum(initial_state_distribution), 3) == 1
        self.initial_state_distribution = initial_state_distribution

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "InitialStateDistributionConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = InitialStateDistributionConfig(
            initial_state_distribution=d["initial_state_distribution"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d = {}
        d["initial_state_distribution"] = self.initial_state_distribution
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"initial_state_distribution: {self.initial_state_distribution}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "InitialStateDistributionConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return InitialStateDistributionConfig.from_dict(json.loads(json_str))
