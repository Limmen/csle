import numpy as np
from csle_tolerance.dao.intrusion_recovery_game_config import IntrusionRecoveryGameConfig
from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil

if __name__ == '__main__':
    eta = 8
    p_a = 1
    p_c_1 = 0.01
    BTR = np.inf
    negate_costs = False
    discount_factor = 0.999
    num_observations = 10
    simulation_name = "csle-tolerance-intrusion-recovery-pomdp-defender-001"
    cost_tensor = IntrusionRecoveryPomdpUtil.cost_tensor(eta=eta, states=IntrusionRecoveryPomdpUtil.state_space(),
                                                         actions=IntrusionRecoveryPomdpUtil.action_space(),
                                                         negate=negate_costs)
    observation_tensor = IntrusionRecoveryPomdpUtil.observation_tensor(
        states=IntrusionRecoveryPomdpUtil.state_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations))
    transition_tensor = IntrusionRecoveryPomdpUtil.transition_tensor_game(
        states=IntrusionRecoveryPomdpUtil.state_space(), defender_actions=IntrusionRecoveryPomdpUtil.action_space(),
        attacker_actions=IntrusionRecoveryPomdpUtil.action_space(), p_a=p_a, p_c_1=p_c_1)
    config = IntrusionRecoveryGameConfig(
        eta=eta, p_a=p_a, p_c_1=p_c_1, BTR=BTR, negate_costs=negate_costs, seed=999,
        discount_factor=discount_factor, states=IntrusionRecoveryPomdpUtil.state_space(),
        actions=IntrusionRecoveryPomdpUtil.action_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations),
        cost_tensor=cost_tensor, observation_tensor=observation_tensor, transition_tensor=transition_tensor,
        b1=IntrusionRecoveryPomdpUtil.initial_belief(), T=BTR,
        simulation_env_name=simulation_name, gym_env_name="csle-tolerance-intrusion-recovery-pomdp-v1"
    )

    # s = 0
    # for i in range(100):
    #     s = IntrusionRecoveryPomdpUtil.sample_next_state_game(transition_tensor=config.transition_tensor, s=s,
    #                                                           a1=0, a2=1)
    #     c = config.cost_tensor[0][s]
    #     print(f"cost: {c}, s: {s}")

    IntrusionRecoveryPomdpUtil.generate_os_posg_game_file(game_config=config)
