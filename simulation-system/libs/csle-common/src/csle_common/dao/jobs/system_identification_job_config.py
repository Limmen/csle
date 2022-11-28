from typing import Dict, Any
from csle_common.dao.system_identification.system_model import SystemModel
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig


class SystemIdentificationJobConfig:
    """
    DTO representing a system identification job
    """

    def __init__(self, emulation_env_name: str, emulation_statistics_id: int,
                 progress_percentage: float, pid: int, log_file_path: str,
                 system_identification_config: SystemIdentificationConfig,
                 descr: str = "",
                 system_model: SystemModel = None):
        """
        Initializes the DTO

        :param emulation_env_name: the name of the emulation that the system identification concerns
        :param emulation_statistics_id: the id of the statistics data to train with
        :param progress_percentage: the progress percentage
        :param pid: the pid of the process
        :param log_file_path: path to the log file
        :param descr: a description of the job
        :param system_model: fitted system model
        :param system_identification_config: the config of the system identification algorithm
        """
        self.emulation_env_name = emulation_env_name
        self.emulation_statistics_id = emulation_statistics_id
        self.progress_percentage = progress_percentage
        self.pid = pid
        self.log_file_path = log_file_path
        self.descr = descr
        self.system_model = system_model
        self.system_identification_config = system_identification_config
        self.id = -1
        self.running = False

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["emulation_env_name"] = self.emulation_env_name
        d["pid"] = self.pid
        d["progress_percentage"] = self.progress_percentage
        d["emulation_statistics_id"] = self.emulation_statistics_id
        d["descr"] = self.descr
        d["log_file_path"] = self.log_file_path
        if self.system_model is None:
            d["system_model"] = None
        else:
            d["system_model"] = self.system_model.to_dict()
        d["system_identification_config"] = self.system_identification_config.to_dict()
        d["id"] = self.id
        d["running"] = self.running
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SystemIdentificationJobConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        system_model = None
        system_model = GaussianMixtureSystemModel.from_dict(d["system_model"])
        obj = SystemIdentificationJobConfig(
            emulation_env_name=d["emulation_env_name"], pid=d["pid"],
            progress_percentage=d["progress_percentage"], emulation_statistics_id=d["emulation_statistics_id"],
            descr=d["descr"], log_file_path=d["log_file_path"], system_model=system_model,
            system_identification_config=SystemIdentificationConfig.from_dict(d["system_identification_config"])
        )
        if "id" in d:
            obj.id = d["id"]
        if "running" in d:
            obj.running = d["running"]
        return obj

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
