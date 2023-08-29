from typing import Optional, Dict, Any, Union
from csle_common.dao.system_identification.system_model import SystemModel
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
from csle_common.dao.system_identification.empirical_system_model import EmpiricalSystemModel
from csle_common.dao.system_identification.gp_system_model import GPSystemModel
from csle_common.dao.system_identification.mcmc_system_model import MCMCSystemModel
from csle_base.json_serializable import JSONSerializable


class SystemIdentificationJobConfig(JSONSerializable):
    """
    DTO representing a system identification job
    """

    def __init__(self, emulation_env_name: str, emulation_statistics_id: int,
                 progress_percentage: float, pid: int, log_file_path: str,
                 system_identification_config: SystemIdentificationConfig, physical_host_ip: str,
                 descr: str = "", system_model: Optional[SystemModel] = None):
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
        :param physical_host_ip: the IP of the physical host where the job is running
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
        self.physical_host_ip = physical_host_ip

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
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
        d["physical_host_ip"] = self.physical_host_ip
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SystemIdentificationJobConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        # system_model = None
        parse_models = [GaussianMixtureSystemModel.from_dict, EmpiricalSystemModel.from_dict,
                        GPSystemModel.from_dict, MCMCSystemModel.from_dict]
        system_model: Union[None, SystemModel] = None
        for parse_model in parse_models:
            try:
                system_model = parse_model(d['system_model'])
                break
            except Exception:
                pass
        obj = SystemIdentificationJobConfig(
            emulation_env_name=d["emulation_env_name"], pid=d["pid"],
            progress_percentage=d["progress_percentage"], emulation_statistics_id=d["emulation_statistics_id"],
            descr=d["descr"], log_file_path=d["log_file_path"], system_model=system_model,
            system_identification_config=SystemIdentificationConfig.from_dict(d["system_identification_config"]),
            physical_host_ip=d["physical_host_ip"]
        )
        if "id" in d:
            obj.id = d["id"]
        if "running" in d:
            obj.running = d["running"]
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "SystemIdentificationJobConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SystemIdentificationJobConfig.from_dict(json.loads(json_str))
