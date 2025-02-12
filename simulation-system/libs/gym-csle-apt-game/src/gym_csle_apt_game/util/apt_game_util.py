from typing import List, Any
import math
import numpy as np
import numpy.typing as npt
from scipy.stats import betabinom
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig


class AptGameUtil:
    """
    Class with utility functions for the APTGame Environment
    """

    @staticmethod
    def b1(N: int) -> npt.NDArray[np.float64]:
        """
        Gets the initial belief

        :param N: the number of servers
        :return: the initial belief
        """
        b1 = [0] * (N + 1)
        b1[0] = 1
        return np.array(b1)

    @staticmethod
    def state_space(N: int):
        """
        Gets the state space

        :param N: the number of servers
        :return: the state space of the game
        """
        return np.array(list(range(N + 1)))

    @staticmethod
    def defender_actions() -> npt.NDArray[np.int32]:
        """
        Gets the action space of the defender

        :return: the action space of the defender
        """
        return np.array([0, 1])

    @staticmethod
    def attacker_actions() -> npt.NDArray[np.int32]:
        """
        Gets the action space of the attacker

        :return: the action space of the attacker
        """
        return np.array([0, 1])

    @staticmethod
    def observation_space(num_observations: int):
        """
        Returns the observation space of size n

        :param num_observations: the number of observations
        :return: the observation space
        """
        return np.array(list(range(num_observations)))

    @staticmethod
    def cost_function(s: int, a_1: int) -> float:
        """
        The cost function of the game

        :param s: the state
        :param a_1: the defender action
        :return: the immediate cost
        """
        return float(math.pow(s, 5 / 4) * (1 - a_1) + a_1 - 2 * a_1 * np.sign(s))

    @staticmethod
    def cost_tensor(N: int) -> npt.NDArray[Any]:
        """
        Gets the reward tensor

        :return: a |A1|x|S| tensor
        """
        cost_tensor = []
        for a1 in [0, 1]:
            a_costs = []
            for s in range(N + 1):
                a_costs.append(AptGameUtil.cost_function(s=s, a_1=a1))
            cost_tensor.append(a_costs)
        return np.array(cost_tensor)

    @staticmethod
    def transition_function(N: int, p_a: float, s: int, s_prime: int, a_1: int, a_2: int) -> float:
        """
        The transition function of the game

        :param N: the number of servers
        :param p_a: the intrusion probability
        :param s: the state
        :param s_prime: the next state
        :param a_1: the defender action
        :param a_2: the attacker action
        :return: f(s_prime | s, a_1, a_2)
        """
        if a_1 == 1 and s_prime == 0:
            return 1.0
        if a_1 == 0 and a_2 == 0 and s_prime == s:
            return 1.0
        if a_1 == 0 and s == N and s_prime == N:
            return 1.0
        if a_1 == 0 and a_2 == 1 and s == s_prime:
            return 1 - p_a
        if a_1 == 0 and a_2 == 1 and s_prime == (s + 1):
            return p_a
        return 0.0

    @staticmethod
    def transition_tensor(N: int, p_a: float) -> npt.NDArray[Any]:
        """
        Gets the transition tensor

        :param L: the maximum number of stop actions
        :return: a |A1|x|A2||S|^2 tensor
        """
        transition_tensor = []
        for a_1 in [0, 1]:
            a1_transitions = []
            for a_2 in [0, 1]:
                a2_transitions = []
                for s in range(N + 1):
                    s_a_transitions = []
                    for s_prime in range(N + 1):
                        s_a_transitions.append(AptGameUtil.transition_function(N=N, p_a=p_a, s=s, s_prime=s_prime,
                                                                               a_1=a_1, a_2=a_2))
                    a2_transitions.append(s_a_transitions)
                a1_transitions.append(a2_transitions)
            transition_tensor.append(a1_transitions)
        return np.array(transition_tensor)

    @staticmethod
    def observation_tensor(num_observations, N: int) -> npt.NDArray[Any]:
        """
        Gets the observation tensor of the game

        :param num_observations: the number of observations
        :param N: the number of servers
        :return: a |S|x|O| observation tensor
        """
        intrusion_dist = []
        no_intrusion_dist = []
        terminal_dist = np.zeros(num_observations)
        terminal_dist[-1] = 1
        intrusion_rv = betabinom(n=num_observations - 1, a=1, b=0.7)
        no_intrusion_rv = betabinom(n=num_observations - 1, a=0.7, b=3)
        for i in range(num_observations):
            intrusion_dist.append(intrusion_rv.pmf(i))
            no_intrusion_dist.append(no_intrusion_rv.pmf(i))
        Z = []
        Z.append(no_intrusion_dist)
        for s in range(1, N + 1):
            Z.append(intrusion_dist)
        return np.array(Z)

    @staticmethod
    def sample_next_state(T: npt.NDArray[Any], s: int, a1: int, a2: int, S: npt.NDArray[np.int32]) -> int:
        """
        Samples the next state

        :param T: the transition operator
        :param s: the current state
        :param a1: the defender action
        :param a2: the attacker action
        :param S: the state space
        :return: s'
        """
        state_probs = []
        for s_prime in S:
            state_probs.append(T[a1][a2][s][s_prime])
        return int(np.random.choice(np.arange(0, len(S)), p=state_probs))

    @staticmethod
    def sample_initial_state(b1: npt.NDArray[np.float64]) -> int:
        """
        Samples the initial state

        :param b1: the initial belief
        :return: s1
        """
        return int(np.random.choice(np.arange(0, len(b1)), p=b1))

    @staticmethod
    def sample_next_observation(Z: npt.NDArray[Any], s_prime: int, O: npt.NDArray[np.int32]) -> int:
        """
        Samples the next observation

        :param s_prime: the new state
        :param O: the observation space
        :return: o
        """
        observation_probs = []
        for i, o in enumerate(O):
            observation_probs.append(Z[s_prime][i])
        o = np.random.choice(O, p=observation_probs)
        return int(o)

    @staticmethod
    def bayes_filter(s_prime: int, o: int, a1: int, b: npt.NDArray[np.float64], pi2: npt.NDArray[Any],
                     config: AptGameConfig) -> float:
        """
        A Bayesian filter to compute the belief of player 1
        of being in s_prime when observing o after taking action a in belief b given that the opponent follows
        strategy pi2

        :param s_prime: the state to compute the belief of
        :param o: the observation
        :param a1: the action of player 1
        :param b: the current belief point
        :param pi2: the policy of player 2
        :return: b_prime(s_prime)
        """
        norm = 0
        for s in config.S:
            for a2 in config.A2:
                for s_prime_1 in config.S:
                    prob_1 = config.Z[s_prime_1][o]
                    norm += b[s] * prob_1 * config.T[a1][a2][s][s_prime_1] * pi2[s][a2]
        if norm == 0:
            return 0
        temp = 0

        for s in config.S:
            for a2 in config.A2:
                temp += config.Z[s_prime][o] * config.T[a1][a2][s][s_prime] * b[s] * pi2[s][a2]
        b_prime_s_prime = temp / norm
        if round(b_prime_s_prime, 2) > 1:
            print(f"b_prime_s_prime >= 1: {b_prime_s_prime}, a1:{a1}, s_prime:{s_prime}, o:{o}, pi2:{pi2}")
        assert round(b_prime_s_prime, 2) <= 1
        return b_prime_s_prime

    @staticmethod
    def next_belief(o: int, a1: int, b: npt.NDArray[np.float64], pi2: npt.NDArray[Any],
                    config: AptGameConfig, a2: int = 0, s: int = 0) -> npt.NDArray[np.float64]:
        """
        Computes the next belief using a Bayesian filter

        :param o: the latest observation
        :param a1: the latest action of player 1
        :param b: the current belief
        :param pi2: the policy of player 2
        :param config: the game config
        :param a2: the attacker action (for debugging, should be consistent with pi2)
        :param s: the true state (for debugging)
        :return: the new belief
        """
        b_prime = np.zeros(len(config.S))
        for s_prime in config.S:
            b_prime[s_prime] = AptGameUtil.bayes_filter(s_prime=s_prime, o=o, a1=a1, b=b, pi2=pi2, config=config)
        if round(sum(b_prime), 2) != 1:
            print(f"error, b_prime:{b_prime}, o:{o}, a1:{a1}, b:{b}, pi2:{pi2}, "
                  f"a2: {a2}, s:{s}, P[O|s]={config.Z[s][o]}, b[s]={b[s]}")
        assert round(sum(b_prime), 2) == 1
        return b_prime

    @staticmethod
    def sample_attacker_action(pi2: npt.NDArray[Any], s: int) -> int:
        """
        Samples the attacker action

        :param pi2: the attacker action
        :param s: the game state
        :return: a2 (the attacker action)
        """
        return int(np.random.choice(np.arange(0, len(pi2[s])), p=pi2[s]))

    @staticmethod
    def sample_defender_action(alpha: float, b: List[float]) -> int:
        """
        Samples the attacker action

        :param alpha: the defender threshold
        :param b: the belief state
        :return: a1 (the defender action)
        """
        if sum(b[1:]) >= alpha:
            return 1
        return 0

    @staticmethod
    def generate_transitions(game_config: AptGameConfig) -> List[str]:
        """
        Generates the transition rows of the POSG config file of HSVI

        :param game_config: the game configuration
        :return: list of transition rows
        """
        transitions = []
        for s in game_config.S:
            for a1 in game_config.A1:
                for a2 in game_config.A1:
                    for s_prime in game_config.S:
                        for i, _ in enumerate(game_config.O):
                            tr_prob = game_config.T[a1][a2][s][s_prime]
                            obs_prob = game_config.Z[s_prime][i]
                            prob = tr_prob * obs_prob
                            if prob > 0:
                                transition = f"{s} {a1} {a2} {i} {s_prime} {prob}"
                                transitions.append(transition)

        return transitions

    @staticmethod
    def generate_rewards(game_config: AptGameConfig) -> List[str]:
        """
        Generates the reward rows of the POSG config file of HSVI

        :param game_config: the game configuration
        :return: list of reward rows
        """
        rewards = []
        for s in game_config.S:
            for a1 in game_config.A1:
                for a2 in game_config.A2:
                    r = -game_config.C[a1][s]
                    if r != 0:
                        rew = f"{s} {a1} {a2} {r}"
                        rewards.append(rew)
        return rewards

    @staticmethod
    def generate_os_posg_game_file(game_config: AptGameConfig) -> str:
        """
        Generates the POSG game file for HSVI

        :param game_config: the game configuration
        :return: a string with the contents of the config file
        """
        num_partitions = 1
        transitions = AptGameUtil.generate_transitions(game_config=game_config)
        rewards = AptGameUtil.generate_rewards(game_config=game_config)
        game_description = f"{len(game_config.S)} {num_partitions} {len(game_config.A1)} {len(game_config.A2)} " \
                           f"{len(game_config.O)} {len(transitions)} " \
                           f"{len(rewards)} {game_config.gamma}"
        state_desriptions = []
        for s in game_config.S:
            state_desriptions.append(f"{s} {0}")
        player_1_actions = ["CONTINUE", "STOP"]
        player_2_actions = ["CONTINUE", "STOP"]

        player_2_legal_actions = []
        for _ in game_config.S:
            player_2_legal_actions.append(" ".join(list(map(lambda x: str(x), game_config.A2))))

        player_1_legal_actions = []
        player_1_legal_actions.append(" ".join(list(map(lambda x: str(x), game_config.A1))))

        obs_desriptions = []
        for i, o in enumerate(game_config.O):
            obs_desriptions.append(f"o_{o}")

        initial_belief_str = f"{0} {' '.join(list(map(lambda x: str(x), game_config.b1)))}"
        game_file_str = ""
        game_file_str = game_file_str + game_description + "\n"
        game_file_str = game_file_str + "\n".join(state_desriptions) + "\n"
        game_file_str = game_file_str + "\n".join(player_1_actions) + "\n"
        game_file_str = game_file_str + "\n".join(player_2_actions) + "\n"
        game_file_str = game_file_str + "\n".join(obs_desriptions) + "\n"
        game_file_str = game_file_str + "\n".join(player_2_legal_actions) + "\n"
        game_file_str = game_file_str + "\n".join(player_1_legal_actions) + "\n"
        game_file_str = game_file_str + "\n".join(transitions) + "\n"
        game_file_str = game_file_str + "\n".join(rewards) + "\n"
        game_file_str = game_file_str + initial_belief_str
        with open('apt_game.txt', 'w') as f:
            f.write(game_file_str)
        return game_file_str

    @staticmethod
    def expected_cost(C: List[List[float]], b: List[float], S: List[int], a1: int) -> float:
        """
        Gets the expected cost of defender action a1 in belief state b

        :param C: the cost tensor
        :param b: the belief state
        :param S: the state space
        :param a1: the defender action
        :return: the expected cost
        """
        cost = 0.0
        for s in S:
            cost += b[s] * C[a1][s]
        return cost
