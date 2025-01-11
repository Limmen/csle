import numpy as np
import copy
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState
from cyborg_agg_mdp import Cage2AggregateMDP


# def monte_carlo_most_frequent(elements, num_samples):
#     if not elements:
#         raise ValueError("The input list is empty.")
#
#     # Perform random sampling
#     samples = [random.choice(elements) for _ in range(num_samples)]
#
#     # Count occurrences of sampled elements
#     counter = Counter(samples)
#
#     # Find the most common element
#     most_frequent_element = counter.most_common(1)[0][0]
#     return most_frequent_element

# def particle_filter(particles, max_num_particles, train_env, action, obs):
#     new_particles = []
#     while len(particles) < max_num_particles:
#         x = random.choice(particles)
#         train_env.set_state(state=x)
#         _, r, _, _, info = train_env.step(action)
#         s_prime = info["s"]
#         o = info["o"]
#         if o == obs:
#             new_particles.append(s_prime)
#     return new_particles

def restore_policy(s: CyborgWrapperState):
    a = -1
    if s.s[1][2] == 2:
        a = 0 # Ent0
    if s.s[2][2] == 2:
        a = 1 # Ent 1
    if s.s[3][2] == 2:
        a = 2 # Ent 2
    if s.s[7][2] == 2:
        a = 3 # Opserver

    if s.s[1][2] == 1:
        a = 8 # Ent0
    if s.s[2][2] == 1:
        a = 9 # Ent1
    if s.s[3][2] == 1:
        a = 10 # Ent2
    if s.s[3][2] == 1:
        a = 11 # Opserver
    if s.s[9][2] == 1:
        a = 22 # User1
    if s.s[10][2] == 1:
        a = 23 # User2
    if s.s[11][2] == 1:
        a = 24 # User3
    if s.s[12][2] == 1:
        a = 25 # User4
    return a

def rollout(s: CyborgWrapperState, train_env: CyborgScenarioTwoWrapper, J, state_to_id, mu, l, gamma=0.99):
    # U = [0, 1, 2, 3, 8, 9, 10, 11, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 35]
    U = [27, 28, 29, 30, 31, 32, 35]
    U = [27, 28, 29, 30, 31, 32]
    Q_n = []
    for u in U:
        u_r = restore_policy(s=s)
        if u_r != -1:
            o, c, done, _, info = train_env.step(action=u_r)
            s_prime = info["s"]
            aggregate_state = Cage2AggregateMDP.get_aggregate_state(s=s_prime, state_to_id=state_to_id)
            if l == 1:
                return u_r, J[aggregate_state]
            else:
                returns = []
                for i in range(2):
                    returns.append(rollout(copy.deepcopy(s_prime), train_env=train_env, J=J, state_to_id=state_to_id, mu=mu, l=l-1)[1])
                cost_to_go = np.mean(returns)
        else:
            train_env.set_state(s)
            o, c, done, _, info = train_env.step(action=u)
            s_prime = info["s"]
            aggregate_state = Cage2AggregateMDP.get_aggregate_state(s=s_prime, state_to_id=state_to_id)
            if l == 1:
                cost_to_go = J[aggregate_state]
            else:
                returns = []
                for i in range(2):
                    returns.append(rollout(copy.deepcopy(s_prime), train_env=train_env, J=J, state_to_id=state_to_id, mu=mu, l=l-1)[1])
                cost_to_go = np.mean(returns)
        Q_n.append(-c + gamma*cost_to_go)
    # print(Q_n)
    # print(U[int(np.argmin(Q_n))])
    u_star = int(np.argmin(Q_n))
    return U[u_star], Q_n[u_star]


if __name__ == '__main__':
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2,
                                     red_agent_type=RedAgentType.B_LINE_AGENT)
    env = CyborgScenarioTwoWrapper(config=config)
    train_env = CyborgScenarioTwoWrapper(config=config)
    action_id_to_type_and_host, type_and_host_to_action_id \
        = CyborgEnvUtil.get_action_dicts(scenario=2, reduced_action_space=True, decoy_state=True, decoy_optimization=False)
    N = 10000
    max_env_steps = 100
    mu = np.loadtxt("./mu1.txt")
    J = np.loadtxt("./J1.txt")
    X, state_to_id, id_to_state = Cage2AggregateMDP.X()
    gamma = 0.99
    l = 3
    returns = []
    for i in range(N):
        print(f"{i}/{N}")
        done = False
        _, info = env.reset()
        s = info["s"]
        t = 1
        R = 0
        particles = env.initial_particles
        while not done and t < max_env_steps:
            # monte_carlo_state = monte_carlo_most_frequent(elements=particles, num_samples=100)
            aggregate_state = Cage2AggregateMDP.get_aggregate_state(s=s, state_to_id=state_to_id)
            a = -1
            a = restore_policy(s=s)

            if t <= 1:
                a = 31
            if a == -1:
                a = Cage2AggregateMDP.get_aggregate_control(mu=mu, aggregate_state=aggregate_state,
                                                            id_to_state=id_to_state)
                # print(f"base: {a}")
                a = rollout(s=s, state_to_id=state_to_id, train_env=train_env, J=J, mu=mu, gamma=gamma, l=l)[0]
                # print(f"rollout: {a}")
            o, r, done, _, info = env.step(a)
            # particles = particle_filter(particles=particles, max_num_particles=1000,
            #                             train_env=train_env, action=a, obs=o)
            s = info["s"]
            t+= 1
            R+= r
            # print(f"t:{t}, r: {r}, a: {action_id_to_type_and_host[a]}, R: {R}, aggstate: {id_to_state[aggregate_state]}")
        returns.append(R)
        print(np.mean(returns))