from typing import Dict, Any
import numpy as np
import numpy.typing as npt
import gymnasium as gym
import gym_csle_intrusion_response_game.constants.constants as env_constants
from csle_base.json_serializable import JSONSerializable


class LocalIntrusionResponseGameConfig(JSONSerializable):
    """
    DTO representing the configuration of the local intrusion response game
    """

    def __init__(self, env_name: str, T: npt.NDArray[Any], O: npt.NDArray[np.int32], Z: npt.NDArray[Any],
                 R: npt.NDArray[Any], S: npt.NDArray[np.int32], S_A: npt.NDArray[np.int32],
                 S_D: npt.NDArray[np.int32], s_1_idx: int, zones: npt.NDArray[np.int32],
                 A1: npt.NDArray[np.int32], A2: npt.NDArray[np.int32], d_b1: npt.NDArray[np.float64],
                 a_b1: npt.NDArray[np.float64], gamma: float,
                 beta: float, C_D: npt.NDArray[Any], eta: float, A_P: npt.NDArray[Any],
                 Z_D_P: npt.NDArray[Any], Z_U: npt.NDArray[Any]) -> None:
        """
        Initializes the DTO

        :param env_name: the name of the game
        :param T: the local transition tensor
        :param O: the local observation space
        :param Z: the local observation tensor
        :param R: the local reward tensor
        :param S: the local state space
        :param S_A: the local state space of the attacker
        :param S_D: the local state space of the defender
        :param A1: the local action space of the defender
        :param A2: the local action space of the attacker
        :param zones: the vector of zones in the network
        :param d_b1: the local initial belief state of the defender
        :param a_b1: the local initial belief state of the attacker
        :param s_1_idx: the local initial state index
        :param gamma: the discount factor
        :param beta: the workflow utility scaling factor
        :param C_D: the vector with the costs of the defender actions
        :param eta: the scaling parameter for the local utility function
        :param A_P: the the attack success probabilities
        :param Z_D_P: the zone detection probabilities
        :param Z_U: the vector with zone utilities
        """
        self.env_name = env_name
        self.T = T
        self.O = O
        self.Z = Z
        self.R = R
        self.S = S
        self.A1 = A1
        self.A2 = A2
        self.d_b1 = d_b1
        self.a_b1 = a_b1
        self.gamma = gamma
        self.beta = beta
        self.C_D = C_D
        self.eta = eta
        self.A_P = A_P
        self.Z_D_P = Z_D_P
        self.Z_U = Z_U
        self.S_A = S_A
        self.S_D = S_D
        self.s_1_idx = s_1_idx
        self.zones = zones
        self.states_to_idx = {}
        for i, s in enumerate(self.S):
            self.states_to_idx[(s[env_constants.STATES.D_STATE_INDEX], s[env_constants.STATES.A_STATE_INDEX])] = i

    def attacker_observation_space(self) -> gym.spaces.Box:
        """
        :return: the attacker's observation space
        """
        return gym.spaces.Box(low=np.array([np.float64(0)] * (len(self.S_D) + 1)),
                              high=np.array([np.float64(len(self.S_A))] + [np.float64(1)] * len(self.S_D)),
                              dtype=np.float64, shape=(len(self.S_D) + 1,))

    def defender_observation_space(self) -> gym.spaces.Box:
        """
        :return: the defender's observation space
        """
        return gym.spaces.Box(low=np.array(([np.float64(0)] * (len(self.S_A) + 1))),
                              high=np.array([np.float64(len(self.zones))] + [np.float64(1)] * len(self.S_A)),
                              dtype=np.float64, shape=(len(self.S_A) + 1,))

    def defender_observation_space_stopping(self) -> gym.spaces.Box:
        """
        :return: the defender's observation space
        """
        return gym.spaces.Box(low=np.array(([np.float64(0)] * (len(self.S_A)))),
                              high=np.array([np.float64(1)] * len(self.S_A)),
                              dtype=np.float64, shape=(len(self.S_A),))

    def attacker_action_space(self) -> gym.spaces.Discrete:
        """
        :return: the attacker's action space
        """
        return gym.spaces.Discrete(len(self.A2))

    def defender_action_space(self) -> gym.spaces.Discrete:
        """
        :return: the defender's action space
        """
        return gym.spaces.Discrete(len(self.A1))

    def defender_action_space_stopping(self) -> gym.spaces.Discrete:
        """
        :return: the defender's action space in the stopping POMDP
        """
        return gym.spaces.Discrete(2)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["T"] = list(self.T.tolist())
        d["O"] = list(self.O.tolist())
        d["Z"] = list(self.Z.tolist())
        d["R"] = list(self.R.tolist())
        d["S"] = list(self.S.tolist())
        d["A1"] = list(self.A1.tolist())
        d["A2"] = list(self.A2.tolist())
        d["d_b1"] = list(self.d_b1.tolist())
        d["a_b1"] = list(self.a_b1.tolist())
        d["C_D"] = list(self.C_D.tolist())
        d["A_P"] = list(self.A_P.tolist())
        d["Z_D_P"] = list(self.Z_D_P.tolist())
        d["Z_U"] = list(self.Z_U.tolist())
        d["S_A"] = list(self.S_A.tolist())
        d["S_D"] = list(self.S_D.tolist())
        d["zones"] = list(self.zones.tolist())
        d["gamma"] = self.gamma
        d["env_name"] = self.env_name
        d["beta"] = self.beta
        d["eta"] = self.eta
        d["s_1_idx"] = self.s_1_idx
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LocalIntrusionResponseGameConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = LocalIntrusionResponseGameConfig(
            env_name=d["env_name"], T=np.array(d["T"]), O=np.array(d["O"]), Z=np.array(d["Z"]), R=np.array(d["R"]),
            S=np.array(d["S"]), A1=np.array(d["A1"]), A2=np.array(d["A2"]), a_b1=np.array(d["a_b1"]),
            d_b1=np.array(d["d_b1"]), gamma=d["gamma"], eta=d["eta"], beta=d["beta"], Z_U=np.array(d["Z_U"]),
            Z_D_P=np.array(d["Z_D_P"]), A_P=np.array(d["A_P"]), C_D=np.array(d["C_D"]), S_D=np.array(d["S_D"]),
            S_A=np.array(d["S_A"]), s_1_idx=d["s_1_idx"], zones=np.array(d["zones"]))
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "LocalIntrusionResponseGameConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return LocalIntrusionResponseGameConfig.from_dict(json.loads(json_str))
