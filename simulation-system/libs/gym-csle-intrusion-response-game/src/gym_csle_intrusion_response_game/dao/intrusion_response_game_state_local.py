import numpy as np
import gym_csle_intrusion_response_game.constants.constants as env_constants


class IntrusionResponseGameStateLocal:
    """
    Represents the state of the intrusion response game (A PO-POSG, i.e a partially observed stochastic game
    with public observations)
    """

    def __init__(self, d_b1: np.ndarray, a_b1: np.ndarray, s_1_idx: int, S: np.ndarray, S_A: np.ndarray,
                 S_D: np.ndarray) -> None:
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

    def attacker_observation(self) -> np.ndarray:
        """
        :return: the attacker's observation
        """
        return np.array([self.attacker_state()] + list(self.a_b.tolist()))

    def defender_observation(self) -> np.ndarray:
        """
        :return: the defender's observation
        """
        return np.array([self.defender_state()] + list(self.d_b.tolist()))

    def state_vector(self) -> np.ndarray:
        """
        :return: the state vector
        """
        return self.S[self.s_idx]

    def attacker_state(self) -> int:
        """
        :return: the attacker state
        """
        return self.S[self.s_idx][env_constants.STATES.A_STATE_INDEX]

    def defender_state(self) -> int:
        """
        :return: the defender state
        """
        return self.S[self.s_idx][env_constants.STATES.D_STATE_INDEX]

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"d_b1: {self.d_b1}, a_b1: {self.a_b1}, s_1_idx:{self.s_1_idx}, S:{self.S}, S_A:{self.S_A}, " \
               f"S_D: {self.S_D}, t: {self.t}, s_idx: {self.s_idx}, s: {self.state_vector()}"
