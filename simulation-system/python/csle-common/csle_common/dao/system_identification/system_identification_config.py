from typing import Dict, Any, Optional
from csle_common.dao.training.hparam import HParam
from csle_common.dao.system_identification.system_model_type import SystemModelType


class SystemIdentificationConfig:
    """
    DTO representing the configuration of a system identification job
    """

    def __init__(self, model_type: SystemModelType, hparams: Dict[str, HParam], output_dir: str,
                 title: str, log_every: int):
        """
        Initializes the DTO

        :param hparams: a dict with the hyperparameters for the system identification
        :param model_type: the type of system model
        :param output_dir: the output directory
        """
        self.hparams = hparams
        self.model_type = model_type
        self.output_dir = output_dir
        self.title = title
        self.log_every = log_every

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Optional[SystemIdentificationConfig]":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        if d is None:
            return None
        h_d = {}
        for k, v in d["hparams"].items():
            h_d[k] = HParam.from_dict(v)
        obj = SystemIdentificationConfig(hparams=h_d, model_type=d["model_type"], output_dir=d["output_dir"],
                                         title=d["title"], log_every=d["log_every"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d_h = {}
        for k, v in self.hparams.items():
            d_h[k] = v.to_dict()
        d["hparams"] = d_h
        d["model_type"] = self.model_type
        d["output_dir"] = self.output_dir
        d["title"] = self.title
        d["log_every"] = self.log_every
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"hparams: {self.hparams}, model_type: {self.model_type}, output_dir: {self.output_dir}, " \
               f"title: {self.title}, log_every: {self.log_every}"

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
