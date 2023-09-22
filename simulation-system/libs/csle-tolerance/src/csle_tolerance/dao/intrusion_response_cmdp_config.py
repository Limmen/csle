from typing import List, Dict, Any
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig


class IntrusionResponseCmdpConfig(SimulationEnvInputConfig):
    """
    Configuration of the intrusion response CMDP
    """

    def __init__(self, p_a: float, p_c: float, p_u: float, s_max: int, transition_tensor: List[List[List[float]]],
                 cost_tensor: List[float], negate_costs: bool, seed: int, states: List[int], actions: List[int],
                 initial_state: int, constraint_cost_tensor: List[float], f: int, epsilon_a: float,
                 simulation_env_name: str, gym_env_name: str, discount_factor: float):
        """
        Initializes the DTO

        :param p_a: the intrusion probability
        :param p_c: the crash probability
        :param p_u: the recovery probability
        :param s_max: the maximum node of nodes
        :param transition_tensor: the transition tensor
        :param cost_tensor: the cost tensor
        :param constraint_cost_tensor: the constraint cost tensor
        :param negate_costs: boolean flag indicating whether costs should be negated or not
        :param seed: the random seed
        :param states: the list of states
        :param actions: the list of actions
        :param initial_state: the initial state of the CMDP
        :param cost_tensor: the constraint cost tensor
        :param f: the tolerance threshold
        :param epsilon_a: the expected availability threshold
        :param simulation_env_name: name of the simulation environment
        :param gym_env_name: name of the gym environment
        :param discount_factor: discount factor
        """
        self.p_a = p_a
        self.p_c = p_c
        self.p_u = p_u
        self.s_max = s_max
        self.transition_tensor = transition_tensor
        self.cost_tensor = cost_tensor
        self.negate_costs = negate_costs
        self.seed = seed
        self.states = states
        self.actions = actions
        self.initial_state = initial_state
        self.constraint_cost_tensor = constraint_cost_tensor
        self.f = f
        self.epsilon_a = epsilon_a
        self.simulation_env_name = simulation_env_name
        self.gym_env_name = gym_env_name
        self.discount_factor = discount_factor

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return (f"p_a: {self.p_a}, p_c: {self.p_c}, p_u: {self.p_u}, s_max: {self.s_max}, "
                f"transition_tensor: {self.transition_tensor}, cost_tensor: {self.cost_tensor}, seed: {self.seed}, "
                f"negate_costs: {self.negate_costs}, states: {self.states}, actions: {self.actions}, "
                f"initial state: {self.initial_state}, constraint_cost_tensor: {self.constraint_cost_tensor}, "
                f"f: {self.f}, epsilon_a: {self.epsilon_a}, simulation_env_name: {self.simulation_env_name}, "
                f"gym_env_name: {self.gym_env_name}, discount_factor: {self.discount_factor}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "IntrusionResponseCmdpConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        dto = IntrusionResponseCmdpConfig(
            p_a=d["p_a"], p_c=d["p_c"], p_u=d["p_u"], s_max=d["s_max"], transition_tensor=d["transition_tensor"],
            cost_tensor=d["cost_tensor"], negate_costs=d["negate_costs"], seed=d["seed"], states=d["states"],
            actions=d["actions"], initial_state=d["initial_state"], constraint_cost_tensor=d["constraint_cost_tensor"],
            f=d["f"], epsilon_a=d["epsilon_a"], simulation_env_name=d["simulation_env_name"],
            gym_env_name=d["gym_env_name"], discount_factor=d["discount_factor"])
        return dto

    def to_dict(self) -> Dict[str, Any]:
        """
        Gets a dict representation of the object

        :return: A dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["p_a"] = self.p_a
        d["p_c"] = self.p_c
        d["p_u"] = self.p_u
        d["s_max"] = self.s_max
        d["transition_tensor"] = self.transition_tensor
        d["cost_tensor"] = self.cost_tensor
        d["negate_costs"] = self.negate_costs
        d["seed"] = self.seed
        d["states"] = self.states
        d["actions"] = self.actions
        d["initial_state"] = self.initial_state
        d["constraint_cost_tensor"] = self.constraint_cost_tensor
        d["f"] = self.f
        d["epsilon_a"] = self.epsilon_a
        d["simulation_env_name"] = self.simulation_env_name
        d["gym_env_name"] = self.gym_env_name
        d["discount_factor"] = self.discount_factor
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "IntrusionResponseCmdpConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return IntrusionResponseCmdpConfig.from_dict(json.loads(json_str))
