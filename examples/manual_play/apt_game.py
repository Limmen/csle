import gymnasium as gym
import numpy as np
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig

if __name__ == '__main__':
    simulation_name = "csle-apt-game-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    N = 10
    p_a = 0.1
    num_observations = 10
    negate_costs = False
    discount_factor = 1
    C = AptGameUtil.cost_tensor(N=N)
    Z = AptGameUtil.observation_tensor(N=N, num_observations=num_observations)
    T = AptGameUtil.transition_tensor(N=N, p_a=p_a)
    O = AptGameUtil.observation_space(num_observations=num_observations)
    S = AptGameUtil.state_space(N=N)
    A1 = AptGameUtil.defender_actions()
    A2 = AptGameUtil.attacker_actions()
    b1 = AptGameUtil.b1(N=N)
    gamma = 0.99
    input_config = AptGameConfig(
        T=T, O=O, Z=Z, C=C, S=S, A1=A1, A2=A2, N=N, p_a=p_a, save_dir=".", checkpoint_traces_freq=10000, gamma=gamma,
        b1=b1, env_name="csle-apt-game-v1")
    env = gym.make("csle-apt-game-v1", config=input_config)
    p_intrusion = 0.5
    pi2 = []
    for s in S:
        pi2.append([1-p_intrusion, p_intrusion])
    pi2 = np.array(pi2)
    o, info = env.reset()
    (defender_obs, attacker_obs) = o
    for t in range(200):
        b = attacker_obs[0]
        s = attacker_obs[1]
        a1 = 0
        a2 = (pi2, AptGameUtil.sample_attacker_action(pi2=pi2, s=s))
        action_profile = (a1, a2)
        o, costs, done, _, info = env.step(action_profile)
        (defender_obs, attacker_obs) = o
        c = costs[0]
        b_str = ",".join(list(map(lambda x: f"{x:.2f}", b)))
        print(f"t:{t}, s:{s}, c: {c:.2f}, b: {b_str}")

    # for i in range(10):
    #     env.step(action=0)
    # pomdp_solver_file_str = AptGameUtil.pomdp_solver_file(
    #     config=input_config)
    # with open("/home/kim/intrusion_recover.pomdp", 'w') as f:
    #     f.write(pomdp_solver_file_str)

    # from csle_tolerance.util.pomdp_solve_parser import PomdpSolveParser
    # import numpy as np
    # b = 0.1
    # alpha_vectors = PomdpSolveParser.parse_alpha_vectors(
    #     file_path="./test.alpha")
    # b_vec = [1-b, b]
    # dot_vals = []
    # for i in range(len(alpha_vectors)):
    #     dot_vals.append(-np.dot(b_vec, alpha_vectors[i][1][0:2]))
    # min_index = np.argmin(dot_vals)
    # value = dot_vals[min_index]
    # print(value)

    # threshold = 0.5
    # costs = []
    # for i in range(100):
    #     cumulative_cost = 0
    #     s, _ = env.reset()
    #     done = False
    #     t = 0
    #     while not done:
    #         b = s[2]
    #         a = 0
    #         if b >= threshold:
    #             a = 1
    #         s, c, _, done, info = env.step(a)
    #         cumulative_cost += c
    #         t+= 1
    #     costs.append(cumulative_cost)
    # print(float(np.mean(costs)))

    # env.manual_play()
