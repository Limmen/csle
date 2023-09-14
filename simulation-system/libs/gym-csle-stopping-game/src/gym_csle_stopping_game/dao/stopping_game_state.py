from typing import Dict, Any
import numpy as np
import numpy.typing as npt
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_base.json_serializable import JSONSerializable


class StoppingGameState(JSONSerializable):
    """
    Represents the state of the optimal stopping game
    """

    def __init__(self, b1: npt.NDArray[np.float_], L: int) -> None:
        """
        Intializes the state

        :param b1: the initial belief
        :param L: the maximum number of stop actions of the defender
        """
        self.L = L
        self.b1 = b1
        self.b = self.b1.copy()
        self.l = self.L
        self.s = StoppingGameUtil.sample_initial_state(b1=self.b1)
        self.t = 1

    def reset(self) -> None:
        """
        Resets the state

        :return: None
        """
        self.l = self.L
        self.t = 1
        self.s = StoppingGameUtil.sample_initial_state(b1=self.b1)
        self.b = self.b1.copy()

    def attacker_observation(self) -> npt.NDArray[Any]:
        """
        :return: the attacker's observation
        """
        return np.array([np.float64(self.l), np.float64(self.b[1]), np.float64(self.s)])

    def defender_observation(self) -> npt.NDArray[Any]:
        """
        :return: the defender's observation
        """
        return np.array([np.float64(self.l), np.float64(self.b[1])])

    def __str__(self) -> str:
        """
        :return: a string representation of the objectn
        """
        return f"s:{self.s}, L:{self.L}, l: {self.l}, b:{self.b}, b1:{self.b1}, t:{self.t}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StoppingGameState":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = StoppingGameState(b1=np.array(d["b1"]), L=d["L"])
        obj.t = d["t"]
        obj.l = d["l"]
        obj.s = d["s"]
        obj.b = np.array(d["b"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["L"] = self.L
        d["b1"] = list(self.b1)
        d["b"] = list(self.b)
        d["l"] = self.l
        d["s"] = self.s
        d["t"] = self.t
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "StoppingGameState":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return StoppingGameState.from_dict(json.loads(json_str))
