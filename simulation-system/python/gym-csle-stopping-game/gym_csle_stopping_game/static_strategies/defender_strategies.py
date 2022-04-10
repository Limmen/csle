from typing import Tuple, List
import numpy as np
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig


def random_defender_strategy(obs: np.ndarray, config: StoppingGameConfig) -> Tuple[int, List[float]]:
    """
    Represents a random defender strategy, returns a sampled defender action and its probability vector

    :param obs: the defender observation
    :param config: the configuration of the game
    :return: the sampled action, the probability distribution over the action space
    """
    p = 1/len(config.A1)
    probabiltiy_vector = [p]*len(config.A1)
    a1 = np.random.choice(np.arange(0, len(config.A1)),
                          p=probabiltiy_vector)
    return a1, probabiltiy_vector