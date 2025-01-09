import numpy as np


class VI:
    """
    Implements the Value Iteration Algorithm for MDPs
    """

    @staticmethod
    def vi(X, U, P, gamma, C, epsilon, verbose):
        """
        Value iteration
        """
        J = np.zeros(len(X))
        iteration = 0
        while True:
            delta = 0
            for x in X:
                u_star, J_u_star = VI.TJx(x=x, J=J, U=U, X=X, P=P, gamma=gamma, C=C)
                delta = max(delta, np.abs(J_u_star - J[x]))
                J[x] = J_u_star
            iteration += 1
            if verbose:
                print(f"VI iteration: {iteration}, delta: {delta}, epsilon: {epsilon}")
            if delta < epsilon:
                break
        mu = VI.policy(X=X, U=U, gamma=gamma, P=P, J=J, C=C)
        return mu, J

    @staticmethod
    def TJx(x, J, U, X, P, gamma, C):
        """
        Implements the Bellman operator (TJ))(x)
        """
        Q_x = np.zeros(len(U))
        for u in U:
            for x_prime in X:
                Q_x[u] += P[u][x][x_prime] * (C[x][u] + gamma * J[x_prime])
        u_star = int(np.argmin(Q_x))
        return u_star, Q_x[u_star]

    @staticmethod
    def policy(X, U, gamma, P, J, C):
        """
        Constructs a policy based on J
        """
        mu = np.zeros((len(X), len(U)))
        for x in X:
            mu[x][VI.TJx(x=x, J=J, U=U, X=X, P=P, gamma=gamma, C=C)[0]] = 1.0
        return mu
