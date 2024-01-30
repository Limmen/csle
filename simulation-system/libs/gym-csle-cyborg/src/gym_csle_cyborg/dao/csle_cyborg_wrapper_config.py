from typing import Dict, Any
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig


class CSLECyborgWrapperConfig(SimulationEnvInputConfig):
    """
    DTO representing the input configuration to a gym-csle-cyborg environment
    """

    def __init__(self, maximum_steps: int, gym_env_name: str, save_trace: bool = False, reward_shaping: bool = False):
        """
        Initializes the DTO

        :param maximum_steps: the maximum number of steps in the environment
        :param gym_env_name: the name of the gym environment
        :param save_trace: boolean flag indicating whether traces should be saved
        :param reward_shaping: boolean flag indicating whether reward shaping should be used
        """
        self.maximum_steps = maximum_steps
        self.gym_env_name = gym_env_name
        self.save_trace = save_trace
        self.reward_shaping = reward_shaping

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["baseline_red_agents"] = self.maximum_steps
        d["gym_env_name"] = self.gym_env_name
        d["save_trace"] = self.save_trace
        d["reward_shaping"] = self.reward_shaping
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CSLECyborgWrapperConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = CSLECyborgWrapperConfig(gym_env_name=d["gym_env_name"], maximum_steps=d["maximum_steps"],
                                      save_trace=d["save_trace"], reward_shaping=d["reward_shaping"])
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"gym_env_name: {self.gym_env_name}, maximum_steps: {self.maximum_steps}, "
                f"save_trace: {self.save_trace}, reward_shaping: {self.reward_shaping}")

    @staticmethod
    def from_json_file(json_file_path: str) -> "CSLECyborgWrapperConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return CSLECyborgWrapperConfig.from_dict(json.loads(json_str))
