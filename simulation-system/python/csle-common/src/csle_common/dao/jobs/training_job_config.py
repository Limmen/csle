from typing import Dict, Any, List, Union
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace


class TrainingJobConfig:
    """
    DTO representing the configuration of a training job
    """

    def __init__(self, simulation_env_name: str, experiment_config: ExperimentConfig,
                 progress_percentage: float, pid: int, experiment_result: ExperimentResult,
                 emulation_env_name: Union[str, None], simulation_traces: List[SimulationTrace],
                 num_cached_traces: int, log_file_path: str, descr: str) -> None:
        """
        Initializes the DTO

        :param simulation_env_name: the simulation environment name
        :param simulation_env_name: the emulation environment name
        :param experiment_config: the experiment configuration
        :param progress_percentage:the progress of the job in percentage
        :param pid: the pid of the process
        :param experiment_result: the result of the job
        :param emulation_env_config: the configuration of the emulation environment
        :param simulation_env_config: the configuration of the simulation environment
        :param simulation_traces: the list of simulation traces
        :param num_cached_traces: number of cached simulation traces
        :param descr: description of the job
        """
        self.simulation_env_name = simulation_env_name
        self.emulation_env_name = emulation_env_name
        self.experiment_config = experiment_config
        self.experiment_result = experiment_result
        self.progress_percentage = round(progress_percentage, 3)
        self.pid = pid
        self.id = -1
        self.running = False
        self.simulation_traces = simulation_traces
        self.num_cached_traces = num_cached_traces
        self.log_file_path = log_file_path
        self.descr = descr

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["simulation_env_name"] = self.simulation_env_name
        d["emulation_env_name"] = self.emulation_env_name
        d["experiment_config"] = self.experiment_config.to_dict()
        d["progress_percentage"] = round(self.progress_percentage, 2)
        d["pid"] = self.pid
        d["id"] = self.id
        d["experiment_result"] = self.experiment_result.to_dict()
        d["running"] = self.running
        d["simulation_traces"] = list(map(lambda x: x.to_dict(), self.simulation_traces))
        d["num_cached_traces"] = self.num_cached_traces
        d["log_file_path"] = self.log_file_path
        d["descr"] = self.descr
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TrainingJobConfig":
        """
        Converts a dict representation of the object to an instance
        :param d: the dict to convert
        :return: the created instance
        """
        obj = TrainingJobConfig(
            simulation_env_name=d["simulation_env_name"],
            experiment_config=ExperimentConfig.from_dict(d["experiment_config"]),
            progress_percentage=d["progress_percentage"], pid=d["pid"],
            experiment_result=ExperimentResult.from_dict(d["experiment_result"]),
            emulation_env_name=d["emulation_env_name"],
            simulation_traces=list(map(lambda x: SimulationTrace.from_dict(x), d["simulation_traces"])),
            num_cached_traces=d["num_cached_traces"], log_file_path=d["log_file_path"], descr=d["descr"])
        obj.id = d["id"]
        obj.running = d["running"]
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"simulation_env_name: {self.simulation_env_name}, experiment_config: {self.experiment_config}, " \
               f"progress_percentage: {self.progress_percentage}, pid: {self.pid}," \
               f"id: {self.id}, experiment_result: {self.experiment_result}, running: {self.running}, " \
               f"emulation_env_name: {self.emulation_env_name}, " \
               f"simulation_traces: {list(map(lambda x: str(x), self.simulation_traces))}," \
               f"num_cached_traces: {self.num_cached_traces}, log_file_path: {self.log_file_path}, descr: {self.descr}"

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
