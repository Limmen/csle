from typing import List, Dict, Any
from csle_base.json_serializable import JSONSerializable


class EmpiricalConditional(JSONSerializable):
    """
    A DTO representing an empirical conditional distribution
    """

    def __init__(self, conditional_name: str, metric_name: str,
                 sample_space: List[int],
                 probabilities: List[float]) -> None:
        """
        Initializes the DTO

        :param conditional_name: the name of the conditional
        :param metric_name: the name of the metric
        :param sample_space: the sample space (the domain of the distribution)
        :param probabilities: the probability distribution
        """
        self.conditional_name = conditional_name
        self.probabilities = probabilities
        assert round(sum(probabilities), 2) == 1
        self.metric_name = metric_name
        self.sample_space = sample_space

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmpiricalConditional":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        return EmpiricalConditional(
            conditional_name=d["conditional_name"], metric_name=d["metric_name"],
            sample_space=d["sample_space"], probabilities=d["probabilities"]
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["conditional_name"] = self.conditional_name
        d["metric_name"] = self.metric_name
        d["sample_space"] = self.sample_space
        d["probabilities"] = self.probabilities
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"conditional_name:{self.conditional_name}, metric_name: {self.metric_name}, " \
               f"sample_space: {self.sample_space}, probabilities: {self.probabilities}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmpiricalConditional":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmpiricalConditional.from_dict(json.loads(json_str))
