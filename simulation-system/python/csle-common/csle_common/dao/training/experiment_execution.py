from typing import Dict, Any
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_result import ExperimentResult


class ExperimentExecution:
    """
    DTO representing an experiment execution
    """

    def __init__(self, config: ExperimentConfig, result: ExperimentResult, timestamp: float):
        self.config = config
        self.result = result
        self.timestamp = timestamp

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ExperimentExecution":
        """
        Converts a dict representation of the object

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ExperimentExecution(
            config=ExperimentConfig.from_dict(d["config"]),
            result=ExperimentResult.from_dict(d["result"]),
            timestamp=d["timestamp"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["config"] = self.config
        d["result"] = self.result
        d["timestamp"] = self.timestamp
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"config: {self.config}, result: {self.result}, timestamp: {self.timestamp}"