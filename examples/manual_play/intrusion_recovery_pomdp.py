import gymnasium as gym
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_tolerance.util.general_util import GeneralUtil
from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil
from csle_tolerance.dao.intrusion_recovery_pomdp_config import IntrusionRecoveryPomdpConfig

if __name__ == '__main__':
    GeneralUtil.register_envs()
    simulation_name = "csle-tolerance-intrusion-recovery-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    eta = 1
    p_a = 0.1
    p_c_1 = 0.00001
    p_c_2 = 0.001
    p_u = 0.02
    BTR = 100
    negate_costs = False
    discount_factor = 1
    num_observations = 1000
    cost_tensor = IntrusionRecoveryPomdpUtil.cost_tensor(eta=eta, states=IntrusionRecoveryPomdpUtil.state_space(),
                                                         actions=IntrusionRecoveryPomdpUtil.action_space(),
                                                         negate=negate_costs)
    observation_tensor = IntrusionRecoveryPomdpUtil.observation_tensor(
        states=IntrusionRecoveryPomdpUtil.state_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations))
    transition_tensor = IntrusionRecoveryPomdpUtil.transition_tensor(
        states=IntrusionRecoveryPomdpUtil.state_space(), actions=IntrusionRecoveryPomdpUtil.action_space(), p_a=p_a,
        p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u)
    input_config = IntrusionRecoveryPomdpConfig(
        eta=eta, p_a=p_a, p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u, BTR=BTR, negate_costs=negate_costs, seed=999,
        discount_factor=discount_factor, states=IntrusionRecoveryPomdpUtil.state_space(),
        actions=IntrusionRecoveryPomdpUtil.action_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations),
        cost_tensor=cost_tensor, observation_tensor=observation_tensor, transition_tensor=transition_tensor,
        b1=IntrusionRecoveryPomdpUtil.initial_belief(), T=BTR,
        simulation_env_name=simulation_name, gym_env_name="csle-tolerance-intrusion-recovery-pomdp-v1"
    )
    env = gym.make("csle-tolerance-intrusion-recovery-pomdp-v1",
                   config=simulation_env_config.simulation_env_input_config)
    env.reset()
    for i in range(10):
        env.step(action=0)
    pomdp_solver_file_str = IntrusionRecoveryPomdpUtil.pomdp_solver_file(
        config=input_config)
    with open("/home/kim/intrusion_recover.pomdp", 'w') as f:
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
