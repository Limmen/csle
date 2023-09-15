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


def linear_system(P, N, f):
    A = []
    b = []
    for s in range(0, N + 1):
        s_coefficients = []
        for s_prime in range(0, N + 1):
            if s_prime == s:
                if s <= f:
                    s_coefficients.append(1)
                else:
                    s_coefficients.append(1 - P[s][s_prime])
            else:
                if s <= f:
                    s_coefficients.append(0)
                else:
                    s_coefficients.append(-P[s][s_prime])
        A.append(s_coefficients)
        if s <= f:
            b.append(0)
        else:
            b.append(1)
    return A, b


if __name__ == '__main__':
    f = 3
    p_a = 0.005
    p_c_1 = 0.00001
    p = p_c_1 + (1 - p_c_1) * p_a
    mttfs = []
    for N in range(4, 101):
        print(f"{N}/{100}")
        P = mc(N, p)
        f = (N - 1) / 2
        A, b = linear_system(P=P, N=N, f=f)
        analytical_mttf = np.linalg.solve(A, b)[-1]
        mttfs.append(analytical_mttf)
    for i in range(4, 4 + len(mttfs)):
        print(f"{i} {mttfs[i - 4]}")
