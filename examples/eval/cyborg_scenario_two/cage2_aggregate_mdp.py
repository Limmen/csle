from typing import List, Tuple, Dict
import random
import numpy as np
from itertools import product
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState


class Cage2AggregateMDP:
    """
    Aggregate MDP for Cage-2 with the bline attacker
    """

    @staticmethod
    def get_aggregate_control(mu: List[List[float]], aggregate_state: int, id_to_state: Dict[int, List[int]]) -> int:
        """
        Gets the aggregate control prescribed by policy mu to the aggregate state

        :param mu: the base policy
        :param aggregate_state: the aggregate state id
        :param id_to_state: the aggregate-state-id to aggregate state map
        :return: the control prescribed by the base policy in the aggregate MDP
        """
        u = int(np.argmax(mu[aggregate_state]))
        decoys_per_host = CyborgEnvUtil.get_decoy_actions_per_host(scenario=2)
        state = id_to_state[aggregate_state]
        decoy_state = state[2:]
        if decoy_state[u] >= len(decoys_per_host[Cage2AggregateMDP.aggregate_control_to_original_target(u)]):
            possible_targets = [2, 6]
            if state[3] != -1:
                possible_targets.append(state[3])
                if state[3] in [3, 4]:
                    possible_targets.append(1)
                else:
                    possible_targets.append(0)
            for ph in possible_targets:
                if decoy_state[ph] < \
                        len(decoys_per_host[Cage2AggregateMDP.aggregate_control_to_original_target(ph)]):
                    u = ph
        return Cage2AggregateMDP.aggregate_control_to_original_control()[u]

    @staticmethod
    def target_2(target_1: int) -> int:
        """
        Gets the second bline target based on the first target

        :param target_1: the first host targeted by bline
        :return: the second host targeted by bline
        """
        if target_1 == -1:
            return -1
        if target_1 in [3, 4]:
            return 1
        return 0

    @staticmethod
    def target(target_1: int, red_state: int) -> int:
        """
        Gets the current bline target based on the first target and the state

        :param target_1: the first host targeted by bline
        :param red_state: the current attacker satte
        :return: the current target of bline
        """
        if red_state == 0:
            return -1
        if red_state in [1, 2]:
            return target_1
        if red_state in [3, 4, 5]:
            if target_1 in [3, 4]:
                return 1
            else:
                return 0
        if red_state in [6, 7, 8, 9]:
            return 2
        if red_state in [10, 11, 12, 13, 14]:
            return 7

    @staticmethod
    def get_aggregate_state(s: CyborgWrapperState, state_to_id: Dict[str, int]) -> int:
        """
        Converts the cyborg state into the aggregate state

        :param s: the cyborg wrapper state
        :param state_to_id: the aggegate-state-to-aggregate-id map
        :return: the aggregate state correspnding to the cyborg state
        """
        decoy_state = Cage2AggregateMDP.get_aggregate_decoy_state(s.get_decoy_state())
        red_state = s.red_agent_state
        target_1 = -1
        if red_state == 1:
            target_1 = Cage2AggregateMDP.red_target_to_aggregate_target(s.red_agent_target)
        elif red_state >= 1:
            target_1 = Cage2AggregateMDP.red_target_to_aggregate_target(s.red_action_targets[1])
        decoy_state_str = ",".join(list(map(lambda x: str(x), decoy_state)))
        state_str = f"{red_state},{target_1},{decoy_state_str}"
        return state_to_id[state_str]

    @staticmethod
    def max_decoy(u: int) -> int:
        """
        Gets the max decoy state of a given aggregate control

        :param u: the aggregate control
        :return: the max decoy state for the host targeted by that control
        """
        return {0: 4, 1: 1, 2: 1, 3: 4, 4: 4, 5: 2, 6: 4}[u]

    @staticmethod
    def feasible_next_states(state_id: int, state_to_id: Dict[str, int], id_to_state: Dict[int, List[int]], u: int) \
            -> List[int]:
        """
        Calculates the feasible set of next aggregate states when taking a control in a given aggregate state

        :param state_id: the id of the current aggregate state
        :param state_to_id: the aggregate state to aggregate state id map
        :param id_to_state: the aggregate state id to aggregate state map
        :param u: the aggregate control
        :return: a list of feasible next aggregate states
        """
        B_LINE_AGENT_JUMPS = [0, 1, 2, 2, 2, 2, 5, 5, 5, 5, 9, 9, 9, 12, 13]
        state = id_to_state[state_id]
        red_state = state[0]
        target_1 = state[1]
        decoy_state = state[2:]
        feasible_next_red_states = []
        if red_state in [0, 1, 3, 4, 6, 7, 8, 10, 11, 13]:
            feasible_next_red_states = [red_state + 1]
        if red_state == 14:
            feasible_next_red_states = [14]
        if red_state == 2:
            feasible_next_red_states = [red_state, red_state + 1]
        if red_state in [5, 9, 12]:
            feasible_next_red_states = [red_state + 1, B_LINE_AGENT_JUMPS[red_state]]

        next_decoy_state = decoy_state.copy()
        if u == 0:
            next_decoy_state[0] = min(next_decoy_state[0] + 1, Cage2AggregateMDP.max_decoy(u))
        elif u == 1:
            next_decoy_state[1] = min(next_decoy_state[1] + 1, Cage2AggregateMDP.max_decoy(u))
        elif u == 2:
            next_decoy_state[2] = min(next_decoy_state[2] + 1, Cage2AggregateMDP.max_decoy(u))
        elif u == 3:
            next_decoy_state[3] = min(next_decoy_state[3] + 1, Cage2AggregateMDP.max_decoy(u))
        elif u == 4:
            next_decoy_state[4] = min(next_decoy_state[4] + 1, Cage2AggregateMDP.max_decoy(u))
        elif u == 5:
            next_decoy_state[5] = min(next_decoy_state[5] + 1, Cage2AggregateMDP.max_decoy(u))
        elif u == 6:
            next_decoy_state[6] = min(next_decoy_state[6] + 1, Cage2AggregateMDP.max_decoy(u))

        feasible_next_target_1 = []
        if red_state == 0:
            feasible_next_target_1.append(3)
            feasible_next_target_1.append(4)
            feasible_next_target_1.append(5)
            feasible_next_target_1.append(6)
        else:
            feasible_next_target_1 = [target_1]

        feasible_next_states = []
        for feasible_target_1 in feasible_next_target_1:
            for feasible_red_state in feasible_next_red_states:
                f_state = f"{feasible_red_state},{feasible_target_1}," \
                          f"{','.join(list(map(lambda x: str(x), next_decoy_state)))}"
                feasible_next_states.append(state_to_id[f_state])
        return feasible_next_states

    @staticmethod
    def exploit_success_probability(target: int, decoy_state: int) -> float:
        """
        Calculates the probability that an exploit against the given target is successful, given the decoy state

        :param target: the targeted host
        :param decoy_state: the current decoy state
        :return: the probability that an exploit against the target is successful
        """
        if target == 0:
            return [1.0, 0.25, 0.1238899, 0.0838379, 0.083196][decoy_state]
        elif target == 1:
            return [1.0, 0.250012][decoy_state]
        elif target == 2:
            return [1.0, 0.25029][decoy_state]
        elif target == 3:
            return [1.0, 0.87456, 0.832632, 0.813176, 0.799056][decoy_state]
        elif target == 4:
            return [1.0, 0.250698, 0.166932, 0.124348, 0.09942][decoy_state]
        elif target == 5:
            return [1.0, 1.0, 0.93785][decoy_state]
        elif target == 6:
            return 1
        elif target == 7:
            return [1.0, 0.25038, 0.12526, 0.082999, 0.083086][decoy_state]

    @staticmethod
    def transition_probability(state_to_id: Dict[str, int], id_to_state: Dict[int, List[int]], x: int,
                               x_prime: int, u: int) -> float:
        """
        Calculates P(x_prime | x, u), where ,x_prime,x,u are aggregate states and controls

        :param state_to_id: the aggregate state to aggregate state id map
        :param id_to_state: the aggregate state id to aggregate state map
        :param x: the current aggregate state ID
        :param x_prime: the next aggregate state ID
        :param u: the aggregate control
        :return: P(x_prime | x, u)
        """
        feasible_next_states = Cage2AggregateMDP.feasible_next_states(state_id=x, state_to_id=state_to_id,
                                                                      id_to_state=id_to_state, u=u)
        if x_prime not in feasible_next_states:
            return 0
        state = id_to_state[x]
        state_prime = id_to_state[x_prime]
        red_state = state[0]
        target_1 = state[1]
        decoy_state = state[2:]
        if red_state == 0:
            return 0.25
        if red_state == 14:
            return 1
        if red_state in [1, 3, 4, 6, 7, 8, 10, 11, 13]:
            return 1
        target = Cage2AggregateMDP.target(target_1=target_1, red_state=red_state)
        next_red_state = state_prime[0]
        if target == 6:
            ds = 0
        elif target == 7:
            ds = decoy_state[6]
        else:
            ds = decoy_state[target]
        exploit_success_prob = Cage2AggregateMDP.exploit_success_probability(target=target, decoy_state=ds)
        if (next_red_state == red_state + 1) and red_state in [2, 5, 9, 12]:
            return exploit_success_prob
        else:
            return 1 - exploit_success_prob

    @staticmethod
    def aggregate_control_to_original_control() -> Dict[int, int]:
        """
        Returns a dict that maps an aggregate control to the original control space

        :return: a dict that maps an aggregate control to the original control space
        """
        return {0: 27, 1: 28, 2: 29, 3: 30, 4: 31, 5: 32, 6: 35}

    @staticmethod
    def get_aggregate_decoy_state(decoy_state: List[int]) -> List[int]:
        """
        Converts a decoy state into an aggregate decoy state

        :param decoy_state: the cyborg decoy state
        :return: the aggregate decoy state
        """
        ds = []
        decoy_hosts = [1, 2, 3, 9, 10, 11, 7]
        for dh in decoy_hosts:
            ds.append(decoy_state[dh])
        return ds

    @staticmethod
    def get_aggregate_decoy_state_space() -> List[Tuple[int]]:
        """
        Gets the aggregate decoy state space

        :return: the aggregate decoy state space
        """
        values = [range(5), range(2), range(2), range(5), range(5), range(3), range(5)]
        return list(product(*values))

    @staticmethod
    def red_target_to_aggregate_target(target: int) -> int:
        """
        Converts a red target to the corresponding aggregate target

        :param target: the red target in cyborg
        :return: the aggregate red target
        """
        red_target_to_agg_target = {0: -1, 1: 0, 2: 1, 3: 2, 4: 0, 5: 0, 6: 0, 7: 7, 8: -1, 9: 3, 10: 4, 11: 5, 12: 6}
        return red_target_to_agg_target[target]

    @staticmethod
    def aggregate_control_to_original_target(u: int) -> int:
        """
        Converts an aggregate control to the corresponding target host in cyborg

        :param u: the control
        :return: the cyborg target
        """
        aggregate_target_to_red_target = {0: 1, 1: 2, 2: 3, 3: 9, 4: 10, 5: 11, 6: 7}
        return aggregate_target_to_red_target[u]

    @staticmethod
    def X() -> Tuple[List[int], Dict[str, int], Dict[int, List[int]]]:
        """
        Gets the aggregate state space

        :return: The state aggregate space, a lookup dict from state id to state, and a lookup dict from state to id
        """
        decoy_states = Cage2AggregateMDP.get_aggregate_decoy_state_space()
        state_to_id = {}
        id_to_state = {}
        X = []
        state_id = 0
        target_1s = [-1, 3, 4, 5, 6]
        for red_state in range(15):
            for target_1 in target_1s:
                if red_state == 0 and target_1 != -1:
                    continue
                if red_state >= 1 and target_1 == -1:
                    continue
                for decoy_state in decoy_states:
                    state_to_id[f"{red_state},{target_1},"
                                f"{','.join(list(map(lambda x: str(x), list(decoy_state))))}"] = state_id
                    id_to_state[state_id] = [red_state, target_1] + list(decoy_state)
                    X.append(state_id)
                    state_id += 1
        return X, state_to_id, id_to_state

    @staticmethod
    def U() -> List[int]:
        """
        Gets the aggregate control space

        :return: the aggregate control space
        """
        return list(range(7))

    @staticmethod
    def meaningful_decoys(red_state: int, target_1: int) -> List[int]:
        """
        Returns the list of meaningful decoys, i.e., decoys that may influence the attacker

        :param red_state: the state of the attacker
        :param target_1: the first targeted host of the attacker
        :return: the list of decoys that can affect the attacker
        """
        if red_state == 0:
            return [0, 1, 2, 3, 4, 5, 6]
        if red_state > 0 and target_1 in [3, 4]:
            return [target_1, 1, 2, 6]
        return [target_1, 0, 2, 6]

    @staticmethod
    def cost_function(x: int, id_to_state: Dict[int, List[int]], u: int) -> float:
        """
        The aggregate cost function

        :param x: the aggregate state id
        :param id_to_state: the map of aggregate state ids to aggregate states
        :param u: the aggregate control
        :return: the cost c(x,u)
        """
        cost = 0
        red_state = id_to_state[x][0]
        target_1 = id_to_state[x][1]
        decoy_state = id_to_state[x][2:]
        if u not in Cage2AggregateMDP.meaningful_decoys(red_state=red_state, target_1=target_1):
            cost += 0.05  # Unnecessary decoy
        if decoy_state[u] == Cage2AggregateMDP.max_decoy(u):
            decoys_left = sum(list(map(lambda x: int(decoy_state[x] != Cage2AggregateMDP.max_decoy(x)),
                                       Cage2AggregateMDP.meaningful_decoys(red_state=red_state, target_1=target_1))))
            if decoys_left > 0:
                cost += 0.05  # Unnecessary decoy
        if red_state in [3, 4, 5]:
            return cost + 0.1
        elif red_state in [6, 7, 8, 9]:
            return cost + 1
        elif red_state in [10, 11, 12]:
            return cost + 2
        elif red_state in [13, 14]:
            return cost + 3
        return cost

    @staticmethod
    def vi(X: List[int], U: List[int], gamma: float, epsilon: float, verbose: bool, state_to_id: Dict[str, int],
           id_to_state: Dict[int, List[int]]) -> Tuple[List[List[float]], List[float]]:
        """
        Implements value iteration in the aggregate MDP

        :param X: the aggregate state space
        :param U: the aggregate control space
        :param gamma: the discount factor
        :param epsilon: the convergence threshold
        :param verbose: booleain flag indicating whether verbose logging should be enabled or not
        :param state_to_id: the aggregate state to aggregate state id map
        :param id_to_state: the aggregate state id to aggregate state map
        :return:  mu (computed policy), J (computed cost-to-go)
        """
        action_id_to_type_and_host, type_and_host_to_action_id \
            = CyborgEnvUtil.get_action_dicts(scenario=2, reduced_action_space=True, decoy_state=True,
                                             decoy_optimization=False)
        J = np.zeros(len(X))
        iteration = 0
        while True:
            delta = 0
            for x in X:
                if x % 100000 == 0:
                    print(f"{x}/{len(X)}")
                u_star, J_u_star = Cage2AggregateMDP.TJx(x=x, J=J, U=U, gamma=gamma, state_to_id=state_to_id,
                                                         id_to_state=id_to_state)
                delta = max(delta, np.abs(J_u_star - J[x]))
                J[x] = J_u_star
            iteration += 1
            if verbose:
                print(f"VI iteration: {iteration}, delta: {delta}, epsilon: {epsilon}")
                ssx = [state_to_id["0,-1,0,0,0,0,0,0,0"], state_to_id["1,3,0,0,0,0,0,0,0"],
                       state_to_id["2,3,0,0,0,0,0,0,0"],
                       state_to_id["3,3,0,1,0,0,0,0,0"], state_to_id["4,3,0,1,0,0,0,0,0"],
                       state_to_id["5,3,0,1,0,0,0,0,0"], state_to_id["6,3,0,1,0,0,0,0,0"],
                       state_to_id["7,3,0,1,0,0,0,0,0"], state_to_id["8,3,0,1,0,0,0,0,0"],
                       state_to_id["9,3,0,1,0,0,0,0,0"], state_to_id["10,3,0,1,0,0,0,0,0"],
                       state_to_id["11,3,0,1,0,0,0,0,0"], state_to_id["12,3,0,1,0,0,0,0,0"],
                       state_to_id["13,3,0,1,0,0,0,0,0"], state_to_id["14,3,0,1,0,0,0,0,0"]]
                for sx in ssx:
                    u = Cage2AggregateMDP.TJx(x=sx, J=J, U=U, gamma=gamma, state_to_id=state_to_id,
                                              id_to_state=id_to_state)[0]
                    action = Cage2AggregateMDP.aggregate_control_to_original_control()[u]
                    sts = id_to_state[sx]
                    print(f"mu({sts})={action_id_to_type_and_host[action]}")
            if delta < epsilon:
                break
        mu = Cage2AggregateMDP.policy(X=X, U=U, gamma=gamma, J=J, state_to_id=state_to_id, id_to_state=id_to_state)
        return mu, J

    @staticmethod
    def TJx(x: int, J: List[float], U: List[int], gamma: float, state_to_id: Dict[str, int],
            id_to_state: Dict[int, List[int]]) -> Tuple[int, float]:
        """
        Implements the Bellman operator (TJ))(x)

        :param x: the aggregate state id
        :param J: the cost-to-go function
        :param U: the aggregate control space
        :param gamma: the discount factor
        :param state_to_id: the aggregate state to aggregate state Id map
        :param id_to_state: the aggregate state id to aggregate state map
        :return: the best control and its value
        """
        Q_x = np.zeros(len(U))
        for u in U:
            feasible_x_prime = Cage2AggregateMDP.feasible_next_states(state_id=x, state_to_id=state_to_id,
                                                                      id_to_state=id_to_state, u=u)
            for x_prime in feasible_x_prime:
                p = Cage2AggregateMDP.transition_probability(state_to_id=state_to_id, id_to_state=id_to_state, x=x,
                                                             x_prime=x_prime, u=u)
                c = Cage2AggregateMDP.cost_function(x=x, id_to_state=id_to_state, u=u)
                Q_x[u] += p * (c + gamma * J[x_prime])
        u_star = int(np.argmin(Q_x))
        return u_star, Q_x[u_star]

    @staticmethod
    def policy(X: List[int], U: List[int], gamma: float, J: List[int], state_to_id: Dict[str, int],
               id_to_state: Dict[int, List[int]]) -> List[List[float]]:
        """
        Constructs a policy based on J

        :param X: the aggregate state space
        :param U: the aggregate control spac
        :param gamma: the discount factor
        :param J: the cost-to-go function
        :param state_to_id: the aggregate state to aggregate state id map
        :param id_to_state: the aggregate state id to aggregate state map
        :return: the policy mu that acts greedily according to J
        """
        mu = np.zeros((len(X), len(U)))
        for x in X:
            mu[x][Cage2AggregateMDP.TJx(x=x, J=J, U=U, gamma=gamma, state_to_id=state_to_id,
                                        id_to_state=id_to_state)[0]] = 1.0
        return list(mu.tolist())

    @staticmethod
    def run_vi(epsilon: float = 0.1, gamma: float = 0.99) -> None:
        """
        Runs value iteration and saves the results to disk

        :param epsilon: the convergence threshold
        :param gamma: the discount factor
        :return: None
        """
        X, state_to_id, id_to_state = Cage2AggregateMDP.X()
        U = Cage2AggregateMDP.U()
        mu, J = Cage2AggregateMDP.vi(X=X, U=U, gamma=gamma, epsilon=epsilon, verbose=True, state_to_id=state_to_id,
                                     id_to_state=id_to_state)
        np.savetxt("mu3.txt", mu)
        np.savetxt("J3.txt", J)

    @staticmethod
    def test(N: int) -> None:
        """
        Simulates N test trajectories of the aggregate MDP

        :param N: the number of test trajectories
        :return: None
        """
        X, state_to_id, id_to_state = Cage2AggregateMDP.X()
        print(len(X))
        U = Cage2AggregateMDP.U()
        for k in range(N):
            x = state_to_id["0,-1,0,0,0,0,0,0,0"]
            while id_to_state[x][0] != 14:
                u = random.choice(U)
                feasible_states = Cage2AggregateMDP.feasible_next_states(state_id=x, state_to_id=state_to_id,
                                                                         id_to_state=id_to_state, u=u)
                probs = list(map(lambda x_prime: Cage2AggregateMDP.transition_probability(
                    state_to_id=state_to_id, id_to_state=id_to_state, x=x, x_prime=x_prime, u=u), feasible_states))
                print(f"u: {u}, x: {id_to_state[x]}")
                x = np.random.choice(feasible_states, p=probs)


if __name__ == '__main__':
    # Cage2AggregateMDP.test(N=1)
    Cage2AggregateMDP.run_vi(epsilon=0.3, gamma=0.99)
