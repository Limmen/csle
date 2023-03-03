from typing import List
import numpy as np
from scipy.stats import betabinom
from gym_csle_intrusion_response_game.dao.intrusion_response_game_config import LocalIntrusionResponseGameConfig
import gym_csle_intrusion_response_game.constants.constants as env_constants


class IntrusionResponseGameUtil:
    """
    Class with utility functions for the intrusion response game environment
    """

    @staticmethod
    def is_local_state_terminal(s: np.ndarray) -> bool:
        """
        Utility function for checking if a local state is terminal or not

        :param s: the local state to check
        :return: True if terminal, otherwise False
        """
        return s[env_constants.STATES.D_STATE_INDEX] == -1 and s[env_constants.STATES.A_STATE_INDEX] == -1

    @staticmethod
    def is_local_state_in_zone(s: np.ndarray, zone: int) -> bool:
        """
        Utility function for checking if a local state is in a given zone or not

        :param s: the local state to check
        :param zone: the zone to check
        :return: True if the state is in the given zone, false otherwise
        """
        return s[env_constants.STATES.D_STATE_INDEX] == zone

    @staticmethod
    def is_local_state_compromised(s: np.ndarray) -> bool:
        """
        Utility function for checking if a local state has been compromised

        :param s: the local state to check
        :return: True if compromised, otherwise False
        """
        return s[env_constants.STATES.A_STATE_INDEX] == env_constants.ATTACK_STATES.COMPROMISED

    @staticmethod
    def is_local_state_healthy(s: np.ndarray) -> bool:
        """
        Utility function for checking if a local state is healthy and not discovered nor compromised

        :param s: the local state to check
        :return: True if compromised, otherwise False
        """
        return s[env_constants.STATES.A_STATE_INDEX] == env_constants.ATTACK_STATES.HEALTHY

    @staticmethod
    def is_local_state_recon(s: np.ndarray) -> bool:
        """
        Utility function for checking if a local state has been discovered by the attacker

        :param s: the local state to check
        :return: True if compromised, otherwise False
        """
        return s[env_constants.STATES.A_STATE_INDEX] == env_constants.ATTACK_STATES.RECON

    @staticmethod
    def are_local_states_equal(s: np.ndarray, s_prime: np.ndarray) -> bool:
        """
        Utility function for checking if two local states are equal

        :param s: the first local state to check
        :param s_prime: the second local state to check
        :return: True if equal, otherwise False
        """
        return s[env_constants.STATES.D_STATE_INDEX] == s_prime[env_constants.STATES.D_STATE_INDEX] and s[
            env_constants.STATES.A_STATE_INDEX] == s_prime[env_constants.STATES.A_STATE_INDEX]

    @staticmethod
    def are_local_defense_states_equal(s: np.ndarray, s_prime: np.ndarray) -> bool:
        """
        Utility function for checking if two local defense states are equal

        :param s: the first local state to check
        :param s_prime: the second local state to check
        :return: True if equal, otherwise False
        """
        return s[env_constants.STATES.D_STATE_INDEX] == s_prime[env_constants.STATES.D_STATE_INDEX]

    @staticmethod
    def are_local_attack_states_equal(s: np.ndarray, s_prime: np.ndarray) -> bool:
        """
        Utility function for checking if two local attack states are equal

        :param s: the first local state to check
        :param s_prime: the second local state to check
        :return: True if equal, otherwise False
        """
        return s[env_constants.STATES.A_STATE_INDEX] == s_prime[env_constants.STATES.A_STATE_INDEX]

    @staticmethod
    def local_initial_state(initial_zone: int, S: np.ndarray) -> np.ndarray:
        """
        Gets the initial state for a local version of the game

        :param initial_zone: the initial zone of the local node
        :param S: the state space of the local game
        :return: the initial state belief
        """
        for i in range(len(S)):
            if IntrusionResponseGameUtil.is_local_state_in_zone(s=S[i][0], zone=initial_zone) and \
                    IntrusionResponseGameUtil.is_local_state_healthy(s=S[i][1]):
                return S[i]
        raise ValueError("Initial state not recognized")

    @staticmethod
    def local_initial_state_idx(initial_zone: int, S: np.ndarray) -> int:
        """
        Gets the initial state for a local version of the game

        :param initial_zone: the initial zone of the local node
        :param S: the state space of the local game
        :return: the initial state belief
        """
        for i in range(len(S)):
            if IntrusionResponseGameUtil.is_local_state_in_zone(s=S[i], zone=initial_zone) and \
                    IntrusionResponseGameUtil.is_local_state_healthy(s=S[i]):
                return i
        raise ValueError("Initial state not recognized")

    @staticmethod
    def local_initial_state_distribution(initial_state_idx, S: np.ndarray) -> np.ndarray:
        """
        Gets the initial state distribution

        :param initial_state_idx: the initial state index
        :param S: the state space
        :return: the initial state distribution
        """
        rho = np.zeros((len(S),))
        rho[initial_state_idx] = 1
        return rho

    @staticmethod
    def local_initial_defender_belief(S_A: np.ndarray) -> np.ndarray:
        """
        Gets the initial defender belief for a local version of the game

        :param S_A: the attacker's state space of the local game
        :return: the initial defender belief
        """
        d_b1 = np.zeros((len(S_A),))
        d_b1[env_constants.ATTACK_STATES.HEALTHY] = 1  # the node is not compromised or discovered initially
        return d_b1

    @staticmethod
    def local_initial_attacker_belief(S_D: np.ndarray) -> np.ndarray:
        """
        Gets the initial attacker belief for a local version of the game

        :param S_D: the defender's state space of the local game
        :return: the initial defender belief
        """
        d_b1 = np.zeros((len(S_D),))
        for i in range(len(S_D)):
            d_b1[i] = 1 / len(S_D)  # The attacker has no clue about the zones initially
        return d_b1

    @staticmethod
    def local_state_space(number_of_zones: int) -> np.ndarray:
        """
        Gets the state space of the local version of the game

        :param number_of_zones: the number of zones in the network
        :return: the state space
        """
        S = []
        S.append(env_constants.STATES.TERMINAL_STATE)
        for i in range(1, number_of_zones + 1):
            S.append([i, env_constants.ATTACK_STATES.HEALTHY])
            S.append([i, env_constants.ATTACK_STATES.RECON])
            S.append([i, env_constants.ATTACK_STATES.COMPROMISED])
        return np.array(S)

    @staticmethod
    def local_defender_state_space(number_of_zones: int) -> np.ndarray:
        """
        Gets the defender state space of the local version of the game

        :param number_of_zones: the number of zones in the network
        :return: the local defender state space
        """
        S = []
        for i in range(1, number_of_zones + 1):
            S.append(i)
        return np.array(S)

    @staticmethod
    def local_attacker_state_space() -> np.ndarray:
        """
        Gets the attacker state space of the local version of the game

        :return: the local attacker state space
        """
        S = []
        S.append(env_constants.ATTACK_STATES.HEALTHY)
        S.append(env_constants.ATTACK_STATES.RECON)
        S.append(env_constants.ATTACK_STATES.COMPROMISED)
        return np.array(S)

    @staticmethod
    def local_defender_actions(number_of_zones: int) -> np.ndarray:
        """
        Gets the defender's action space in the local version of the game

        :param number_of_zones: the number of zones in the game
        :return: a vector with the actions of the defender
        """
        return np.array(list(range(number_of_zones + 1)))

    @staticmethod
    def local_attacker_actions() -> np.ndarray:
        """
        Gets the attacker's action space in the local version of the game

        :return: a vector with the actions of the defender
        """
        return np.array([env_constants.ATTACKER_ACTIONS.WAIT, env_constants.ATTACKER_ACTIONS.RECON,
                         env_constants.ATTACKER_ACTIONS.BRUTE_FORCE, env_constants.ATTACKER_ACTIONS.EXPLOIT])

    @staticmethod
    def local_observation_space(X_max: int) -> np.ndarray:
        """
        Gets the observation space of the local version of the game

        :param X_max: the maximum observation
        :return: a vector with all possible observations
        """
        return np.array(list(range(X_max)))

    @staticmethod
    def local_workflow_utility(beta: float, reachable: bool, s: np.ndarray, initial_zone: int) -> float:
        """
        The local utility function for workflow QoS

        :param beta: a scaling parameter indicating how important the workflow is
        :param reachable: a boolean flag indicating whether the node is reachable from the public gateway or not
        :param s: the local state vector
        :param initial_zone: the initial zone of the node in the local version of the game
        :return: the workflow utility
        """
        impact = 0
        if reachable and not IntrusionResponseGameUtil.is_local_state_compromised(s):
            impact = 1
        return beta * impact * int(IntrusionResponseGameUtil.is_local_state_in_zone(s=s, zone=initial_zone))

    @staticmethod
    def constant_defender_action_costs(A1: np.ndarray, constant_cost: float) -> np.ndarray:
        """
        Returns a vector with the local defender action costs where each action has the same constant cost

        :param A1: a vector with the actions of the defender in the local game
        :param constant_cost: the constant action cost
        :return: a vector with the action costs
        """
        action_costs = []
        for a1 in A1:
            if a1 == env_constants.DEFENDER_ACTIONS.WAIT:
                action_costs.append(0)
            else:
                action_costs.append(constant_cost)
        return np.array(action_costs)

    @staticmethod
    def zones(num_zones: int) -> np.ndarray:
        """
        Gets the vector with the network zones

        :param num_zones: the number of zones
        :return: a vector with the zones
        """
        return np.array(list(range(1, num_zones + 1)))

    @staticmethod
    def constant_zone_utilities(zones: np.ndarray, constant_utility: float) -> np.ndarray:
        """
        Returns a vector with the zone utilities where each zone has the same constant utility

        :param zones: the vector with zones
        :param constant_utility: the constant utility of a zone
        :return: the vector with zone utilities
        """
        Z_U = []
        for z in zones:
            Z_U.append(constant_utility)
        return np.array(Z_U)

    @staticmethod
    def uniform_zone_detection_probabilities(zones: np.ndarray) -> np.ndarray:
        """
        Returns a vector with the zone detection probabilities where each zone as the same uniform detection
        probability

        :param zones: the vector with zones
        :return: the vector with zone detection probabilities
        """
        zone_detection_probabilities = []
        for z in zones:
            zone_detection_probabilities.append(1 / len(zones))
        return np.array(zone_detection_probabilities)

    @staticmethod
    def local_attack_success_probabilities_uniform(p: float, A2: np.ndarray) -> np.ndarray:
        """
        Returns a vector with the success probabilities of the attacker actions for the local version of the game
        where the attacks have the same constant success probability

        :param A2: the local action space of the attacker
        :return: a vector with the attack success probabilities
        """
        assert p <= 1
        assert p >= 0
        A_P = np.zeros((len(A2),))
        A_P[env_constants.ATTACKER_ACTIONS.WAIT] = 1
        A_P[env_constants.ATTACKER_ACTIONS.RECON] = 1
        A_P[env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] = p
        A_P[env_constants.ATTACKER_ACTIONS.EXPLOIT] = p
        return A_P

    @staticmethod
    def local_intrusion_cost(a1: int, D_C: np.ndarray, reachable: bool, s: np.ndarray, Z_U: np.ndarray) -> float:
        """
        The defender's local cost function for intrusions

        :param a1: the defender action
        :param D_C: the vector with the costs of the defender actions
        :param reachable: a boolean flag indicating whether the node is reachable
        :param s: the current state
        :param Z_U: the vector with zone utilities
        :return: the intrusion cost
        """
        if not reachable:
            return D_C[a1]  # No intrusion cost if the node is not reachable
        compromised = int((s[env_constants.STATES.A_STATE_INDEX] == env_constants.ATTACK_STATES.COMPROMISED))
        return Z_U[s[env_constants.STATES.D_STATE_INDEX] - 1] * compromised + D_C[a1]

    @staticmethod
    def local_defender_utility_function(s: np.ndarray, a1: int, eta: float, reachable: bool, initial_zone: int,
                                        beta: float, D_C: np.ndarray, Z_U: np.ndarray):
        """
        The local utility function of the defender

        :param s: the current state of the local game
        :param a1: the defender action
        :param eta: a scaling parameter to balance QoS and security
        :param reachable: a boolean flag indicating whether the node is reachable from the public gateway or not
        :param initial_zone: the initial zone of the node in the local game
        :param beta: a scaling parameter indicating the importance of the workflow of the local game
        :param D_C: the vector with the costs of the local defender actions
        :param Z_U: the utilities of the zones in the network
        :return: the utility of the defender
        """
        if IntrusionResponseGameUtil.is_local_state_terminal(s):
            return 0
        workflow_utility = IntrusionResponseGameUtil.local_workflow_utility(beta=beta, reachable=reachable, s=s,
                                                                            initial_zone=initial_zone)
        intrusion_cost = IntrusionResponseGameUtil.local_intrusion_cost(a1=a1, D_C=D_C, reachable=reachable, s=s,
                                                                        Z_U=Z_U)
        return eta * workflow_utility - (1 - eta) * intrusion_cost

    @staticmethod
    def local_reward_tensor(eta: float, D_C: np.ndarray, reachable: bool, Z_U: np.ndarray, initial_zone: int,
                            beta: float, S: np.ndarray, A1: np.ndarray, A2: np.ndarray) -> np.ndarray:
        """
        Gets the defender's utility tensor of the local version of the game

        :param eta: a scaling parameter for the local rewards
        :param D_C: the vector with the costs of the local defender actions
        :param reachable: a boolean flag indicating whether the node of the local game is reachable or not
        :param Z_U: the vector with utilities of the different zones in the network
        :param initial_zone: the initial zone of the node
        :param beta: a scaling parameter for the workflow utility
        :param S: the local state space of the game
        :param A1: the local action space of the defender
        :param A2: teh local action space of the attacker
        :return: a |A1|x|A2|x|S| tensor giving the rewards of the state transitions in the local game
        """
        R = []
        for a1 in A1:
            a1_rews = []
            for a2 in A2:
                a1_a2_rews = []
                for s in S:
                    a1_a2_rews.append(IntrusionResponseGameUtil.local_defender_utility_function(
                        s=s, a1=a1, eta=eta, reachable=reachable, initial_zone=initial_zone,
                        beta=beta, D_C=D_C, Z_U=Z_U
                    ))
                a1_rews.append(a1_a2_rews)
            R.append(a1_rews)
        R = np.array(R)
        return R

    @staticmethod
    def local_transition_probability(s: np.ndarray, s_prime: np.ndarray, a1: int, a2: int, Z_D_P: np.ndarray,
                                     A_P: np.ndarray):
        """
        Gets the probability of a local state transition

        :param s: the current state
        :param s_prime: the next  state
        :param a1: the defender action
        :param a2: the attacker action
        :param Z_D_P: the zone detection probabilities
        :param A_P: the attack success probabilities
        :return: the transition probabilitiy
        """
        # If you are in terminal state you stay there
        if IntrusionResponseGameUtil.is_local_state_terminal(s):
            if IntrusionResponseGameUtil.is_local_state_terminal(s_prime):
                return 1
            else:
                return 0

        # Detection probability
        if IntrusionResponseGameUtil.is_local_state_terminal(s_prime) and a2 != env_constants.ATTACKER_ACTIONS.WAIT:
            return Z_D_P[s[env_constants.STATES.D_STATE_INDEX] - 1]

        P_not_detected = (1 - int(a2 != env_constants.ATTACKER_ACTIONS.WAIT) *
                          Z_D_P[s[env_constants.STATES.D_STATE_INDEX] - 1])

        # Defender takes defensive action
        if a1 != env_constants.DEFENDER_ACTIONS.WAIT:
            # Deterministic transition, attacker state is reset and node is migrated to the new zone
            if IntrusionResponseGameUtil.is_local_state_in_zone(s=s_prime, zone=a1) \
                    and IntrusionResponseGameUtil.is_local_state_healthy(s=s_prime):
                return 1 * P_not_detected
            else:
                return 0
        else:
            # Defender did not take defensive action

            # If attacker waits, then the state remains the same
            if a2 == env_constants.ATTACKER_ACTIONS.WAIT and \
                    IntrusionResponseGameUtil.are_local_states_equal(s=s, s_prime=s_prime):
                return 1 * P_not_detected

            # If the attacker performs recon and the node was not already compromised, then it is discovered
            if a2 == env_constants.ATTACKER_ACTIONS.RECON and \
                    IntrusionResponseGameUtil.are_local_defense_states_equal(s=s, s_prime=s_prime) and \
                    not IntrusionResponseGameUtil.is_local_state_compromised(s=s) \
                    and IntrusionResponseGameUtil.is_local_state_recon(s=s_prime):
                return 1 * P_not_detected

            # If the attacker performs recon and the node was already compromised, then the state remains the same
            if a2 == env_constants.ATTACKER_ACTIONS.RECON and \
                    IntrusionResponseGameUtil.is_local_state_compromised(s=s) \
                    and IntrusionResponseGameUtil.are_local_states_equal(s=s, s_prime=s_prime):
                return 1 * P_not_detected

            # The attacker can only attack nodes it has discovered:
            if a2 in [env_constants.ATTACKER_ACTIONS.BRUTE_FORCE, env_constants.ATTACKER_ACTIONS.EXPLOIT] \
                    and s[env_constants.STATES.A_STATE_INDEX] > env_constants.ATTACK_STATES.HEALTHY:

                # The zone cannot change as a result of an attacker action
                if not IntrusionResponseGameUtil.is_local_state_in_zone(s_prime,
                                                                        zone=s[env_constants.STATES.D_STATE_INDEX]):
                    return 0

                # The node cannot become undiscovered as a result of an attacker action
                if IntrusionResponseGameUtil.is_local_state_healthy(s_prime):
                    return 0

                # If the node is compromised, it cannot become uncompromised
                if IntrusionResponseGameUtil.is_local_state_compromised(s) \
                        and not IntrusionResponseGameUtil.is_local_state_compromised(s_prime):
                    return 0

                # If the node is already compromised, the state remains the same
                if IntrusionResponseGameUtil.is_local_state_compromised(s):
                    return P_not_detected

                # If the attacker attacks a node that was not already compromised, it is
                # compromised with a probability given by A_P.
                if a2 in [env_constants.ATTACKER_ACTIONS.BRUTE_FORCE, env_constants.ATTACKER_ACTIONS.EXPLOIT] \
                        and IntrusionResponseGameUtil.is_local_state_compromised(s_prime):
                    return (A_P[a2]) * P_not_detected

                # If the attacker attacks a node that was not already compromised, it
                # remains uncompromised w.p 1-A_P
                if a2 in [env_constants.ATTACKER_ACTIONS.BRUTE_FORCE, env_constants.ATTACKER_ACTIONS.EXPLOIT] \
                        and not IntrusionResponseGameUtil.is_local_state_compromised(s_prime):
                    return (1 - A_P[a2]) * P_not_detected

                # If the attacker attacks a node that is already compromised, it
                # remains compromised
                if a2 in [env_constants.ATTACKER_ACTIONS.BRUTE_FORCE, env_constants.ATTACKER_ACTIONS.EXPLOIT] \
                        and not IntrusionResponseGameUtil.is_local_state_compromised(s_prime):
                    return P_not_detected

            # If the attacker would try to attack a node that it has not discovered (illegal action)
            # then the action has no effect
            if a2 in [env_constants.ATTACKER_ACTIONS.BRUTE_FORCE, env_constants.ATTACKER_ACTIONS.EXPLOIT] \
                    and IntrusionResponseGameUtil.is_local_state_healthy(s) and \
                    IntrusionResponseGameUtil.are_local_states_equal(s=s, s_prime=s_prime):
                return P_not_detected

        # If none of the above cases match, the transition is impossible ans has probability 0
        return 0

    @staticmethod
    def local_transition_tensor(Z_D: np.ndarray, A_P: np.ndarray, S: np.ndarray, A1: np.ndarray,
                                A2: np.ndarray) -> np.ndarray:
        """
        Gets the transition tensor of the local game

        :param Z_D: the zone detection probabilities
        :param A_P: the attack success probabilities
        :param S: the local state space
        :param A1: the local action space of the defender
        :param A2: the local action space of the attacker
        :return: a |A1|x|A2||S|^2 tensor
        """
        T = []
        for a1 in A1:
            a1_probs = []
            for a2 in A2:
                a1_a2_probs = []
                for s in S:
                    a1_a2_s_probs = []
                    for s_prime in S:
                        p = IntrusionResponseGameUtil.local_transition_probability(
                            s=s, s_prime=s_prime, a1=a1, a2=a2,
                            Z_D_P=Z_D,
                            A_P=A_P,
                        )
                        a1_a2_s_probs.append(p)
                    assert sum(a1_a2_s_probs) == 1
                    a1_a2_probs.append(a1_a2_s_probs)
                a1_probs.append(a1_a2_probs)
            T.append(a1_probs)
        T = np.array(T)
        return T

    @staticmethod
    def local_observation_tensor_betabinom(S: np.ndarray, A1: np.ndarray, A2: np.ndarray, O: np.ndarray):
        """
        Gets the observation tensor of the local game where the observations follow beta-binomial distributions

        :param S: the local state space of the game
        :param A1: the local action space of the defender
        :param A2: the local action space of the attacker
        :param O: the local observation space
        :return: a |A1|x|A2|x|S|x|O| tensor
        """
        intrusion_dist = []
        no_intrusion_dist = []
        intrusion_rv = betabinom(n=len(O) - 1, a=1, b=0.7)
        no_intrusion_rv = betabinom(n=len(O) - 1, a=0.7, b=3)
        for i in range(len(O)):
            intrusion_dist.append(intrusion_rv.pmf(i))
            no_intrusion_dist.append(no_intrusion_rv.pmf(i))
        Z = []
        for a1 in A1:
            a1_probs = []
            for a2 in A2:
                a1_a2_probs = []
                for s in S:
                    if a2 != 0:
                        a1_a2_s_probs = intrusion_dist
                    else:
                        a1_a2_s_probs = no_intrusion_dist
                    assert round(sum(a1_a2_s_probs), 5) == 1
                    a1_a2_probs.append(a1_a2_s_probs)
                a1_probs.append(a1_a2_probs)
            Z.append(a1_probs)
        Z = np.array(Z)
        return Z

    @staticmethod
    def sample_next_state(T: np.ndarray, s_idx: int, a1: int, a2: int, S: np.ndarray) -> int:
        """
        Samples the next state

        :param T: the transition operator
        :param s_idx: the current state index
        :param a1: the defender action
        :param a2: the attacker action
        :param S: the state space
        :param l: the number of stops remaining
        :return: s'
        """
        state_probs = []
        for s_prime in range(len(S)):
            state_probs.append(T[a1][a2][s_idx][s_prime])
        s_prime = np.random.choice(np.arange(0, len(S)), p=state_probs)
        return s_prime

    @staticmethod
    def sample_next_observation(Z: np.ndarray, a1: int, a2: int, s_prime_idx: int, O: np.ndarray) -> int:
        """
        Samples the next observation
        """
        return int(np.random.choice(O, p=Z[a1][a2][s_prime_idx]))

    @staticmethod
    def bayes_filter_defender_belief(s_a_prime: int, o: int, a1: int, d_b: np.ndarray, pi2: np.ndarray,
                                     config: LocalIntrusionResponseGameConfig, s_d: int) -> float:
        """
        A Bayesian filter to compute the belief of player 1 of being in s_prime when observing o after
        taking action a in belief b given that the opponent follows strategy pi2

        :param s_a_prime: the attacker state to compute the belief of
        :param o: the observation
        :param a1: the action of player 1
        :param d_b: the current defender belief point
        :param pi2: the policy of player 2
        :param s_d: the defender state
        :return: b_prime(s_prime)
        """
        norm = 0
        for s in config.S_A:
            s_idx = config.states_to_idx[(s_d, s)]
            for a2 in config.A2:
                for s_prime_1 in config.S_A:
                    s_prime_idx = config.states_to_idx[(s_d, s_prime_1)]
                    prob_1 = config.Z[a1][a2][s_prime_idx][o]
                    norm += d_b[s] * prob_1 * config.T[a1][a2][s_idx][s_prime_idx] * pi2[s][a2]
        if norm == 0:
            return 0
        temp = 0
        s_prime_idx = config.states_to_idx[(s_d, s_a_prime)]
        for s in config.S_A:
            s_idx = config.states_to_idx[(s_d, s)]
            for a2 in config.A2:
                temp += config.Z[a1][a2][s_prime_idx][o] * config.T[a1][a2][s_idx][s_prime_idx] * d_b[s] * pi2[s][a2]
        b_prime_s_prime = temp / norm
        if round(b_prime_s_prime, 2) > 1:
            print(f"b_prime_s_prime >= 1: {b_prime_s_prime}, a1:{a1}, s_prime:{s_a_prime}, o:{o}, pi2:{pi2}")
        assert round(b_prime_s_prime, 2) <= 1
        return b_prime_s_prime

    @staticmethod
    def p_o_given_b_1_a1_a2(o: int, b: List, a1: int, a2: int, config: LocalIntrusionResponseGameConfig,
                            s_d: int) -> float:
        """
        Computes P[o|a,b]

        :param o: the observation
        :param b: the belief point
        :param a1: the action of player 1
        :param a2: the action of player 2
        :param s_d: the defender state
        :param config: the game config
        :return: the probability of observing o when taking action a in belief point b
        """
        prob = 0
        for s in config.S_A:
            s_idx = config.states_to_idx[(s_d, s)]
            for s_prime in config.S_A:
                s_prime_idx = config.states_to_idx[(s_d, s_prime)]
                prob += b[s] * config.T[a1][a2][s_idx][s_prime_idx] * config.Z[a1][a2][s_prime_idx][o]
        assert prob < 1
        return prob

    @staticmethod
    def next_local_defender_belief(o: int, a1: int, d_b: np.ndarray, pi2: np.ndarray,
                                   config: LocalIntrusionResponseGameConfig, a2: int, s_a: int,
                                   s_d: int) -> np.ndarray:
        """
        Computes the next belief using a Bayesian filter

        :param o: the latest observation
        :param a1: the latest action of player 1
        :param d_b: the current defender belief
        :param pi2: the policy of player 2
        :param config: the game config
        :param a2: the attacker action (for debugging, should be consistent with pi2)
        :param s_a: the true current attacker state (for debugging)
        :param s_d: the defender state
        :return: the new belief
        """
        b_prime = np.zeros(len(config.S_A))
        for s_a_prime in config.S_A:
            b_prime[s_a_prime] = IntrusionResponseGameUtil.bayes_filter_defender_belief(
                s_a_prime=s_a_prime, o=o, a1=a1, d_b=d_b, pi2=pi2, config=config, s_d=s_d)
        if round(sum(b_prime), 2) != 1:
            print(f"error, b_prime:{b_prime}, o:{o}, a1:{a1}, d_b:{d_b}, pi2:{pi2}, "
                  f"a2: {a2}, s:{s_a}")
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
