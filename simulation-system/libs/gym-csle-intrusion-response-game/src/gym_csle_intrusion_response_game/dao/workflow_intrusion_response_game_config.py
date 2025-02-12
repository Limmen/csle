from typing import Dict, Any
import gymnasium as gym
import numpy as np
import numpy.typing as npt
from csle_base.json_serializable import JSONSerializable


class WorkflowIntrusionResponseGameConfig(JSONSerializable):
    """
    DTO representing the configuration of a workflow intrusion response game
    """

    def __init__(self, env_name: str, adjacency_matrix: npt.NDArray[Any],
                 nodes: npt.NDArray[np.int32], initial_zones: npt.NDArray[np.int32], X_max: int, beta: float,
                 gamma: float,
                 zones: npt.NDArray[np.int32], Z_D_P: npt.NDArray[Any], C_D: npt.NDArray[Any], A_P: npt.NDArray[Any],
                 Z_U: npt.NDArray[Any], eta: float, gw_reachable: npt.NDArray[np.int32]):
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
        return gym.spaces.Box(
            low=np.array([np.float64(0)] * ((len(self.zones) + 1) * len(self.nodes))),
            high=np.array([len(self.zones)] * ((1 + len(self.zones)) * len(self.nodes))),
            dtype=np.float64, shape=((1 + len(self.zones)) * len(self.nodes),))

    def defender_observation_space(self) -> gym.spaces.Box:
        """
        :return: the defender's observation space
        """
        return gym.spaces.Box(low=np.array([np.float64(0)] * (4 * len(self.nodes))),
                              high=np.array([np.float64(len(self.zones))] * (4 * len(self.nodes))),
                              dtype=np.float64, shape=(4 * len(self.nodes),))

    def attacker_action_space(self) -> gym.spaces.MultiDiscrete:
        """
        :return: the attacker's action space
        """
        return gym.spaces.MultiDiscrete(nvec=np.array([4] * len(self.nodes)), dtype=np.int64)

    def defender_action_space(self) -> gym.spaces.MultiDiscrete:
        """
        :return: the defender's action space
        """
        return gym.spaces.MultiDiscrete(nvec=np.array([1 + len(self.zones)] * len(self.nodes)), dtype=np.int64)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
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

    @staticmethod
    def from_json_file(json_file_path: str) -> "WorkflowIntrusionResponseGameConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return WorkflowIntrusionResponseGameConfig.from_dict(json.loads(json_str))
