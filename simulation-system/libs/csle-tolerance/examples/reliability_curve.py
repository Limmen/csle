import numpy as np
from scipy.stats import binom


def mc(N, p):
    P = []
    for s in range(0, N + 1):
        s_probs = []
        for s_prime in range(0, N + 1):
            if s_prime > s:
                s_probs.append(0)
            else:
                s_probs.append(binom.pmf(s - s_prime, s, p))
        assert round(sum(s_probs), 3) == 1
        P.append(s_probs)
    return P

if __name__ == '__main__':
    f = 3
    p_a = 0.05
    p_c_1 = 0.00001
    p = p_c_1 + (1 - p_c_1) * p_a
    for N in [25, 50, 100, 200, 400]:
        P = mc(N, p)
        pi1 = np.zeros(N+1)
        pi1[-1] = 1
        reliability_curve = []
        for t in range(1, 101):
            pi_t = np.dot(np.transpose(pi1), np.linalg.matrix_power(P, t))
            assert round(sum(pi_t), 3) == 1
            reliability = 0
            for s in range(0, N+1):
                if s > f:
                    reliability += pi_t[s]
            reliability_curve.append(reliability)
        print(f"N: {N}")
        for i in range(len(reliability_curve)):
            print(f"{i+1} {reliability_curve[i]:10f}")
        print("\n")
        print("\n")


