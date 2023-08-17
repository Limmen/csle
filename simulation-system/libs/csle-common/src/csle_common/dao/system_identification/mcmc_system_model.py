from typing import List, Dict, Any
from csle_common.dao.system_identification.mcmc_posterior import MCMCPosterior
from csle_common.dao.system_identification.system_model import SystemModel
from csle_common.dao.system_identification.system_model_type import SystemModelType


class MCMCSystemModel(SystemModel):
    """
    A system model (list of posterior distributions) made up of posterior distributions
    """

    def __init__(self, emulation_env_name: str, emulation_statistic_id: int,
                 posteriors: List[MCMCPosterior], descr: str):
        """
        Initializes the object

        :param emulation: the emulation that this system model is for
        :param emulation_statistic_id: the emulation statistic that this model was built from
        :param posteriors: the list of posteriors
        :param descr: description of the model
        """
        super(MCMCSystemModel, self).__init__(descr=descr, model_type=SystemModelType.MCMC)
        self.posteriors = posteriors
        self.emulation_env_name = emulation_env_name
        self.emulation_statistic_id = emulation_statistic_id
        self.id = -1

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "MCMCSystemModel":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        dto = MCMCSystemModel(
            posteriors=list(map(lambda y: MCMCPosterior.from_dict(y), d["posteriors"])),
            emulation_env_name=d["emulation_env_name"], emulation_statistic_id=d["emulation_statistic_id"],
            descr=d["descr"]
        )
        if "id" in d:
            dto.id = d["id"]
        return dto

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["posteriors"] = list(map(lambda y: y.to_dict(), self.posteriors))
        d["emulation_env_name"] = self.emulation_env_name
        d["emulation_statistic_id"] = self.emulation_statistic_id
        d["descr"] = self.descr
        d["id"] = self.id
        d["model_type"] = self.model_type
        return d

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"posteriors: {self.posteriors}, " \
               f"emulation_env_name: {self.emulation_env_name}, " \
               f"emulation_statistic_id: {self.emulation_statistic_id}," \
               f"descr: {self.descr}, model_type: {self.model_type}"

    def copy(self) -> "MCMCSystemModel":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())

    @staticmethod
    def from_json_file(json_file_path: str) -> "MCMCSystemModel":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return MCMCSystemModel.from_dict(json.loads(json_str))
