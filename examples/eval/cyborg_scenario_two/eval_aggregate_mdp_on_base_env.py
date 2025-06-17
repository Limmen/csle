import copy
from typing import List, Dict, Tuple
import random
import numpy as np
from collections import Counter
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState
from cage2_aggregate_mdp import Cage2AggregateMDP
import csle_agents.constants.constants as agents_constants
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender


def get_wrapper_state_from_cyborg(cyborg_env: CyborgScenarioTwoDefender, obs_id, t) -> CyborgWrapperState:
    scan_state = cyborg_env.scan_state
    op_server_restored = False
    privilege_escalation_detected = False
    obs_vector = CyborgEnvUtil.state_id_to_state_vector(state_id=obs_id, observation=True)
    decoy_state = cyborg_env.decoy_state.copy()
    bline_base_jump = False
    scanned_subnets = [0, 0, 0]
    for i in range(len(scan_state)):
        if i in [9, 10, 11, 12] and scan_state[i] > 0:
            scanned_subnets[0] = 1
        if i in [3, 4, 5, 6, 7] and scan_state[i] > 0:
            scanned_subnets[1] = 1
        if i in [4, 5, 6, 7] and scan_state[i] > 0:
            scanned_subnets[2] = 1
    red_action_targets = {}
    red_action_targets[0] = 0
    if scan_state[9] > 0:
        red_action_targets[1] = 9
        red_action_targets[2] = 9
        red_action_targets[3] = 9
        red_action_targets[4] = 2
        red_action_targets[5] = 2
        red_action_targets[6] = 2
    elif scan_state[10] > 0:
        red_action_targets[1] = 10
        red_action_targets[2] = 10
        red_action_targets[3] = 10
        red_action_targets[4] = 2
        red_action_targets[5] = 2
        red_action_targets[6] = 2
    elif scan_state[11] > 0:
        red_action_targets[1] = 11
        red_action_targets[2] = 11
        red_action_targets[3] = 11
        red_action_targets[4] = 1
        red_action_targets[5] = 1
        red_action_targets[6] = 1
    elif scan_state[12] > 0:
        red_action_targets[1] = 12
        red_action_targets[2] = 12
        red_action_targets[3] = 12
        red_action_targets[4] = 1
        red_action_targets[5] = 1
        red_action_targets[6] = 1
    red_action_targets[7] = 1
    red_action_targets[8] = 3
    red_action_targets[9] = 3
    red_action_targets[10] = 7
    red_action_targets[11] = 7
    red_action_targets[12] = 7
    s = []
    access_list = cyborg_env.get_access_list()
    red_agent_state = cyborg_env.get_bline_state()
    for i in range(len(CyborgEnvUtil.get_cyborg_hosts())):
        known = 0
        scanned = min(scan_state[i], 1)
        if scanned:
            known = 1
        if t > 0 and i in [9, 10, 11, 12]:
            known = 1
        if red_agent_state >= 6 and i in [0, 1, 2, 3]:
            known = 1
        if red_agent_state >= 8 and i in [4, 5, 6, 7]:
            known = 1
        access = access_list[i]
        decoy = len(decoy_state[i])
        host_state = [known, scanned, access, decoy]
        s.append(host_state)
    malware_state = [0 for _ in range(len(scan_state))]
    ssh_access = [0 for _ in range(len(scan_state))]
    escalated = [0 for _ in range(len(scan_state))]
    exploited = [0 for _ in range(len(scan_state))]
    detected = [0 for _ in range(len(scan_state))]
    attacker_observed_decoy = [len(decoy_state[i]) for i in range(len(decoy_state))]
    red_agent_target = red_action_targets[red_agent_state]
    wrapper_state = CyborgWrapperState(s=s, scan_state=scan_state, op_server_restored=op_server_restored,
                                       obs=obs_vector,
                                       red_action_targets=red_action_targets,
                                       privilege_escalation_detected=privilege_escalation_detected,
                                       red_agent_state=red_agent_state, red_agent_target=red_agent_target,
                                       malware_state=malware_state,
                                       ssh_access=ssh_access, escalated=escalated, exploited=exploited,
                                       bline_base_jump=bline_base_jump, scanned_subnets=scanned_subnets,
                                       attacker_observed_decoy=attacker_observed_decoy, detected=detected)
    return wrapper_state


def monte_carlo_most_frequent_particle(particles: List[CyborgWrapperState], N: int) -> CyborgWrapperState:
    """
    Samples N particles and returns the most frequently sampled particle

    :param particles: the list of particles
    :param N: the number of samples
    :return: the most frequently sampled particle
    """
    samples = [random.choice(particles) for _ in range(N)]
    counter = Counter(samples)
    most_frequent_particle = counter.most_common(1)[0][0]
    return most_frequent_particle


def particle_filter(particles: List[CyborgWrapperState], max_num_particles: int, train_env: CyborgScenarioTwoWrapper,
                    obs: int, control_sequence: List[int],
                    cyborg_env: CyborgScenarioTwoDefender, t: int) -> List[CyborgWrapperState]:
    """
    Implements a particle filter

    :param particles: the list of particles
    :param max_num_particles: the maximum number of particles
    :param train_env: the environment used for sampling
    :param obs: the latest observation
    :param control_sequence: the control sequence up to the current observation
    :return: the list of updated particles
    """
    u = control_sequence[-1]
    new_particles = []
    failed_samples = 0
    while len(new_particles) < max_num_particles:
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
            # Particle deprivation
            failed_samples = 1
            if len(new_particles) == 0:
                while True:
                    t = 0
                    train_env.reset()
                    while t < len(control_sequence):
                        _, _, _, _, info = train_env.step(control_sequence[t])
                        o = info[agents_constants.COMMON.OBSERVATION]
                        if int(o) == int(obs):
                            return [info[agents_constants.COMMON.STATE]]
                        t += 1
                        failed_samples += 1
                    if failed_samples > 500:
                        s = get_wrapper_state_from_cyborg(cyborg_env=cyborg_env, t=t, obs_id=obs)
                        print(f"particle filter failed, {s.s}")
                        return [s]
                        # return particles
            else:
                return new_particles
    return new_particles


def restore_policy(x: CyborgWrapperState, train_env: CyborgScenarioTwoWrapper, particles: List[CyborgWrapperState]) \
        -> int:
    """
    Implements a heuristic restore policy for Cage2

    :param x: the certainty-equivalence state
    :param train_env: the environment used for simulation
    :param particles: the current list of particles
    :return: the control
    """
    u = -1
    restore_actions = [0, 1, 2, 3]
    remove_actions = [8, 9, 10, 11, 22, 23, 24, 25]
    remove_hosts = [1, 2, 3, 7, 9, 10, 11, 12]
    restore_hosts = [1, 2, 3, 7]
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


def rollout_eval(mu, train_env, m, particles, control_sequence, t, mc_samples):
    costs = []
    for j in range(mc_samples):
        C = 0
        k = t
        while t <= 100 and k < t + m:
            monte_carlo_state = monte_carlo_most_frequent_particle(particles=particles, N=100)
            u = restore_policy(x=monte_carlo_state, train_env=train_env, particles=particles)
            if t <= 2:
                u = 31
            if u == -1:
                u = base_policy(x=monte_carlo_state, mu=mu, id_to_state=id_to_state)
            _, r, _, _, info = env.step(u)
            control_sequence.append(u)
            particles = particle_filter(particles=particles, max_num_particles=50,
                                        train_env=train_env, obs=info[agents_constants.COMMON.OBSERVATION],
                                        control_sequence=control_sequence, cyborg_env=env, t=t)
            c = -r
            C += c
            k += 1
        monte_carlo_state = monte_carlo_most_frequent_particle(particles=particles, N=100)
        aggregate_state = Cage2AggregateMDP.get_aggregate_state(s=monte_carlo_state, state_to_id=state_to_id)
        C += J[aggregate_state]
        costs.append(C)
    return np.mean(costs)


def rollout_policy(train_env: CyborgScenarioTwoWrapper, J: List[float], state_to_id: Dict[str, int],
                   mu: List[List[float]], l: int, id_to_state: Dict[int, List[int]],
                   particles: List[CyborgWrapperState], control_sequence, env: CyborgScenarioTwoDefender, t: int,
                   gamma=0.99, mc_samples=10, m=0) -> Tuple[int, float]:
    """
    A rollout policy for cage-2

    :param train_env: the environment to use for sampling
    :param J: the cost-to-go function of the base policy
    :param state_to_id: the aggreate state to aggregate state id map
    :param mu: the base policy
    :param l: the lookahead horizon
    :param id_to_state: the aggregate state id to aggregate state map
    :param particles: the current particle state
    :param gamma: the discount factor
    :param mc_samples: the number of Monte-Carlo samples to use
    :return: the next control and its estimated value
    """
    U = [27, 28, 29, 30, 31, 32, 35]
    Q_n = []
    for u in U:
        # print(f"{u}/{len(U)}")
        returns = []
        for i in range(mc_samples):
            particle = random.choice(particles)
            control_sequence_prime = control_sequence.copy()
            control_sequence_prime.append(u)
            train_env.set_state(particle)
            _, _, _, _, info = train_env.step(action=u)
            # x_prime = info[agents_constants.COMMON.STATE]
            particles_prime = particle_filter(particles=copy.deepcopy(particles), max_num_particles=50,
                                              train_env=train_env, obs=info[agents_constants.COMMON.OBSERVATION],
                                              control_sequence=control_sequence_prime, cyborg_env=env, t=t)
            # aggregate_state = Cage2AggregateMDP.get_aggregate_state(s=x_prime, state_to_id=state_to_id)
            c = -info[agents_constants.COMMON.REWARD]
            if l == 1:
                returns.append(c + gamma * rollout_eval(mu=mu, train_env=train_env, m=m, particles=particles_prime,
                                                        control_sequence=control_sequence_prime, t=t,
                                                        mc_samples=mc_samples))
            else:
                returns.append(c + gamma * rollout_policy(train_env=train_env, J=J,
                                                          state_to_id=state_to_id, id_to_state=id_to_state,
                                                          mu=mu, l=l - 1, particles=particles_prime,
                                                          control_sequence=control_sequence_prime, m=m, env=env, t=t)[
                    1])
        Q_n.append(np.mean(returns))
    u_star = int(np.argmin(Q_n))
    J_star = float(Q_n[u_star])
    u_star = U[u_star]
    monte_carlo_state = monte_carlo_most_frequent_particle(particles=particles, N=100)
    u_r = restore_policy(x=monte_carlo_state, train_env=train_env, particles=particles)
    if u_r != -1:
        u_star = u_r
    return u_star, J_star


def base_policy(x: CyborgWrapperState, mu: List[List[float]], id_to_state: Dict[int, List[int]]) -> int:
    """
    Implements the base policy mu

    :param x: the current state id
    :param mu: the base policy
    :param id_to_state: the aggregate state id to aggregate state map
    :return: the next control
    """
    aggregate_state = Cage2AggregateMDP.get_aggregate_state(s=x, state_to_id=state_to_id)
    return Cage2AggregateMDP.get_aggregate_control(mu=mu, aggregate_state=aggregate_state, id_to_state=id_to_state)


if __name__ == '__main__':
    seed = 441902
    np.random.seed(seed)
    random.seed(seed)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    env = CyborgScenarioTwoDefender(config=config)
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2,
                                     red_agent_type=RedAgentType.B_LINE_AGENT)
    train_env = CyborgScenarioTwoWrapper(config=config)
    action_id_to_type_and_host, type_and_host_to_action_id \
        = CyborgEnvUtil.get_action_dicts(scenario=2, reduced_action_space=True, decoy_state=True,
                                         decoy_optimization=False)
    print(CyborgEnvUtil.get_cyborg_hosts())
    import sys
    sys.exit(0)
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
        # x = info[agents_constants.COMMON.STATE]
        control_sequence = []
        t = 1
        C = 0
        train_env.reset()
        particles = train_env.initial_particles
        while not done and t < max_env_steps:
            print(f"{t}/{max_env_steps}")
            monte_carlo_state = monte_carlo_most_frequent_particle(particles=particles, N=100)
            u = restore_policy(x=monte_carlo_state, train_env=train_env, particles=particles)
            if t <= 2:
                u = 31
            if u == -1:
                # u = base_policy(x=monte_carlo_state, mu=mu, id_to_state=id_to_state)
                # import time
                # start = time.time()
                u = rollout_policy(state_to_id=state_to_id, id_to_state=id_to_state, train_env=train_env, J=J, mu=mu,
                                   gamma=gamma, l=l, particles=copy.deepcopy(particles), mc_samples=20, m=0,
                                   control_sequence=copy.deepcopy(control_sequence), env=env, t=t)[0]
                # print((time.time() - start)/60)
            _, r, _, _, info = env.step(u)
            control_sequence.append(u)
            particles = particle_filter(particles=copy.deepcopy(particles), max_num_particles=50,
                                        train_env=train_env, obs=info[agents_constants.COMMON.OBSERVATION],
                                        control_sequence=control_sequence, cyborg_env=env, t=t)
            c = -r
            C += c
            # aggstate = id_to_state[Cage2AggregateMDP.get_aggregate_state(s=monte_carlo_state,
            #                                                               state_to_id=state_to_id)]
            # print(f"t:{t}, u: {u}, c: {c}, a: {action_id_to_type_and_host[u]}, C: {C}, "
            #       f"aggstate: {aggstate},"
            #       f"true state: {id_to_state[Cage2AggregateMDP.get_aggregate_state(s=x, state_to_id=state_to_id)]}")
            # x = info[agents_constants.COMMON.STATE]
            t += 1
        returns.append(C)
        print(f"{i}/{N}, {np.mean(returns)}, {C}")
