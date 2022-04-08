from typing import Any, Dict, Union


class ExperimentResult:
    """
    DTO representing the results of an experiment
    """

    def __init__(self):
        self.metrics = {}


    def update_metric(self, metric_name: str, value: Union[float, int, str]) -> None:
        """
        Updates a given metric with a given value

        :param metric_name: the metric to update
        :param value: the new value
        :return: None
        """
        if metric_name in self.metrics:
            self.metrics[metric_name].append(value)
        else:
            self.metrics[metric_name] = [value]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ExperimentResult":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created insatnce
        """
        obj = ExperimentResult()
        obj.metrics = d["metrics"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["metrics"] = self.metrics
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"metrics: {self.metrics}"