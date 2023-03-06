from typing import Dict, Any
import gym
import numpy as np


class WorkflowIntrusionResponseGameConfig:
    """
    DTO representing the configuration of a workflow intrusion response game
    """

    def __init__(self, env_name: str, adjacency_matrix: np.ndarray,
                 nodes: np.ndarray, initial_zones: np.ndarray, X_max: int, beta: float, gamma: float,
                 zones: np.ndarray, Z_D_P: np.ndarray, C_D: np.ndarray, A_P: np.ndarray, Z_U: np.ndarray,
                 eta: float, gw_reachable: np.ndarray):
        """
        Initializes the DTO

        :param env_name: the name of the environment
        :param adjacency_matrix: the adjacency matrix defining the topology of the workflow
        :param nodes: the nodes in the workflow
        :param initial_zones: the initial zones of all nodes
        :param X_max: the maximum observation
        :param beta: the beta scaling parameter of the workflow
        :param gamma: the discount factor
        :param zones: the list of zones in the network
        :param Z_D_P: the zone detection probabilities
        :param C_D: the costs of defensive actions
        :param A_P: the probabilities that an attacker action is successful
        :param Z_U: the zone utilities
        :param gw_reachable: indicating which nodes are reachable from the public gateway
        """
        self.env_name = env_name
        self.nodes = nodes
        self.initial_zones = initial_zones
        self.X_max = X_max
        self.beta = beta
        self.gamma = gamma
        self.zones = zones
        self.Z_D_P = Z_D_P
        self.C_D = C_D
        self.A_P = A_P
        self.Z_U = Z_U
        self.adjacency_matrix = adjacency_matrix
        self.eta = eta
        self.gw_reachable = gw_reachable

    def attacker_observation_space(self) -> gym.spaces.Box:
        """
        :return: the attacker's observation space
        """
        pass

    def defender_observation_space(self) -> gym.spaces.Box:
        """
        :return: the defender's observation space
        """
        pass

    def attacker_action_space(self) -> gym.spaces.Discrete:
        """
        :return: the attacker's action space
        """
        pass

    def defender_action_space(self) -> gym.spaces.Discrete:
        """
        :return: the defender's action space
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["nodes"] = list(self.nodes.tolist())
        d["initial_zones"] = list(self.initial_zones.tolist())
        d["zones"] = list(self.zones.tolist())
        d["Z_D_P"] = list(self.Z_D_P.tolist())
        d["C_D"] = list(self.C_D.tolist())
        d["A_P"] = list(self.A_P.tolist())
        d["Z_U"] = list(self.Z_U.tolist())
        d["adjacency_matrix"] = list(self.adjacency_matrix.tolist())
        d["gw_reachable"] = list(self.gw_reachable.tolist())
        d["X_max"] = self.X_max
        d["beta"] = self.beta
        d["gamma"] = self.gamma
        d["env_name"] = self.env_name
        d["eta"] = self.eta
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "WorkflowIntrusionResponseGameConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = WorkflowIntrusionResponseGameConfig(
            env_name=d["env_name"], nodes=np.array(d["nodes"]), initial_zones=np.array(d["initial_zones"]),
            zones=np.array(d["zones"]), Z_D_P=np.array(d["Z_D_P"]), C_D=np.array(d["C_D"]),
            A_P=np.array(d["A_P"]), Z_U=np.array(d["Z_U"]), X_max=d["X_max"], beta=d["beta"], gamma=d["gamma"],
            adjacency_matrix=np.array(d["adjacency_matrix"]), eta=d["eta"], gw_reachable=np.array(d["gw_reachable"]))
        return obj