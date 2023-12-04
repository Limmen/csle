from typing import Any, List, Tuple
import numpy as np
import random
from multiprocessing import Pool
from csle_common.util.multiprocessing_util import NestablePool
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
from gym_csle_apt_game.envs.apt_game_env import AptGameEnv
import numpy.typing as npt


class RolloutUtil:
    """
    Class with utility functions for rollout
    """

    @staticmethod
    def eval_defender_base(alpha: float, pi2: npt.NDArray[Any], config: AptGameConfig, horizon: int, id: int) -> float:
        """
        Function for evaluating a base threshold strategy of the defender

        :param alpha: the defender's threshold
        :param pi2: the attacker's strategy
        :param config: the game configuration
        :param horizon: the horizon for the Monte-Carlo sampling
        :param id: the id of the parallel processor
        :return: the average return
        """
        np.random.seed(100 * id + 378 * id + 23 + id)
        random.seed(100 * id + 378 * id + 23 + id)
        env = AptGameEnv(config=config)
        o, info = env.reset()
        cumulative_cost = 0.0
        (defender_obs, attacker_obs) = o
        for j in range(horizon):
            b = attacker_obs[0]
            s = attacker_obs[1]
            a1 = 0
            if sum(b[1:] >= alpha):
                a1 = 1
            a2 = (pi2, AptGameUtil.sample_attacker_action(pi2=pi2, s=s))
            action_profile = (a1, a2)
            o, costs, done, _, info = env.step(action_profile)
            (defender_obs, attacker_obs) = o
            c = costs[0]
            cumulative_cost += c
        return cumulative_cost

    @staticmethod
    def eval_defender_base_parallel(alpha: float, pi2: npt.NDArray[Any], config: AptGameConfig, num_samples: int,
                                    horizon: int) -> float:
        """
        Starts a pool of parallel processors for evaluating a threshold base strategy of the defender

        :param alpha: the threshold
        :param pi2: the defender strategy
        :param config: the game configuration
        :param num_samples: the number of monte carlo samples
        :param horizon: the horizon of the Monte-Carlo sampling
        :return: the average cost-to-go of the base strategy
        """
        p = Pool(num_samples)
        args = []
        for i in range(num_samples):
            args.append((alpha, pi2, config, horizon, i))
        cumulative_costs = p.starmap(RolloutUtil.eval_defender_base, args)
        return float(np.mean(cumulative_costs))

    @staticmethod
    def exact_defender_rollout(alpha: float, pi2: npt.NDArray[Any], config: AptGameConfig, num_samples: int,
                               horizon: int, ell: int, b: List[float]) -> Tuple[int, float]:
        """
        Performs exact rollout of the defender against a fixed attacker strategy and with a threshold base strategy

        :param alpha: the threshold base strategy
        :param pi2: the strategy of the attacker
        :param config: the game configuraton
        :param num_samples: the number of Monte-Carlo samples
        :param horizon: the horizon for the Monte-Carlo sampling
        :param ell: the lookahead length
        :param b: the belief state
        :return: The rollout action and the corresponding Q-factor
        """
        if ell == 0:
            return 0, RolloutUtil.eval_defender_base_parallel(alpha=alpha, pi2=pi2, config=config,
                                                              num_samples=num_samples, horizon=horizon)
        else:
            A_costs = []
            for a1 in config.A1:
                print(f"{a1}/{len(config.A1)}, ell: {ell}")
                expected_immediate_cost = AptGameUtil.expected_cost(C=list(config.C), S=list(config.S), b=b, a1=a1)
                expected_future_cost = 0.0
                for a2 in config.A2:
                    for i, o in enumerate(config.O):
                        b_prime = AptGameUtil.next_belief(o=i, a1=a1, b=np.array(b), pi2=pi2, config=config, a2=a2)
                        _, cost = RolloutUtil.exact_defender_rollout(alpha=alpha, pi2=pi2, config=config,
                                                                     num_samples=num_samples, horizon=horizon,
                                                                     ell=ell - 1, b=list(b_prime))
                        obs_prob = 0.0
                        action_prob = 0.0
                        for s in config.S:
                            action_prob += b[s] * pi2[s][a2]
                            for s_prime in config.S:
                                obs_prob += b[s] * config.T[a1][a2][s][s_prime] * config.Z[s_prime][i]
                        expected_future_cost += action_prob * obs_prob * cost
                A_costs.append(expected_immediate_cost + config.gamma * expected_future_cost)
            best_action = np.argmax(A_costs)
            return int(best_action), float(A_costs[best_action])

    @staticmethod
    def monte_carlo_defender_rollout(alpha: float, pi2: npt.NDArray[Any], config: AptGameConfig, num_samples: int,
                                     horizon: int,
                                     ell: int, b: List[float]) -> Tuple[int, float]:
        """
        Monte-Carlo based on rollout of the defender with a threshold base strategy

        :param alpha: the threshold of the base strategy
        :param pi2: the attacker strategy
        :param config: the game configuration
        :param num_samples: the number of monte-carlo samples
        :param horizon: the horizon for monte-carlo sampling
        :param ell: the lookahead length
        :param b: the belief state
        :return: The rollout action and the corresponding Q-factor
        """
        if ell == 0:
            return 0, RolloutUtil.eval_defender_base_parallel(alpha=alpha, pi2=pi2, config=config,
                                                              num_samples=num_samples, horizon=horizon)
        else:
            A_costs = []
            for a1 in config.A1:
                print(f"{a1}/{len(config.A1)}, ell: {ell}")
                expected_immediate_cost = AptGameUtil.expected_cost(C=list(config.C), S=list(config.S), b=b, a1=a1)
                expected_future_cost = 0
                for a2 in config.A2:
                    p = NestablePool(num_samples)
                    args = []
                    for i in range(num_samples):
                        s = AptGameUtil.sample_initial_state(b1=np.array(b))
                        AptGameUtil.sample_attacker_action(pi2=pi2, s=s)
                        s_prime = AptGameUtil.sample_next_state(T=config.T, s=s, a1=a1, a2=a2, S=config.S)
                        o = AptGameUtil.sample_next_observation(Z=config.Z, s_prime=s_prime, O=config.O)
                        o_idx = list(config.O).index(o)
                        b_prime = AptGameUtil.next_belief(o=o_idx, a1=a1, b=np.array(b), pi2=pi2, config=config, a2=a2)
                        args.append((alpha, pi2, config, num_samples, horizon, ell - 1, b_prime))
                    cumulative_costs = p.starmap(RolloutUtil.monte_carlo_defender_rollout, args)
                    expected_future_cost = np.mean(cumulative_costs)
                A_costs.append(expected_immediate_cost + config.gamma * expected_future_cost)
            best_action = np.argmax(A_costs)
            return int(best_action), float(A_costs[best_action])
