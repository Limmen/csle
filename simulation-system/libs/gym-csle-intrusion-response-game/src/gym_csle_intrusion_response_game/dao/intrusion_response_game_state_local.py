from typing import Dict, Any
import numpy as np
import numpy.typing as npt
import gym_csle_intrusion_response_game.constants.constants as env_constants
from csle_base.json_serializable import JSONSerializable


class IntrusionResponseGameStateLocal(JSONSerializable):
    """
    Represents the state of the intrusion response game (A PO-POSG, i.e a partially observed stochastic game
    with public observations)
    """

    def __init__(self, d_b1: npt.NDArray[np.float64], a_b1: npt.NDArray[np.float64], s_1_idx: int,
                 S: npt.NDArray[Any], S_A: npt.NDArray[Any], S_D: npt.NDArray[Any]) -> None:
        """
        Initializes the DTO
        :param d_b1: the initial belief of the defender
        :param a_b1: the initial belief of the attakcer
        :param s_1_idx: the initial state of the game
        :param S: the local state space
        :param S_A: the local attacker state space
        :param S_D: the local defender state space
        """
        self.d_b1 = d_b1
        self.a_b1 = a_b1
        self.s_1_idx = s_1_idx
        self.s_idx = s_1_idx
        self.S = S
        self.S_A = S_A
        self.S_D = S_D
        self.d_b = self.d_b1.copy()
        self.a_b = self.a_b1.copy()
        self.t = 1

    def reset(self) -> None:
        """
        Resets the state

        :return: None
        """
        self.t = 1
        self.s_idx = self.s_1_idx
        self.d_b = self.d_b1.copy()
        self.a_b = self.a_b1.copy()

    def attacker_observation(self) -> npt.NDArray[Any]:
        """
        :return: the attacker's observation
        """
        return np.array([self.attacker_state()] + list(self.a_b.tolist()))

    def defender_observation(self) -> npt.NDArray[Any]:
        """
        :return: the defender's observation
        """
        return np.array([self.defender_state()] + list(self.d_b.tolist()))

    def state_vector(self) -> Any:
        """
        :return: the state vector
        """
        return self.S[self.s_idx]

    def attacker_state(self) -> int:
        """
        :return: the attacker state
        """
        return int(self.S[self.s_idx][env_constants.STATES.A_STATE_INDEX])

    def defender_state(self) -> int:
        """
        :return: the defender state
        """
        return int(self.S[self.s_idx][env_constants.STATES.D_STATE_INDEX])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"d_b1: {self.d_b1}, a_b1: {self.a_b1}, s_1_idx:{self.s_1_idx}, S:{self.S}, S_A:{self.S_A}, " \
               f"S_D: {self.S_D}, t: {self.t}, s_idx: {self.s_idx}, s: {self.state_vector()}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["d_b1"] = list(self.d_b1)
        d["a_b1"] = list(self.a_b1)
        d["s_1_idx"] = self.s_1_idx
        d["s_idx"] = self.s_idx
        d["S"] = list(self.S)
        d["S_A"] = list(self.S_A)
        d["S_D"] = list(self.S_D)
        d["d_b"] = list(self.d_b)
        d["a_b"] = list(self.a_b)
        d["t"] = self.t
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "IntrusionResponseGameStateLocal":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = IntrusionResponseGameStateLocal(
            d_b1=np.array(d["d_b1"]), a_b1=np.array(d["a_b1"]), s_1_idx=d["s_1_idx"], S=np.array(d["S"]),
            S_A=np.array(d["S_A"]), S_D=np.array(d["S_D"]))
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "IntrusionResponseGameStateLocal":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return IntrusionResponseGameStateLocal.from_dict(json.loads(json_str))
