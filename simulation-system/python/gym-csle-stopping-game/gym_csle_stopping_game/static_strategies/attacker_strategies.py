import numpy as np
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig


def random_attacker_strategy(obs: np.ndarray, config: StoppingGameConfig) -> np.ndarray:
    pi2 = np.zeros((3,2))
    pi2[0][0] = np.random.rand()
    pi2[0][1] = 1-pi2[0][0]
    pi2[1][0] = np.random.rand()
    pi2[1][1] = 1-pi2[1][0]
    pi2[2] = pi2[1]
    return pi2