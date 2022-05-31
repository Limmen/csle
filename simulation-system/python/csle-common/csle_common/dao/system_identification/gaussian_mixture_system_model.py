from typing import List, Dict, Any
from csle_common.dao.system_identification.gaussian_mixture_conditional import GaussianMixtureConditional
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.system_identification.system_model import SystemModel


class GaussianMixtureSystemModel(SystemModel):
    """
    A system model (list of conditional distributions) made up of Gaussian Mixtures
    """

    def __init__(self, emulation_env_name: str, emulation_statistic_id: int,
                 conditional_metric_distributions: List[List[GaussianMixtureConditional]]):
        """
        Initializes the object

        :param emulation: the emulation that this system model is for
        :param emulation_statistic_id: the emulation statistic that this model was built from
        :param conditional_metric_distributions: the list of conditional distributions
        """
        super(SystemModel, self).__init__()
        self.conditional_metric_distributions = conditional_metric_distributions
        self.emulation_env_name = emulation_env_name
        self.emulation_statistic_id = emulation_statistic_id


    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "GaussianMixtureSystemModel":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        return GaussianMixtureSystemModel(
            conditional_metric_distributions=list(map(
                lambda x: list(map(lambda y: GaussianMixtureConditional.from_dict(y), x)),
                d["conditional_metric_distributions"])),
            emulation_env_name=d["emulation_env_name"], emulation_statistic_id=d["emulation_statistic_id"]
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d = {}
        d["conditional_metric_distributions"] = list(map(lambda x: list(map(lambda y: y.to_dict(), x)),
                                                  self.conditional_metric_distributions))
        d["emulation_env_name"] = self.emulation_env_name
        d["emulation_statistic_id"] = self.emulation_statistic_id
        return d

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"conditional_distributions: {self.conditional_metric_distributions}, " \
               f"emulation_env_name: {self.emulation_env_name}, emulation_statistic_id: {self.emulation_statistic_id}"

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