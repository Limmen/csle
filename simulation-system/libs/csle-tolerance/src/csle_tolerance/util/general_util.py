from typing import List
import math
import numpy as np


class GeneralUtil:
    """
    Class with general utility functions related to csle-tolerance
    """

    @staticmethod
    def threshold_probability(b1: float, threshold: float, k=-20) -> float:
        """
        Returns the probability of taking an action given a belief and a threshold

        :param b1: the belief
        :param threshold: the threshold
        :return: the stopping probability
        """
        if (1 - round(b1, 2)) == 0:
            return 1.0
        if round(b1, 2) == 0:
            return 0.0
        if (threshold * (1 - b1)) > 0 and (b1 * (1 - threshold)) / (
            threshold * (1 - b1)
        ) > 0:
            try:
                return math.pow(
                    1 + math.pow(((b1 * (1 - threshold)) / (threshold * (1 - b1))), k),
                    -1,
                )
            except Exception:
                return 0.0
        else:
            return 0.0

    @staticmethod
    def sigmoid(x) -> float:
        """
        The sigmoid function

        :param x: the input
        :return: sigmoid(x)
        """
        return 1 / (1 + math.exp(-x))

    @staticmethod
    def inverse_sigmoid(y) -> float:
        """
        The inverse sigmoid function

        :param y: sigmoid(x)
        :return: sigmoid(x)^(-1)
        """
        return math.log(y / (1 - y), math.e)

    @staticmethod
    def sample_next_state(
        transition_tensor: List[List[List[float]]], s: int, a: int, states: List[int]
    ) -> int:
        """
        Samples the next state of a MDP or POMDP

        :param transition_tensor: the transition tensor
        :param s: the current state
        :param a: the current action
        :param states: the list of states
        :return: the next state
        """
        state_probs = []
        for s_prime in states:
            state_probs.append(transition_tensor[a][s][s_prime])
        return int(np.random.choice(np.arange(0, len(states)), p=state_probs))

    @staticmethod
    def register_envs() -> None:
        """
        Utility method for registering Gymnasium environments

        :return: None
        """
        from gymnasium.envs.registration import register

        register(
            id="csle-tolerance-intrusion-recovery-pomdp-v1",
            entry_point="csle_tolerance.envs.intrusion_recovery_pomdp_env:IntrusionRecoveryPomdpEnv",
            kwargs={"config": None},
        )
        register(
            id="csle-tolerance-intrusion-response-cmdp-v1",
            entry_point="csle_tolerance.envs.intrusion_response_cmdp_env:IntrusionResponseCmdpEnv",
            kwargs={"config": None},
        )
