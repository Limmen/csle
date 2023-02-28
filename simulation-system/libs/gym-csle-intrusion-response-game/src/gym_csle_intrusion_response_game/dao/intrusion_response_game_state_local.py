import numpy as np
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil


class IntrusionResponseGameStateLocal:
    """
    Represents the state of the intrusion response game
    """

    def __init__(self, b1: np.ndarray, S: np.ndarray):
        self.b1 = b1
        self.S = S
        self.b = self.b1.copy()
        self.s = IntrusionResponseGameUtil.sample_initial_state(b1=self.b1, state_space=self.S)
        self.t = 1

    def reset(self) -> None:
        """
        Resets the state

        :return: None
        """
        self.t = 1
        self.s = IntrusionResponseGameUtil.sample_initial_state(b1=self.b1, state_space=self.S)
        self.b = self.b1.copy()

    def attacker_observation(self) -> np.ndarray:
        """
        :return: the attacker's observation
        """
        pass

    def defender_observation(self) -> np.ndarray:
        """
        :return: the defender's observation
        """
        pass

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        pass
