import time
from typing import List, Any, Dict, Tuple
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


def get_observation_distribution(data_dict: Dict[str, Any], t: int, N: int) -> Tuple[List[Any], List[int]]:
    """
    Gets the observation distribution for a given time-step

    :param data_dict: the data dict with the statistics from the digital twin
    :param t: the time-step
    :param N: the number of servers
    :return: the observation distribution and the observation space
    """
    Z = []
    no_intrusion_min_val = max([0, int(data_dict["no_intrusion_alerts_means"][t] -
                                       data_dict["no_intrusion_alerts_stds"][t])])
    no_intrusion_max_val = data_dict["no_intrusion_alerts_means"][t] + data_dict["no_intrusion_alerts_stds"][t]
    no_intrusion_range = (no_intrusion_min_val, no_intrusion_max_val)
    intrusion_min_val = max([0, int(data_dict["intrusion_alerts_means"][t] * (1 + N * 0.2) -
                                    data_dict["intrusion_alerts_stds"][t])])
    intrusion_max_val = data_dict["intrusion_alerts_means"][t] * (1 + N * 0.2) + data_dict["intrusion_alerts_stds"][t]
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
        min_val = max([0, int(data_dict["intrusion_alerts_means"][t] * (1 + s * 0.2) -
                              data_dict["intrusion_alerts_stds"][t])])
        max_val = data_dict["intrusion_alerts_means"][t] * (1 + s * 0.2) + data_dict["intrusion_alerts_stds"][t]
        intrusion_range = (min_val, max_val)
        for i in O:
            if i in range(int(intrusion_range[0]), int(intrusion_range[1])):
                intrusion_dist.append(round(1 / (intrusion_range[1] - intrusion_range[0]), 10))
            else:
                intrusion_dist.append(0)
        Z.append(list(np.array(intrusion_dist) / sum(intrusion_dist)))
    return Z, O


def empirical_discrepancy(feedback_probabilities: List[Any], theta: int, true_theta: int, Theta: List[int]) -> float:
    """
    Calculates the empirical discrepancy of the conjecture 'theta'

    :param feedback_probabilities: the feedback probabilities of the fictitious thetas horizons
    :param theta: the conjecture
    :param true_theta: the true theta
    :param Theta: the set of fictitious lookahead horizons
    :return: the empirical discrepancy
    """
    Z = 0
    conjecture_idx = Theta.index(theta)
    true_theta_idx = Theta.index(true_theta)
    for tau in range(len(feedback_probabilities[true_theta_idx])):
        if feedback_probabilities[conjecture_idx][tau] > 0:
            Z += math.log(feedback_probabilities[true_theta_idx][tau] / feedback_probabilities[conjecture_idx][tau],
                          math.e)
        else:
            Z += 10
    Z = Z / len(feedback_probabilities[true_theta_idx])
    return Z


def defender_information_feedback_probability(theta: int, game_config: AptGameConfig,
                                              b: List[float], o: int, a1: int, observation_models: Dict[int, Any],
                                              a2: int) -> float:
    """
    Calculates the probability of observing a given information feedback (o) given a certain theta

    :param theta: the theta parameter vector
    :param game_config: the game configuration
    :param b: the belief state
    :param o: the latest information feedback
    :param a1: the latest defender action
    :param observation_models: the observation models
    :param a2: the latest attacker action
    :return:
    """
    Z, O = observation_models[theta]
    prob = 0
    for s in game_config.S:
        for s_prime in game_config.S:
            if o in O:
                prob += b[s] * game_config.T[a1][a2][s][s_prime] * Z[s_prime][O.index(o)]
    return prob


def bayesian_estimator(rho: List[float], Theta: List[int], feedback_probabilities: List[Any]):
    """
    Implements the Bayesian estimator in the paper "Strategic Learning in Security Games with Information Asymmetry"

    :param rho: the prior
    :param Theta: the set of fictitious model parameters
    :param feedback_probabilities: probabilities of observing the information feedback under different conjectures
    :return: the posterior
    """
    denominator = 0
    for i, ell in enumerate(Theta):
        denominator += feedback_probabilities[i][-1] * rho[i]
    for i, ell in enumerate(Theta):
        numerator = feedback_probabilities[i][-1] * rho[i]
        rho[i] = numerator / denominator
    return rho


def expected_discrepancy(discrepancies: List[Any], Theta: List[int], rho: List[float]) -> float:
    """
    Calculates the expected discrepancy based on the posterior

    :param discrepancies: the discrepancies of all conjectures
    :param Theta: the set of fictitious lookahead horizons
    :param rho: the posterior
    :return: the expected discrepancy
    """
    expected_d = 0
    for i, ell in enumerate(Theta):
        expected_d += discrepancies[i][-1] * rho[i]
    return expected_d


def online_play(T: int, b1: List[float], pi_d_1: float, pi_a_1: npt.NDArray[Any], gamma: float, ell_d: int, ell_a: int,
                game_config: AptGameConfig, num_samples: int, mc_horizon: int, Theta: List[int],
                rho: List[float], seed: int, observation_models: Dict[int, Any]) -> None:
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
    :param Theta: the list of fictitious lookahead horizons
    :param rho: the lookahead posterior of the defender
    :param seed: the random seed
    :param observation_models: the observation models for different theta
    :return: None
    """
    defender_history = ([b1], [], [])
    attacker_history = ([b1], [], [], [], [])
    feedback_probabilities = []
    discrepancies = []
    for _ in Theta:
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
    data["rho_1"] = []
    data["costs"] = []
    start = time.time()
    true_theta = 2
    for t in range(2, T):
        print(f"t:{t}, b:{np.round(b, 3)}, s: {s}, a1: {a1}, a2: {a2}, time: {time.time() - start}")
        o = AptGameUtil.sample_next_observation(Z=game_config.Z, s_prime=s, O=game_config.O)
        for i, theta in enumerate(Theta):
            # print(f"feedback {i}/{len(Theta)}")
            feedback_probabilities[i].append(defender_information_feedback_probability(
                theta=theta, game_config=game_config, b=b, o=o, a1=a1, a2=a2, observation_models=observation_models))
        for i, theta in enumerate(Theta):
            # print(f"discrepancy {i}/{len(Theta)}")
            discrepancies[i].append(empirical_discrepancy(feedback_probabilities=feedback_probabilities, theta=theta,
                                                          true_theta=true_theta, Theta=Theta))

        # print(f"feedback probs: {list(map(lambda x: x[-1], feedback_probabilities))}")
        # print(f"discrepenacies: {list(map(lambda x: x[-1], discrepancies))}")
        rho = bayesian_estimator(rho=rho, Theta=Theta, feedback_probabilities=feedback_probabilities)
        expected_d = expected_discrepancy(discrepancies=discrepancies, Theta=Theta, rho=rho)
        data["discrepancy"].append(expected_d)
        data["rho_1"].append(rho[1])
        # data["discrepancies"] = discrepancies
        print(f"argmax posterior: {np.argmax(rho)}, E[discrepancy]: {expected_d}, rho: {rho}")
        b = AptGameUtil.next_belief(o=game_config.O.index(o), a1=a1, b=b, pi2=pi_a_1, config=game_config)
        defender_history[0].append(b)
        defender_history[1].append(o)
        defender_history[2].append(a1)
        a2, _ = RolloutUtil.monte_carlo_attacker_rollout(
            alpha=pi_d_1, pi2=pi_a_1, config=game_config, num_samples=num_samples, horizon=mc_horizon,
            ell=ell_a, b=b, a1=a1, s=s)
        a1, _ = RolloutUtil.monte_carlo_defender_rollout(
            alpha=pi_d_1, pi2=pi_a_1, config=game_config, num_samples=num_samples, horizon=mc_horizon,
            ell=ell_d, b=b, a2=a2)
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
        Z, O = observation_models[true_theta]
        game_config.Z = Z
        game_config.O = O


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
    p_a = 1
    C = AptGameUtil.cost_tensor(N=N)
    Z, O = get_observation_distribution(data_dict=data_dict, t=2, N=N)
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
    # Theta = list(range(len(data_dict["no_intrusion_alerts_means"])))
    Theta = list(range(2, 5))
    Theta = [2, 10]
    print(data_dict["rate_means"][2])
    print(data_dict["rate_means"][10])
    rho = [1 / len(Theta)] * len(Theta)
    seed = 781932
    np.random.seed(seed)
    random.seed(seed)
    observation_models = {}
    for theta in Theta:
        print(f"{theta}/{Theta[-1]}")
        Z, O = get_observation_distribution(data_dict=data_dict, t=theta, N=N)
        observation_models[theta] = (Z, O)
    online_play(T=online_play_horizon, b1=b1, pi_d_1=alpha, pi_a_1=pi2, gamma=gamma, ell_d=ell_d, ell_a=ell_a,
                game_config=game_config, num_samples=num_samples, mc_horizon=mc_horizon, Theta=Theta, rho=rho,
                seed=seed, observation_models=observation_models)
