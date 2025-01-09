import numpy as np
import json, io
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil

if __name__ == '__main__':
    # with io.open("./particles.json", 'r') as f:
    #     particles = json.loads(f.read())
    #     for k,v in particles.items():
    #         particles[k] = list(map(lambda x: CyborgWrapperState.from_dict(x), v))

    action_id_to_type_and_host, type_and_host_to_action_id \
        = CyborgEnvUtil.get_action_dicts(scenario=2, reduced_action_space=True, decoy_state=True, decoy_optimization=False)
    # hosts = CyborgEnvUtil.get_cyborg_hosts()
    # print(hosts)
    # import sys
    # sys.exit()

    with io.open("./id_to_state_2.json", 'r') as f:
        id_to_state = json.loads(f.read())

    with io.open("./state_to_id_2.json", 'r') as f:
        state_to_id = json.loads(f.read())

    with io.open("./transitions_2.json", 'r') as f:
        transitions = json.loads(f.read())

    X = list(range(len(id_to_state.keys())))
    U = list(range(36))

    P = np.zeros((len(U),len(X),len(X)))
    for u in U:
        for x in X:
            for x_prime in X:
                if str(x) in transitions and str(u) in transitions[str(x)] and str(x_prime) in transitions[str(x)][str(u)]:
                    total = sum(transitions[str(x)][str(u)].values())
                    P[u][x][x_prime] = float(transitions[str(x)][str(u)][str(x_prime)]/total)

    with io.open("./costs_2.json", 'r') as f:
        costs = json.loads(f.read())

    C = np.zeros((len(X),len(U)))
    for u in U:
        for x in X:
            if str(x) in costs and str(u) in costs[str(x)]:
                C[x][u] = float(np.mean(costs[str(x)][str(u)]))

    print(C)


    from value_iteration import VI
    gamma = 0.99
    mu, J = VI.vi(X=X, U=U, P=P, gamma=gamma, C=C, epsilon=0.01, verbose=True)
    for x in X:
        print(f"mu({x})={action_id_to_type_and_host[int(np.argmax(mu[x]))]}")
    print(f"J(0): {J[0]}")

    print(J)
    np.savetxt("mu2.txt", mu)
    np.savetxt("J2.txt", J)



