import numpy as np


class IntrusionResponseGameState:
    """
    Represents the state of the intrusion response game
    """

    def __init__(self):
        pass

    def reset(self) -> None:
        """
        Resets the state

        :return: None
        """
        pass

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
