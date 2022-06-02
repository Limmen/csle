from typing import List
import numpy as np
import pulp


def check_duplicate(alpha_set: np.ndarray, alpha: np.ndarray) -> bool:
    """
    Check whether alpha vector av is already in set a

    :param alpha_set: the set of alpha vectors
    :param alpha: the vector to check
    :return: true or false
    """
    for alpha_i in alpha_set:
        if np.allclose(alpha_i, alpha):
            return True
    return False


def prune_lower_bound(lower_bound: List, S: np.ndarray) -> np.ndarray:
    """
    Lark's filtering algorithm to prune the lower bound, (Cassandra, Littman, Zhang, 1997)

    :param lower_bound: the current lower bound
    :param S: the set of states
    :return: the pruned lower bound
    """
    # dirty set
    F = set()
    for i in range(len(lower_bound)):
        F.add(tuple(lower_bound[i]))

    # clean set
    Q = []

    for s in S:
        max_alpha_val_s = -np.inf
        max_alpha_vec_s = None
        for alpha_vec in F:
            if alpha_vec[s] > max_alpha_val_s:
                max_alpha_val_s = alpha_vec[s]
                max_alpha_vec_s = alpha_vec
        if max_alpha_vec_s is not None and len(F) > 0:
            # Q.update({max_alpha_vec_s})
            Q.append(np.array(list(max_alpha_vec_s)))
            F.remove(max_alpha_vec_s)
    while F:
        alpha_vec = F.pop()  # just to get a reference
        F.add(alpha_vec)
        x = check_dominance_lp(alpha_vec, np.array(Q))
        if x is None:
            F.remove(alpha_vec)
        else:
            max_alpha_val = -np.inf
            max_alpha_vec = None
            for phi in F:
                phi_vec = np.array(list(phi))
                if phi_vec.dot(alpha_vec) > max_alpha_val:
                    max_alpha_val = phi_vec.dot(alpha_vec)
                    max_alpha_vec = phi_vec
            Q.append(max_alpha_vec)
            F.remove(tuple(list(max_alpha_vec)))
    return Q


def check_dominance_lp(alpha_vec: np.ndarray, Q: np.ndarray):
    """
    Uses LP to check whether a given alpha vector is dominated or not (Cassandra, Littman, Zhang, 1997)

    :param alpha_vec: the alpha vector to check
    :param Q: the set of vectors to check dominance against
    :return: None if dominated, otherwise return the vector
    """

    problem = pulp.LpProblem("AlphaDominance", pulp.LpMaximize)

    # --- Decision Variables ----

    # x
    x_vars = []
    for i in range(len(alpha_vec)):
        x_var_i = pulp.LpVariable("x_" + str(i), lowBound=0, upBound=1, cat=pulp.LpContinuous)
        x_vars.append(x_var_i)

    # delta
    delta = pulp.LpVariable("delta", lowBound=None, upBound=None, cat=pulp.LpContinuous)

    # --- Objective Function ----
    problem += delta, "maximize delta"

    # --- The constraints ---

    # x sum to 1
    x_sum = 0
    for i in range(len(x_vars)):
        x_sum += x_vars[i]
    problem += x_sum == 1, "XSumWeights"

    # alpha constraints
    for i, alpha_vec_prime in enumerate(Q):
        x_dot_alpha_sum = 0
        x_dot_alpha_prime_sum = 0
        for j in range(len(alpha_vec)):
            x_dot_alpha_sum += x_vars[j] * alpha_vec[j]
            x_dot_alpha_prime_sum += x_vars[j] * alpha_vec_prime[j]
        problem += x_dot_alpha_sum >= delta + x_dot_alpha_prime_sum, "alpha_constraint _" + str(i)

    # Solve
    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    # Obtain solution
    delta = delta.varValue
    if delta > 0:
        return alpha_vec
    else:
        return None
