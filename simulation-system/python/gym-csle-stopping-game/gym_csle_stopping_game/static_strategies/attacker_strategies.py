import numpy as np
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig


def random_attacker_strategy(obs: np.ndarray, config: StoppingGameConfig) -> np.ndarray:
    """
    Represents a random attacker strategy. It starts the intrusion with probability 0.1 and aborts
    with probability 0.1

    :param obs: the attacker's observation
    :param config: the configuration of the game
    :return: None
    """
    pi2 = np.zeros((3,2))
    pi2[0][0] = 0.9
    pi2[0][1] = 0.1
    pi2[1][0] = 0.9
    pi2[1][1] = 0.1
    pi2[2] = pi2[1]
    return pi2