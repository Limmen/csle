import numpy as np
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_tolerance.util.pomdp_solve_parser import PomdpSolveParser

if __name__ == '__main__':
    eta = 2
    p_a = 0.05
    p_c_1 = 0.01
    p_c_2 = 0.01
    p_u = 0.0
    BTR = np.inf
    negate_costs = False
    discount_factor = 1 - p_c_1
    num_observations = 100
    simulation_name = "csle-stopping-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    simulation_env_config.simulation_env_input_config.stopping_game_config.R = list(StoppingGameUtil.reward_tensor(
        R_INT=-1, R_COST=-10, R_SLA=0, R_ST=0, L=1))
    simulation_env_config.simulation_env_input_config.stopping_game_config.L = 1
    simulation_env_config.simulation_env_input_config.stopping_game_config.O = list(range(10))
    simulation_env_config.simulation_env_input_config.stopping_game_config.Z = \
        StoppingGameUtil.observation_tensor(n=10 - 1)
    gamma = 0.95
    pi2 = np.array([
        [0.9, 0.1],
        [1, 0],
        [1, 0]
    ])
    pomdp_solve_file_str = StoppingGameUtil.pomdp_solver_file(
        config=simulation_env_config.simulation_env_input_config.stopping_game_config,
        discount_factor=gamma, pi2=pi2)
    with open("/home/kim/thesis/paper_1.pomdp", 'w') as f:
        f.write(pomdp_solve_file_str)

    alpha_vectors = PomdpSolveParser.parse_alpha_vectors(
        file_path="/home/kim/thesis/paper_1-2337581.alpha")
    belief_space = np.linspace(0.0, 1, int(1.0 / 0.01))
    print(belief_space)
    for i in range(len(alpha_vectors)):
        print(f"a*:{alpha_vectors[i][0]}, vector: {list(-np.array(alpha_vectors[i][1][0:2]))}")
    values_01 = []
    for j, b in enumerate(belief_space):
        b_vec = [1 - b, b]
        dot_vals = []
        for i in range(len(alpha_vectors)):
            dot_vals.append(np.dot(b_vec, list(-np.array(alpha_vectors[i][1][0:2]))))
        max_index = np.argmax(dot_vals)
        values_01.append(dot_vals[max_index])
        vec_dots = []
        print(f"{b} {values_01[-1]}")
        for b in belief_space:
            b_vec = [1 - b, b]
            vec_dots.append(np.dot(b_vec, list(-np.array(alpha_vectors[max_index][1][0:2]))))
    # print(values_01)
