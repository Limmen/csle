from typing import Dict, Any
from csle_common.dao.training.experiment_config import ExperimentConfig


class TrainingJobConfig:
    """
    DTO representing the configuration of a training job
    """

    def __init__(self, simulation_env_name: str, experiment_config: ExperimentConfig, average_r: float,
                 progress_percentage: float, pid: int):
        """
        Initializes the DTO

        :param simulation_env_name: the simulation environment name
        :param experiment_config:
        :param average_r:
        :param progress_percentage:
        """
        self.simulation_env_name = simulation_env_name
        self.experiment_config = experiment_config
        self.average_r = average_r
        self.progress_percentage = progress_percentage
        self.pid = pid
        self.id = -1

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["simulation_env_name"] = self.simulation_env_name
        d["experiment_config"] = self.experiment_config.to_dict()
        d["average_r"] = self.average_r
        d["progress_percentage"] = self.progress_percentage
        d["pid"] = self.pid
        d["id"] = self.id
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
            experiment_config=ExperimentConfig.from_dict(d["experiment_config"]), average_r=d["average_r"],
            progress_percentage=d["progress_percentage"], pid=d["pid"]
        )
        obj.id = d["id"]
        return obj

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"simulation_env_name: {self.simulation_env_name}, experiment_config: {self.experiment_config}, " \
               f"average_r: {self.average_r}, progress_percentage: {self.progress_percentage}, pid: {self.pid}," \
               f"id: {self.id}"