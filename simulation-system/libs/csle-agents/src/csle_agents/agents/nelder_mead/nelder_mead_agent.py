import numpy as np
import random

def f(p):
    return (p[0]-1)**2 + (p[1]-4)**2 + 10

def reflection(x_c, x_n, alpha=1):
    print("kommer jag hit nån gång")
    x_r = x_c + alpha * (x_c - x_n)
    return x_r

def expantion(x_c, x_r, gamma=2):
    x_e = x_c + gamma * (x_r - x_c)
    return x_e

def contraction(x_c, x_w, rho=0.5):
    x_co = x_c + rho * (x_w - x_c)
    return x_co

def shrink(x_i, x_0, sigma=0.5):
    x = x_0 + sigma * (x_i - x_0)
    return x

def nelder_mead(x_list, tolerance = 0.1):

    func_evals = []
    
    x_n = 0 #the point genrating the worst (aka of higehst magnitiude) function evaluation
    f_n = 0 # current worst function evalutaion
    x_0 = 0 # the point that is to generate the best function evaluation
    f_best = f((101, 101))

    for k in range(len(x_list)):
        f_k = f(x_list[k])
        func_evals.append(f_k)
        if f_k > f_n:
            f_n = f_k # assign new worst evaluation
            x_n = x_list[k] # assign new worst evalution point
        else:
            if f_k <= f_best:
                f_best = f_k
                x_0 = x_list[k]

    # print(func_evals)
    # print(len(func_evals))

    func_evals.sort() # sorting from best to worst evalutaion

    std_f = np.std(func_evals)

    if std_f <= tolerance: # base case
        return x_0

    # print(f_best)
    # print(func_evals[0])
    # f_best = func_evals[0]
    f_2worst = func_evals[-2]

    # x_c = np.mean(x_list[:-1]) # calculating centroid point
    sum1 = 0
    sum2 = 0
    for j in range(len(x_list[:-1])):
        sum1 += x_list[i][0]
        sum2 += x_list[i][1]
    x_c = (sum1 / len(x_list[:-1]), sum1 / len(x_list[:-1])) # calculating the centroid point

    x_r = reflection(x_c, x_n) # calculating reflection
    print(x_r)
    

    assert f_n == func_evals[-1]
    assert f_best == func_evals[0]

    f_r = f(x_r)

    if f_best <= f_r < f_2worst: # 3 - reflection
        x_list = [x_r if x == x_n else x_n for x in x_list]
        nelder_mead(x_list)

    elif f_r < f_best: #4 - expantion
        x_e = expantion(x_c, x_r)
        f_e = f(x_e)
        if f_e < f_r:
            x_list = [x_e if x == x_n else x_n for x in x_list]
            nelder_mead(x_list)
        else:
            x_list = [x_r if x == x_n else x_n for x in x_list]

    else: # 5 - contraction
        if f_r < f_n:
            x_co = contraction(x_c, x_r) # outside contraction
            f_co = f(x_co)
            if f_co < f_r:
                x_list = [x_c if x == x_n else x_n for x in x_list]
        elif f_r >= f_n:
            x_co = contraction(x_c, x_n)
            f_co = f(x_co)
            if f_co < f_n:
                x_list = [x_c if x == x_n else x_n for x in x_list]
                nelder_mead(x_list)

    for i in range(1, len(x_list)): # shrink the shape
        x_i = x_list[i]
        x_list[i] = shrink(x_i, x_0)
    nelder_mead(x_list)

def main():
    x_list = [(random.randint(0,100), random.randint(0, 100)) for i in range(10)]
    solution = nelder_mead(x_list)
    print(solution)

if __name__ == "__main__":
    main()