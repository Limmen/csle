import numpy as np
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
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
    returns = []
    for i in range(N):
        print(f"{i}/{N}")
        done = False
        _, info = env.reset()
        s = info["s"]
        t = 1
        R = 0
        particles = env.initial_particles
        while not done and t <= max_env_steps:
            # monte_carlo_state = monte_carlo_most_frequent(elements=particles, num_samples=100)
            aggregate_state = Cage2AggregateMDP.get_aggregate_state(s=s, state_to_id=state_to_id)
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
                a = 11 # OpServer
            if s.s[9][2] == 1:
                a = 22 # User1
            if s.s[10][2] == 1:
                a = 23 # User2
            if s.s[11][2] == 1:
                a = 24 # User3
            if s.s[12][2] == 1:
                a = 25 # User4

            if t <= 1:
                a = 31
            if a == -1:
                a = Cage2AggregateMDP.get_aggregate_control(mu=mu, aggregate_state=aggregate_state,
                                                            id_to_state=id_to_state)
            o, r, done, _, info = env.step(a)
            # particles = particle_filter(particles=particles, max_num_particles=1000,
            #                             train_env=train_env, action=a, obs=o)
            s = info["s"]
            t+= 1
            R+= r
            # print(f"t:{t}, r: {r}, a: {action_id_to_type_and_host[a]}, R: {R}, aggstate: {id_to_state[aggregate_state]}")
        returns.append(R)
        print(np.mean(returns))