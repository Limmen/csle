from typing import List, Dict, Any
from csle_base.json_serializable import JSONSerializable


class MCMCPosterior(JSONSerializable):
    """
    A DTO representing a posterior obtained through MCMC
    """

    def __init__(self, posterior_name: str, samples: List[float], densities: List[float],
                 sample_space: List[float]) -> None:
        """
        Initializes the DTO

        :param posterior_name: the name of the posterior
        :param samples: samples from the posterior
        :param densities: densities from the posterior
        :param sample_space: the set of unique values (sample space)
        """
        self.posterior_name = posterior_name
        self.samples = samples
        self.densities = densities
        self.sample_space = sample_space

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "MCMCPosterior":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        return MCMCPosterior(posterior_name=d["posterior_name"], samples=d["samples"], densities=d["densities"],
                             sample_space=d["sample_space"])

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["posterior_name"] = self.posterior_name
        d["samples"] = self.samples
        d["densities"] = self.densities
        d["sample_space"] = self.sample_space
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"posterior_name:{self.posterior_name}, samples: {self.samples}, densities: {self.densities}, " \
               f"sample_space: {self.sample_space}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "MCMCPosterior":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return MCMCPosterior.from_dict(json.loads(json_str))
