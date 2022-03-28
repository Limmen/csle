import numpy as np
from gym_csle_stopping_game.util.env_util import EnvUtil


class StoppingGameState:
    """
    Represents the state of the optimal stopping game
    """

    def __init__(self, b1: np.ndarray, L: int) -> None:
        """
        Intializes the state

        :param b1: the initial belief
        :param L: the maximum number of stop actions of the defender
        """
        self.L = L
        self.b1 = b1
        self.b = self.b1.copy()
        self.l = self.L
        self.s = EnvUtil.sample_initial_state(b1=self.b1)
        self.t = 1

    def reset(self) -> None:
        """
        Resets the state

        :return: None
        """
        self.l = self.L
        self.t = 1
        self.s = EnvUtil.sample_initial_state(b1=self.b1)
        self.b = self.b1.copy()

    def __str__(self) -> str:
        """
        :return: a string representation of the objectn
        """
        return f"s:{self.s}, L:{self.L}, l: {self.l}, b:{self.b}, b1:{self.b1}, t:{self.t}"