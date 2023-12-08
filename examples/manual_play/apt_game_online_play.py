from typing import List, Any
# import time
# import numpy as np
import numpy.typing as npt
# import json
# import io
# from csle_common.metastore.metastore_facade import MetastoreFacade
# from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
# from gym_csle_apt_game.envs.apt_game_env import AptGameEnv
# from gym_csle_apt_game.util.rollout_util import RolloutUtil


def online_play(T: int, b1: List[float], pi_d_1: float, pi_a_1: npt.NDArray[Any], gamma: float, ell_d: int, ell_a: int,
                game_config: AptGameConfig) -> None:
    """
    Implements Alg. 1 in the paper "Strategic Learning in Security Games with Information Asymmetry"

    :param T: the time horizon
    :param b1: the initial belief
    :param pi_d_1: the base strategy of the defender
    :param pi_a_1: the base strategy of the attacker
    :param gamma: the discount factor
    :param ell_d: the lookahead horizon of the defender
    :param ell_a: the lookahead horizon of the attacker
    :param game_config: the configuration of the game
    :return: None
    """
    pass
    # defender_history = ([b1], [], [])
    # attacker_history = ([], [], [])
    # b = b1.copy()
    # s = AptGameUtil.sample_initial_state(b1=b)
    # pi_a_bar = pi_a_1
    # pi_d_bar = pi_d_1
    # a1_d = AptGameUtil.sample_defender_action(alpha=pi_d_1, b=b)
    # a1_a = AptGameUtil.sample_attacker_action(pi2=pi_a_1, s=s)
    # for t in range(2, T):
    #     pass


if __name__ == '__main__':
    pass
