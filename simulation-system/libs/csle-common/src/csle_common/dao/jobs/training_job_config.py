from typing import Dict, Any, List
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_base.json_serializable import JSONSerializable


class TrainingJobConfig(JSONSerializable):
    """
    DTO representing the configuration of a training job
    """

    def __init__(self, simulation_env_name: str, experiment_config: ExperimentConfig,
                 progress_percentage: float, pid: int, experiment_result: ExperimentResult,
                 emulation_env_name: str, simulation_traces: List[SimulationTrace],
                 num_cached_traces: int, log_file_path: str, descr: str, physical_host_ip: str) -> None:
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
        :param physical_host_ip: the IP of the physical host where the job is running
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
        self.physical_host_ip = physical_host_ip

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
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
        d["physical_host_ip"] = self.physical_host_ip
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
            num_cached_traces=d["num_cached_traces"], log_file_path=d["log_file_path"], descr=d["descr"],
            physical_host_ip=d["physical_host_ip"])
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
               f"num_cached_traces: {self.num_cached_traces}, log_file_path: {self.log_file_path}, " \
               f"descr: {self.descr}, physical_host_ip: {self.physical_host_ip}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "TrainingJobConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return TrainingJobConfig.from_dict(json.loads(json_str))
