from typing import List, Dict, Any
import numpy as np
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig


class IntrusionRecoveryPomdpConfig(SimulationEnvInputConfig):
    """
    DTO containing the configuration of an intrusion recovery POMDP
    """

    def __init__(self, eta: float, p_a: float, p_c_1: float, p_c_2: float, p_u: float, BTR: int, negate_costs: bool,
                 seed: int, discount_factor: float, states: List[int], actions: List[int], observations: List[int],
                 cost_tensor: List[List[float]], observation_tensor: List[List[float]],
                 transition_tensor: List[List[List[float]]], b1: List[float], T: int, simulation_env_name: str,
                 gym_env_name: str, max_horizon: float = np.inf) -> None:
        """
        Initializes the DTO

        :param eta: the scaling factor for the cost function
        :param p_a: the intrusion probability
        :param p_c_1: the crash probability in the healthy state
        :param p_c_2: the crash probability in the compromised state
        :param p_u: the software upgrade probability
        :param BTR: the periodic recovery interval
        :param negate_costs: boolean flag indicating whether costs should be negated or not
        :param seed: the random seed
        :param discount_factor: the discount factor
        :param states: the list of states
        :param actions: the list of actions
        :param observations: the list of observations
        :param cost_tensor: the cost tensor
        :param observation_tensor: the observation tensor
        :param transition_tensor: the transition tensor
        :param b1: the initial belief
        :param T: the time horizon
        :param simulation_env_name: name of the simulation environment
        :param gym_env_name: name of the gym environment
        :param max_horizon: the maximum horizon to avoid infinie simulations
        """
        self.eta = eta
        self.p_a = p_a
        self.p_c_1 = p_c_1
        self.p_c_2 = p_c_2
        self.p_u = p_u
        self.BTR = BTR
        self.negate_costs = negate_costs
        self.seed = seed
        self.discount_factor = discount_factor
        self.states = states
        self.actions = actions
        self.observations = observations
        self.cost_tensor = cost_tensor
        self.observation_tensor = observation_tensor
        self.transition_tensor = transition_tensor
        self.b1 = b1
        self.T = T
        self.simulation_env_name = simulation_env_name
        self.gym_env_name = gym_env_name
        self.max_horizon = max_horizon

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return (f"eta: {self.eta}, p_a: {self.p_a}, p_c_1: {self.p_c_1}, p_c_2: {self.p_c_2}, p_u: {self.p_u}, "
                f"BTR: {self.BTR}, negate_costs: {self.negate_costs}, seed: {self.seed}, "
                f"discount_factor: {self.discount_factor}, states: {self.states}, actions: {self.actions}, "
                f"observations: {self.observation_tensor}, cost_tensor: {self.cost_tensor}, "
                f"observation_tensor: {self.observation_tensor}, transition_tensor: {self.transition_tensor}, "
                f"b1:{self.b1}, T: {self.T}, simulation_env_name: {self.simulation_env_name}, "
                f"gym_env_name: {self.gym_env_name}, max_horizon: {self.max_horizon}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "IntrusionRecoveryPomdpConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        dto = IntrusionRecoveryPomdpConfig(
            eta=d["eta"], p_a=d["p_a"], p_c_1=d["p_c_1"], p_c_2=d["p_c_2"], p_u=d["p_u"], BTR=d["BTR"],
            negate_costs=d["negate_costs"], seed=d["seed"], discount_factor=d["discount_factor"], states=d["states"],
            actions=d["actions"], observations=d["observations"], cost_tensor=d["cost_tensor"],
            observation_tensor=d["observation_tensor"], transition_tensor=d["transition_tensor"], b1=d["b1"],
            T=d["T"], simulation_env_name=d["simulation_env_name"], gym_env_name=d["gym_env_name"])
        return dto

    def to_dict(self) -> Dict[str, Any]:
        """
        Gets a dict representation of the object

        :return: A dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["eta"] = self.eta
        d["p_a"] = self.p_a
        d["p_c_1"] = self.p_c_1
        d["p_c_2"] = self.p_c_2
        d["p_u"] = self.p_u
        d["BTR"] = self.BTR
        d["negate_costs"] = self.negate_costs
        d["seed"] = self.seed
        d["discount_factor"] = self.discount_factor
        d["states"] = self.states
        d["actions"] = self.actions
        d["observations"] = self.observations
        d["cost_tensor"] = self.cost_tensor
        d["observation_tensor"] = self.observation_tensor
        d["transition_tensor"] = self.transition_tensor
        d["b1"] = self.b1
        d["T"] = self.T
        d["simulation_env_name"] = self.simulation_env_name
        d["gym_env_name"] = self.simulation_env_name
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "IntrusionRecoveryPomdpConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return IntrusionRecoveryPomdpConfig.from_dict(json.loads(json_str))
