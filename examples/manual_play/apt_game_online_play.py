from typing import List, Any
import random
import numpy as np
import numpy.typing as npt
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
from gym_csle_apt_game.util.rollout_util import RolloutUtil


def online_play(T: int, b1: List[float], pi_d_1: float, pi_a_1: npt.NDArray[Any], gamma: float, ell_d: int, ell_a: int,
                game_config: AptGameConfig, num_samples: int, mc_horizon: int) -> None:
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
    :param num_samples: the number of Monte-Carlo samples
    :param mc_horizon: the monte-carlo horizon
    :return: None
    """
    defender_history = ([b1], [], [])
    attacker_history = ([b1], [], [], [], [])
    b = b1.copy()
    s = AptGameUtil.sample_initial_state(b1=b)
    a1 = AptGameUtil.sample_defender_action(alpha=pi_d_1, b=b)
    a2 = AptGameUtil.sample_attacker_action(pi2=pi_a_1, s=s)
    attacker_history[4].append(s)
    attacker_history[3].append(a2)
    attacker_history[2].append(a1)
    defender_history[2].append(a1)
    s = AptGameUtil.sample_next_state(T=game_config.T, s=s, a1=a1, a2=a2, S=game_config.S)
    ell_a_bar = 1
    for t in range(2, T):
        print(f"t:{t}, b:{np.round(b, 3)}, s: {s}, a1: {a1}, a2: {a2}")
        o = AptGameUtil.sample_next_observation(Z=game_config.Z, s_prime=s, O=game_config.O)
        b = AptGameUtil.next_belief(o=o, a1=a1, b=b, pi2=pi_a_1, config=game_config)
        defender_history[0].append(b)
        defender_history[1].append(o)
        defender_history[2].append(a1)
        # TODO update ell_a_bar here
        a2_hat, _ = RolloutUtil.monte_carlo_attacker_rollout(
            alpha=pi_d_1, pi2=pi_a_1, config=game_config, num_samples=num_samples, horizon=mc_horizon,
            ell=ell_a_bar, b=b)
        a1, _ = RolloutUtil.monte_carlo_defender_rollout(
            alpha=pi_d_1, pi2=pi_a_1, config=game_config, num_samples=num_samples, horizon=mc_horizon,
            ell=ell_d, b=b, a2=a2_hat)
        a2, _ = RolloutUtil.monte_carlo_attacker_rollout(
            alpha=pi_d_1, pi2=pi_a_1, config=game_config, num_samples=num_samples, horizon=mc_horizon,
            ell=ell_a, b=b, a1=a1, s=s)
        attacker_history[0].append(b)
        attacker_history[1].append(o)
        attacker_history[2].append(a1)
        attacker_history[3].append(a2)
        attacker_history[4].append(s)
        s = AptGameUtil.sample_next_state(T=game_config.T, s=s, a1=a1, a2=a2, S=game_config.S)
        if random.random() < (1 - gamma):
            b = b1
            s = AptGameUtil.sample_initial_state(b1=b)
            attacker_history[0].append(b)
            defender_history[0].append(b)
            attacker_history[4].append(s)


if __name__ == '__main__':
    N = 10
    p_a = 0.2
    C = AptGameUtil.cost_tensor(N=N)
    num_observations = 3
    Z = AptGameUtil.observation_tensor(N=N, num_observations=num_observations)
    O = list(AptGameUtil.observation_space(num_observations=num_observations))
    T = AptGameUtil.transition_tensor(N=N, p_a=p_a)
    S = AptGameUtil.state_space(N=N)
    A1 = AptGameUtil.defender_actions()
    A2 = AptGameUtil.attacker_actions()
    b1 = AptGameUtil.b1(N=N)
    gamma = 0.99
    game_config = AptGameConfig(
        T=T, O=O, Z=Z, C=C, S=S, A1=A1, A2=A2, N=N, p_a=p_a, save_dir=".", checkpoint_traces_freq=10000, gamma=gamma,
        b1=b1, env_name="csle-apt-game-v1")
    p_intrusion = 0.2
    pi2 = []
    for s in S:
        pi2.append([1 - p_intrusion, p_intrusion])
    pi2 = np.array(pi2)
    alpha = 0.75
    ell_d = 1
    ell_a = 1
    num_samples = 5
    mc_horizon = 20
    online_play_horizon = 20
    online_play(T=online_play_horizon, b1=b1, pi_d_1=alpha, pi_a_1=pi2, gamma=gamma, ell_d=1, ell_a=1,
                game_config=game_config, num_samples=num_samples, mc_horizon=mc_horizon)
