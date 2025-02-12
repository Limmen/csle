from typing import Any, Tuple
import itertools
import numpy as np
import numpy.typing as npt
from scipy.stats import betabinom
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from csle_common.dao.training.policy import Policy


class StoppingGameUtil:
    """
    Class with utility functions for the StoppingGame Environment
    """

    @staticmethod
    def b1() -> npt.NDArray[np.float64]:
        """
        Gets the initial belief

        :return: the initial belief
        """
        return np.array([1.0, 0.0, 0.0])

    @staticmethod
    def state_space():
        """
        Gets the state space

        :return: the state space of the game
        """
        return np.array([0, 1, 2])

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
    def observation_space(n):
        """
        Returns the observation space of size n

        :param n: the maximum observation
        :return: the observation space
        """
        return np.array(list(range(n + 1)))

    @staticmethod
    def reward_tensor(R_SLA: int, R_INT: int, R_COST: int, L: int, R_ST: int) -> npt.NDArray[Any]:
        """
        Gets the reward tensor

        :param R_SLA: the R_SLA constant
        :param R_INT: the R_INT constant
        :param R_COST: the R_COST constant
        :param R_ST: the R_ST constant
        :return: a |L|x|A1|x|A2|x|S| tensor
        """

        R_l = []
        for l in range(1, L + 1):
            R = [
                # Defender continues
                [
                    # Attacker continues
                    [R_SLA, R_SLA + R_INT, 0],
                    # Attacker stops
                    [R_SLA, R_SLA, 0]
                ],
                # Defender stops
                [
                    # Attacker continues
                    [R_COST / l, R_ST / l, 0],
                    # Attacker stops
                    [R_COST / l, R_SLA, 0]
                ]
            ]
            R_l.append(R)
        return np.array(R_l)

    @staticmethod
    def transition_tensor(L: int) -> npt.NDArray[Any]:
        """
        Gets the transition tensor

        :param L: the maximum number of stop actions
        :return: a |L|x|A1|x|A2||S|^2 tensor
        """
        T_l = []
        for l in range(1, L + 1):
            if l == 1:
                T = [
                    # Defender continues
                    [
                        # Attacker continues
                        [
                            [1.0, 0.0, 0.0],  # No intrusion
                            [0.0, 1.0, 0.0],  # Intrusion
                            [0.0, 0.0, 1.0]  # Terminal
                        ],
                        # Attacker stops
                        [
                            [0.0, 1.0, 0.0],  # No intrusion
                            [0.0, 0.0, 1.0],  # Intrusion
                            [0.0, 0.0, 1.0]  # Terminal
                        ]
                    ],

                    # Defender stops
                    [
                        # Attacker continues
                        [
                            [0.0, 0.0, 1.0],  # No intrusion
                            [0.0, 0.0, 1.0],  # Intrusion
                            [0.0, 0.0, 1.0]  # Terminal
                        ],
                        # Attacker stops
                        [
                            [0.0, 0.0, 1.0],  # No Intrusion
                            [0.0, 0.0, 1.0],  # Intrusion
                            [0.0, 0.0, 1.0]  # Terminal
                        ]
                    ]
                ]
            else:
                T = [
                    # Defender continues
                    [
                        # Attacker continues
                        [
                            [1.0, 0.0, 0.0],  # No intrusion
                            [0.0, 1.0 - 1.0 / (2.0 * l), 1.0 / (2.0 * l)],  # Intrusion
                            [0.0, 0.0, 1.0]  # Terminal
                        ],
                        # Attacker stops
                        [
                            [0.0, 1.0, 0.0],  # No intrusion
                            [0.0, 0.0, 1.0],  # Intrusion
                            [0.0, 0.0, 1.0]  # Terminal
                        ]
                    ],

                    # Defender stops
                    [
                        # Attacker continues
                        [
                            [1.0, 0.0, 0.0],  # No intrusion
                            [0.0, 1.0 - 1.0 / (2.0 * l), 1.0 / (2.0 * l)],  # Intrusion
                            [0.0, 0.0, 1.0]  # Terminal
                        ],
                        # Attacker stops
                        [
                            [0.0, 1.0, 0.0],  # No Intrusion
                            [0.0, 0.0, 1.0],  # Intrusion
                            [0.0, 0.0, 1.0]  # Terminal
                        ]
                    ]
                ]
            T_l.append(T)
        return np.array(T_l)

    @staticmethod
    def observation_tensor(n):
        """
        :return: a |A1|x|A2|x|S|x|O| tensor
        """
        intrusion_dist = []
        no_intrusion_dist = []
        terminal_dist = np.zeros(n + 1)
        terminal_dist[-1] = 1
        intrusion_rv = betabinom(n=n, a=1, b=0.7)
        no_intrusion_rv = betabinom(n=n, a=0.7, b=3)
        for i in range(n + 1):
            intrusion_dist.append(intrusion_rv.pmf(i))
            no_intrusion_dist.append(no_intrusion_rv.pmf(i))
        Z = np.array(
            [
                [
                    [
                        no_intrusion_dist,
                        intrusion_dist,
                        terminal_dist
                    ],
                    [
                        no_intrusion_dist,
                        intrusion_dist,
                        terminal_dist
                    ],
                ],
                [
                    [
                        no_intrusion_dist,
                        intrusion_dist,
                        terminal_dist
                    ],
                    [
                        no_intrusion_dist,
                        intrusion_dist,
                        terminal_dist
                    ],
                ]
            ]
        )
        return Z

    @staticmethod
    def sample_next_state(T: npt.NDArray[Any], l: int, s: int, a1: int, a2: int, S: npt.NDArray[np.int32]) -> int:
        """
        Samples the next state

        :param T: the transition operator
        :param s: the currrent state
        :param a1: the defender action
        :param a2: the attacker action
        :param S: the state space
        :param l: the number of stops remaining
        :return: s'
        """
        state_probs = []
        for s_prime in S:
            state_probs.append(T[l - 1][a1][a2][s][s_prime])
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

        :param Z: observation tensor which include the observation probables
        :param s_prime: the new state
        :param O: the observation space
        :return: o
        """
        observation_probs = []
        for o in O:
            if len(Z.shape) == 4:
                observation_probs.append(Z[0][0][s_prime][o])
            elif len(Z.shape) == 3:
                observation_probs.append(Z[0][s_prime][o])
            elif len(Z.shape) == 2:
                observation_probs.append(Z[s_prime][o])
        o = np.random.choice(np.arange(0, len(O)), p=observation_probs)
        return int(o)

    @staticmethod
    def bayes_filter(s_prime: int, o: int, a1: int, b: npt.NDArray[np.float64], pi2: npt.NDArray[Any], l: int,
                     config: StoppingGameConfig) -> float:
        """
        A Bayesian filter to compute the belief of player 1
        of being in s_prime when observing o after taking action a in belief b given that the opponent follows
        strategy pi2

        :param s_prime: the state to compute the belief of
        :param o: the observation
        :param a1: the action of player 1
        :param b: the current belief point
        :param pi2: the policy of player 2
        :param l: stops remaining
        :return: b_prime(s_prime)
        """
        l = l - 1
        norm = 0
        for s in config.S:
            for a2 in config.A2:
                for s_prime_1 in config.S:
                    prob_1 = config.Z[a1][a2][s_prime_1][o]
                    norm += b[s] * prob_1 * config.T[l][a1][a2][s][s_prime_1] * pi2[s][a2]
        if norm == 0:
            return 0
        temp = 0

        for s in config.S:
            for a2 in config.A2:
                temp += config.Z[a1][a2][s_prime][o] * config.T[l][a1][a2][s][s_prime] * b[s] * pi2[s][a2]
        b_prime_s_prime = temp / norm
        if round(b_prime_s_prime, 2) > 1:
            print(f"b_prime_s_prime >= 1: {b_prime_s_prime}, a1:{a1}, s_prime:{s_prime}, l:{l}, o:{o}, pi2:{pi2}")
        assert round(b_prime_s_prime, 2) <= 1
        if s_prime == 2 and o != config.O[-1]:
            assert round(b_prime_s_prime, 2) <= 0.01
        return float(b_prime_s_prime)

    @staticmethod
    def next_belief(o: int, a1: int, b: npt.NDArray[np.float64], pi2: npt.NDArray[Any],
                    config: StoppingGameConfig, l: int, a2: int = 0, s: int = 0) -> npt.NDArray[np.float64]:
        """
        Computes the next belief using a Bayesian filter

        :param o: the latest observation
        :param a1: the latest action of player 1
        :param b: the current belief
        :param pi2: the policy of player 2
        :param config: the game config
        :param l: stops remaining
        :param a2: the attacker action (for debugging, should be consistent with pi2)
        :param s: the true state (for debugging)
        :return: the new belief
        """
        b_prime = np.zeros(len(config.S))
        for s_prime in config.S:
            b_prime[s_prime] = StoppingGameUtil.bayes_filter(s_prime=s_prime, o=o, a1=a1, b=b,
                                                             pi2=pi2, config=config, l=l)
        if round(sum(b_prime), 2) != 1:
            print(f"error, b_prime:{b_prime}, o:{o}, a1:{a1}, b:{b}, pi2:{pi2}, "
                  f"a2: {a2}, s:{s}")
        assert round(sum(b_prime), 2) == 1
        return b_prime

    @staticmethod
    def sample_attacker_action(pi2: npt.NDArray[Any], s: int) -> int:
        """
        Samples the attacker action

        :param pi2: the attacker policy
        :param s: the game state
        :return: a2 is the attacker action
        """
        return int(np.random.choice(np.arange(0, len(pi2[s])), p=pi2[s]))

    @staticmethod
    def pomdp_solver_file(config: StoppingGameConfig, discount_factor: float, pi2: npt.NDArray[Any]) -> str:
        """
        Gets the POMDP environment specification based on the format at http://www.pomdp.org/code/index.html,
        for the defender's local problem against a static attacker

        :param config: the POMDP config
        :param discount_factor: the discount factor
        :param pi2: the attacker strategy
        :return: the file content as a string
        """
        file_str = ""
        file_str = file_str + f"discount: {discount_factor}\n\n"
        file_str = file_str + "values: reward\n\n"
        file_str = file_str + f"states: {len(config.S)}\n\n"
        file_str = file_str + f"actions: {len(config.A1)}\n\n"
        file_str = file_str + f"observations: {len(config.O)}\n\n"
        initial_belief_str = " ".join(list(map(lambda x: str(x), config.b1)))
        file_str = file_str + f"start: {initial_belief_str}\n\n\n"
        num_transitions = 0
        for s in config.S:
            for a1 in config.A1:
                probs = []
                for s_prime in range(len(config.S)):
                    num_transitions += 1
                    prob = 0
                    for a2 in config.A2:
                        prob += config.T[0][a1][a2][s][s_prime] * pi2[s][a2]
                    file_str = file_str + f"T: {a1} : {s} : {s_prime} {prob:.80f}\n"
                    probs.append(prob)
                assert round(sum(probs), 3) == 1
        file_str = file_str + "\n\n"
        for a1 in config.A1:
            for s_prime in config.S:
                probs = []
                for o in range(len(config.O)):
                    prob = config.Z[0][0][s_prime][o]
                    file_str = file_str + f"O : {a1} : {s_prime} : {o} {prob:.80f}\n"
                    probs.append(prob)
                assert round(sum(probs), 3) == 1
        file_str = file_str + "\n\n"
        for s in config.S:
            for a1 in config.A1:
                for s_prime in config.S:
                    for o in config.O:
                        r = config.R[0][a1][0][s]
                        file_str = file_str + f"R: {a1} : {s} : {s_prime} : {o} {r:.80f}\n"
        return file_str

    @staticmethod
    def reduce_T_attacker(T: npt.NDArray[np.float64], strategy: Policy) -> npt.NDArray[np.float64]:
        """
        Reduces the transition tensor based on a given attacker strategy

        :param T: the tensor to reduce
        :param strategy: the strategy to use for the reduction
        :return: the reduced tensor (|A1|x|S|x|S|)
        """
        if len(T.shape) == 5:
            T = T[0]
        reduced_T = np.zeros((T.shape[0], T.shape[2], T.shape[3]))
        for i in range(T.shape[0]):
            for j in range(T.shape[2]):
                for k in range(T.shape[3]):
                    reduced_T[i][j][k] = T[i][0][j][k] * strategy.probability(j, 0) + T[i][1][j][
                        k] * strategy.probability(j, 1)
                    # if j == 0:
                    #     reduced_T[i][j][k] = T[i][0][j][k] * strategy.probability(j, 0) + T[i][1][j][
                    #         k] * strategy.probability(j, 1)
                    # else:
                    #     reduced_T[i][j][k] = (T[i][0][j][k] * (1 - strategy.probability(j, 0)) + T[i][1][j][k] *
                    #                           strategy.probability(j, 1))
        return reduced_T

    @staticmethod
    def reduce_R_attacker(R: npt.NDArray[np.float64], strategy: Policy) -> npt.NDArray[np.float64]:
        """
        Reduces the reward tensor based on a given attacker strategy

        :param R: the reward tensor to reduce
        :param strategy: the strategy to use for the reduction
        :return: the reduced reward tensor (|A1|x|S|)
        """
        if len(R.shape) == 4:
            R = R[0]
        reduced_R = np.zeros((R.shape[0], R.shape[2]))
        for i in range(R.shape[0]):
            for j in range(R.shape[2]):
                reduced_R[i][j] = (R[i][0][j] * strategy.probability(j, 0) + R[i][1][j] *
                                   strategy.probability(j, 1))
        return reduced_R

    @staticmethod
    def reduce_Z_attacker(Z: npt.NDArray[np.float64], strategy: Policy) -> npt.NDArray[np.float64]:
        """
        Reduces the observation tensor based on a given attacker strategy

        :param Z: the observation tensor to reduce
        :param strategy: the strategy to use for the reduction
        :return: the reduced observation tensor (|A1|x|S|x|O|)
        """
        reduced_Z = np.zeros((Z.shape[0], Z.shape[2], Z.shape[3]))
        for i in range(Z.shape[0]):
            for j in range(Z.shape[2]):
                for k in range(Z.shape[3]):
                    reduced_Z[i][j][k] = Z[i][0][j][k] * strategy.probability(j, 0) + Z[i][1][j][
                        k] * strategy.probability(j, 1)
        return reduced_Z

    @staticmethod
    def reduce_T_defender(T: npt.NDArray[np.float64], strategy: Policy) -> npt.NDArray[np.float64]:
        """
        Reduces the transition tensor based on a given defender strategy

        :param T: the tensor to reduce
        :param strategy: the strategy to use for the reduction
        :return: the reduced tensor (|A2|x|S|x|S|)
        """
        if len(T.shape) == 5:
            T = T[0]
        reduced_T = np.zeros((T.shape[1], T.shape[2], T.shape[3]))
        for i in range(T.shape[1]):
            for j in range(T.shape[2]):
                for k in range(T.shape[3]):
                    reduced_T[i][j][k] = (T[0][i][j][k] * strategy.probability(j, 0) + T[1][i][j][k]
                                          * strategy.probability(j, 1))
        return reduced_T

    @staticmethod
    def reduce_R_defender(R: npt.NDArray[np.float64], strategy: Policy) -> npt.NDArray[np.float64]:
        """
        Reduces the reward tensor based on a given defender strategy

        :param R: the reward tensor to reduce
        :param strategy: the strategy to use for the reduction
        :return: the reduced reward tensor (|A2|x|S|)
        """
        if len(R.shape) == 4:
            R = R[0]
        reduced_R = np.zeros((R.shape[1], R.shape[2]))
        for i in range(R.shape[1]):
            for j in range(R.shape[2]):
                reduced_R[i][j] = (R[0][i][j] * strategy.probability(j, 0) + R[1][i][j] *
                                   strategy.probability(j, 1))
        return reduced_R

    @staticmethod
    def aggregate_belief_mdp_defender(aggregation_resolution: int, T: npt.NDArray[np.float64],
                                      R: npt.NDArray[np.float64], Z: npt.NDArray[np.float64],
                                      S: npt.NDArray[np.int32], A: npt.NDArray[np.int32], O: npt.NDArray[np.int32]) \
            -> Tuple[npt.NDArray[np.float64], npt.NDArray[np.int32], npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        """
        Generates an aggregate belief MDP from a given POMDP specification and aggregation resolution

        :param aggregation_resolution: the belief aggregation resolution
        :param T: the transition tensor of the POMDP
        :param R: the reward tensor of the POMDP
        :param Z: the observation tensor of the POMDP
        :param S: the state space of the POMDP
        :param A: the action space of the POMDP
        :param O: the observation space of the POMDP
        :return: the state space, action space, transition operator, and belief operator of the belief MDP
        """
        aggregate_belief_space = StoppingGameUtil.generate_aggregate_belief_space(
            n=aggregation_resolution, belief_space_dimension=len(S))
        belief_T = StoppingGameUtil.generate_aggregate_belief_transition_operator(
            aggregate_belief_space=aggregate_belief_space, S=S, A=A, O=O, T=T, Z=Z)
        belief_R = StoppingGameUtil.generate_aggregate_belief_reward_tensor(
            aggregate_belief_space=aggregate_belief_space, S=S, A=A, R=R)
        return aggregate_belief_space, A, belief_T, belief_R

    @staticmethod
    def generate_aggregate_belief_space(n: int, belief_space_dimension: int) -> npt.NDArray[np.float64]:
        """
        Generate an aggregate belief space B_n.

        :param n: the aggregation resolution
        :param belief_space_dimension: the belief space dimension
        :return: the aggregate belief space
        """

        # Generate all combinations of integer allocations k_i such that sum(k_i) = n
        combinations = [k for k in itertools.product(range(n + 1), repeat=belief_space_dimension) if sum(k) == n]

        # Convert integer allocations to belief points by dividing each k_i by n
        belief_points = [list(k_i / n for k_i in k) for k in combinations]

        # Remove all beliefs that violate the stopping dynamics
        belief_points = list(filter(lambda x: x[-1] == 1.0 or x[-1] == 0.0, belief_points))

        return np.array(belief_points)

    @staticmethod
    def generate_aggregate_belief_reward_tensor(
            aggregate_belief_space: npt.NDArray[np.float64], S: npt.NDArray[np.int32], A: npt.NDArray[np.int32],
            R: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """
        Generates an aggregate reward tensor for the aggregate belief MDP

        :param aggregate_belief_space: the aggregate belief space
        :param S: the state space of the POMDP
        :param A: the action space of the POMDP
        :param R: the reward tensor of the POMDP
        :return: the reward tensor of the aggregate belief MDP
        """
        belief_R = np.zeros((len(A), len(aggregate_belief_space)))
        belief_space_list = aggregate_belief_space.tolist()
        for a in A:
            for b in aggregate_belief_space:
                expected_reward = 0
                for s in S:
                    expected_reward += R[a][s] * b[s]
                belief_R[a][belief_space_list.index(b.tolist())] = expected_reward
        return belief_R

    @staticmethod
    def generate_aggregate_belief_transition_operator(
            aggregate_belief_space: npt.NDArray[np.float64], S: npt.NDArray[np.int32], A: npt.NDArray[np.int32],
            O: npt.NDArray[np.int32], T: npt.NDArray[np.float64], Z: npt.NDArray[np.float64]) \
            -> npt.NDArray[np.float64]:
        """
        Generates an aggregate belief space transition operator

        :param aggregate_belief_space: the aggregate belief space
        :param O: the observation space of the POMDP
        :param S: the state space of the POMDP
        :param A: the action space of the POMDP
        :param T: the transition operator of the POMDP
        :param Z: the observation tensor of the POMDP
        :return: the aggregate belief space operator
        """
        belief_space_list = aggregate_belief_space.tolist()
        belief_T = np.zeros((len(A), len(aggregate_belief_space), len(aggregate_belief_space)))
        for a in A:
            for b1 in aggregate_belief_space:
                for b2 in aggregate_belief_space:
                    belief_T[a][belief_space_list.index(b1.tolist())][belief_space_list.index(b2.tolist())] \
                        = StoppingGameUtil.aggregate_belief_transition_probability(
                        b1=b1, b2=b2, a=a, S=S, O=O, T=T, Z=Z, aggregate_belief_space=aggregate_belief_space, A=A)
        return belief_T

    @staticmethod
    def aggregate_belief_transition_probability(b1: npt.NDArray[np.float64], b2: npt.NDArray[np.float64], a: int,
                                                S: npt.NDArray[np.int32], O: npt.NDArray[np.int32],
                                                A: npt.NDArray[np.int32],
                                                T: npt.NDArray[np.float64], Z: npt.NDArray[np.float64],
                                                aggregate_belief_space: npt.NDArray[np.float64]) -> float:
        """
        Calculates the probability of transitioning from belief b1 to belief b2 when taking action a

        :param b1: the source belief
        :param b2: the target belief
        :param a: the action
        :param S: the state space of the POMDP
        :param O: the observation space of the POMDP
        :param A: the action space of the POMDP
        :param T: the transition operator
        :param Z: the observation tensor
        :param aggregate_belief_space: the aggregate belief space
        :return: the probability P(b2 | b1, a)
        """
        prob = 0
        for o in O:
            if sum([Z[a][s_prime][o] * b1[s] * T[a][s][s_prime] for s in S for s_prime in S]) == 0:
                continue
            b_prime = StoppingGameUtil.pomdp_next_belief(
                o=o, a=a, b=b1, states=S, observations=O, observation_tensor=Z, transition_tensor=T)
            nearest_neighbor = StoppingGameUtil.find_nearest_neighbor_belief(belief_space=aggregate_belief_space,
                                                                             target_belief=b_prime)
            if np.array_equal(nearest_neighbor, b2):
                for s in S:
                    for s_prime in S:
                        prob += Z[a][s_prime][o] * b1[s] * T[a][s][s_prime]
        return prob

    @staticmethod
    def pomdp_next_belief(o: int, a: int, b: npt.NDArray[np.float64], states: npt.NDArray[np.int32],
                          observations: npt.NDArray[np.int32], observation_tensor: npt.NDArray[np.float64],
                          transition_tensor: npt.NDArray[np.float64]) \
            -> npt.NDArray[np.float64]:
        """
        Computes the next belief of the POMDP using a Bayesian filter

        :param o: the latest observation
        :param a: the latest action of player 1
        :param b: the current belief
        :param states: the list of states
        :param observations: the list of observations
        :param observation_tensor: the observation tensor
        :param transition_tensor: the transition tensor
        :return: the new belief
        """
        b_prime = [0.0] * len(states)
        for s_prime in states:
            b_prime[s_prime] = StoppingGameUtil.pomdp_bayes_filter(
                s_prime=s_prime, o=o, a=a, b=b, states=states, observations=observations,
                transition_tensor=transition_tensor, observation_tensor=observation_tensor)
        if round(sum(b_prime), 2) != 1:
            print(f"error, b_prime:{b_prime}, o:{o}, a:{a}, b:{b}")
        assert round(sum(b_prime), 2) == 1
        return np.array(b_prime)

    @staticmethod
    def pomdp_bayes_filter(s_prime: int, o: int, a: int, b: npt.NDArray[np.float64], states: npt.NDArray[np.int32],
                           observations: npt.NDArray[np.int32], observation_tensor: npt.NDArray[np.float64],
                           transition_tensor: npt.NDArray[np.float64]) -> float:
        """
        A Bayesian filter to compute b[s_prime] of the POMDP

        :param s_prime: the state to compute the belief for
        :param o: the latest observation
        :param a: the latest action
        :param b: the current belief
        :param states: the list of states
        :param observations: the list of observations
        :param observation_tensor: the observation tensor
        :param transition_tensor: the transition tensor of the POMDP
        :return: b[s_prime]
        """
        norm = 0.0
        for s in states:
            for s_prime_1 in states:
                prob_1 = observation_tensor[a][s_prime_1][o]
                norm += b[s] * prob_1 * transition_tensor[a][s][s_prime_1]
        if norm == 0.0:
            print(f"zero norm, a: {a}, b: {b}, o: {o}")
            return 0.0
        temp = 0.0

        for s in states:
            temp += observation_tensor[a][s_prime][o] * transition_tensor[a][s][s_prime] * b[s]
        b_prime_s_prime = temp / norm
        if round(b_prime_s_prime, 2) > 1:
            print(f"b_prime_s_prime >= 1: {b_prime_s_prime}, a1:{a}, s_prime:{s_prime}")
        assert round(b_prime_s_prime, 2) <= 1
        if s_prime == 2 and o != observations[-1]:
            assert round(b_prime_s_prime, 2) <= 0.01
        return b_prime_s_prime

    @staticmethod
    def find_nearest_neighbor_belief(belief_space: npt.NDArray[np.float64], target_belief: npt.NDArray[np.float64]) \
            -> npt.NDArray[np.float64]:
        """
        Finds the nearest neighbor (in the Euclidean sense) of a given belief in a certain belief space

        :param belief_space: the belief to search from
        :param target_belief: the belief to find the nearest neighbor of
        :return: the nearest neighbor belief from the belief space
        """

        # Compute Euclidean distances between the target belief and all points in the belief space
        distances = np.linalg.norm(belief_space - target_belief, axis=1)

        # Find the index of the minimum distance (break ties consistently by choosing the smallest index)
        nearest_index = int(np.argmin(distances))

        return np.array(belief_space[nearest_index])
