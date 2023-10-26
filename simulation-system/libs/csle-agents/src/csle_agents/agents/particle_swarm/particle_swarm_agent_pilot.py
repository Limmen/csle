import numpy as np
from numpy.random import rand
import random as rnd
def J(x):
    return (x[0]-4)**2 + (x[1]-1)**2 + 10


def particle_swarm(S, b_lo, b_up, Phi_p, Phi_g, w):
    g = [rnd.uniform(b_lo, b_up), rnd.uniform(b_lo, b_up)]
    X = np.zeros((2, S))
    P = np.zeros((2, S))
    V = np.zeros((2, S))
    for i in range(S):
        X[0, i] = rnd.uniform(b_lo, b_up)
        X[1, i] = rnd.uniform(b_lo, b_up)
        P[:, i] = X[:, i]
        if J(P[:, i]) < J(g):
            g = P[:, i]
        V[0, i] = rnd.uniform(-abs(b_up - b_lo), abs(b_up - b_lo))
        V[1, i] = rnd.uniform(-abs(b_up - b_lo), abs(b_up - b_lo))
    k = 0
    while k <= 100:
        for j in range(S):
            for l in range(len(X[:, j])):
                r_p = np.random.random()
                r_g = np.random.random()
                V[l, j] = w * V[l, j] + Phi_p * r_p * (P[l, j] - X[l, j]) + Phi_g * r_g * (g[l] - X[l, j])
            X[:, j] += V[:, j]
            if J(X[:, j]) < J(P[:, j]):
                 P[:, j] = X[:, j]
                 if J(P[:, j]) < J(g):
                     g = P[:, j]
        k += 1
    return (g[0],  g[1])


def main():
    S = 10
    b_lo = 0
    b_up = 10
    Phi_p = 1
    Phi_g = 1
    w = 0.5
    a = particle_swarm(S, b_lo, b_up, Phi_p, Phi_g, w)
    print(a)

if __name__ == "__main__":
    main()
