from typing import Dict, Any
import gym
import numpy as np
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig


class StoppingGameConfig(SimulationEnvInputConfig):
    """
    DTO class containing the configuration of the stopping game
    """

    def __init__(self, env_name: str,
                 T: np.ndarray, O: np.ndarray, Z: np.ndarray, R: np.ndarray, S: np.ndarray, A1: np.ndarray,
                 A2: np.ndarray, L: int, R_INT: int, R_COST: int, R_SLA: int, R_ST: int, b1: np.ndarray,
                 save_dir: str, checkpoint_traces_freq: int, gamma: float = 1) -> None:
        """
        Initializes the DTO

        :param env_name: the name of the environment
        :param T: the transition tensor
        :param O: the observation space
        :param Z: the observation tensor
        :param R: the reward function
        :param S: the state space
        :param A1: the action space of the defender
        :param A2: the action space of the attacker
        :param L: the maximum number of stops of the defender
        :param R_INT: the R_INT constant for the reward function
        :param R_COST: the R_COST constant for the reward function
        :param R_SLA: the R_SLA constant for the reward function
        :param R_ST: the R_ST constant for the reward function
        :param b1: the initial belief
        :param save_dir: the directory to save artefacts produced by the environment
        :param checkpoint_traces_freq: how frequently to checkpoint traces to disk
        :param gamma: the discount factor
        """
        super().__init__()
        self.T = T
        self.O = O
        self.Z = Z
        self.R = R
        self.S = S
        self.L = L
        self.R_INT = R_INT
        self.R_COST = R_COST
        self.R_SLA = R_SLA
        self.R_ST = R_ST
        self.A1 = A1
        self.A2 = A2
        self.b1 = b1
        self.save_dir = save_dir
        self.env_name = env_name
        self.checkpoint_traces_freq = checkpoint_traces_freq
        self.gamma = gamma

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
        d["L"] = self.L
        d["R_INT"] = self.R_INT
        d["R_COST"] = self.R_COST
        d["R_SLA"] = self.R_SLA
        d["R_ST"] = self.R_ST
        d["A1"] = list(self.A1.tolist())
        d["A2"] = list(self.A2.tolist())
        d["b1"] = list(self.b1.tolist())
        d["save_dir"] = self.save_dir
        d["env_name"] = self.env_name
        d["checkpoint_traces_freq"] = self.checkpoint_traces_freq
        d["gamma"] = self.gamma
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StoppingGameConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = StoppingGameConfig(
            T=np.array(d["T"]), O=np.array(d["O"]), Z=np.array(d["Z"]), R=np.array(d["R"]), S=np.array(d["S"]),
            A1=np.array(d["A1"]), A2=np.array(d["A2"]), L=d["L"], R_INT=d["R_INT"],
            R_COST=d["R_COST"], R_SLA=d["R_SLA"], R_ST=d["R_ST"], b1=np.array(d["b1"]), save_dir=d["save_dir"],
            env_name=d["env_name"], checkpoint_traces_freq=d["checkpoint_traces_freq"], gamma=d["gamma"]
        )
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"T:{self.T}, O:{self.O}, Z:{self.Z}, R:{self.R}, S:{self.S}, A1:{self.A1}, A2:{self.A2}, L:{self.L}, " \
               f"R_INT:{self.R_INT}, R_COST:{self.R_COST}, R_SLA:{self.R_SLA}, R_ST:{self.R_ST}, b1:{self.b1}, " \
               f"save_dir: {self.save_dir}, env_name: {self.env_name}, " \
               f"checkpoint_traces_freq: {self.checkpoint_traces_freq}, gamma: {self.gamma}"

    def attacker_observation_space(self) -> gym.spaces.Box:
        """
        :return: the attacker's observation space
        """
        return gym.spaces.Box(low=np.array([0, 0, 0]), high=np.array([self.L, 1, 2]), dtype=np.float32, shape=(3, ))

    def defender_observation_space(self) -> gym.spaces.Box:
        """
        :return: the defender's observation space
        """
        return gym.spaces.Box(low=np.array([0, 0]), high=np.array([self.L, 1]), dtype=np.float32, shape=(2, ))

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
