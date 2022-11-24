from typing import List, Dict, Tuple
import numpy as np
from scipy.stats import betabinom
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.simulation_config.observation_space_config import ObservationSpaceConfig
from csle_common.dao.simulation_config.joint_action_space_config import JointActionSpaceConfig
from csle_common.dao.simulation_config.state_space_config import StateSpaceConfig
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig


class StoppingGameUtil:
    """
    Class with utility functions for the StoppingGame Environment
    """

    @staticmethod
    def b1() -> np.ndarray:
        """
        :return: the initial belief
        """
        return np.array([1, 0, 0])

    @staticmethod
    def state_space():
        return np.array([0, 1, 2])

    @staticmethod
    def defender_actions() -> np.ndarray:
        """
        :return: the action space of the defender
        """
        return np.array([0, 1])

    @staticmethod
    def attacker_actions() -> np.ndarray:
        """
        :return: the action space of the attacker
        """
        return np.array([0, 1])

    @staticmethod
    def observation_space(n):
        """
        Returns the observation space of size n

        :param n: the maximum observation
        :return: O
        """
        return np.array(list(range(n + 1)))

    @staticmethod
    def reward_tensor(R_SLA: int, R_INT: int, R_COST: int, L: int, R_ST: int) -> np.ndarray:
        """
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
        R = np.array(R_l)
        return R

    @staticmethod
    def transition_tensor(L: int, p: float) -> np.ndarray:
        """
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
                            [1, 0, 0],  # No intrusion
                            [0, 1 - 1 / (2 * l), 1 / (2 * l)],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ],
                        # Attacker stops
                        [
                            [0, 1, 0],  # No intrusion
                            [0, 0, 1],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ]
                    ],

                    # Defender stops
                    [
                        # Attacker continues
                        [
                            [0, 0, 1],  # No intrusion
                            [0, 0, 1],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ],
                        # Attacker stops
                        [
                            [0, 0, 1],  # No Intrusion
                            [0, 0, 1],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ]
                    ]
                ]
            else:
                T = [
                    # Defender continues
                    [
                        # Attacker continues
                        [
                            [1, 0, 0],  # No intrusion
                            [0, 1 - 1 / (2 * l), 1 / (2 * l)],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ],
                        # Attacker stops
                        [
                            [0, 1, 0],  # No intrusion
                            [0, 0, 1],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ]
                    ],

                    # Defender stops
                    [
                        # Attacker continues
                        [
                            [1, 0, 0],  # No intrusion
                            [0, 1 - 1 / (2 * l), 1 / (2 * l)],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ],
                        # Attacker stops
                        [
                            [0, 1, 0],  # No Intrusion
                            [0, 0, 1],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ]
                    ]
                ]
            T_l.append(T)
        T = np.array(T_l)
        return T

    @staticmethod
    def observation_tensor_from_emulation_statistics(emulation_statistic: EmulationStatistics,
                                                     observation_space_defender: ObservationSpaceConfig,
                                                     joint_action_space: JointActionSpaceConfig,
                                                     state_space: StateSpaceConfig) \
            -> Tuple[np.ndarray, Dict[str, List]]:
        """
        Returns an observation tensor based on measured emulation statistics

        :param emulation_statistic: the measured statistics
        :param observation_space_defender: the observation space of the defender
        :param joint_action_space: the joint action space
        :param state_space: the state space
        :return: a |A1|x|A2|x|S|x|O| tensor
        """
        intrusion_severe_alerts_probabilities = []
        intrusion_warning_alerts_probabilities = []
        intrusion_login_attempts_probabilities = []
        norm = sum(emulation_statistic.conditionals_counts["intrusion"]["severe_alerts"].values())
        for severe_alert_obs in observation_space_defender.component_observations["severe_alerts"]:
            count = emulation_statistic.conditionals_counts["intrusion"]["severe_alerts"][severe_alert_obs.id]
            intrusion_severe_alerts_probabilities.append(count / norm)
        for warning_alert_obs in observation_space_defender.component_observations["warning_alerts"]:
            count = emulation_statistic.conditionals_counts["intrusion"]["warning_alerts"][warning_alert_obs.id]
            intrusion_warning_alerts_probabilities.append(count / norm)
        for login_attempt_obs in observation_space_defender.component_observations["login_attempts"]:
            count = emulation_statistic.conditionals_counts["intrusion"]["login_attempts"][login_attempt_obs.id]
            intrusion_login_attempts_probabilities.append(count / norm)

        no_intrusion_severe_alerts_probabilities = []
        no_intrusion_warning_alerts_probabilities = []
        no_intrusion_login_attempts_probabilities = []
        norm = sum(emulation_statistic.conditionals_counts["no_intrusion"]["severe_alerts"].values())
        for severe_alert_obs in observation_space_defender.component_observations["severe_alerts"]:
            count = emulation_statistic.conditionals_counts["no_intrusion"]["severe_alerts"][severe_alert_obs.id]
            no_intrusion_severe_alerts_probabilities.append(count / norm)
        for warning_alert_obs in observation_space_defender.component_observations["warning_alerts"]:
            count = emulation_statistic.conditionals_counts["no_intrusion"]["warning_alerts"][warning_alert_obs.id]
            no_intrusion_warning_alerts_probabilities.append(count / norm)
        for login_attempt_obs in observation_space_defender.component_observations["login_attempts"]:
            count = emulation_statistic.conditionals_counts["no_intrusion"]["login_attempts"][login_attempt_obs.id]
            no_intrusion_login_attempts_probabilities.append(count / norm)

        component_observation_tensors = {}
        observation_tensor = []
        severe_alerts_tensor = []
        warning_alerts_tensor = []
        login_attempts_tensor = []
        for a1 in range(len(joint_action_space.action_spaces[0].actions)):
            a1_a2_s_o_dist = []
            severe_alerts_a1_a2_s_o_dist = []
            warning_alerts_a1_a2_s_o_dist = []
            login_attempts_a1_a2_s_o_dist = []
            for a2 in range(len(joint_action_space.action_spaces[1].actions)):
                a2_s_o_dist = []
                severe_alerts_a2_s_o_dist = []
                warning_alerts_a2_s_o_dist = []
                login_attempts_a2_s_o_dist = []
                for s in range(len(state_space.states)):
                    s_o_dist = []
                    severe_alerts_s_o_dist = []
                    warning_alerts_s_o_dist = []
                    login_attempts_s_o_dist = []
                    for o in range(len(observation_space_defender.observations)):
                        obs_vector = observation_space_defender.observation_id_to_observation_id_vector[o]
                        if s == 0:
                            severe_alerts_s_o_dist.append(no_intrusion_severe_alerts_probabilities[obs_vector[0]])
                            warning_alerts_s_o_dist.append(no_intrusion_warning_alerts_probabilities[obs_vector[0]])
                            login_attempts_s_o_dist.append(no_intrusion_login_attempts_probabilities[obs_vector[0]])
                            p = (no_intrusion_severe_alerts_probabilities[obs_vector[0]] *
                                 no_intrusion_warning_alerts_probabilities[obs_vector[1]] *
                                 no_intrusion_login_attempts_probabilities[obs_vector[2]])
                        else:
                            severe_alerts_s_o_dist.append(intrusion_severe_alerts_probabilities[obs_vector[0]])
                            warning_alerts_s_o_dist.append(intrusion_warning_alerts_probabilities[obs_vector[0]])
                            login_attempts_s_o_dist.append(intrusion_login_attempts_probabilities[obs_vector[0]])
                            p = (intrusion_severe_alerts_probabilities[obs_vector[0]] *
                                 intrusion_warning_alerts_probabilities[obs_vector[1]] *
                                 intrusion_login_attempts_probabilities[obs_vector[2]])
                        s_o_dist.append(p)
                    a2_s_o_dist.append(s_o_dist)
                    severe_alerts_a2_s_o_dist.append(severe_alerts_s_o_dist)
                    warning_alerts_a2_s_o_dist.append(warning_alerts_a2_s_o_dist)
                    login_attempts_a2_s_o_dist.append(login_attempts_a2_s_o_dist)
                a1_a2_s_o_dist.append(a2_s_o_dist)
                severe_alerts_a1_a2_s_o_dist.append(severe_alerts_a2_s_o_dist)
                warning_alerts_a1_a2_s_o_dist.append(warning_alerts_a2_s_o_dist)
                login_attempts_a1_a2_s_o_dist.append(login_attempts_a2_s_o_dist)
            observation_tensor.append(a1_a2_s_o_dist)
            severe_alerts_tensor.append(severe_alerts_a1_a2_s_o_dist)
            warning_alerts_tensor.append(warning_alerts_a1_a2_s_o_dist)
            login_attempts_tensor.append(login_attempts_a1_a2_s_o_dist)
        component_observation_tensors["severe_alerts"] = severe_alerts_tensor
        component_observation_tensors["warning_alerts"] = warning_alerts_tensor
        component_observation_tensors["login_attempts"] = login_attempts_tensor
        return np.array(observation_tensor), component_observation_tensors

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
    def sample_next_state(T: np.ndarray, l: int, s: int, a1: int, a2: int, S: np.ndarray) -> int:
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
        s_prime = np.random.choice(np.arange(0, len(S)), p=state_probs)
        return s_prime

    @staticmethod
    def sample_initial_state(b1: np.ndarray) -> int:
        """
        Samples the initial state

        :param b1: the initial belief
        :return: s1
        """
        s1 = np.random.choice(np.arange(0, len(b1)), p=b1)
        return s1

    @staticmethod
    def sample_next_observation(Z: np.ndarray, s_prime: int, O: np.ndarray) -> int:
        """
        Samples the next observation

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
    def bayes_filter(s_prime: int, o: int, a1: int, b: np.ndarray, pi2: np.ndarray, l: int,
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
        return b_prime_s_prime

    @staticmethod
    def p_o_given_b_a1_a2(o: int, b: List, a1: int, a2: int, config: StoppingGameConfig) -> float:
        """
        Computes P[o|a,b]

        :param o: the observation
        :param b: the belief point
        :param a1: the action of player 1
        :param a2: the action of player 2
        :param config: the game config
        :return: the probability of observing o when taking action a in belief point b
        """
        prob = 0
        for s in config.S:
            for s_prime in config.S:
                prob += b[s] * config.T[a1][a2][s][s_prime] * config.Z[a1][a2][s_prime][o]
        assert prob < 1
        return prob

    @staticmethod
    def next_belief(o: int, a1: int, b: np.ndarray, pi2: np.ndarray, config: StoppingGameConfig, l: int,
                    a2: int = 0, s: int = 0) -> np.ndarray:
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
    def sample_attacker_action(pi2: np.ndarray, s: int) -> int:
        """
        Samples the attacker action

        :param pi2: the attacker action
        :param s: the game state
        :return: a2 (the attacker action
        """
        a2 = np.random.choice(np.arange(0, len(pi2[s])), p=pi2[s])
        return a2
