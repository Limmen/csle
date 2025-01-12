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
                    obs: int, control_sequence: List[int]) -> List[CyborgWrapperState]:
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


def rollout_policy(train_env: CyborgScenarioTwoWrapper, J: List[float], state_to_id: Dict[str, int],
                   mu: List[List[float]], l: int, id_to_state: Dict[int, List[int]],
                   particles: List[CyborgWrapperState], gamma=0.99, mc_samples=10) -> Tuple[int, float]:
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
        returns = []
        for i in range(mc_samples):
            particle = random.choice(particles)
            train_env.set_state(particle)
            _, _, _, _, info = train_env.step(action=u)
            x_prime = info[agents_constants.COMMON.STATE]
            aggregate_state = Cage2AggregateMDP.get_aggregate_state(s=x_prime, state_to_id=state_to_id)
            c = -info[agents_constants.COMMON.REWARD]
            if l == 1:
                returns.append(c + gamma * J[aggregate_state])
            else:
                returns.append(c + gamma * rollout_policy(train_env=train_env, J=J,
                                                          state_to_id=state_to_id, id_to_state=id_to_state,
                                                          mu=mu, l=l - 1)[1])
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
            monte_carlo_state = monte_carlo_most_frequent_particle(particles=particles, N=100)
            u = restore_policy(x=monte_carlo_state, train_env=train_env, particles=particles)
            if t <= 2:
                u = 31
            if u == -1:
                # u = base_policy(x=monte_carlo_state, mu=mu, id_to_state=id_to_state)
                u = rollout_policy(state_to_id=state_to_id, id_to_state=id_to_state, train_env=train_env, J=J, mu=mu,
                                   gamma=gamma, l=l, particles=particles, mc_samples=20)[0]
            _, r, _, _, info = env.step(u)
            control_sequence.append(u)
            particles = particle_filter(particles=particles, max_num_particles=50,
                                        train_env=train_env, obs=info[agents_constants.COMMON.OBSERVATION],
                                        control_sequence=control_sequence)
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
        print(f"{i}/{N}, {np.mean(returns)}")
