from typing import Dict, Any
from csle_common.dao.training.hparam import HParam
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_base.json_serializable import JSONSerializable


class SystemIdentificationConfig(JSONSerializable):
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
    def from_dict(d: Dict[str, Any]) -> "SystemIdentificationConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        h_d = {}
        for k, v in d["hparams"].items():
            h_d[k] = HParam.from_dict(v)
        obj = SystemIdentificationConfig(hparams=h_d, model_type=d["model_type"], output_dir=d["output_dir"],
                                         title=d["title"], log_every=d["log_every"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
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

    @staticmethod
    def from_json_file(json_file_path: str) -> "SystemIdentificationConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SystemIdentificationConfig.from_dict(json.loads(json_str))
