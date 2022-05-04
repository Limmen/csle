from typing import Any, Dict, Union, List
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.ppo_policy import PPOPolicy


class ExperimentResult:
    """
    DTO representing the results of an experiment
    """

    def __init__(self):
        """
        Initializes the DTO
        """
        self.all_metrics : Dict[int, Dict[str, List[Union[int, float]]]]= {}
        self.policies: Dict[int, Policy] = {}
        self.plot_metrics = []
        self.avg_metrics = {}
        self.std_metrics = {}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ExperimentResult":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created insatnce
        """
        obj = ExperimentResult()
        obj.std_metrics = d["std_metrics"]
        obj.avg_metrics = d["avg_metrics"]
        obj.all_metrics = d["all_metrics"]
        obj.plot_metrics = d["plot_metrics"]
        d2 = {}
        for k,v in d["policies"].items():
            try:
                d2[k] = MultiThresholdStoppingPolicy.from_dict(v)
            except:
                pass
            try:
                d2[k] = PPOPolicy.from_dict(v)
            except:
                pass
        obj.policies = d2
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["all_metrics"] = self.all_metrics
        d2 = {}
        for k,v in self.policies.items():
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
               f"avg_metrtics: {self.avg_metrics}, std metrics: {self.std_metrics}"