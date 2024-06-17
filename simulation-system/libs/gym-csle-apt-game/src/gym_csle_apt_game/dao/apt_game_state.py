from typing import Dict, Any, Tuple
import numpy as np
import numpy.typing as npt
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from csle_base.json_serializable import JSONSerializable


class AptGameState(JSONSerializable):
    """
    Represents the state of the optimal APT game
    """

    def __init__(self, b1: npt.NDArray[np.float64]) -> None:
        """
        Intializes the state

        :param b1: the initial belief
        :param L: the maximum number of stop actions of the defender
        """
        self.b1 = b1
        self.b = self.b1.copy()
        self.s = AptGameUtil.sample_initial_state(b1=self.b1)
        self.t = 1

    def reset(self) -> None:
        """
        Resets the state

        :return: None
        """
        self.t = 1
        self.s = AptGameUtil.sample_initial_state(b1=self.b1)
        self.b = self.b1.copy()

    def attacker_observation(self) -> Tuple[npt.NDArray[Any], int]:
        """
        :return: the attacker's observation
        """
        return (self.b, int(self.s))

    def defender_observation(self) -> npt.NDArray[Any]:
        """
        :return: the defender's observation
        """
        return np.array([self.b])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"s:{self.s}, b:{self.b}, b1:{self.b1}, t:{self.t}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AptGameState":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = AptGameState(b1=np.array(d["b1"]))
        obj.t = d["t"]
        obj.s = d["s"]
        obj.b = np.array(d["b"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["b1"] = list(self.b1)
        d["b"] = list(self.b)
        d["s"] = self.s
        d["t"] = self.t
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "AptGameState":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return AptGameState.from_dict(json.loads(json_str))
