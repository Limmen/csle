from typing import Dict, Any
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig
import gym_csle_cyborg.constants.constants as env_constants
from gym_csle_cyborg.dao.red_agent_type import RedAgentType


class CSLECyborgConfig(SimulationEnvInputConfig):
    """
    DTO representing the input configuration to a gym-csle-cyborg environment
    """

    def __init__(self, gym_env_name: str, scenario: int, baseline_red_agent: RedAgentType, maximum_steps: int) -> None:
        """
        Initializes the DTO

        :param gym_env_name: the name of the environment
        :param baseline_red_agent: the name of the baseline red agent
        :param maximum_steps: the maximum number of steps in the environment (i.e., the horizon)
        :param scenario: the Cage scenario number
        """
        self.gym_env_name = gym_env_name
        self.scenario = scenario
        self.baseline_red_agent = baseline_red_agent
        self.maximum_steps = maximum_steps

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["baseline_red_agent"] = self.baseline_red_agent
        d["gym_env_name"] = self.gym_env_name
        d["scenario"] = self.scenario
        d["maximum_steps"] = self.maximum_steps
        return d

    def get_agents_dict(self) -> Dict[str, Any]:
        """
        Gets the agents dict to pass into the cage environment

        :return: the agents dict for the cage environment
        """
        agents_dict = {}
        if self.baseline_red_agent == RedAgentType.B_LINE_AGENT:
            from csle_cyborg.agents.simple_agents.b_line import B_lineAgent
            agents_dict[env_constants.CYBORG.RED] = B_lineAgent
        elif self.baseline_red_agent == RedAgentType.MEANDER_AGENT:
            from csle_cyborg.agents.simple_agents.meander import RedMeanderAgent
            agents_dict[env_constants.CYBORG.RED] = RedMeanderAgent
        elif self.baseline_red_agent == RedAgentType.SLEEP_AGENT:
            from csle_cyborg.agents.simple_agents.sleep_agent import Sleep
            agents_dict[env_constants.CYBORG.RED] = Sleep
        else:
            raise ValueError(f"Red agent type: {self.baseline_red_agent} not recognized")
        return agents_dict

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CSLECyborgConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = CSLECyborgConfig(gym_env_name=d["gym_env_name"], scenario=d["scenario"],
                               baseline_red_agent=d["baseline_red_agent"], maximum_steps=d["maximum_steps"])
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"gym_env_name: {self.gym_env_name}, scenario: {self.scenario}, " \
               f"baseline_red_agent: {self.baseline_red_agent}, maximum_steps: {self.maximum_steps}"

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
