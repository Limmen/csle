import numpy as np
from itertools import product
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil


class CyborgAggMDP:

    @staticmethod
    def feasible_next_states(state_id, state_to_id, id_to_state, u):
        state = id_to_state[state_id]
        target = state[0]
        decoy_state = state[1:]
        feasible_next_targets = [target]
        if target in [3, 4]:
            feasible_next_targets = feasible_next_targets + [1]
        elif target in [5, 6]:
            feasible_next_targets = feasible_next_targets + [0]
        elif target in [0, 1]:
            feasible_next_targets = feasible_next_targets + [2]
        next_decoy_state = decoy_state.copy()
        if u == 0:
            next_decoy_state[0] = min(next_decoy_state[0] + 1, 4)
        elif u == 1:
            next_decoy_state[1] = min(next_decoy_state[1] + 1, 1)
        elif u == 2:
            next_decoy_state[2] = min(next_decoy_state[2] + 1, 1)
        elif u == 3:
            next_decoy_state[3] = min(next_decoy_state[3] + 1, 2)
        elif u == 4:
            next_decoy_state[4] = min(next_decoy_state[4] + 1, 4)
        elif u == 5:
            next_decoy_state[5] = min(next_decoy_state[5] + 1, 2)
        feasible_next_states = []
        for feasible_target in feasible_next_targets:
            state = f"{feasible_target},{','.join(list(map(lambda x: str(x), next_decoy_state)))}"
            feasible_next_states.append(state_to_id[state])
        return feasible_next_states

    @staticmethod
    def exploit_success_probability(target, decoy_state):
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

    @staticmethod
    def transition_probability(state_to_id, id_to_state, x, x_prime, u):
        feasible_next_states = CyborgAggMDP.feasible_next_states(state_id=x, state_to_id=state_to_id,
                                                                 id_to_state=id_to_state, u=u)
        if x_prime not in feasible_next_states:
            return 0
        state = id_to_state[x]
        state_prime = id_to_state[x_prime]
        target = state[0]
        next_decoy_state = state_prime[1:]
        next_target = state_prime[0]
        if target == 6:
            ds = -1
        else:
            ds = next_decoy_state[target]
        exploit_success_prob = CyborgAggMDP.exploit_success_probability(target=target, decoy_state=ds)
        if next_target != target:
            return exploit_success_prob
        else:
            return 1 - exploit_success_prob

    @staticmethod
    def host_to_action_id(host):
        if host == 1:
            return 27
        elif host == 2:
            return 28
        elif host == 3:
            return 29
        elif host == 9:
            return 30
        elif host == 10:
            return 31
        elif host == 11:
            return 32

    @staticmethod
    def control_to_action_id():
        return {0: 27, 1: 28, 2: 29, 3: 30, 4: 31, 5: 32}

    @staticmethod
    def check_if_decoy_redundant(target_host, decoy_state):
        decoy_actions_per_host = CyborgEnvUtil.get_decoy_actions_per_host(scenario=2)
        if decoy_state[target_host] == decoy_actions_per_host[target_host]:
            for host in [1, 2, 3, 9, 10, 11]:
                if decoy_state[target_host] != decoy_actions_per_host[target_host]:
                    return host

    @staticmethod
    def get_decoy_state(decoy_state):
        ds = []
        decoy_hosts = [1, 2, 3, 9, 10, 11]
        for dh in decoy_hosts:
            ds.append(CyborgAggMDP.decoy_state_to_id(host=dh, state=decoy_state[dh]))
        return ds

    @staticmethod
    def decoy_state_to_id(host, state):
        if host in [1, 2, 3, 10, 11]:
            return state
        if host == 9:
            if state > 2:
                return 2
            else:
                return state

    @staticmethod
    def get_decoy_state_space():
        values = [range(5), range(2), range(2), range(3), range(5), range(3)]
        return list(product(*values))

    @staticmethod
    def red_target_to_target_idx(target):
        red_target_to_target_idx = {
            0: 3,
            1: 0,
            2: 1,
            3: 2,
            4: 3,
            5: 3,
            6: 3,
            7: 6,
            8: 3,
            9: 3,
            10: 4,
            11: 5,
            12: 6
        }
        return red_target_to_target_idx[target]

    @staticmethod
    def X():
        decoy_states = CyborgAggMDP.get_decoy_state_space()
        state_to_id = {}
        id_to_state = {}
        X = []
        state_id = 0
        for target in range(7):
            for decoy_state in decoy_states:
                state_to_id[f"{target},{','.join(list(map(lambda x: str(x), list(decoy_state))))}"] = \
                    state_id
                id_to_state[state_id] = [target] + list(decoy_state)
                X.append(state_id)
                state_id += 1
        return X, state_to_id, id_to_state

    @staticmethod
    def U():
        return [0, 1, 2, 3, 4, 5]

    @staticmethod
    def cost_function(x, x_prime, id_to_state):
        target = id_to_state[x][0]
        next_target = id_to_state[x_prime][0]
        if next_target > target:
            if target in [3, 4, 5, 6]:
                return 0.1
            elif target in [0, 1, 2]:
                return 1
        return 0

    @staticmethod
    def vi(X, U, gamma, epsilon, verbose, state_to_id, id_to_state):
        """
        Value iteration
        """
        J = np.zeros(len(X))
        iteration = 0
        while True:
            delta = 0
            for x in X:
                u_star, J_u_star = CyborgAggMDP.TJx(x=x, J=J, U=U, gamma=gamma, state_to_id=state_to_id,
                                                    id_to_state=id_to_state)
                delta = max(delta, np.abs(J_u_star - J[x]))
                J[x] = J_u_star
            iteration += 1
            if verbose:
                print(f"VI iteration: {iteration}, delta: {delta}, epsilon: {epsilon}")
            if delta < epsilon:
                break
        mu = CyborgAggMDP.policy(X=X, U=U, gamma=gamma, J=J, state_to_id=state_to_id, id_to_state=id_to_state)
        return mu, J

    @staticmethod
    def TJx(x, J, U, gamma, state_to_id, id_to_state):
        """
        Implements the Bellman operator (TJ))(x)
        """
        Q_x = np.zeros(len(U))
        for u in U:
            feasible_x_prime = CyborgAggMDP.feasible_next_states(state_id=x, state_to_id=state_to_id,
                                                                 id_to_state=id_to_state, u=u)
            for x_prime in feasible_x_prime:
                p = CyborgAggMDP.transition_probability(state_to_id=state_to_id, id_to_state=id_to_state, x=x,
                                                        x_prime=x_prime, u=u)
                c = CyborgAggMDP.cost_function(x=x, x_prime=x_prime, id_to_state=id_to_state)
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
            mu[x][CyborgAggMDP.TJx(x=x, J=J, U=U, gamma=gamma, state_to_id=state_to_id,
                                   id_to_state=id_to_state)[0]] = 1.0
        return mu


if __name__ == '__main__':
    action_id_to_type_and_host, type_and_host_to_action_id \
        = CyborgEnvUtil.get_action_dicts(scenario=2, reduced_action_space=True, decoy_state=True,
                                         decoy_optimization=False)
    X, state_to_id, id_to_state = CyborgAggMDP.X()
    U = CyborgAggMDP.U()
    # x = state_to_id[f"3,0,0,0,0,0,0"]
    # for fx in CyborgAggMDP.feasible_next_states(state_id=x, state_to_id=state_to_id, id_to_state=id_to_state, u=0):
    #     print(id_to_state[fx])
    gamma = 0.99
    epsilon = 0.1
    mu, J = CyborgAggMDP.vi(X=X, U=U, gamma=gamma, epsilon=epsilon, verbose=True, state_to_id=state_to_id,
                            id_to_state=id_to_state)
    for x in X:
        u = int(np.argmax(mu[x]))
        action = CyborgAggMDP.control_to_action_id()[u]
        state = id_to_state[x]
        print(f"mu({state[0]})={action_id_to_type_and_host[action][1]}")
    print(f"J(0): {J[0]}")
