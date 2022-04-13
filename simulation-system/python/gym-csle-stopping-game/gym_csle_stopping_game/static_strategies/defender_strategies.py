from typing import Tuple, List
import numpy as np
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig


def random_defender_strategy(obs: np.ndarray) -> Tuple[int, List[float]]:
    """
    Represents a random defender strategy, returns a sampled defender action and its probability vector

    :param obs: the defender observation
    :return: the sampled action, the probability distribution over the action space
    """
    p = 0.5
    probabiltiy_vector = [p,p]
    a1 = np.random.choice(np.arange(0, len(probabiltiy_vector)), p=probabiltiy_vector)
    return a1, probabiltiy_vector