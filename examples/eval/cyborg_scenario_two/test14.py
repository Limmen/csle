import math

if __name__ == '__main__':
    # gamma = 0.99
    # gamma = 0.75
    # gamma = 0.5
    # gamma = 0.25
    # gamma = 0.98
    gamma = 0.975
    for l in range(1000):
        bound_factor = 2*math.pow(gamma, l)/(1-gamma)
        print(f"{l} {bound_factor}")