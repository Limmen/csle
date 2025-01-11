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
    def get_aggregate_control(mu, aggregate_state, id_to_state):
        """
        Gets the aggregate control prescribed by policy mu to the aggregate state
        """
        a = int(np.argmax(mu[aggregate_state]))
        decoys_per_host = CyborgEnvUtil.get_decoy_actions_per_host(scenario=2)
        state = id_to_state[aggregate_state]
        decoy_state = state[4:]
        if decoy_state[a] >= len(decoys_per_host[Cage2AggregateMDP.aggregate_control_target_to_original_target(a)]):
            possible_targets = [2, 6]
            if state[3] != -1:
                possible_targets.append(state[3])
                if state[3] in [3, 4]:
                    possible_targets.append(1)
                else:
                    possible_targets.append(0)
            for ph in possible_targets:
                if decoy_state[ph] < \
                        len(decoys_per_host[Cage2AggregateMDP.aggregate_control_target_to_original_target(ph)]):
                    a = ph
        return Cage2AggregateMDP.aggregate_control_to_original_control()[a]

    @staticmethod
    def get_aggregate_state(s: CyborgWrapperState, state_to_id):
        """
        Converts the cyborg state into the aggregate state
        """
        decoy_state = Cage2AggregateMDP.get_aggregate_decoy_state(s.get_decoy_state())
        red_state = s.red_agent_state
        target = -1
        target_1 = -1
        target_2 = -1
        if red_state == 1:
            target_1 = Cage2AggregateMDP.red_target_to_aggregate_target(s.red_agent_target)
            target = target_1
            if target_1 in [3, 4]:
                target_2 = 1
            else:
                target_2 = 0
        elif red_state >= 1:
            target_1 = Cage2AggregateMDP.red_target_to_aggregate_target(s.red_action_targets[1])
            if target_1 in [3, 4]:
                target_2 = 1
            else:
                target_2 = 0
            if red_state == 2:
                target = target_1
            if red_state in [3, 4, 5]:
                if target_1 in [3, 4]:
                    target = 1
                else:
                    target = 0
            if red_state in [6, 7, 8, 9]:
                target = 2
            if red_state in [10, 11, 12, 13, 14]:
                target = 7
        decoy_state_str = ",".join(list(map(lambda x: str(x), decoy_state)))
        state_str = f"{red_state},{target},{target_1},{target_2},{decoy_state_str}"
        return state_to_id[state_str]

    @staticmethod
    def feasible_next_states(state_id, state_to_id, id_to_state, u):
        """
        Calculates the feasible set of next aggregate states when taking a control in a given aggregate state
        """
        B_LINE_AGENT_JUMPS = [0, 1, 2, 2, 2, 2, 5, 5, 5, 5, 9, 9, 9, 12, 13]
        state = id_to_state[state_id]
        red_state = state[0]
        target = state[1]
        target_1 = state[2]
        target_2 = state[3]
        decoy_state = state[4:]
        feasible_next_red_states = []
        if red_state in [0, 1, 3, 4, 6, 7, 8, 10, 11, 13]:
            feasible_next_red_states = [red_state + 1]
        if red_state == 14:
            feasible_next_red_states = [14]
        if red_state == 2:
            feasible_next_red_states = [red_state, red_state + 1]
        if red_state in [5, 9, 12]:
            feasible_next_red_states = [red_state + 1, B_LINE_AGENT_JUMPS[red_state]]
        feasible_next_targets = []
        if target == -1 and red_state == 0:
            feasible_next_targets = [3, 4, 5, 6]
        if red_state in [1, 3, 4, 6, 7, 8, 10, 11, 13]:
            feasible_next_targets = [target]
        if target in [3, 4] and red_state == 2:
            feasible_next_targets = [target] + [1]
        elif target in [5, 6] and red_state == 2:
            feasible_next_targets = [target] + [0]
        elif target in [0, 1] and red_state == 5:
            feasible_next_targets = [2, target_1]
        elif target == 2 and red_state == 9:
            feasible_next_targets = [7, target_2]
        elif target == 7 and red_state == 12:
            feasible_next_targets = [2, target]
        next_decoy_state = decoy_state.copy()
        if u == 0:
            next_decoy_state[0] = min(next_decoy_state[0] + 1, 4)
        elif u == 1:
            next_decoy_state[1] = min(next_decoy_state[1] + 1, 1)
        elif u == 2:
            next_decoy_state[2] = min(next_decoy_state[2] + 1, 1)
        elif u == 3:
            next_decoy_state[3] = min(next_decoy_state[3] + 1, 4)
        elif u == 4:
            next_decoy_state[4] = min(next_decoy_state[4] + 1, 4)
        elif u == 5:
            next_decoy_state[5] = min(next_decoy_state[5] + 1, 2)
        elif u == 6:
            next_decoy_state[6] = min(next_decoy_state[6] + 1, 4)
        feasible_next_target_1 = []
        feasible_next_target_2 = []
        if red_state == 0:
            feasible_next_target_1.append(3)
            feasible_next_target_1.append(4)
            feasible_next_target_1.append(5)
            feasible_next_target_1.append(6)
            feasible_next_target_2.append(0)
            feasible_next_target_2.append(1)
        elif red_state == 1:
            feasible_next_target_1 = [target]
            if target in [3, 4]:
                feasible_next_target_2 = [1]
            else:
                feasible_next_target_2 = [0]
        else:
            feasible_next_target_1 = [target_1]
            feasible_next_target_2 = [target_2]
        feasible_next_states = []

        for feasible_target_1 in feasible_next_target_1:
            for feasible_target_2 in feasible_next_target_2:
                for feasible_red_state in feasible_next_red_states:
                    for feasible_target in feasible_next_targets:
                        if feasible_red_state == 1 and (feasible_target != feasible_target_1):
                            continue
                        if feasible_target_1 in [3, 4] and feasible_target_2 != 1:
                            continue
                        if feasible_target_1 in [5, 6] and feasible_target_2 != 0:
                            continue
                        if red_state == 5 and feasible_red_state == 2 and feasible_target != target_1:
                            continue
                        if red_state == 9 and feasible_red_state == 5 and feasible_target != target_2:
                            continue
                        if red_state == 12 and feasible_red_state == 9 and feasible_target != 2:
                            continue
                        if feasible_red_state == 6 and feasible_target == target_1:
                            continue
                        if feasible_red_state == 10 and feasible_target == target_2:
                            continue
                        if feasible_red_state == 13 and feasible_target == 2:
                            continue
                        if feasible_target != target and (feasible_red_state == red_state):
                            continue
                        if red_state in [2, 5, 9] and feasible_red_state != red_state and feasible_target == target:
                            continue
                        f_state = f"{feasible_red_state},{feasible_target},{feasible_target_1},{feasible_target_2}," \
                                  f"{','.join(list(map(lambda x: str(x), next_decoy_state)))}"
                        try:
                            feasible_next_states.append(state_to_id[f_state])
                        except Exception as e:
                            print(type(e))
                            print(f"curr state: {state}, next state: {f_state}")
                            print(feasible_next_target_1)
                            print(feasible_next_target_2)
                            import sys
                            sys.exit()
        return feasible_next_states

    @staticmethod
    def exploit_success_probability(target, decoy_state):
        """
        Calculates the probability that an exploit against the given target is successful, given the decoy state
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
    def transition_probability(state_to_id, id_to_state, x, x_prime, u):
        """
        Calculates P(x_prime | x, u), where ,x_prime,x,u are aggregate states and controls
        """
        feasible_next_states = Cage2AggregateMDP.feasible_next_states(state_id=x, state_to_id=state_to_id,
                                                                      id_to_state=id_to_state, u=u)
        if x_prime not in feasible_next_states:
            return 0
        state = id_to_state[x]
        state_prime = id_to_state[x_prime]
        red_state = state[0]

        if red_state == 0:
            return 0.25

        if red_state == 14:
            return 1
        if red_state in [1, 3, 4, 6, 7, 8, 10, 11, 13]:
            return 1
        target = state[1]
        next_decoy_state = state_prime[4:]
        next_target = state_prime[1]
        next_red_state = state_prime[0]
        next_target_1 = state_prime[2]
        next_target_2 = state_prime[3]
        if next_target in [3, 4, 5, 6] and next_target_1 != next_target:
            return 0
        if next_target in [0, 1] and next_target_2 != next_target:
            return 0
        if target == 6:
            ds = -1
        elif target == 7:
            ds = next_decoy_state[6]
        else:
            ds = next_decoy_state[target]
        exploit_success_prob = Cage2AggregateMDP.exploit_success_probability(target=target, decoy_state=ds)
        if red_state == 12 and next_red_state == 13:
            return exploit_success_prob
        if red_state == 12 and next_red_state == 12:
            return 1 - exploit_success_prob
        if (next_red_state == red_state + 1) and next_target != target:
            return exploit_success_prob
        else:
            return 1 - exploit_success_prob

    @staticmethod
    def aggregate_control_to_original_control():
        """
        Returns a dict that maps an aggregate control to the original control space
        """
        return {0: 27, 1: 28, 2: 29, 3: 30, 4: 31, 5: 32, 6: 35}

    @staticmethod
    def get_aggregate_decoy_state(decoy_state):
        """
        Converts a decoy state into an aggregate decoy state
        """
        ds = []
        decoy_hosts = [1, 2, 3, 9, 10, 11, 12]
        for dh in decoy_hosts:
            ds.append(decoy_state[dh])
        return ds

    @staticmethod
    def get_aggregate_decoy_state_space():
        """
        Gets the aggregate decoy state space
        """
        values = [range(5), range(2), range(2), range(5), range(5), range(3), range(5)]
        return list(product(*values))

    @staticmethod
    def red_target_to_aggregate_target(target):
        """
        Converts a red target to the corresponding aggregate target
        """
        red_target_to_target_idx = {0: -1, 1: 0, 2: 1, 3: 2, 4: 0, 5: 0, 6: 0, 7: 7, 8: -1, 9: 3, 10: 4, 11: 5, 12: 6}
        return red_target_to_target_idx[target]

    @staticmethod
    def aggregate_control_target_to_original_target(target):
        """
        Converts a red target to the corresponding aggregate target
        """
        aggregate_target_to_red_target = {0: 1, 1: 2, 2: 3, 3: 9, 4: 10, 5: 11, 6: 7}
        return aggregate_target_to_red_target[target]

    @staticmethod
    def X():
        """
        Aggregate state space
        """
        decoy_states = Cage2AggregateMDP.get_aggregate_decoy_state_space()
        state_to_id = {}
        id_to_state = {}
        X = []
        state_id = 0
        targets = [-1] + list(range(8))
        target_1s = [-1, 3, 4, 5, 6]
        target_2s = [-1, 0, 1]
        for red_state in range(15):
            for target_1 in target_1s:
                for target_2 in target_2s:
                    if target_1 in [3, 4] and target_2 != 1:
                        continue
                    if target_1 in [5, 6] and target_2 != 0:
                        continue
                    if target_2 != -1 and target_1 == -1:
                        continue
                    for target in targets:
                        if target == -1 and (target_1 != -1 or target_2 != -1):
                            continue
                        if target != -1 and (target_1 == -1 or target_2 == -1):
                            continue
                        if red_state in [1, 2] and target not in [3, 4, 5, 6]:
                            continue
                        if red_state in [3, 4, 5] and target not in [0, 1]:
                            continue
                        if red_state in [6, 7, 8, 9] and target != 2:
                            continue
                        if red_state in [10, 11, 12, 13] and target != 7:
                            continue
                        if target in [3, 4, 5, 6] and target_1 != target:
                            continue
                        if target in [0, 1] and target_2 != target:
                            continue
                        if target in [3, 4, 5, 6] and red_state not in [0, 1, 2]:
                            continue
                        if target in [0, 1] and red_state not in [3, 4, 5]:
                            continue
                        if target == 2 and red_state not in [6, 7, 8, 9]:
                            continue
                        if target == 7 and red_state not in [10, 11, 12, 13, 14]:
                            continue
                        if red_state == 0 and (target != -1 or target_1 != -1 or target_2 != -1):
                            continue
                        if red_state >= 1 and (target_1 == -1 or target == -1 or target_2 == -1):
                            continue
                        for decoy_state in decoy_states:
                            state_to_id[f"{red_state},{target},{target_1},{target_2}," \
                                        f"{','.join(list(map(lambda x: str(x), list(decoy_state))))}"] = state_id
                            id_to_state[state_id] = [red_state, target, target_1, target_2] + list(decoy_state)
                            X.append(state_id)
                            state_id += 1
        return X, state_to_id, id_to_state

    @staticmethod
    def U():
        """
        Aggregate control space
        """
        return [0, 1, 2, 3, 4, 5, 6]

    @staticmethod
    def cost_function(x, id_to_state):
        """
        Aggregate cost function
        """
        red_state = id_to_state[x][0]
        if red_state in [3, 4, 5]:
            return 0.1
        elif red_state in [6, 7, 8, 9]:
            return 1
        elif red_state in [10, 11, 12]:
            return 2
        elif red_state in [13, 14]:
            return 3
        return 0

    @staticmethod
    def vi(X, U, gamma, epsilon, verbose, state_to_id, id_to_state):
        """
        Value iteration
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
                ssx = [state_to_id[f"0,-1,-1,-1,0,0,0,0,0,0,0"], state_to_id[f"1,3,3,1,0,0,0,0,0,0,0"],
                       state_to_id[f"2,3,3,1,0,0,0,0,0,0,0"],
                       state_to_id[f"3,1,3,1,0,0,0,0,0,0,0"], state_to_id[f"4,1,3,1,0,0,0,0,0,0,0"],
                       state_to_id[f"5,1,3,1,0,0,0,0,0,0,0"], state_to_id[f"6,2,3,1,0,0,0,0,0,0,0"],
                       state_to_id[f"7,2,3,1,0,0,0,0,0,0,0"], state_to_id[f"8,2,3,1,0,0,0,0,0,0,0"],
                       state_to_id[f"9,2,3,1,0,0,0,0,0,0,0"], state_to_id[f"10,7,3,1,0,0,0,0,0,0,0"],
                       state_to_id[f"11,7,3,1,0,0,0,0,0,0,0"], state_to_id[f"12,7,3,1,0,0,0,0,0,0,0"],
                       state_to_id[f"13,7,3,1,0,0,0,0,0,0,0"], state_to_id[f"14,7,3,1,0,0,0,0,0,0,0"]]
                for sx in ssx:
                    u = Cage2AggregateMDP.TJx(x=sx, J=J, U=U, gamma=gamma, state_to_id=state_to_id,
                                              id_to_state=id_to_state)[0]
                    action = Cage2AggregateMDP.aggregate_control_to_original_control()[u]
                    sts = id_to_state[sx]
                    print(f"mu({sts})={action_id_to_type_and_host[action][1]}")
            if delta < epsilon:
                break
        mu = Cage2AggregateMDP.policy(X=X, U=U, gamma=gamma, J=J, state_to_id=state_to_id, id_to_state=id_to_state)
        return mu, J

    @staticmethod
    def TJx(x, J, U, gamma, state_to_id, id_to_state):
        """
        Implements the Bellman operator (TJ))(x)
        """
        Q_x = np.zeros(len(U))
        for u in U:
            feasible_x_prime = Cage2AggregateMDP.feasible_next_states(state_id=x, state_to_id=state_to_id,
                                                                      id_to_state=id_to_state, u=u)
            for x_prime in feasible_x_prime:
                p = Cage2AggregateMDP.transition_probability(state_to_id=state_to_id, id_to_state=id_to_state, x=x,
                                                             x_prime=x_prime, u=u)
                c = Cage2AggregateMDP.cost_function(x=x, id_to_state=id_to_state)
                Q_x[u] += p * (c + gamma * J[x_prime])
        u_star = int(np.argmin(Q_x))
        return u_star, Q_x[u_star]

    @staticmethod
    def policy(X, U, gamma, J, state_to_id, id_to_state):
        """
        Constructs a policy based on J
        """
        mu = np.zeros((len(X), len(U)))
        for x in X:
            mu[x][Cage2AggregateMDP.TJx(x=x, J=J, U=U, gamma=gamma, state_to_id=state_to_id,
                                        id_to_state=id_to_state)[0]] = 1.0
        return mu

    @staticmethod
    def run_vi():
        """
        Runs value iteration and saves the results to disk
        """
        X, state_to_id, id_to_state = Cage2AggregateMDP.X()
        U = Cage2AggregateMDP.U()
        gamma = 0.99
        epsilon = 0.1
        mu, J = Cage2AggregateMDP.vi(X=X, U=U, gamma=gamma, epsilon=epsilon, verbose=True, state_to_id=state_to_id,
                                     id_to_state=id_to_state)
        np.savetxt("mu1.txt", mu)
        np.savetxt("J1.txt", J)

    @staticmethod
    def test():
        """
        Simulates N test trajectories of the aggregate MDP
        """
        X, state_to_id, id_to_state = Cage2AggregateMDP.X()
        U = Cage2AggregateMDP.U()
        N = 1000
        for k in range(N):
            x = state_to_id[f"0,-1,-1,0,0,0,0,0,0,0"]
            while id_to_state[x][0] != 14:
                u = random.choice(U)
                feasible_states = Cage2AggregateMDP.feasible_next_states(state_id=x, state_to_id=state_to_id,
                                                                         id_to_state=id_to_state, u=u)
                probs = list(map(lambda x_prime: Cage2AggregateMDP.transition_probability(
                    state_to_id=state_to_id, id_to_state=id_to_state, x=x, x_prime=x_prime, u=u), feasible_states))
                print(f"u: {u}, x: {id_to_state[x]}")
                x = np.random.choice(feasible_states, p=probs)


if __name__ == '__main__':
    pass
