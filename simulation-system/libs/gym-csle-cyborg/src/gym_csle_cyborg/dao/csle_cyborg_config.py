from typing import Dict, Any
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig


class CSLECyborgConfig(SimulationEnvInputConfig):
    """
    DTO representing the input configuration to a gym-csle-cyborg environment
    """

    def __init__(self, env_name: str, scenario: int) -> None:
        """
        Initializes the DTO

        :param env_name: the name of the environment
        :param scenario: the Cage scenario number
        """
        self.env_name = env_name
        self.scenario = scenario

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["env_name"] = self.env_name
        d["scenario"] = self.scenario
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CSLECyborgConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = CSLECyborgConfig(env_name=d["env_name"], scenario=d["scenario"])
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"env_name: {self.env_name}, scenario: {self.scenario}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "CSLECyborgConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return CSLECyborgConfig.from_dict(json.loads(json_str))
