from typing import List
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig


class IntrusionRecoveryPomdpConfig(SimulationEnvInputConfig):
    """
    DTO containing the configuration of an intrusion recovery POMDP
    """

    def __init__(self, eta: float, p_a: float, p_c_1: float, p_c_2: float, p_u: float, BTR: int, negate_costs: bool,
                 seed: int, discount_factor: float, states: List[int], actions: List[int], observations: List[int],
                 cost_tensor: List[List[float]], observation_tensor: List[List[float]],
                 transition_tensor: List[List[List[float]]], b1: List[float], T: int, simulation_env_name: str,
                 gym_env_name: str) -> None:
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
                f"gym_env_name: {self.gym_env_name}")
