from typing import Dict, Any
import numpy as np
import gym


class IntrusionResponseGameConfig:

    def __init__(self, env_name: str, T: np.ndarray, O: np.ndarray, Z: np.ndarray, R: np.ndarray, S: np.ndarray,
                 A1: np.ndarray, A2: np.ndarray, d_b1: np.ndarray, a_b1: np.ndarray, gamma: float):
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

    def attacker_observation_space(self) -> gym.spaces.Discrete:
        """
        :return: the attacker's observation space
        """
        return gym.spaces.Discrete(len(self.O))

    def defender_observation_space(self) -> gym.spaces.Discrete:
        """
        :return: the defender's observation space
        """
        return gym.spaces.Discrete(len(self.O))

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

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["T"] = list(self.T.tolist())
        d["O"] = list(self.O.tolist())
        d["Z"] = list(self.Z.tolist())
        d["R"] = list(self.R.tolist())
        d["S"] = list(self.S.tolist())
        d["A1"] = list(self.A1.tolist())
        d["A2"] = list(self.A2.tolist())
        d["d_b1"] = list(self.d_b1.tolist())
        d["a_b1"] = list(self.a_b1.tolist())
        d["gamma"] = self.gamma
        d["env_name"] = self.env_name
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "IntrusionResponseGameConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = IntrusionResponseGameConfig(
            env_name=d["env_name"], T=np.array(d["T"]), O=np.array(d["O"]), Z=np.array(d["Z"]), R=np.array(d["R"]),
            S=np.array(d["S"]), A1=np.array(d["A1"]), A2=np.array(d["A2"]), a_b1=np.array(d["a_b1"]),
            d_b1=np.array(d["d_b1"]), gamma=d["gamma"])
        return obj