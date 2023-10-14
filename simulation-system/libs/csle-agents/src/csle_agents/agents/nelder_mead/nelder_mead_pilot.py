import numpy as np
import random
import copy
def f(p):
    return (p[0]-1)**2 + (p[1]-4)**2 + 10

def reflection(x_c, x_n, alpha=1):
    t = tuple(alpha * (i - j) for i,j in zip(x_c, x_n))
    x_r = tuple(k+l for k,l in zip(x_c, t))
    return x_r

def expansion(x_c, x_r, gamma=2):
    t = tuple(gamma * (i - j) for i,j in zip(x_r, x_c))
    x_e = tuple(k + l for k,l in zip(x_c, t))
    return x_e

def contraction(x_c, x_w, rho=0.5):
    t = tuple(rho * (i - j) for i, j in zip(x_w, x_c))
    x_co = tuple(k + l for k, l in zip(x_c, t))
    # x_co = x_c + rho * (x_w - x_c)
    return x_co

def shrink(x_i, x_0, sigma=0.5):
    t = tuple(sigma * (i - j) for i, j in zip(x_i, x_0))
    x = tuple(k + l for k, l in zip(x_0, t))
    return x

def nelder_mead(x_list, no_improve_thr = 10e-6, no_improv_break = 10, step = 0.1):

    dim = len(x_list)
    prev_best = f(x_list)
    no_improv = 0
    func_evals = [[x_list, prev_best]]
    for i in range(len(x_list)):
        x = copy.copy(x_list)
        x[i] = x[i] + step
        f_x = f(x)
        func_evals.append([x, f_x])

    while True:

        func_evals.sort(key=lambda x: x[1])
        f_best = func_evals[0][1]

        if f_best < prev_best - no_improve_thr:
            no_improv = 0
            prev_best = f_best
        else:
            no_improv += 1

        if no_improv >= no_improv_break:
            return func_evals[0]

        x_c = [0.] * dim

        for tup in func_evals[:-1]:
            for i, c in enumerate(tup[0]):
                x_c[i] += c / (len(func_evals)-1)

        x_n = func_evals[-1][0]
        xr = reflection(x_c, x_n)
        f_r = f(xr)
        if f_best <= f_r < func_evals[-2][1]:
            del func_evals[-1]
            func_evals.append([xr, f_r])
            continue

        if f_r < f_best:
            x_e = expansion(x_c, x_n)
            f_e = f(x_e)
            if f_e < f_r:
                del func_evals[-1]
                func_evals.append([x_e, f_e])
                continue
            else:
                del func_evals[-1]
                func_evals.append([xr, f_r])
                continue
    
        x_co = contraction(x_c, x_n)
        f_co = f(x_co)
        f_worst = func_evals[-1][1]
        if f_co < f_worst:
            del func_evals[-1]
            func_evals.append([x_co, f_co])
            continue


        x_0 = func_evals[0][0]
        nres = []

        for tup in func_evals:
            # x_s = x_0 + sigma*(tup[0] - x1)
            x_s = shrink(x_0, tup[0])
            f_s = f(x_s)
            nres.append([x_s, f_s])

        func_evals = nres

def main():
    x_list = np.array([0., 0.])
    # print("first x_list: ", x_list)
    solution = nelder_mead(x_list)
    print(solution)

if __name__ == "__main__":
    main()