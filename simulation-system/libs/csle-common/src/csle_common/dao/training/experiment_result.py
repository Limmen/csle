from typing import Any, Dict
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_base.json_serializable import JSONSerializable


class ExperimentResult(JSONSerializable):
    """
    DTO representing the results of an experiment
    """

    def __init__(self):
        """
        Initializes the DTO
        """
        self.all_metrics: Dict[int, Dict[str, Any]] = {}
        self.policies: Dict[int, Policy] = {}
        self.plot_metrics = []
        self.avg_metrics = {}
        self.std_metrics = {}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ExperimentResult":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ExperimentResult()
        obj.std_metrics = d["std_metrics"]
        obj.avg_metrics = d["avg_metrics"]
        obj.all_metrics = d["all_metrics"]
        obj.plot_metrics = d["plot_metrics"]
        d2 = {}
        for k, v in d["policies"].items():
            try:
                d2[k] = MultiThresholdStoppingPolicy.from_dict(v)
            except Exception:
                pass
            try:
                d2[k] = PPOPolicy.from_dict(v)
            except Exception:
                pass
        obj.policies = d2
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["all_metrics"] = self.all_metrics
        d2 = {}
        for k, v in self.policies.items():
            d2[k] = v.to_dict()
        d["policies"] = d2
        d["plot_metrics"] = self.plot_metrics
        d["avg_metrics"] = self.avg_metrics
        d["std_metrics"] = self.std_metrics
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"all_metrics: {self.all_metrics}, policies: {self.policies}, plot_metrics: {self.plot_metrics}, " \
               f"avg_metrics: {self.avg_metrics}, std metrics: {self.std_metrics}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "ExperimentResult":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ExperimentResult.from_dict(json.loads(json_str))
