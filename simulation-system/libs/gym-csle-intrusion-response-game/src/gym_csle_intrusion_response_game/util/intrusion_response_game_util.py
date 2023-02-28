from typing import List
import numpy as np
from scipy.stats import betabinom
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig


class IntrusionResponseGameUtil:
    """
    Class with utility functions for the intrusion response game environment
    """
    @staticmethod
    def local_initial_defender_belief(initial_zone: int, state_space: np.ndarray) -> np.ndarray:
        """
        :return: the initial belief
        """
        b1 = np.zeros((len(state_space)))
        for i in range(len(state_space)):
            if state_space[i][0] == initial_zone and state_space[i][1] == 0:
                b1[i] = 1
        return b1

    @staticmethod
    def local_state_space(number_of_zones: int):
        """
        Gets the state space of a specific node in the game

        :param number_of_zones: the number of zones in the network
        :return: the state space
        """
        state_space = []
        state_space.append([-1,-1]) # Terminal state
        for i in range(number_of_zones):
            state_space.append([i,0])
            state_space.append([i,1])
            state_space.append([i,2])
        return np.array(state_space)

    @staticmethod
    def local_defender_actions(number_of_zones: int) -> np.ndarray:
        """
        :return: the action space of the defender
        """
        return np.array(list(range(number_of_zones+1)))

    @staticmethod
    def local_attacker_actions() -> np.ndarray:
        """
        :return: the action space of the attacker
        """
        return np.array([0, 1, 2, 3])

    @staticmethod
    def local_observation_space(X_max: int):
        """
        Returns the observation space

        :param X_max: the maximum observation
        :return: O
        """
        return np.array(list(range(X_max)))

    @staticmethod
    def local_workflow_cost(beta: float, reachable: bool, s: np.ndarray, initial_zone: int):
        impact = 1
        if reachable and s[1] == 0:
            impact = 0
        return beta*impact*int(initial_zone == s[0])

    @staticmethod
    def defender_action_costs(defender_actions: np.ndarray) -> np.ndarray:
        action_costs = []
        for a1 in defender_actions:
            action_costs.append(1)
        return np.array(action_costs)

    @staticmethod
    def zones(num_zones: int) -> np.ndarray:
        return np.array(list(range(1,num_zones+1)))

    @staticmethod
    def zone_utilities(zones: np.ndarray) -> np.ndarray:
        zone_utilities = []
        for zone in zones:
            zone_utilities.append(1)
        return np.array(zone_utilities)

    @staticmethod
    def zone_detection_probabilities(zones: np.ndarray) -> np.ndarray:
        zone_detection_probabilities = []
        for zone in zones:
            zone_detection_probabilities.append(1/len(zones))
        return np.array(zone_detection_probabilities)

    @staticmethod
    def local_attack_success_probabilities():
        attack_success_probabilities = [
            0.2,
            0.3
        ]
        return np.array(attack_success_probabilities)

    @staticmethod
    def local_intrusion_cost(defender_action: int, defender_action_costs: np.ndarray, reachable: bool, s: np.ndarray,
                             zone_utilities: np.ndarray) -> float:
        if not reachable:
            return defender_action_costs[defender_action]
        return zone_utilities[s[0]]*int((s[1]==2)) + defender_action_costs[defender_action]

    @staticmethod
    def local_reward_function(s: np.ndarray, defender_action: int, lamb: float, mu: float,
                              reachable: bool, initial_zone: int, beta: float, defender_action_costs: np.ndarray,
                              zone_utilities: np.ndarray):
        if s[0] == -1 and s[1] == -1:
            return 0
        workflow_cost = IntrusionResponseGameUtil.local_workflow_cost(beta=beta,reachable=reachable, s=s,
                                                                      initial_zone=initial_zone)
        intrusion_cost = IntrusionResponseGameUtil.local_intrusion_cost(defender_action=defender_action,
                                                                        defender_action_costs=defender_action_costs,
                                                                        reachable=reachable, s=s,
                                                                        zone_utilities=zone_utilities)
        return lamb*workflow_cost + mu*intrusion_cost

    @staticmethod
    def local_reward_tensor(lamb: float, mu: float,
                            defender_action_costs: np.ndarray,
                            reachable: bool, zone_utilities: np.ndarray,
                            initial_zone: int, beta: float,
                            state_space: np.ndarray, defender_actions: np.ndarray,
                            attacker_actions: np.ndarray) -> np.ndarray:
        """
        :return: a |A1|x|A2|x|S| tensor
        """
        R_tensor = []
        for a1 in defender_actions:
            a1_rews = []
            for a2 in attacker_actions:
                a1_a2_rews = []
                for s in state_space:
                    a1_a2_rews.append(IntrusionResponseGameUtil.local_reward_function(
                        s=s, defender_action=a1, lamb=lamb, mu=mu, reachable=reachable, initial_zone=initial_zone,
                        beta=beta, defender_action_costs=defender_action_costs, zone_utilities=zone_utilities
                    ))
                a1_rews.append(a1_a2_rews)
            R_tensor.append(a1_rews)
        R_tensor = np.array(R_tensor)
        return R_tensor

    @staticmethod
    def local_transition_probability(s: np.ndarray, s_prime: np.ndarray, a1: int, a2: int,
                                     zone_detection_probabilities: np.ndarray, attack_success_probabilities: np.ndarray):
        if s_prime[0] == -1 and s_prime[1] == -1 and a2 != 0:
            return zone_detection_probabilities[s[0]]
        if a1 != 0:
            if s_prime[0] == a1 and s_prime[1] == 0:
                return 1*(1-int(a2 != 0)*zone_detection_probabilities[s[0]])
            else:
                return 0
        else:
            if a2 == 0 and s_prime[0] == s[0] and s_prime[1] == s[1]:
                return 1*(1-int(a2 != 0)*zone_detection_probabilities[s[0]])
            # Recon
            if a2 == 1 and s_prime[0] == s[0] and s[1] < 2 and s_prime[1] == 1:
                return 1*(1-int(a2 != 0)*zone_detection_probabilities[s[0]])
            # Brute-force
            if a2 == 2 and s[1] == 1:
                if s_prime[1] == 2:
                    return (attack_success_probabilities[0])*(1-int(a2 != 0)*zone_detection_probabilities[s[0]])
                elif s_prime[1] == 1:
                    return (1-attack_success_probabilities[0])*(1-int(a2 != 0)*zone_detection_probabilities[s[0]])
            # Exploit
            if a2 == 3 and s[1] == 1 and s_prime[1] == 2:
                if s_prime[1] == 2:
                    return attack_success_probabilities[1]*(1-int(a2 != 0)*zone_detection_probabilities[s[0]])
                elif s_prime[1] == 1:
                    return (1-attack_success_probabilities[1])*(1-int(a2 != 0)*zone_detection_probabilities[s[0]])
        return 0

    @staticmethod
    def local_transition_tensor(zone_detection_probabilities: np.ndarray, attack_success_probabilities: np.ndarray,
                                state_space: np.ndarray, defender_actions: np.ndarray,
                                attacker_actions: np.ndarray) -> np.ndarray:
        """
        :return: a |A1|x|A2||S|^2 tensor
        """
        T = []
        for a1 in defender_actions:
            a1_probs = []
            for a2 in attacker_actions:
                a1_a2_probs = []
                for s in state_space:
                    a1_a2_s_probs = []
                    for s_prime in state_space:
                        p = IntrusionResponseGameUtil.local_transition_probability(
                            s=s,s_prime=s_prime, a1=a1, a2=a2,
                            zone_detection_probabilities=zone_detection_probabilities,
                            attack_success_probabilities=attack_success_probabilities,
                        )
                        a1_a2_s_probs.append(p)
                    a1_a2_probs.append(a1_a2_s_probs)
                a1_probs.append(a1_a2_probs)
            T.append(a1_probs)
        T = np.array(T)
        return T

    @staticmethod
    def local_observation_tensor(X_max: int, state_space: np.ndarray, defender_actions: np.ndarray,
                                 attacker_actions: np.ndarray, observation_space: np.ndarray):
        """
        :return: a |A1|x|A2|x|S|x|O| tensor
        """
        intrusion_dist = []
        no_intrusion_dist = []
        intrusion_rv = betabinom(n=X_max-1, a=1, b=0.7)
        no_intrusion_rv = betabinom(n=X_max-1, a=0.7, b=3)
        for i in range(X_max):
            intrusion_dist.append(intrusion_rv.pmf(i))
            no_intrusion_dist.append(no_intrusion_rv.pmf(i))
        Z = []
        for a1 in defender_actions:
            a1_probs = []
            for a2 in attacker_actions:
                a1_a2_probs = []
                for s in state_space:
                    if a2 != 0:
                        a1_a2_s_probs = intrusion_dist
                    else:
                        a1_a2_s_probs = no_intrusion_dist
                    a1_a2_probs.append(a1_a2_s_probs)
                a1_probs.append(a1_a2_probs)
            Z.append(a1_probs)
        Z = np.array(Z)
        return Z

    @staticmethod
    def sample_next_state(T: np.ndarray, s: int, a1: int, a2: int, S: np.ndarray) -> int:
        """
        Samples the next state

        :param T: the transition operator
        :param s: the current state
        :param a1: the defender action
        :param a2: the attacker action
        :param S: the state space
        :param l: the number of stops remaining
        :return: s'
        """
        state_probs = []
        for s_prime in range(len(S)):
            state_probs.append(T[a1][a2][s][s_prime])
        s_prime = np.random.choice(np.arange(0, len(S)), p=state_probs)
        return s_prime

    @staticmethod
    def sample_initial_state(b1: np.ndarray, state_space: np.ndarray) -> np.ndarray:
        """
        Samples the initial state

        :param b1: the initial belief
        :param state_space: the state space
        :return: s1
        """
        s1 = np.random.choice(np.arange(0, len(b1)), p=b1)
        return state_space[s1]

    @staticmethod
    def sample_next_observation(Z: np.ndarray, a1: int, a2: int, s_prime: int, O: np.ndarray) -> int:
        """
        Samples the next observation
        """
        o = np.random.choice(O, p=Z[a1][a2][s_prime])
        return int(o)

    @staticmethod
    def bayes_filter(s_prime: int, o: int, a1: int, b: np.ndarray, pi2: np.ndarray,
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
        norm = 0
        for s in config.S:
            for a2 in config.A2:
                for s_prime_1 in config.S:
                    prob_1 = config.Z[a1][a2][s_prime_1][o]
                    norm += b[s] * prob_1 * config.T[a1][a2][s][s_prime_1] * pi2[s][a2]
        if norm == 0:
            return 0
        temp = 0

        for s in config.S:
            for a2 in config.A2:
                temp += config.Z[a1][a2][s_prime][o] * config.T[a1][a2][s][s_prime] * b[s] * pi2[s][a2]
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
    def next_belief(o: int, a1: int, b: np.ndarray, pi2: np.ndarray, config: StoppingGameConfig,
                    a2: int = 0, s: int = 0) -> np.ndarray:
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
            b_prime[s_prime] = IntrusionResponseGameUtil.bayes_filter(s_prime=s_prime, o=o, a1=a1, b=b,
                                                                      pi2=pi2, config=config)
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
