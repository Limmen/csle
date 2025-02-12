from typing import Dict, Any
import gymnasium as gym
import numpy as np
import numpy.typing as npt
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig


class AptGameConfig(SimulationEnvInputConfig):
    """
    DTO class containing the configuration of the APT game
    """

    def __init__(self, env_name: str,
                 T: npt.NDArray[Any], O: npt.NDArray[np.int32], Z: npt.NDArray[Any],
                 C: npt.NDArray[Any], S: npt.NDArray[np.int32], A1: npt.NDArray[np.int32],
                 A2: npt.NDArray[np.int32], b1: npt.NDArray[np.float64], N: int, p_a: float,
                 save_dir: str, checkpoint_traces_freq: int, gamma: float = 1) -> None:
        """
        Initializes the DTO

        :param env_name: the name of the environment
        :param T: the transition tensor
        :param O: the observation space
        :param Z: the observation tensor
        :param C: the cost tensor
        :param S: the state space
        :param A1: the action space of the defender
        :param A2: the action space of the attacker
        :param N: the number of servers
        :param p_a: the attack success probability
        :param b1: the initial belief
        :param save_dir: the directory to save artefacts produced by the environment
        :param checkpoint_traces_freq: how frequently to checkpoint traces to disk
        :param gamma: the discount factor
        """
        super().__init__()
        self.T = T
        self.O = O
        self.Z = Z
        self.C = C
        self.S = S
        self.N = N
        self.p_a = p_a
        self.A1 = A1
        self.A2 = A2
        self.b1 = b1
        self.save_dir = save_dir
        self.env_name = env_name
        self.checkpoint_traces_freq = checkpoint_traces_freq
        self.gamma = gamma

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["T"] = list(self.T.tolist())
        d["O"] = list(self.O.tolist())
        d["Z"] = list(self.Z.tolist())
        d["R"] = list(self.C.tolist())
        d["S"] = list(self.S.tolist())
        d["A1"] = list(self.A1.tolist())
        d["A2"] = list(self.A2.tolist())
        d["b1"] = list(self.b1.tolist())
        d["N"] = self.N
        d["p_a"] = self.p_a
        d["save_dir"] = self.save_dir
        d["env_name"] = self.env_name
        d["checkpoint_traces_freq"] = self.checkpoint_traces_freq
        d["gamma"] = self.gamma
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AptGameConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = AptGameConfig(
            T=np.array(d["T"]), O=np.array(d["O"]), Z=np.array(d["Z"]), C=np.array(d["R"]), S=np.array(d["S"]),
            A1=np.array(d["A1"]), A2=np.array(d["A2"]), b1=np.array(d["b1"]), save_dir=d["save_dir"],
            env_name=d["env_name"], checkpoint_traces_freq=d["checkpoint_traces_freq"], gamma=d["gamma"],
            N=d["N"], p_a=d["p_a"]
        )
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"T:{self.T}, O:{self.O}, Z:{self.Z}, R:{self.C}, S:{self.S}, A1:{self.A1}, A2:{self.A2}, " \
               f"b1:{self.b1}, N: {self.N}, p_a: {self.p_a}, " \
               f"save_dir: {self.save_dir}, env_name: {self.env_name}," \
               f"checkpoint_traces_freq: {self.checkpoint_traces_freq}, gamma: {self.gamma}"

    def attacker_observation_space(self) -> gym.spaces.Box:
        """
        :return: the attacker's observation space
        """
        return gym.spaces.Box(low=np.array([np.float64(0), np.float64(0)]),
                              high=np.array([np.float64(1), np.float64(2)]),
                              dtype=np.float64, shape=(2,))

    def defender_observation_space(self) -> gym.spaces.Box:
        """
        :return: the defender's observation space
        """
        return gym.spaces.Box(low=np.array([np.float64(0)]),
                              high=np.array([np.float64(1)]),
                              dtype=np.float64, shape=(1,))

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

    @staticmethod
    def from_json_file(json_file_path: str) -> "AptGameConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return AptGameConfig.from_dict(json.loads(json_str))
