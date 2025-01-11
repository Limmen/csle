import random
import numpy as np
import copy
from collections import Counter
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState
from cage2_aggregate_mdp import Cage2AggregateMDP
import csle_agents.constants.constants as agents_constants


def monte_carlo_most_frequent_particle(particles, N):
    """
    Samples N particles and returns the most frequently sampled particle
    """
    samples = [random.choice(particles) for _ in range(N)]
    counter = Counter(samples)
    most_frequent_particle = counter.most_common(1)[0][0]
    return most_frequent_particle


def particle_filter(particles, max_num_particles, train_env, u, obs, x_s):
    """
    Implements a particle filter
    """
    new_particles = []
    failed_samples = 0
    while len(new_particles) < max_num_particles:
        # print(f"{len(new_particles)}/{max_num_particles}")
        x = random.choice(particles)
        train_env.set_state(state=x)
        _, _, _, _, info = train_env.step(u)
        x_prime = info[agents_constants.COMMON.STATE]
        o = info[agents_constants.COMMON.OBSERVATION]
        if int(o) == int(obs):
            failed_samples = 0
            new_particles.append(x_prime)
        failed_samples += 1
        if failed_samples > 500:
            if len(new_particles) == 0:
                return [x_s]
            return new_particles
    return new_particles


def restore_policy(x: CyborgWrapperState, train_env, particles):
    """
    Implements a heuristic restore policy for Cage2
    """
    u = -1
    restore_actions = [0, 1, 2, 3]
    remove_actions = [8, 9, 10, 11, 22, 23, 24, 25]
    remove_hosts = [1, 2, 3, 7, 9, 10, 11, 12]
    restore_hosts = [1,2,3,7]
    outcomes = {}
    for h in remove_hosts:
        outcomes[h] = []
    for i, host in enumerate(remove_hosts):
        for p in particles:
            if p.s[host][2] == 1:
                train_env.set_state(p)
                train_env.step(action=remove_actions[i])
                if train_env.s[host][2] == 0:
                    outcomes[host].append(1)
                else:
                    outcomes[host].append(0)

    for i, h in enumerate(remove_hosts):
        if len(outcomes[h]) > 0:
            remove_p = np.mean(outcomes[h])
            if remove_p >= 0.9:
                return remove_actions[i]

    for i, host in enumerate(restore_hosts):
        if x.s[host][2] > 0:
            return restore_actions[i]
    return u

    # if x.s[1][2] == 2:
    #     u = 0  # Ent0
    # if x.s[2][2] == 2:
    #     u = 1  # Ent 1
    # if x.s[3][2] == 2:
    #     u = 2  # Ent 2
    # if x.s[7][2] == 2:
    #     u = 3  # Opserver
    #
    # if x.s[1][2] == 1:
    #     u = 8  # Ent0
    # if x.s[2][2] == 1:
    #     u = 9  # Ent1
    # if x.s[3][2] == 1:
    #     u = 10  # Ent2
    # if x.s[3][2] == 1:
    #     u = 11  # Opserver
    # if x.s[9][2] == 1:
    #     u = 22  # User1
    # if x.s[10][2] == 1:
    #     u = 23  # User2
    # if x.s[11][2] == 1:
    #     u = 24  # User3
    # if x.s[12][2] == 1:
    #     u = 25  # User4
    # return u


def rollout_policy(train_env: CyborgScenarioTwoWrapper, J, state_to_id, mu, l, id_to_state,
                   particles, gamma=0.99, mc_samples=10):
    """
    A rollout policy for cage-2
    """
    U = [27, 28, 29, 30, 31, 32, 35]
    Q_n = []
    for u in U:
        returns = []
        for i in range(mc_samples):
            particle = random.choice(particles)
            train_env.set_state(particle)
            _, _, _, _, info = train_env.step(action=u)
            x_prime = info[agents_constants.COMMON.STATE]
            aggregate_state = Cage2AggregateMDP.get_aggregate_state(s=x_prime, state_to_id=state_to_id)
            c = -info[agents_constants.COMMON.REWARD]
            # c = Cage2AggregateMDP.cost_function(x=aggregate_state, u=U.index(u), id_to_state=id_to_state)
            if l == 1:
                returns.append(c + gamma * J[aggregate_state])
            else:
                returns.append(c + gamma * rollout_policy(train_env=train_env, J=J,
                                                          state_to_id=state_to_id, id_to_state=id_to_state,
                                                          mu=mu, l=l - 1)[1])
        Q_n.append(np.mean(returns))
    u_star = int(np.argmin(Q_n))
    J_star = Q_n[u_star]
    u_star = U[u_star]
    u_r = restore_policy(x=x, train_env=train_env, particles=particles)
    if u_r != -1:
        u_star = u_r
    return u_star, J_star


def base_policy(x, mu, id_to_state):
    """
    Implements the base policy mu
    """
    aggregate_state = Cage2AggregateMDP.get_aggregate_state(s=x, state_to_id=state_to_id)
    return Cage2AggregateMDP.get_aggregate_control(mu=mu, aggregate_state=aggregate_state, id_to_state=id_to_state)


if __name__ == '__main__':
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2,
                                     red_agent_type=RedAgentType.B_LINE_AGENT)
    env = CyborgScenarioTwoWrapper(config=config)
    train_env = CyborgScenarioTwoWrapper(config=config)
    action_id_to_type_and_host, type_and_host_to_action_id \
        = CyborgEnvUtil.get_action_dicts(scenario=2, reduced_action_space=True, decoy_state=True,
                                         decoy_optimization=False)
    N = 10000
    max_env_steps = 100
    mu = np.loadtxt("./mu2.txt")
    J = np.loadtxt("./J2.txt")
    X, state_to_id, id_to_state = Cage2AggregateMDP.X()
    gamma = 0.99
    l = 1
    returns = []
    for i in range(N):
        done = False
        _, info = env.reset()
        x = info[agents_constants.COMMON.STATE]
        t = 1
        C = 0
        particles = env.initial_particles
        while not done and t < max_env_steps:
            monte_carlo_state = monte_carlo_most_frequent_particle(particles=particles, N=100)
            # monte_carlo_state = x
            # u = restore_policy(x=x)
            u = restore_policy(x=monte_carlo_state, train_env=train_env, particles=particles)
            if t <= 2:
                u = 31
            if u == -1:
                # if t == 1:
                # u = base_policy(x=monte_carlo_state, mu=mu, id_to_state=id_to_state)
                # else:
                u = rollout_policy(state_to_id=state_to_id, id_to_state=id_to_state, train_env=train_env, J=J, mu=mu,
                                   gamma=gamma, l=l, particles=particles, mc_samples=20)[0]
            _, _, _, _, info = env.step(u)
            particles = particle_filter(particles=particles, max_num_particles=50,
                                        train_env=train_env, u=u, obs=info[agents_constants.COMMON.OBSERVATION],
                                        x_s=info[agents_constants.COMMON.STATE])
            # particles = particle_filter(particles=[monte_carlo_state], max_num_particles=50,
            #                             train_env=train_env, u=u, obs=info[agents_constants.COMMON.OBSERVATION],
            #                             x_s=info[agents_constants.COMMON.STATE])
            c = -info[agents_constants.COMMON.REWARD]
            # C += math.pow(gamma, t - 1) * c
            C += c
            # print(f"t:{t}, u: {u}, c: {c}, a: {action_id_to_type_and_host[u]}, C: {C}, "
            #       f"aggstate: {id_to_state[Cage2AggregateMDP.get_aggregate_state(s=monte_carlo_state, state_to_id=state_to_id)]},"
            #       f"true state: {id_to_state[Cage2AggregateMDP.get_aggregate_state(s=x, state_to_id=state_to_id)]}")
            x = info[agents_constants.COMMON.STATE]
            # x = info[agents_constants.COMMON.STATE]
            t += 1
        returns.append(C)
        print(f"{i}/{N}, {np.mean(returns)}")
