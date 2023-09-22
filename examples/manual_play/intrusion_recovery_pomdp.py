import gymnasium as gym
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_tolerance.util.general_util import GeneralUtil
from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil

if __name__ == '__main__':
    GeneralUtil.register_envs()
    simulation_name = "csle-tolerance-intrusion-recovery-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    env = gym.make("csle-tolerance-intrusion-recovery-pomdp-v1",
                   config=simulation_env_config.simulation_env_input_config)
    pomdp_solver_file_str = IntrusionRecoveryPomdpUtil.pomdp_solver_file(
        config=simulation_env_config.simulation_env_input_config)
    with open("./intrusion_recover_pa_01.pomdp", 'w') as f:
        f.write(pomdp_solver_file_str)

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
