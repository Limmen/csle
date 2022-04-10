from typing import Any, Dict, Union, List
from csle_common.dao.training.policy import Policy


class ExperimentResult:
    """
    DTO representing the results of an experiment
    """

    def __init__(self):
        self.metrics : Dict[int, Dict[str, List[Union[int, float]]]]= {}
        self.policies: Dict[int, Policy] = {}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ExperimentResult":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created insatnce
        """
        obj = ExperimentResult()
        obj.metrics = d["metrics"]
        d2 = {}
        for k,v in d["policies"].items():
            d2[k] = Policy.from_dict(v)
        obj.policies = d2
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["metrics"] = self.metrics
        d2 = {}
        for k,v in self.policies.items():
            d2[k] = v.to_dict()
        d["policies"] = d2
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"metrics: {self.metrics}, policies: {self.policies}"