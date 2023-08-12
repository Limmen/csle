from typing import Any
import numpy as np
import numpy.typing as npt
from scipy.stats import betabinom
from gym_csle_intrusion_response_game.dao.local_intrusion_response_game_config import LocalIntrusionResponseGameConfig
import gym_csle_intrusion_response_game.constants.constants as env_constants
from csle_common.dao.training.policy import Policy


class IntrusionResponseGameUtil:
    """
    Class with utility functions for the intrusion response game environment
    """

    @staticmethod
    def is_local_state_terminal(s: npt.NDArray[np.int_]) -> bool:
        """
        Utility function for checking if a local state is terminal or not

        :param s: the local state to check
        :return: True if terminal, otherwise False
        """
        return bool(s[env_constants.STATES.D_STATE_INDEX] == -1 and s[env_constants.STATES.A_STATE_INDEX] == -1)

    @staticmethod
    def is_local_state_in_zone(s: npt.NDArray[np.int_], zone: int) -> bool:
        """
        Utility function for checking if a local state is in a given zone or not

        :param s: the local state to check
        :param zone: the zone to check
        :return: True if the state is in the given zone, false otherwise
        """
        return bool(s[env_constants.STATES.D_STATE_INDEX] == zone)

    @staticmethod
    def is_local_state_shutdown_or_redirect(s: npt.NDArray[np.int_]) -> bool:
        """
        Utility function for checking if a local node is in shutdown or redirect state

        :param s: the local state to check
        :param zone: the zone to check
        :return: True if the node is in shutdown or redirect state, otherwise fasle
        """
        return bool(s[env_constants.STATES.D_STATE_INDEX] == env_constants.DEFENDER_STATES.SHUTDOWN
                    and s[env_constants.STATES.D_STATE_INDEX] == env_constants.DEFENDER_STATES.REDIRECT)

    @staticmethod
    def is_local_state_compromised(s: npt.NDArray[np.int_]) -> bool:
        """
        Utility function for checking if a local state has been compromised

        :param s: the local state to check
        :return: True if compromised, otherwise False
        """
        return bool(s[env_constants.STATES.A_STATE_INDEX] == env_constants.ATTACK_STATES.COMPROMISED)

    @staticmethod
    def is_local_state_healthy(s: npt.NDArray[np.int_]) -> bool:
        """
        Utility function for checking if a local state is healthy and not discovered nor compromised

        :param s: the local state to check
        :return: True if compromised, otherwise False
        """
        return bool(s[env_constants.STATES.A_STATE_INDEX] == env_constants.ATTACK_STATES.HEALTHY)

    @staticmethod
    def is_local_state_recon(s: npt.NDArray[np.int_]) -> bool:
        """
        Utility function for checking if a local state has been discovered by the attacker

        :param s: the local state to check
        :return: True if compromised, otherwise False
        """
        return bool(s[env_constants.STATES.A_STATE_INDEX] == env_constants.ATTACK_STATES.RECON)

    @staticmethod
    def are_local_states_equal(s: npt.NDArray[np.int_], s_prime: npt.NDArray[np.int_]) -> bool:
        """
        Utility function for checking if two local states are equal

        :param s: the first local state to check
        :param s_prime: the second local state to check
        :return: True if equal, otherwise False
        """
        return bool(s[env_constants.STATES.D_STATE_INDEX] == s_prime[env_constants.STATES.D_STATE_INDEX] and s[
            env_constants.STATES.A_STATE_INDEX] == s_prime[env_constants.STATES.A_STATE_INDEX])

    @staticmethod
    def are_local_defense_states_equal(s: npt.NDArray[np.int_], s_prime: npt.NDArray[np.int_]) -> bool:
        """
        Utility function for checking if two local defense states are equal

        :param s: the first local state to check
        :param s_prime: the second local state to check
        :return: True if equal, otherwise False
        """
        return bool(s[env_constants.STATES.D_STATE_INDEX] == s_prime[env_constants.STATES.D_STATE_INDEX])

    @staticmethod
    def are_local_attack_states_equal(s: npt.NDArray[np.int_], s_prime: npt.NDArray[np.int_]) -> bool:
        """
        Utility function for checking if two local attack states are equal

        :param s: the first local state to check
        :param s_prime: the second local state to check
        :return: True if equal, otherwise False
        """
        return bool(s[env_constants.STATES.A_STATE_INDEX] == s_prime[env_constants.STATES.A_STATE_INDEX])

    @staticmethod
    def local_initial_state(initial_zone: int, S: npt.NDArray[Any]) -> Any:
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
    def local_initial_state_idx(initial_zone: int, S: npt.NDArray[Any]) -> int:
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
    def local_initial_state_distribution(initial_state_idx, S: npt.NDArray[Any]) -> npt.NDArray[np.float_]:
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
    def local_initial_defender_belief(S_A: npt.NDArray[Any]) -> npt.NDArray[np.float_]:
        """
        Gets the initial defender belief for a local version of the game

        :param S_A: the attacker's state space of the local game
        :return: the initial defender belief
        """
        d_b1 = np.zeros((len(S_A),))
        d_b1[env_constants.ATTACK_STATES.HEALTHY] = 1  # the node is not compromised or discovered initially
        return d_b1

    @staticmethod
    def local_initial_attacker_belief(S_D: npt.NDArray[Any], initial_zone) -> npt.NDArray[np.float_]:
        """
        Gets the initial attacker belief for a local version of the game

        :param S_D: the defender's state space of the local game
        :param initial_zone: the initial zone of the node
        :return: the initial defender belief
        """
        d_a1 = np.zeros((len(S_D),))
        # d_a1[initial_zone] = 1
        for i in range(len(S_D)):
            d_a1[i] = 1 / len(S_D)  # The attacker has no clue about the zones initially
        return d_a1

    @staticmethod
    def local_state_space(number_of_zones: int) -> npt.NDArray[Any]:
        """
        Gets the state space of the local version of the game

        :param number_of_zones: the number of zones in the network
        :return: the state space
        """
        S = []
        S.append(list(env_constants.STATES.TERMINAL_STATE))
        for i in range(1, number_of_zones + 1):
            S.append([i, env_constants.ATTACK_STATES.HEALTHY])
            S.append([i, env_constants.ATTACK_STATES.RECON])
            S.append([i, env_constants.ATTACK_STATES.COMPROMISED])
        return np.array(S)

    @staticmethod
    def local_defender_state_space(number_of_zones: int) -> npt.NDArray[np.int_]:
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
    def local_attacker_state_space() -> npt.NDArray[np.int_]:
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
    def local_defender_actions(number_of_zones: int) -> npt.NDArray[np.int_]:
        """
        Gets the defender's action space in the local version of the game

        :param number_of_zones: the number of zones in the game
        :return: a vector with the actions of the defender
        """
        return np.array(list(range(number_of_zones + 1)))

    @staticmethod
    def local_attacker_actions() -> npt.NDArray[np.int_]:
        """
        Gets the attacker's action space in the local version of the game

        :return: a vector with the actions of the defender
        """
        return np.array([env_constants.ATTACKER_ACTIONS.WAIT, env_constants.ATTACKER_ACTIONS.RECON,
                         env_constants.ATTACKER_ACTIONS.BRUTE_FORCE, env_constants.ATTACKER_ACTIONS.EXPLOIT])

    @staticmethod
    def local_observation_space(X_max: int) -> npt.NDArray[np.int_]:
        """
        Gets the observation space of the local version of the game

        :param X_max: the maximum observation
        :return: a vector with all possible observations
        """
        return np.array(list(range(X_max)))

    @staticmethod
    def local_workflow_utility(beta: float, reachable: bool, s: npt.NDArray[Any], initial_zone: int) -> float:
        """
        The local utility function for workflow QoS

        :param beta: a scaling parameter indicating how important the workflow is
        :param reachable: a boolean flag indicating whether the node is reachable from the public gateway or not
        :param s: the local state vector
        :param initial_zone: the initial zone of the node in the local version of the game
        :return: the workflow utility
        """
        impact = 0
        if reachable and not IntrusionResponseGameUtil.is_local_state_compromised(s) and \
                not s[env_constants.STATES.D_STATE_INDEX] in [env_constants.ZONES.SHUTDOWN_ZONE,
                                                              env_constants.ZONES.REDIRECTION_ZONE]:
            impact = 1
        return beta * impact * int(not IntrusionResponseGameUtil.is_local_state_shutdown_or_redirect(s=s))

    @staticmethod
    def constant_defender_action_costs(A1: npt.NDArray[np.int_], constant_cost: float) -> npt.NDArray[np.float_]:
        """
        Returns a vector with the local defender action costs where each action has the same constant cost

        :param A1: a vector with the actions of the defender in the local game
        :param constant_cost: the constant action cost
        :return: a vector with the action costs
        """
        action_costs = []
        for a1 in A1:
            if a1 == env_constants.DEFENDER_ACTIONS.WAIT:
                action_costs.append(0.0)
            else:
                action_costs.append(constant_cost)
        return np.array(action_costs)

    @staticmethod
    def zones(num_zones: int) -> npt.NDArray[Any]:
        """
        Gets the vector with the network zones

        :param num_zones: the number of zones
        :return: a vector with the zones
        """
        return np.array(list(range(1, num_zones + 1)))

    @staticmethod
    def constant_zone_utilities(zones: npt.NDArray[np.int_], constant_utility: float) -> npt.NDArray[np.float_]:
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
    def constant_zone_detection_probabilities(zones: npt.NDArray[np.int_], constant_detection_prob: float) \
            -> npt.NDArray[np.float_]:
        """
        Returns a vector with the zone detection probabilities where each zone as the same uniform detection
        probability

        :param zones: the vector with zones
        :param constant_detection_prob: the constant detection probability
        :return: the vector with zone detection probabilities
        """
        zone_detection_probabilities = []
        for z in zones:
            if z == env_constants.ZONES.SHUTDOWN_ZONE:
                zone_detection_probabilities.append(0.0)
            else:
                zone_detection_probabilities.append(constant_detection_prob)
        return np.array(zone_detection_probabilities)

    @staticmethod
    def local_attack_success_probabilities_uniform(p: float, A2: npt.NDArray[Any]) -> npt.NDArray[Any]:
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
    def local_intrusion_cost(a1: int, D_C: npt.NDArray[Any], reachable: bool, s: npt.NDArray[Any],
                             Z_U: npt.NDArray[Any]) -> Any:
        """
        The defender's local cost function for intrusions

        :param a1: the defender action
        :param D_C: the vector with the costs of the defender actions
        :param reachable: a boolean flag indicating whether the node is reachable
        :param s: the current state
        :param Z_U: the vector with zone utilities
        :return: the intrusion cost
        """
        if not reachable or s[env_constants.STATES.D_STATE_INDEX] == env_constants.ZONES.SHUTDOWN_ZONE:
            return D_C[a1]  # No intrusion cost if the node is not reachable
        compromised = int((s[env_constants.STATES.A_STATE_INDEX] == env_constants.ATTACK_STATES.COMPROMISED))
        if compromised:
            return Z_U[s[env_constants.STATES.D_STATE_INDEX] - 1]
        else:
            return D_C[a1]

    @staticmethod
    def local_defender_utility_function(s: npt.NDArray[Any], a1: int, eta: float, reachable: bool, initial_zone: int,
                                        beta: float, C_D: npt.NDArray[Any], Z_U: npt.NDArray[Any],
                                        topology_cost: float = 0) -> Any:
        """
        The local utility function of the defender

        :param s: the current state of the local game
        :param a1: the defender action
        :param eta: a scaling parameter to balance QoS and security
        :param reachable: a boolean flag indicating whether the node is reachable from the public gateway or not
        :param initial_zone: the initial zone of the node in the local game
        :param beta: a scaling parameter indicating the importance of the workflow of the local game
        :param C_D: the vector with the costs of the local defender actions
        :param Z_U: the utilities of the zones in the network
        :param topology_cost: extra topology cost
        :return: the utility of the defender
        """
        if IntrusionResponseGameUtil.is_local_state_terminal(s):
            return 0
        workflow_utility = IntrusionResponseGameUtil.local_workflow_utility(beta=beta, reachable=reachable, s=s,
                                                                            initial_zone=initial_zone)
        intrusion_cost = IntrusionResponseGameUtil.local_intrusion_cost(a1=a1, D_C=C_D, reachable=reachable, s=s,
                                                                        Z_U=Z_U)
        if s[env_constants.STATES.D_STATE_INDEX] not in [0, 1]:
            topology_cost = 0
        return eta * workflow_utility - (1 - eta) * intrusion_cost - topology_cost

    @staticmethod
    def local_reward_tensor(eta: float, C_D: npt.NDArray[Any], reachable: bool, Z_U: npt.NDArray[Any],
                            initial_zone: int,
                            beta: float, S: npt.NDArray[Any], A1: npt.NDArray[Any], A2: npt.NDArray[Any],
                            topology_cost: float = 0.0) -> npt.NDArray[Any]:
        """
        Gets the defender's utility tensor of the local version of the game

        :param eta: a scaling parameter for the local rewards
        :param C_D: the vector with the costs of the local defender actions
        :param reachable: a boolean flag indicating whether the node of the local game is reachable or not
        :param Z_U: the vector with utilities of the different zones in the network
        :param initial_zone: the initial zone of the node
        :param beta: a scaling parameter for the workflow utility
        :param S: the local state space of the game
        :param A1: the local action space of the defender
        :param A2: the local action space of the attacker
        :param topology_cost: extra topology costs
        :return: a (A1)(A2)(S) tensor giving the rewards of the state transitions in the local game
        """
        R = []
        for a1 in A1:
            a1_rews = []
            for a2 in A2:
                a1_a2_rews = []
                for s in S:
                    a1_a2_rews.append(IntrusionResponseGameUtil.local_defender_utility_function(
                        s=s, a1=a1, eta=eta, reachable=reachable, initial_zone=initial_zone,
                        beta=beta, C_D=C_D, Z_U=Z_U, topology_cost=topology_cost
                    ))
                a1_rews.append(a1_a2_rews)
            R.append(a1_rews)
        return np.array(R)

    @staticmethod
    def local_stopping_mdp_reward_tensor(S: npt.NDArray[Any], A1: npt.NDArray[Any], A2: npt.NDArray[Any],
                                         R: npt.NDArray[Any], S_D: npt.NDArray[Any]) -> npt.NDArray[Any]:
        """
        Gets the local stopping MDP reward tensor for the attacker

        :param S: the state space of the local game
        :param A1: the action space of the defender in the local game
        :param A2: the action space of the attacker in the local game
        :param R: the reward tensor of the local game
        :param S_D: the state space of the defender in the local game
        :return: the reward tensor of the attacker in the stopping MDP
        """
        R_1 = []
        S_D = np.append([-1], S_D)
        for a1 in A1:
            if a1 == 0:
                continue
            a1_rews = []
            for a2 in A2:
                a1_a2_rews = []
                for s in S_D:
                    r = 0
                    for i, full_s in enumerate(S):
                        if full_s[env_constants.STATES.D_STATE_INDEX] == s and \
                                full_s[env_constants.STATES.A_STATE_INDEX] == env_constants.ATTACK_STATES.COMPROMISED:
                            r = R[a1][a2][i]
                    a1_a2_rews.append(r)
                a1_rews.append(a1_a2_rews)
            R_1.append(a1_rews)
        return np.array(R_1)

    @staticmethod
    def local_stopping_pomdp_reward_tensor(S: npt.NDArray[Any], A2: npt.NDArray[Any],
                                           R: npt.NDArray[Any], S_A: npt.NDArray[Any],
                                           a1: int, zone: int) -> npt.NDArray[Any]:
        """
        Gets the local reward tensor of the stopping POMDP

        :param S: the state space of the local game
        :param A2: the action space of the attacker
        :param R: the reward tensor of the local game
        :param S_A: the state space of the attacker in the local game
        :param a1: the stopping action of the defender
        :param zone: the zone of the local game
        :return: the reward tensor
        """
        R_1 = []
        S_A = np.append([-1], S_A)
        for stop in [0, 1]:
            a1_rews = []
            for a2 in A2:
                a1_a2_rews = []
                for s in S_A:
                    r = 0
                    for i, full_s in enumerate(S):
                        if full_s[env_constants.STATES.A_STATE_INDEX] == s \
                                and full_s[env_constants.STATES.D_STATE_INDEX] == zone:
                            if stop == 1:
                                r = R[a1][a2][i]
                            else:
                                r = R[0][a2][i]
                    a1_a2_rews.append(r)
                a1_rews.append(a1_a2_rews)
            R_1.append(a1_rews)
        return np.array(R_1)

    @staticmethod
    def local_stopping_pomdp_observation_tensor(S: npt.NDArray[Any], A2: npt.NDArray[Any], S_A: npt.NDArray[Any],
                                                Z: npt.NDArray[Any], a1: int, zone: int, O: npt.NDArray[Any]) \
            -> npt.NDArray[Any]:
        """
        Gets the local observation tensor for a stopping POMDP

        :param S: the state space of the local game
        :param A2: the action space of the attacker
        :param S_A: the state space of the attacker
        :param Z: the observation tensor of the game
        :param a1: the defender stop action
        :param zone: the zone of the local game
        :param O: the observation space
        :return: the observation tensor
        """
        Z_1 = []
        S_A = np.append([-1], S_A)
        for stop in [0, 1]:
            a1_obs_probs = []
            for a2 in A2:
                a1_a2_obs_probs = []
                for s in S_A:
                    obs_prob = []
                    for i, full_s_prime in enumerate(S):
                        if full_s_prime[env_constants.STATES.A_STATE_INDEX] == s \
                                and full_s_prime[env_constants.STATES.D_STATE_INDEX] == zone:
                            if stop == 1:
                                obs_prob = Z[a1][a2][i]
                            else:
                                obs_prob = Z[0][a2][i]
                    if len(obs_prob) == 0:
                        obs_prob = np.zeros(len(O)).tolist()
                        obs_prob[0] = 1
                    a1_a2_obs_probs.append(obs_prob)
                a1_obs_probs.append(a1_a2_obs_probs)
            Z_1.append(a1_obs_probs)
        return np.array(Z_1)

    @staticmethod
    def local_transition_probability(s: npt.NDArray[Any], s_prime: npt.NDArray[Any], a1: int, a2: int,
                                     Z_D_P: npt.NDArray[Any], A_P: npt.NDArray[Any]) -> float:
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
                return 1.0
            else:
                return 0.0

        # Detection probability
        if IntrusionResponseGameUtil.is_local_state_terminal(s_prime) and a2 != env_constants.ATTACKER_ACTIONS.WAIT:
            return float(Z_D_P[s[env_constants.STATES.D_STATE_INDEX] - 1])

        P_not_detected = (1 - int(a2 != env_constants.ATTACKER_ACTIONS.WAIT) *
                          Z_D_P[s[env_constants.STATES.D_STATE_INDEX] - 1])

        # Defender takes defensive action
        if a1 != env_constants.DEFENDER_ACTIONS.WAIT:
            # Deterministic transition, attacker state is reset and node is migrated to the new zone
            if IntrusionResponseGameUtil.is_local_state_in_zone(s=s_prime, zone=a1) \
                    and IntrusionResponseGameUtil.is_local_state_healthy(s=s_prime):
                return float(1.0 * P_not_detected)
            else:
                return 0.0
        else:
            # Defender did not take defensive action

            # If the node is shutdown, the state remains the same
            if s[env_constants.STATES.D_STATE_INDEX] in [env_constants.ZONES.SHUTDOWN_ZONE]:
                if IntrusionResponseGameUtil.are_local_states_equal(s=s, s_prime=s_prime):
                    return float(1 * P_not_detected)
                else:
                    return 0.0

            # If attacker waits, then the state remains the same
            if a2 == env_constants.ATTACKER_ACTIONS.WAIT:
                if IntrusionResponseGameUtil.are_local_states_equal(s=s, s_prime=s_prime):
                    return float(1 * P_not_detected)
                else:
                    return 0.0

            # If the attacker performs recon and the node was not already compromised, then it is discovered
            if a2 == env_constants.ATTACKER_ACTIONS.RECON and \
                    IntrusionResponseGameUtil.are_local_defense_states_equal(s=s, s_prime=s_prime) and \
                    not IntrusionResponseGameUtil.is_local_state_compromised(s=s) \
                    and IntrusionResponseGameUtil.is_local_state_recon(s=s_prime):
                return float(1 * P_not_detected)

            # If the attacker performs recon and the node was already compromised, then the state remains the same
            if a2 == env_constants.ATTACKER_ACTIONS.RECON and \
                    IntrusionResponseGameUtil.is_local_state_compromised(s=s) \
                    and IntrusionResponseGameUtil.are_local_states_equal(s=s, s_prime=s_prime):
                return float(1 * P_not_detected)

            # The attacker can only attack nodes it has discovered:
            if a2 in [env_constants.ATTACKER_ACTIONS.BRUTE_FORCE, env_constants.ATTACKER_ACTIONS.EXPLOIT] \
                    and s[env_constants.STATES.A_STATE_INDEX] > env_constants.ATTACK_STATES.HEALTHY:

                # The zone cannot change as a result of an attacker action
                if not IntrusionResponseGameUtil.is_local_state_in_zone(s_prime,
                                                                        zone=s[env_constants.STATES.D_STATE_INDEX]):
                    return 0.0

                # The node cannot become undiscovered as a result of an attacker action
                if IntrusionResponseGameUtil.is_local_state_healthy(s_prime):
                    return 0.0

                # If the node is compromised, it cannot become uncompromised
                if IntrusionResponseGameUtil.is_local_state_compromised(s) \
                        and not IntrusionResponseGameUtil.is_local_state_compromised(s_prime):
                    return 0.0

                # If the node is already compromised, the state remains the same
                if IntrusionResponseGameUtil.is_local_state_compromised(s):
                    return float(P_not_detected)

                # If the attacker attacks a node that was not already compromised, it is
                # compromised with a probability given by A_P.
                if a2 in [env_constants.ATTACKER_ACTIONS.BRUTE_FORCE, env_constants.ATTACKER_ACTIONS.EXPLOIT] \
                        and IntrusionResponseGameUtil.is_local_state_compromised(s_prime):
                    return float((A_P[a2]) * P_not_detected)

                # If the attacker attacks a node that was not already compromised, it
                # remains uncompromised w.p 1-A_P
                if a2 in [env_constants.ATTACKER_ACTIONS.BRUTE_FORCE, env_constants.ATTACKER_ACTIONS.EXPLOIT] \
                        and not IntrusionResponseGameUtil.is_local_state_compromised(s_prime):
                    return float((1 - A_P[a2]) * P_not_detected)

                # If the attacker attacks a node that is already compromised, it
                # remains compromised
                if a2 in [env_constants.ATTACKER_ACTIONS.BRUTE_FORCE, env_constants.ATTACKER_ACTIONS.EXPLOIT] \
                        and not IntrusionResponseGameUtil.is_local_state_compromised(s_prime):
                    return float(P_not_detected)

            # If the attacker would try to attack a node that it has not discovered (illegal action)
            # then the action has no effect
            if a2 in [env_constants.ATTACKER_ACTIONS.BRUTE_FORCE, env_constants.ATTACKER_ACTIONS.EXPLOIT] \
                    and IntrusionResponseGameUtil.is_local_state_healthy(s) and \
                    IntrusionResponseGameUtil.are_local_states_equal(s=s, s_prime=s_prime):
                return float(P_not_detected)

        # If none of the above cases match, the transition is impossible ans has probability 0
        return 0.0

    @staticmethod
    def local_transition_tensor(Z_D: npt.NDArray[Any], A_P: npt.NDArray[Any], S: npt.NDArray[Any],
                                A1: npt.NDArray[Any], A2: npt.NDArray[Any]) -> npt.NDArray[Any]:
        """
        Gets the transition tensor of the local game

        :param Z_D: the zone detection probabilities
        :param A_P: the attack success probabilities
        :param S: the local state space
        :param A1: the local action space of the defender
        :param A2: the local action space of the attacker
        :return: a (A1)(A2)(S)(S) tensor
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
                            s=s, s_prime=s_prime, a1=a1, a2=a2, Z_D_P=Z_D, A_P=A_P)
                        a1_a2_s_probs.append(p)
                    assert round(sum(a1_a2_s_probs), 3) == 1
                    a1_a2_probs.append(a1_a2_s_probs)
                a1_probs.append(a1_a2_probs)
            T.append(a1_probs)
        return np.array(T)

    @staticmethod
    def local_stopping_mdp_transition_tensor(S: npt.NDArray[Any], A1: npt.NDArray[Any], A2: npt.NDArray[Any],
                                             T: npt.NDArray[Any], S_D: npt.NDArray[Any]) -> npt.NDArray[Any]:
        """
        Gets the transition tensor for the local MDP of the stopping decomposition in the temporal domain

        :param S: the full state space of the local problem
        :param A1: the defender's action space in the local problem
        :param A2: the attacker's action space in the local problem
        :param T: the full transition tensor of the local problem
        :param S_D: the defender's state spce
        :return: the transition tensor for the local MDP of the stopping formulation
        """
        S_D = np.append([-1], S_D)
        T_1 = []
        for a1 in A1:
            if a1 == 0:
                continue
            a1_probs = []
            for a2 in A2:
                a1_a2_probs = []
                for s in S_D:
                    a1_a2_s_probs = []
                    for s_prime in S_D:
                        prob = 0.0
                        total_prob = 0.0
                        for i, full_s in enumerate(S):
                            for j, full_s_prime in enumerate(S):
                                if full_s[env_constants.STATES.D_STATE_INDEX] == s:
                                    total_prob += T[a1][a2][i][j]
                                if full_s[env_constants.STATES.D_STATE_INDEX] == s \
                                        and full_s_prime[env_constants.STATES.D_STATE_INDEX] == s_prime:
                                    prob += T[a1][a2][i][j]
                        prob = prob / total_prob
                        prob = min(1, prob)
                        a1_a2_s_probs.append(prob)
                    assert round(sum(a1_a2_s_probs), 3) == 1
                    a1_a2_probs.append(a1_a2_s_probs)
                a1_probs.append(a1_a2_probs)
            T_1.append(a1_probs)
        return np.array(T_1)

    @staticmethod
    def local_stopping_pomdp_transition_tensor(S: npt.NDArray[Any], A2: npt.NDArray[Any], T: npt.NDArray[Any],
                                               S_A: npt.NDArray[Any], a1: int) -> npt.NDArray[Any]:
        """
        Gets the transition tensor for the local POMDP of the stopping decomposition in the temporal domain

        :param S: the full state space of the local problem
        :param A1: the defender's action space in the local problem
        :param A2: the attacker's action space in the local problem
        :param T: the full transition tensor of the local problem
        :param S_D: the defender's state spce
        :return: the transition tensor for the local MDP of the stopping formulation
        """
        S_A = np.append([-1], S_A)
        T_1 = []
        for stop in [0, 1]:
            stop_probs = []
            for a2 in A2:
                a1_a2_probs = []
                for s in S_A:
                    a1_a2_s_probs = []
                    for s_prime in S_A:
                        if a1 == 1:
                            if s_prime == -1:
                                a1_a2_s_probs.append(1.0)
                            else:
                                a1_a2_s_probs.append(0.0)
                        else:
                            prob = 0.0
                            total_prob = 0.0
                            for i, full_s in enumerate(S):
                                for j, full_s_prime in enumerate(S):
                                    if full_s[env_constants.STATES.A_STATE_INDEX] == s:
                                        total_prob += T[a1][a2][i][j]
                                    if full_s[env_constants.STATES.A_STATE_INDEX] == s \
                                            and full_s_prime[env_constants.STATES.A_STATE_INDEX] == s_prime:
                                        prob += T[stop][a2][i][j]
                            prob = prob / total_prob
                            # prob=min(1, prob)
                            a1_a2_s_probs.append(prob)
                    assert round(sum(a1_a2_s_probs), 3) == 1
                    a1_a2_probs.append(a1_a2_s_probs)
                stop_probs.append(a1_a2_probs)
            T_1.append(stop_probs)
        return np.array(T_1)

    @staticmethod
    def local_observation_tensor_betabinom(S: npt.NDArray[Any], A1: npt.NDArray[Any], A2: npt.NDArray[Any],
                                           O: npt.NDArray[Any]) -> npt.NDArray[Any]:
        """
        Gets the observation tensor of the local game where the observations follow beta-binomial distributions

        :param S: the local state space of the game
        :param A1: the local action space of the defender
        :param A2: the local action space of the attacker
        :param O: the local observation space
        :return: a (A1)(A2)(S)(O) tensor
        """
        brute_force_dist = []
        exploit_dist = []
        recon_dist = []
        wait_dist = []
        brute_force_hp_dist = []
        exploit_hp_dist = []
        recon_hp_dist = []
        wait_hp_dist = []
        shutdown_dist = np.zeros(len(O)).tolist()
        shutdown_dist[0] = 1

        brute_force_hp_rv = betabinom(n=len(O) - 1, a=4, b=0.7)
        recon_hp_rv = betabinom(n=len(O) - 1, a=3, b=0.7)
        exploit_hp_rv = betabinom(n=len(O) - 1, a=2, b=0.7)
        wait_hp_rv = betabinom(n=len(O) - 1, a=1, b=2)

        brute_force_rv = betabinom(n=len(O) - 1, a=3, b=0.7)
        recon_rv = betabinom(n=len(O) - 1, a=2, b=0.7)
        exploit_rv = betabinom(n=len(O) - 1, a=1, b=0.7)
        wait_rv = betabinom(n=len(O) - 1, a=0.7, b=3)

        for i in range(len(O)):
            recon_dist.append(recon_rv.pmf(i))
            brute_force_dist.append(brute_force_rv.pmf(i))
            exploit_dist.append(exploit_rv.pmf(i))
            wait_dist.append(wait_rv.pmf(i))
            recon_hp_dist.append(recon_hp_rv.pmf(i))
            brute_force_hp_dist.append(brute_force_hp_rv.pmf(i))
            exploit_hp_dist.append(exploit_hp_rv.pmf(i))
            wait_hp_dist.append(wait_hp_rv.pmf(i))
        Z = []
        for a1 in A1:
            a1_probs = []
            for a2 in A2:
                a1_a2_probs = []
                for s in S:
                    if IntrusionResponseGameUtil.is_local_state_in_zone(s=s, zone=env_constants.ZONES.SHUTDOWN_ZONE):
                        a1_a2_s_probs = shutdown_dist
                    elif a2 == env_constants.ATTACKER_ACTIONS.RECON:
                        if IntrusionResponseGameUtil.is_local_state_in_zone(
                                s=s, zone=env_constants.ZONES.REDIRECTION_ZONE):
                            a1_a2_s_probs = recon_hp_dist
                        else:
                            a1_a2_s_probs = recon_dist
                    elif a2 == env_constants.ATTACKER_ACTIONS.EXPLOIT:
                        if IntrusionResponseGameUtil.is_local_state_in_zone(
                                s=s, zone=env_constants.ZONES.REDIRECTION_ZONE):
                            a1_a2_s_probs = exploit_hp_dist
                        else:
                            a1_a2_s_probs = exploit_dist
                    elif a2 == env_constants.ATTACKER_ACTIONS.BRUTE_FORCE:
                        if IntrusionResponseGameUtil.is_local_state_in_zone(
                                s=s, zone=env_constants.ZONES.REDIRECTION_ZONE):
                            a1_a2_s_probs = brute_force_hp_dist
                        else:
                            a1_a2_s_probs = brute_force_dist
                    else:
                        if IntrusionResponseGameUtil.is_local_state_in_zone(
                                s=s, zone=env_constants.ZONES.REDIRECTION_ZONE):
                            a1_a2_s_probs = wait_hp_dist
                        else:
                            a1_a2_s_probs = wait_dist
                    assert round(sum(a1_a2_s_probs), 5) == 1
                    a1_a2_probs.append(a1_a2_s_probs)
                a1_probs.append(a1_a2_probs)
            Z.append(a1_probs)
        return np.array(Z)

    @staticmethod
    def sample_next_state(T: npt.NDArray[Any], s_idx: int, a1: int, a2: int, S: npt.NDArray[Any]) -> int:
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
    def sample_next_observation(Z: npt.NDArray[Any], a1: int, a2: int, s_prime_idx: int, O: npt.NDArray[Any]) -> int:
        """
        Samples the next observation
        """
        return int(np.random.choice(O, p=Z[a1][a2][s_prime_idx]))

    @staticmethod
    def bayes_filter_defender_belief(s_a_prime: int, o: int, a1: int, d_b: npt.NDArray[Any], pi2: npt.NDArray[Any],
                                     config: LocalIntrusionResponseGameConfig, s_d_prime: int, s_d: int) -> float:
        """
        A Bayesian filter to compute the belief of player 1 of being in s_prime when observing o after
        taking action a in belief b given that the opponent follows strategy pi2

        :param s_a_prime: the attacker state to compute the belief of
        :param o: the observation
        :param a1: the action of player 1
        :param d_b: the current defender belief point
        :param pi2: the policy of player 2
        :param s_d_prime: the defender state
        :param s_d: the previous defender state
        :return: b_prime(s_prime)
        """
        norm = 0
        for s_a in config.S_A:
            s_idx = config.states_to_idx[(s_d, s_a)]
            for a2 in config.A2:
                for s_prime_a_1 in config.S_A:
                    s_prime_idx = config.states_to_idx[(s_d_prime, s_prime_a_1)]
                    obs_prob = config.Z[a1][a2][s_prime_idx][o]
                    norm += d_b[s_a] * obs_prob * config.T[0][a1][a2][s_idx][s_prime_idx] * pi2[s_a][a2]
        if norm == 0:
            return 0
        temp = 0
        s_prime_idx = config.states_to_idx[(s_d_prime, s_a_prime)]
        for s_a in config.S_A:
            s_idx = config.states_to_idx[(s_d, s_a)]
            for a2 in config.A2:
                temp += \
                    (config.Z[a1][a2][s_prime_idx][o] *
                     config.T[0][a1][a2][s_idx][s_prime_idx] * d_b[s_a] * pi2[s_a][a2])
        b_prime_s_prime = temp / norm
        if round(b_prime_s_prime, 2) > 1:
            print(f"b_prime_s_prime >= 1: {b_prime_s_prime}, a1:{a1}, s_prime:{s_a_prime}, o:{o}, pi2:{pi2}")
        assert round(b_prime_s_prime, 2) <= 1
        return b_prime_s_prime

    @staticmethod
    def next_local_defender_belief(o: int, a1: int, d_b: npt.NDArray[Any], pi2: npt.NDArray[Any],
                                   config: LocalIntrusionResponseGameConfig, a2: int, s_a: int,
                                   s_d_prime: int, s_d: int) -> npt.NDArray[Any]:
        """
        Computes the next local belief of the defender using a Bayesian filter

        :param o: the latest observation
        :param a1: the latest action of player 1
        :param d_b: the current defender belief
        :param pi2: the policy of player 2
        :param config: the game config
        :param a2: the attacker action (for debugging, should be consistent with pi2)
        :param s_a: the true current attacker state (for debugging)
        :param s_d: the previous defender state
        :param s_d_prime: the new defender state
        :return: the new belief
        """
        b_prime = np.zeros(len(config.S_A))
        for s_a_prime in config.S_A:
            b_prime[s_a_prime] = IntrusionResponseGameUtil.bayes_filter_defender_belief(
                s_a_prime=s_a_prime, o=o, a1=a1, d_b=d_b, pi2=pi2, config=config, s_d_prime=s_d_prime, s_d=s_d)
        if round(sum(b_prime), 2) != 1:
            print(f"error, b_prime:{b_prime}, o:{o}, a1:{a1}, d_b:{d_b}, pi2:{pi2}, "
                  f"a2: {a2}, s:{s_a}")
        assert round(sum(b_prime), 2) == 1
        return b_prime

    @staticmethod
    def sample_attacker_action(pi2: npt.NDArray[Any], s: int) -> int:
        """
        Samples the attacker action

        :param pi2: the attacker action
        :param s: the game state
        :return: a2 (the attacker action
        """
        return int(np.random.choice(np.arange(0, len(pi2[s])), p=pi2[s]))

    @staticmethod
    def sample_defender_action(pi1: npt.NDArray[Any], s: int) -> int:
        """
        Samples the defender action

        :param pi1: the attacker action
        :param s: the game state
        :return: a1 (the defender action
        """
        return int(np.random.choice(np.arange(0, len(pi1[s])), p=pi1[s]))

    @staticmethod
    def next_local_attacker_belief(o: int, a1: int, a_b: npt.NDArray[Any], pi1: npt.NDArray[Any],
                                   config: LocalIntrusionResponseGameConfig, a2: int, s_d: int,
                                   s_a_prime: int, s_a: int) -> npt.NDArray[Any]:
        """
        Computes the next local belief of the attacker using a Bayesian filter

        :param o: the latest observation
        :param a1: the latest action of player 1 (for debugging, should be consistent with pi1)
        :param a_b: the current attacker belief
        :param pi1: the policy of player 1
        :param config: the game config
        :param a2: the attacker action
        :param s_d: the true current defender state (for debugging)
        :param s_a_prime: the new attacker state
        :param s_a: the previous attacker state
        :return: the new belief
        """
        b_prime = np.zeros(len(config.S_D))
        for s_d_prime in list(range(len(config.S_D))):
            b_prime[s_d_prime] = IntrusionResponseGameUtil.bayes_filter_attacker_belief(
                s_a_prime=s_a_prime, o=o, a2=a2, a_b=a_b, pi1=pi1, config=config, s_d_prime=s_d_prime, s_a=s_a)
        if round(sum(b_prime), 2) != 1:
            print(f"error, b_prime:{b_prime}, o:{o}, a1:{a1}, d_b:{a_b}, pi1:{pi1}, "
                  f"a2: {a2}, s_d:{s_d}, s_a: {s_a}, s_a_prime:{s_a_prime}")
        assert round(sum(b_prime), 2) == 1
        return b_prime

    @staticmethod
    def bayes_filter_attacker_belief(s_a_prime: int, o: int, a2: int, a_b: npt.NDArray[Any], pi1: npt.NDArray[Any],
                                     config: LocalIntrusionResponseGameConfig, s_d_prime: int, s_a: int) -> float:
        """
        A Bayesian filter to compute the belief of player 2 of being in s_prime when observing o after
        taking action a in belief b given that the opponent follows strategy pi1

        :param s_a_prime: the current attacker state
        :param s_a_prime: the previous attacker state
        :param o: the observation
        :param a2: the action of player 2
        :param a_b: the current attacker belief point
        :param pi1: the policy of player 2
        :param s_d_prime: the defender state  to compute the belief of
        :return: b_prime(s_prime_d)
        """
        norm = 0
        for s_d in list(range(len(config.S_D))):
            s_idx = config.states_to_idx[(s_d + 1, s_a)]
            for a1 in config.A1:
                for s_prime_d_1 in list(range(len(config.S_D))):
                    s_prime_idx = config.states_to_idx[(s_prime_d_1 + 1, s_a_prime)]
                    obs_prob = config.Z[a1][a2][s_prime_idx][o]
                    norm += a_b[s_d] * obs_prob * config.T[0][a1][a2][s_idx][s_prime_idx] * pi1[s_d][a1]
        if norm == 0:
            return 0
        temp = 0
        s_prime_idx = config.states_to_idx[(s_d_prime + 1, s_a_prime)]
        for s_d in list(range(len(config.S_D))):
            s_idx = config.states_to_idx[(s_d + 1, s_a)]
            for a1 in config.A1:
                temp += \
                    (config.Z[a1][a2][s_prime_idx][o]
                     * config.T[0][a1][a2][s_idx][s_prime_idx] * a_b[s_d] * pi1[s_d][a1])
        b_prime_s_prime = temp / norm
        if round(b_prime_s_prime, 2) > 1:
            print(f"b_prime_s_prime >= 1: {b_prime_s_prime}, a2:{a2}, s_prime:{s_a_prime}, o:{o}, pi1:{pi1}")
        assert round(b_prime_s_prime, 2) <= 1
        return b_prime_s_prime

    @staticmethod
    def get_local_defender_pomdp_solver_file(S: npt.NDArray[Any], A1: npt.NDArray[Any], A2: npt.NDArray[Any],
                                             O: npt.NDArray[Any], R: npt.NDArray[Any], T: npt.NDArray[Any],
                                             Z: npt.NDArray[Any],
                                             static_attacker_strategy: Policy,
                                             s_1_idx: int, discount_factor: float = 0.99) -> str:
        """
        Gets the POMDP environment specification based on the format at http://www.pomdp.org/code/index.html,
        for the defender's local problem against a static attacker

        :param S: the state spaec
        :param A1: the defender's local action space
        :param A2: the attacker's local action space
        :param O: the observation space
        :param R: the reward tensor
        :param T: the transition tensor
        :param static_attacker_strategy: the static attacker opponent strategy
        :param s_1_idx: the initial state index
        :param discount_factor: the discount  factor
        :return: the file content string
        """
        file_str = ""
        file_str = file_str + f"discount: {discount_factor}\n\n"
        file_str = file_str + "values: reward\n\n"
        file_str = file_str + f"states: {len(S)}\n\n"
        file_str = file_str + f"actions: {len(A1)}\n\n"
        file_str = file_str + f"observations: {len(O)}\n\n"
        initial_belief = [0] * len(S)
        initial_belief[s_1_idx] = 1
        initial_belief_str = " ".join(list(map(lambda x: str(x), initial_belief)))
        file_str = file_str + f"start: {initial_belief_str}\n\n\n"
        T = T[0]
        num_transitions = 0
        for s in range(len(S)):
            for a1 in range(len(A1)):
                probs = []
                for s_prime in range(len(S)):
                    num_transitions += 1
                    prob = 0.0
                    pi2 = np.array(static_attacker_strategy.stage_policy(None))[
                        S[s][env_constants.STATES.A_STATE_INDEX]]
                    for a2 in range(len(A2)):
                        prob += pi2[a2] * T[a1][a2][s][s_prime]
                    file_str = file_str + f"T: {a1} : {s} : {s_prime} {prob}\n"
                    probs.append(prob)
                assert round(sum(probs), 3) == 1
        file_str = file_str + "\n\n"
        for s_prime in range(len(S)):
            for a1 in range(len(A1)):
                total_transition_prob = 0
                a2_transition_probs = np.zeros(len(A2))
                for s in range(len(S)):
                    pi2 = np.array(static_attacker_strategy.stage_policy(None))[
                        S[s][env_constants.STATES.A_STATE_INDEX]]
                    for a2 in range(len(A2)):
                        total_transition_prob += pi2[a2] * T[a1][a2][s][s_prime]
                        a2_transition_probs[a2] += T[a1][a2][s][s_prime] * pi2[a2]
                probs = []
                for o in range(len(O)):
                    prob = 0.0
                    if total_transition_prob == 0:
                        prob = (1 / len(O))
                    else:
                        for a2 in range(len(A2)):
                            a2_prob = (a2_transition_probs[a2]) / total_transition_prob
                            prob += a2_prob * Z[a1][a2][s_prime][o]
                    file_str = file_str + f"O : {a1} : {s_prime} : {o} {prob}\n"
                    probs.append(prob)
                assert round(sum(probs), 3) == 1
        file_str = file_str + "\n\n"

        for s in range(len(S)):
            for a1 in range(len(A1)):
                for s_prime in range(len(S)):
                    pi2 = np.array(static_attacker_strategy.stage_policy(None))[
                        S[s][env_constants.STATES.A_STATE_INDEX]]
                    for o in range(len(O)):
                        r = 0
                        for a2 in range(len(A2)):
                            r += pi2[a2] * R[0][a1][a2][s]
                        file_str = file_str + f"R: {a1} : {s} : {s_prime} : {o} {r}\n"
        return file_str

    @staticmethod
    def stopping_bayes_filter(s_prime: int, o: int, a1: int, b: npt.NDArray[Any], pi2: npt.NDArray[Any],
                              S: npt.NDArray[Any], Z: npt.NDArray[Any], T: npt.NDArray[Any], A2: npt.NDArray[Any],
                              O: npt.NDArray[Any]) -> float:
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
        norm = 0
        for s in S:
            for a2 in A2:
                for s_prime_1 in S:
                    prob_1 = Z[a1][a2][s_prime_1 + 1][o]
                    norm += b[s] * prob_1 * T[a1][a2][s + 1][s_prime_1 + 1] * pi2[s][a2]
        if norm == 0:
            print(f"zero norm, s_prime:{s_prime}, o:{o}, a1:{a1}, b:{b}")
            return 0
        temp = 0

        for s in S:
            for a2 in A2:
                temp += Z[a1][a2][s_prime + 1][o] * T[a1][a2][s + 1][s_prime + 1] * b[s] * pi2[s][a2]
        b_prime_s_prime = temp / norm
        if round(b_prime_s_prime, 3) > 1:
            print(f"b_prime_s_prime >= 1: {b_prime_s_prime}, a1:{a1}, s_prime:{s_prime}, o:{o}, pi2:{pi2}")
        assert round(b_prime_s_prime, 3) <= 1
        return b_prime_s_prime

    @staticmethod
    def stopping_p_o_given_b_a1_a2(o: int, b: npt.NDArray[Any], a1: int, a2: int, S: npt.NDArray[Any],
                                   Z: npt.NDArray[Any], T: npt.NDArray[Any]) -> float:
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
        for s in S:
            for s_prime in S:
                prob += b[s] * T[a1][a2][s][s_prime] * Z[a1][a2][s_prime][o]
        assert prob < 1
        return prob

    @staticmethod
    def next_stopping_belief(o: int, a1: int, b: npt.NDArray[Any], pi2: npt.NDArray[Any], S: npt.NDArray[Any],
                             Z: npt.NDArray[Any], O: npt.NDArray[Any], T: npt.NDArray[Any], A2: npt.NDArray[Any],
                             a2: int = 0, s: int = 0) -> npt.NDArray[Any]:
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
        b_prime = np.zeros(len(S))
        for s_prime in S:
            b_prime[s_prime] = IntrusionResponseGameUtil.stopping_bayes_filter(s_prime=s_prime, o=o, a1=a1, b=b,
                                                                               pi2=pi2, S=S, Z=Z, T=T, A2=A2, O=O)
        if round(sum(b_prime), 2) != 1:
            print(f"error, b_prime:{b_prime}, o:{o}, a1:{a1}, b:{b}, pi2:{pi2}, "
                  f"a2: {a2}, s:{s}")
        assert round(sum(b_prime), 2) == 1
        return b_prime
