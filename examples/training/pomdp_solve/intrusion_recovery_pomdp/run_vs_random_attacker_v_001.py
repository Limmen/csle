import numpy as np
from csle_tolerance.dao.intrusion_recovery_pomdp_config import IntrusionRecoveryPomdpConfig
from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil
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
    simulation_name = "csle-tolerance-intrusion-recovery-pomdp-defender-001"
    cost_tensor = IntrusionRecoveryPomdpUtil.cost_tensor(eta=eta, states=IntrusionRecoveryPomdpUtil.state_space(),
                                                         actions=IntrusionRecoveryPomdpUtil.action_space(),
                                                         negate=negate_costs)
    observation_tensor = IntrusionRecoveryPomdpUtil.observation_tensor(
        states=IntrusionRecoveryPomdpUtil.state_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations))
    transition_tensor = IntrusionRecoveryPomdpUtil.transition_tensor(
        states=IntrusionRecoveryPomdpUtil.state_space(), actions=IntrusionRecoveryPomdpUtil.action_space(), p_a=p_a,
        p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u)
    config = IntrusionRecoveryPomdpConfig(
        eta=eta, p_a=p_a, p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u, BTR=BTR, negate_costs=negate_costs, seed=999,
        discount_factor=discount_factor, states=IntrusionRecoveryPomdpUtil.state_space(),
        actions=IntrusionRecoveryPomdpUtil.action_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations),
        cost_tensor=cost_tensor, observation_tensor=observation_tensor, transition_tensor=transition_tensor,
        b1=IntrusionRecoveryPomdpUtil.initial_belief(), T=BTR,
        simulation_env_name=simulation_name, gym_env_name="csle-tolerance-intrusion-recovery-pomdp-v1"
    )
    pomdp_solve_file_str = IntrusionRecoveryPomdpUtil.pomdp_solver_file(config=config)
    with open("/home/kim/gamesec24/intrusion_recovery.pomdp", 'w') as f:
        f.write(pomdp_solve_file_str)

    alpha_vectors = PomdpSolveParser.parse_alpha_vectors(
        file_path="/home/kim/gamesec24/intrusion_recovery-3361312.alpha")
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
        min_index = np.argmin(dot_vals)
        values_01.append(dot_vals[min_index])
        vec_dots = []
        print(f"{b} {values_01[-1]}")
        for b in belief_space:
            b_vec = [1 - b, b]
            vec_dots.append(-np.dot(b_vec, list(-np.array(alpha_vectors[min_index][1][0:2]))))
