from typing import Dict, Any
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_base.json_serializable import JSONSerializable


class ExperimentExecution(JSONSerializable):
    """
    DTO representing an experiment execution
    """

    def __init__(self, config: ExperimentConfig, result: ExperimentResult, timestamp: float, emulation_name: str,
                 simulation_name: str, descr: str, log_file_path: str):
        """
        Initializes the DTO

        :param config: the experiment configuration
        :param result: the experiment result
        :param timestamp: the timestamp
        :param emulation_name: the emulation name
        :param simulation_name: the simulation name
        :param descr: a description of the training run
        """
        self.config = config
        self.result = result
        self.timestamp = timestamp
        self.emulation_name = emulation_name
        self.simulation_name = simulation_name
        self.id = -1
        self.descr = descr
        self.log_file_path = log_file_path

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
            timestamp=d["timestamp"], simulation_name=d["simulation_name"], emulation_name=d["emulation_name"],
            descr=d["descr"], log_file_path=d["log_file_path"]
        )
        obj.id = d["id"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["config"] = self.config.to_dict()
        d["result"] = self.result.to_dict()
        d["timestamp"] = self.timestamp
        d["simulation_name"] = self.simulation_name
        d["emulation_name"] = self.emulation_name
        d["id"] = self.id
        d["descr"] = self.descr
        d["log_file_path"] = self.log_file_path
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"config: {self.config}, result: {self.result}, timestamp: {self.timestamp}, " \
               f"simulation_name: {self.simulation_name}, emulation_name: {self.emulation_name}, id: {self.id}," \
               f"descr: {self.descr}, log_file_path: {self.log_file_path}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "ExperimentExecution":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ExperimentExecution.from_dict(json.loads(json_str))
