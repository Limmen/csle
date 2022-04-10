from typing import List, Dict, Any, Union
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam


class ExperimentConfig:
    """
    DTO representing the configuration of an experiment
    """

    def __init__(self, output_dir:str, title: str, random_seeds: List[int], agent_type: AgentType,
                 hparams: Dict[str, HParam], log_every: int):
        self.output_dir = output_dir
        self.title = title
        self.random_seeds = random_seeds
        self.agent_type = agent_type
        self.hparams = hparams
        self.log_every = log_every

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ExperimentConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        h_d = {}
        for k,v in d["hparams"].items():
            h_d[k] = HParam.from_dict(v)
        obj = ExperimentConfig(
            output_dir=d["output_dir"], title=d["title"], random_seeds=d["random_seeds"],
            agent_type=d["agent_type"], hparams=h_d, log_every=d["log_every"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["output_dir"] = self.output_dir
        d["title"] = self.title
        d["random_seeds"] = self.random_seeds
        d["agent_type"] = self.agent_type
        d_h = {}
        for k,v in self.hparams.items():
            d_h[k] = v.to_dict()
        d["hparams"] = d_h
        d["log_every"] = self.log_every
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"output_dir:{self.output_dir}, title:{self.title}, random_seeds:{self.random_seeds}, " \
               f"agent_type: {self.agent_type}, hparams: {self.hparams}, log_every: {self.log_every}"