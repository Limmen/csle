import time
from typing import List, Any, Union
import random
import numpy as np
import math
import numpy.typing as npt
import json
import io
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
from gym_csle_apt_game.util.rollout_util import RolloutUtil


def empirical_discrepancy(feedback_probabilities: List[Any], ell_a_hat: int, ell_a: int, cal_L: List[int]) -> float:
    """
    Calculates the empirical discrepancy of the conjecture ell_a_hat

    :param feedback_probabilities: the feedback probabilities of the fictitious lookahead horizons
    :param ell_a_hat: the conjecture
    :param ell_a: the true lookahead horizon of the attacker
    :param cal_L: the set of fictitious lookahead horizons
    :return: the empirical discrepancy
    """
    Z = 0
    ell_a_hat_idx = cal_L.index(ell_a_hat)
    ell_a_idx = cal_L.index(ell_a)
    for tau in range(len(feedback_probabilities[ell_a_idx])):
        if feedback_probabilities[ell_a_hat_idx][tau] > 0:
            Z += math.log(feedback_probabilities[ell_a_idx][tau] / feedback_probabilities[ell_a_hat_idx][tau], math.e)
        else:
            Z += 10
    Z = Z / len(feedback_probabilities[ell_a_idx])
    return Z


def defender_information_feedback_probability(pi_d_1: float, pi_a_1: npt.NDArray[Any], ell: int,
                                              game_config: AptGameConfig,
                                              num_samples: int, mc_horizon: int, b: List[float], o: int, a1: int,
                                              true_s: int, a2: Union[None, int] = None) -> float:
    """
    Calculates the probability of observing a given information feedback (o) given that the attacker follows a
    certain lookahead horizon

    :param pi_d_1: the base strategy of the defender
    :param pi_a_1: the base strategy of the attacker
    :param ell: the conjectured lookahead horizon of the attacker
    :param game_config: the configuration of the game
    :param num_samples: the number of samples for Monte-Carlo approximations
    :param mc_horizon: the horizon of the Monte-Carlo sampling
    :param b: the belief
    :param o: the observation (the information feedback)
    :param a1: the action of the defender
    :param true_s: the state
    :return: the probability
    """
    if a2 is not None:
        a2_hat = a2
    elif ell == 0:
        a2_hat = AptGameUtil.sample_attacker_action(pi2=pi_a_1, s=AptGameUtil.sample_initial_state(b1=b))
    else:
        a2_hat, _ = RolloutUtil.monte_carlo_attacker_rollout(
            alpha=pi_d_1, pi2=pi_a_1, config=game_config, num_samples=num_samples, horizon=mc_horizon,
            ell=ell, b=b)
    prob = 0
    true_s_prob = 0
    for s in game_config.S:
        for s_prime in game_config.S:
            prob += b[s] * game_config.T[a1][a2_hat][s][s_prime] * game_config.Z[s_prime][game_config.O.index(o)]
            if s_prime == true_s:
                true_s_prob += b[s] * game_config.T[a1][a2_hat][s][s_prime]
    print(f"a2hat: {a2_hat}, conjecture: {ell}, prob: {prob}, true_a_2: {a2}, o: {o}, a1: {a1}, s: {true_s},"
          f"true prob: {game_config.Z[true_s][game_config.O.index(o)]}, true_s_prime_prob: {true_s_prob}")
    return prob


def bayesian_estimator(mu: List[float], cal_L: List[int], feedback_probabilities: List[Any]):
    """
    Implements the Bayesian estimator in the paper "Strategic Learning in Security Games with Information Asymmetry"

    :param mu: the prior
    :param cal_L: the set of fictitious lookahead horizons
    :param feedback_probabilities: probabilities of observing the information feedback under different conjectures
    :return: the posterior
    """
    denominator = 0
    for i, ell in enumerate(cal_L):
        denominator += feedback_probabilities[i][-1] * mu[i]
    for i, ell in enumerate(cal_L):
        numerator = feedback_probabilities[i][-1] * mu[i]
        mu[i] = numerator / denominator
    return mu


def expected_discrepancy(discrepancies: List[Any], cal_L: List[int], mu: List[float]) -> float:
    """
    Calculates the expected discrepancy based on the posterior

    :param discrepancies: the discrepancies of all conjectures
    :param cal_L: the set of fictitious lookahead horizons
    :param mu: the posterior
    :return: the expected discrepancy
    """
    expected_d = 0
    for i, ell in enumerate(cal_L):
        expected_d += discrepancies[i][-1] * mu[i]
    return expected_d


def online_play(T: int, b1: List[float], pi_d_1: float, pi_a_1: npt.NDArray[Any], gamma: float, ell_d: int, ell_a: int,
                game_config: AptGameConfig, num_samples: int, mc_horizon: int, cal_L: List[int],
                mu: List[float], seed: int) -> None:
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
    :param cal_L: the list of fictitious lookahead horizons
    :param mu: the lookahead posterior of the defender
    :param seed: the random seed
    :return: None
    """
    defender_history = ([b1], [], [])
    attacker_history = ([b1], [], [], [], [])
    feedback_probabilities = []
    discrepancies = []
    for _ in cal_L:
        feedback_probabilities.append([])
        discrepancies.append([])
    b = b1.copy()
    s = AptGameUtil.sample_initial_state(b1=b)
    a1 = AptGameUtil.sample_defender_action(alpha=pi_d_1, b=b)
    a2 = AptGameUtil.sample_attacker_action(pi2=pi_a_1, s=s)
    attacker_history[4].append(s)
    attacker_history[3].append(a2)
    attacker_history[2].append(a1)
    defender_history[2].append(a1)
    s = AptGameUtil.sample_next_state(T=game_config.T, s=s, a1=a1, a2=a2, S=game_config.S)
    data = {}
    data["discrepancy"] = []
    data["mu_1"] = []
    data["costs"] = []
    start = time.time()
    for t in range(2, T):
        print(f"t:{t}, b:{np.round(b, 3)}, s: {s}, a1: {a1}, a2: {a2}, time: {time.time() - start}")
        o = AptGameUtil.sample_next_observation(Z=game_config.Z, s_prime=s, O=game_config.O)
        for i, ell in enumerate(cal_L):
            true_a2 = None
            if ell == ell_a:
                true_a2 = a2
            feedback_probabilities[i].append(defender_information_feedback_probability(
                pi_d_1=pi_d_1, pi_a_1=pi_a_1, ell=ell, game_config=game_config, num_samples=num_samples,
                mc_horizon=mc_horizon, b=b, o=o, a1=a1, a2=true_a2, true_s=s))
        for i, ell in enumerate(cal_L):
            discrepancies[i].append(empirical_discrepancy(feedback_probabilities=feedback_probabilities, ell_a_hat=ell,
                                                          ell_a=ell_a, cal_L=cal_L))
        # print(f"feedback probs: {list(map(lambda x: x[-1], feedback_probabilities))}")
        # print(f"discrepenacies: {list(map(lambda x: x[-1], discrepancies))}")
        mu = bayesian_estimator(mu=mu, cal_L=cal_L, feedback_probabilities=feedback_probabilities)
        expected_d = expected_discrepancy(discrepancies=discrepancies, cal_L=cal_L, mu=mu)
        data["discrepancy"].append(expected_d)
        data["mu_1"].append(mu[1])
        data["discrepancies"] = discrepancies
        print(f"posterior: {mu}, E[discrepancy]: {expected_d}")
        ell_a_bar = int(np.random.choice(np.arange(0, len(mu)), p=mu))
        b = AptGameUtil.next_belief(o=game_config.O.index(o), a1=a1, b=b, pi2=pi_a_1, config=game_config)
        defender_history[0].append(b)
        defender_history[1].append(o)
        defender_history[2].append(a1)
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
        c = AptGameUtil.cost_function(s=s, a_1=a1)
        data["costs"].append(c)
        print(f"costs: {data['costs']}")
        s = AptGameUtil.sample_next_state(T=game_config.T, s=s, a1=a1, a2=a2, S=game_config.S)
        # if random.random() < (1 - gamma):
        #     b = b1
        #     s = AptGameUtil.sample_initial_state(b1=b)
        #     attacker_history[0].append(b)
        #     defender_history[0].append(b)
        #     attacker_history[4].append(s)
        if t % 5 == 0:
            json_str = json.dumps(data, indent=4, sort_keys=True)
            with io.open(f"/home/kim/bayesian_estimator_seed_{seed}.json", 'w', encoding='utf-8') as f:
                f.write(json_str)


if __name__ == '__main__':
    N = 10
    filename = "/home/kim/nyu_data_dict_3"
    with io.open(filename, 'r') as f:
        json_str = f.read()
    data_dict = json.loads(json_str)

    simulation_name = "csle-apt-game-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    Z = []
    no_intrusion_min_val = max([0, int(data_dict["no_intrusion_alerts_means"][10] -
                                       data_dict["no_intrusion_alerts_stds"][10])])
    no_intrusion_max_val = data_dict["no_intrusion_alerts_means"][10] + data_dict["no_intrusion_alerts_stds"][10]
    no_intrusion_range = (no_intrusion_min_val, no_intrusion_max_val)
    intrusion_min_val = max([0, int(data_dict["intrusion_alerts_means"][10] * (1 + N * 0.2) -
                                    data_dict["intrusion_alerts_stds"][10])])
    intrusion_max_val = data_dict["intrusion_alerts_means"][10] * (1 + N * 0.2) + data_dict["intrusion_alerts_stds"][10]
    max_intrusion_range = (intrusion_min_val, intrusion_max_val)
    O = list(range(int(no_intrusion_range[0]), int(max_intrusion_range[1])))
    no_intrusion_dist = []
    for i in O:
        if i in list(range(int(no_intrusion_range[0]), int(no_intrusion_range[1]))):
            no_intrusion_dist.append(round(1 / (no_intrusion_range[1] - no_intrusion_range[0]), 10))
        else:
            no_intrusion_dist.append(0)
    Z.append(list(np.array(no_intrusion_dist) / sum(no_intrusion_dist)))
    for s in range(1, N + 1):
        intrusion_dist = []
        min_val = max([0, int(data_dict["intrusion_alerts_means"][10] * (1 + s * 0.2) -
                              data_dict["intrusion_alerts_stds"][10])])
        max_val = data_dict["intrusion_alerts_means"][10] * (1 + s * 0.2) + data_dict["intrusion_alerts_stds"][10]
        intrusion_range = (min_val, max_val)
        for i in O:
            if i in range(int(intrusion_range[0]), int(intrusion_range[1])):
                intrusion_dist.append(round(1 / (intrusion_range[1] - intrusion_range[0]), 10))
            else:
                intrusion_dist.append(0)
        Z.append(list(np.array(intrusion_dist) / sum(intrusion_dist)))
    p_a = 1
    C = AptGameUtil.cost_tensor(N=N)
    # num_observations = 3
    # Z = AptGameUtil.observation_tensor(N=N, num_observations=num_observations)
    # O = list(AptGameUtil.observation_space(num_observations=num_observations))
    T = AptGameUtil.transition_tensor(N=N, p_a=p_a)
    S = AptGameUtil.state_space(N=N)
    A1 = AptGameUtil.defender_actions()
    A2 = AptGameUtil.attacker_actions()
    b1 = AptGameUtil.b1(N=N)
    gamma = 0.99
    game_config = AptGameConfig(
        T=T, O=O, Z=Z, C=C, S=S, A1=A1, A2=A2, N=N, p_a=p_a, save_dir=".", checkpoint_traces_freq=10000, gamma=gamma,
        b1=b1, env_name="csle-apt-game-v1")
    p_intrusion = 0.05
    pi2 = []
    for s in S:
        pi2.append([1 - p_intrusion, p_intrusion])
    pi2 = np.array(pi2)
    alpha = 0.75
    ell_d = 1
    ell_a = 1
    num_samples = 10
    mc_horizon = 50
    online_play_horizon = 200
    cal_L = [0, 1]
    mu = [1 / len(cal_L)] * len(cal_L)
    seed = 781233
    np.random.seed(seed)
    random.seed(seed)
    online_play(T=online_play_horizon, b1=b1, pi_d_1=alpha, pi_a_1=pi2, gamma=gamma, ell_d=ell_d, ell_a=ell_a,
                game_config=game_config, num_samples=num_samples, mc_horizon=mc_horizon, cal_L=cal_L, mu=mu, seed=seed)
