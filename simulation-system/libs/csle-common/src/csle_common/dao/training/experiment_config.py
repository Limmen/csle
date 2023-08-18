from typing import List, Dict, Any
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.hparam import HParam
from csle_base.json_serializable import JSONSerializable


class ExperimentConfig(JSONSerializable):
    """
    DTO representing the configuration of an experiment
    """

    def __init__(self, output_dir: str, title: str, random_seeds: List[int], agent_type: AgentType,
                 hparams: Dict[str, HParam], log_every: int, player_type: PlayerType, player_idx: int,
                 br_log_every: int = 10):
        """
        Initializes the DTO

        :param output_dir: the directory to save logs etc of the experiment
        :param title: the title of the experiment
        :param random_seeds: the random seeds to use in the experiment
        :param agent_type: the type of agent for the experiment
        :param hparams: the hyperparameters
        :param log_every: frequency of logging
        :param player_type: the type of player (e.g. defender or attacker)
        :param player_idx: the player index
        :param br_log_every: frequency of logging when training best response strategies (for game-theoretic algorithms)
        """
        self.output_dir = output_dir
        self.title = title
        self.random_seeds = random_seeds
        self.agent_type = agent_type
        self.hparams = hparams
        self.log_every = log_every
        self.player_type = player_type
        self.player_idx = player_idx
        self.br_log_every = br_log_every

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ExperimentConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """

        h_d = {}
        for k, v in d["hparams"].items():
            h_d[k] = HParam.from_dict(v)
        obj = ExperimentConfig(
            output_dir=d["output_dir"], title=d["title"], random_seeds=d["random_seeds"],
            agent_type=d["agent_type"], hparams=h_d, log_every=d["log_every"], player_type=d["player_type"],
            player_idx=d["player_idx"], br_log_every=d["br_log_every"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["output_dir"] = self.output_dir
        d["title"] = self.title
        d["random_seeds"] = self.random_seeds
        d["agent_type"] = self.agent_type
        d_h = {}
        for k, v in self.hparams.items():
            d_h[k] = v.to_dict()
        d["hparams"] = d_h
        d["log_every"] = self.log_every
        d["player_type"] = self.player_type
        d["player_idx"] = self.player_idx
        d["br_log_every"] = self.br_log_every
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"output_dir:{self.output_dir}, title:{self.title}, random_seeds:{self.random_seeds}, " \
               f"agent_type: {self.agent_type}, hparams: {self.hparams}, log_every: {self.log_every}, " \
               f"player_type: {self.player_type}, player_idx: {self.player_idx}, br_log_every: {self.br_log_every}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "ExperimentConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ExperimentConfig.from_dict(json.loads(json_str))
