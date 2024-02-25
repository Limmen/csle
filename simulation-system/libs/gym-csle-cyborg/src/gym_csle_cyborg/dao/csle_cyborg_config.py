from typing import Dict, Any, List, Union, Tuple
import numpy as np
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig
import gym_csle_cyborg.constants.constants as env_constants
from gym_csle_cyborg.dao.red_agent_type import RedAgentType


class CSLECyborgConfig(SimulationEnvInputConfig):
    """
    DTO representing the input configuration to a gym-csle-cyborg environment
    """

    def __init__(self, gym_env_name: str, scenario: int, baseline_red_agents: List[RedAgentType], maximum_steps: int,
                 red_agent_distribution: List[float], reduced_action_space: bool,
                 scanned_state: bool, decoy_state: bool, decoy_optimization: bool,
                 cache_visited_states: bool = False, save_trace: bool = False, randomize_topology: bool = False) \
            -> None:
        """
        Initializes the DTO

        :param gym_env_name: the name of the environment
        :param baseline_red_agents: the name of the baseline red agent
        :param maximum_steps: the maximum number of steps in the environment (i.e., the horizon)
        :param scenario: the Cage scenario number
        :param red_agent_distribution: probability distribution of red agents
        :param reduced_action_space: boolean flag indicating whether a reduced action space should be used
        :param scanned_state: boolean flag indicating whether the scanned defender state should be used
        :param decoy_state: boolean flag indicating whether the decoy defender state should be used
        :param decoy_optimization: boolean flag indicating whether the special decoy optimization should be used
        :param cache_visited_states: boolean flag indicating whether visited states should be cached
        :param save_trace: boolean flag indicating whether traces should be saved
        :param randomize_topology: boolean flag indicating whether the topology should be randomized
        """
        self.gym_env_name = gym_env_name
        self.scenario = scenario
        self.baseline_red_agents = baseline_red_agents
        self.maximum_steps = maximum_steps
        self.red_agent_distribution = red_agent_distribution
        self.reduced_action_space = reduced_action_space
        self.scanned_state = scanned_state
        self.decoy_state = decoy_state
        self.decoy_optimization = decoy_optimization
        self.cache_visited_states = cache_visited_states
        self.save_trace = save_trace
        self.randomize_topology = randomize_topology

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["baseline_red_agents"] = self.baseline_red_agents
        d["gym_env_name"] = self.gym_env_name
        d["scenario"] = self.scenario
        d["maximum_steps"] = self.maximum_steps
        d["red_agent_distribution"] = self.red_agent_distribution
        d["reduced_action_space"] = self.reduced_action_space
        d["scanned_state"] = self.scanned_state
        d["decoy_state"] = self.decoy_state
        d["decoy_optimization"] = self.decoy_optimization
        d["cache_visited_states"] = self.cache_visited_states
        d["save_trace"] = self.save_trace
        d["randomize_topology"] = self.randomize_topology
        return d

    def get_agents_dict(self, agent: Union[RedAgentType, None] = None) -> Tuple[Dict[str, Any], RedAgentType]:
        """
        Gets the agents dict to pass into the cage environment

        :param agent: the agent to use, if None, sample agent randomly
        :return: the agents dict for the cage environment
        """
        if agent is None:
            agent_idx = int(
                np.random.choice(np.arange(0, len(self.red_agent_distribution)), p=self.red_agent_distribution))
            agent = self.baseline_red_agents[agent_idx]
        agents_dict = {}
        if agent == RedAgentType.B_LINE_AGENT:
            from csle_cyborg.agents.simple_agents.b_line import B_lineAgent
            agents_dict[env_constants.CYBORG.RED] = B_lineAgent
        elif agent == RedAgentType.MEANDER_AGENT:
            from csle_cyborg.agents.simple_agents.meander import RedMeanderAgent
            agents_dict[env_constants.CYBORG.RED] = RedMeanderAgent
        elif agent == RedAgentType.SLEEP_AGENT:
            from csle_cyborg.agents.simple_agents.sleep_agent import Sleep
            agents_dict[env_constants.CYBORG.RED] = Sleep
        else:
            raise ValueError(f"Red agent type: {agent} not recognized")
        return agents_dict, agent

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CSLECyborgConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        save_trace = False
        if "save_trace" in d:
            save_trace = d["save_trace"]
        obj = CSLECyborgConfig(gym_env_name=d["gym_env_name"], scenario=d["scenario"],
                               baseline_red_agents=d["baseline_red_agents"], maximum_steps=d["maximum_steps"],
                               red_agent_distribution=d["red_agent_distribution"],
                               reduced_action_space=d["reduced_action_space"],
                               scanned_state=d["scanned_state"], decoy_state=d["decoy_state"],
                               decoy_optimization=d["decoy_optimization"],
                               cache_visited_states=d["cache_visited_states"], save_trace=save_trace)
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"gym_env_name: {self.gym_env_name}, scenario: {self.scenario}, " \
               f"baseline_red_agents: {self.baseline_red_agents}, maximum_steps: {self.maximum_steps}, " \
               f"red_agent_distribution: {self.red_agent_distribution}, " \
               f"reduced_action_space: {self.reduced_action_space}, scanned_state: {self.scanned_state}, " \
               f"decoy_state: {self.decoy_state}, decoy_optimization: {self.decoy_optimization}, " \
               f"cache_visited_states: {self.cache_visited_states}, save_trace: {self.save_trace}, " \
               f"randomize_topology: {self.randomize_topology}"

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
