from typing import List, Dict, Any


class EmpiricalConditional:
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
        d = {}
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

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
