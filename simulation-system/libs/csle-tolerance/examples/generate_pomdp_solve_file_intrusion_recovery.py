from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil
from csle_tolerance.dao.intrusion_recovery_pomdp_config import IntrusionRecoveryPomdpConfig

if __name__ == '__main__':
    num_observations = 10
    eta = 1
    p_a = 0.1
    p_c_1 = 0.00001
    p_c_2 = 0.001
    p_u = 0.02
    BTR = 50
    negate_costs = False
    seed = 999
    discount_factor = 1.0
    config = IntrusionRecoveryPomdpConfig(
        eta=eta, p_a=p_a, p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u, BTR=BTR, negate_costs=negate_costs, seed=seed,
        discount_factor=discount_factor, states=IntrusionRecoveryPomdpUtil.state_space(),
        actions=IntrusionRecoveryPomdpUtil.action_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations),
        cost_tensor=IntrusionRecoveryPomdpUtil.cost_tensor(eta=eta, states=IntrusionRecoveryPomdpUtil.state_space(),
                                                           actions=IntrusionRecoveryPomdpUtil.action_space()),
        observation_tensor=IntrusionRecoveryPomdpUtil.observation_tensor(
            states=IntrusionRecoveryPomdpUtil.state_space(),
            observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations)),
        transition_tensor=IntrusionRecoveryPomdpUtil.transition_tensor(
            states=IntrusionRecoveryPomdpUtil.state_space(), actions=IntrusionRecoveryPomdpUtil.action_space(),
            p_c_2=p_c_2, p_c_1=p_c_1, p_u=p_u, p_a=p_a),
        b1=IntrusionRecoveryPomdpUtil.initial_belief(p_a=p_a), T=BTR
    )
    pomdp_solver_file_str = IntrusionRecoveryPomdpUtil.pomdp_solver_file(config=config)
    with open("data/intrusion_recover_pa_01.pomdp", 'w') as f:
        f.write(pomdp_solver_file_str)
